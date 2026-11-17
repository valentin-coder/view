"""23. kör: fagyasztott mini-LM aktivációiból kiolvasható-e a grounding és a kontextus-jel,
és jobb-e ez egy szózsák (BoW) alapvonalnál?

Futtatás: python -m minilm.probe_exp --out results/r23
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from .corpus import CATS, CONTEXTS, HELDOUT_SOURCES, PROPS, World, generate
from .model import TinyGPT, Vocab, activations, train


def logreg(Xtr, ytr, Xte, n_cls, l2=1e-3, iters=200):
    """Multinomiális logisztikus regresszió (torch, LBFGS), standardizált jellemzőkkel."""
    mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    W = torch.zeros(Xtr.shape[1], n_cls, requires_grad=True)
    b = torch.zeros(n_cls, requires_grad=True)
    opt = torch.optim.LBFGS([W, b], max_iter=iters, line_search_fn="strong_wolfe")
    ytr_t = torch.as_tensor(ytr)

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(Xtr @ W + b, ytr_t) + l2 * (W ** 2).sum()
        loss.backward()
        return loss

    opt.step(closure)
    with torch.no_grad():
        return torch.softmax(Xte @ W + b, -1).numpy()


def auc(scores, labels):
    pos, neg = scores[labels == 1], scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    return float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())


class _T:
    def __init__(self, text):
        self.text = text


def _strip_ctx(s):
    """Az explicit kontextus-kifejezés (a mondat eleje az első vesszőig) kivágása."""
    text = s.text.split(" , ", 1)[1] if s.explicit_ctx and " , " in s.text else s.text
    return _T(text)


def bow(sents, vocab):
    X = torch.zeros(len(sents), len(vocab))
    for i, s in enumerate(sents):
        for w in s.text.split():
            X[i, vocab.stoi.get(w, 2)] = 1.0
    return X


TASKS = {
    "context": (lambda s: CONTEXTS.index(s.context), 2, lambda s: not s.explicit_ctx),
    "polarity": (lambda s: int(s.pos), 2, lambda s: True),
    "kind": (lambda s: ["isa", "has", "gen"].index(s.kind), 3, lambda s: True),
    "object": (lambda s: (CATS + PROPS).index(s.obj), len(CATS) + len(PROPS), lambda s: True),
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs/r23")
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--n-pretrain", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(a.seed)
    world = World(a.seed)
    pre = generate(world, a.n_pretrain, seed=a.seed + 1, templates="all")     # „előtanítás”
    probe_pool = generate(world, 6000, seed=a.seed + 2, templates="train")
    held_t = generate(world, 2000, seed=a.seed + 3, templates="heldout")
    vocab = Vocab([s.text for s in pre + probe_pool + held_t])
    model = TinyGPT(len(vocab))
    print(f"mini-LM: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M paraméter, szótár {len(vocab)}")
    t0 = time.time()
    hist = train(model, [vocab.encode(s.text) for s in pre], steps=a.steps, seed=a.seed)
    train_s = time.time() - t0

    ptr = [s for s in probe_pool if s.source not in HELDOUT_SOURCES]
    sets = {
        "kitartott_sablon": [s for s in held_t if s.source not in HELDOUT_SOURCES],
        "kitartott_forras": [s for s in probe_pool if s.source in HELDOUT_SOURCES],
    }

    def acts(ss):
        seqs = [vocab.encode(s.text) for s in ss]
        return activations(model, seqs, [len(q) - 1 for q in seqs])

    A_tr = acts(ptr)
    A_te = {k: acts(v) for k, v in sets.items()}
    B_tr = bow(ptr, vocab)
    B_te = {k: bow(v, vocab) for k, v in sets.items()}
    n_layers = A_tr.shape[0]
    results = {"train_seconds": train_s, "loss_hist": hist, "n_layers": n_layers}
    # rétegválasztás: a tanítókészlet egy kitartott részén (sablon-szintű általánosítás nélkül)
    rng = np.random.default_rng(a.seed)
    idx = rng.permutation(len(ptr))
    fit, val = idx[: int(0.8 * len(idx))], idx[int(0.8 * len(idx)):]
    for task, (lab, ncls, filt) in TASKS.items():
        ytr_all = np.array([lab(s) for s in ptr])
        keep_tr = np.array([filt(s) for s in ptr])
        best_l, best_acc = None, -1
        for l in range(n_layers):
            f = fit[keep_tr[fit]]
            v = val[keep_tr[val]]
            p = logreg(A_tr[l][f], ytr_all[f], A_tr[l][v], ncls)
            acc = float((p.argmax(1) == ytr_all[v]).mean())
            if acc > best_acc:
                best_l, best_acc = l, acc
        res = {"best_layer": best_l, "val_acc": best_acc}
        f = np.where(keep_tr)[0]
        for name, ss in sets.items():
            yte = np.array([lab(s) for s in ss])
            keep = np.array([filt(s) for s in ss])
            if keep.sum() == 0:
                continue
            p_act = logreg(A_tr[best_l][f], ytr_all[f], A_te[name][best_l][keep], ncls)
            p_bow = logreg(B_tr[f], ytr_all[f], B_te[name][keep], ncls)
            r = {"n": int(keep.sum()),
                 "acc_act": float((p_act.argmax(1) == yte[keep]).mean()),
                 "acc_bow": float((p_bow.argmax(1) == yte[keep]).mean())}
            if ncls == 2:
                r["auc_act"] = auc(p_act[:, 1], yte[keep])
                r["auc_bow"] = auc(p_bow[:, 1], yte[keep])
            res[name] = r
        if task == "context":
            # távoli felügyeletű BoW: ugyanazon az előtanító korpuszon, a címkét az explicit
            # kontextus-kifejezés adja, amelyet a jellemzőkből kivágunk
            ds = [s for s in pre if s.explicit_ctx]
            ds_x = bow([_strip_ctx(s) for s in ds], vocab)
            ds_y = np.array([CONTEXTS.index(s.context) for s in ds])
            for name, ss in sets.items():
                keep = [s for s in ss if not s.explicit_ctx]
                yte = np.array([CONTEXTS.index(s.context) for s in keep])
                p = logreg(ds_x, ds_y, bow(keep, vocab), 2)
                res[name]["acc_bow_ds"] = float((p.argmax(1) == yte).mean())
                res[name]["auc_bow_ds"] = auc(p[:, 1], yte)
        results[task] = res
        print(task, json.dumps(res), flush=True)
    (out / "results.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
