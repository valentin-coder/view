"""35. kör: a B fázis kísérletei valódi (fagyasztott) nyelvi modellen.

E0  – literálkinyerés lineáris probe-okkal, kitartott parafrázisokon; alapvonalak: BoW és a
      modell saját, kontextus nélküli bemeneti beágyazásainak átlaga (statikus alapvonal).
CTX – kontextus-jel (fikció vs. tény) kitartott forráskifejezésekkel; a 21. kör küszöbe 0,95.
ISZB – interventív szabálybányászat (8. kör) a KTP-transzplantációval vs. promptolás.
B4  – LLM-oldali hiszterézis (11. kör): ellentmondó kontextusmondatok két sorrendben.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np
import torch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ktp"))
from ktp import data as D                                             # noqa: E402
from ktp.core import Op, Patch, get_layers, margins, subject_states  # noqa: E402

# ------------------------------------------------------------------ kijelentő mondatok
PHRASE = {
    "breathe_underwater": ("can breathe underwater", "cannot breathe underwater"),
    "feathers": ("has feathers", "does not have feathers"),
    "fins": ("has fins", "does not have fins"),
    "fur": ("has fur", "does not have fur"),
    "six_legs": ("has six legs", "does not have six legs"),
    "wheels": ("has wheels", "does not have wheels"),
    "seeds": ("has seeds", "does not have seeds"),
    "beak": ("has a beak", "does not have a beak"),
    "scales": ("has scales", "does not have scales"),
    "antennae": ("has antennae", "does not have antennae"),
    "engine": ("has an engine", "does not have an engine"),
    "grows_on_trees": ("grows on trees", "does not grow on trees"),
    "lays_eggs": ("lays eggs", "does not lay eggs"),
    "is_animal": ("is an animal", "is not an animal"),
    "bones": ("has bones", "does not have bones"),
    "milk": ("feeds its babies milk", "does not feed its babies milk"),
    "fuel": ("needs fuel", "does not need fuel"),
}
STATEMENT_T = ["{Art} {X} {P}.", "It is well known that {art} {X} {P}.", "Everyone agrees that {art} {X} {P}.",
               "I read that {art} {X} {P}.",
               "Scientists confirmed that {art} {X} {P}.", "My teacher said that {art} {X} {P}."]   # 2 kitartott
N_TRAIN_T = 4
# A felszíni szerkezet ("In the ..." / "According to the ...") mindkét típusban kiegyensúlyozott, és
# típusonként 20 kifejezés van, ebből 8 kitartott: a hatásos mintaméret a kifejezések száma (35. kör).
CTX_FICTION = ['In the fairy tale,', 'According to the fantasy novel,', 'In the cartoon,', 'According to the legend,', 'In the video game,', 'According to the comic book,', 'In the bedtime story,', 'According to the folk tale,', "In the children's book,", 'According to the animated film,', 'In the fable,', 'According to the superhero movie,', 'In the myth,', 'According to the nursery rhyme,', 'In the puppet show,', 'According to the riddle,', 'In the daydream,', 'According to the pantomime,', 'In the sitcom,', 'According to the limerick,']
CTX_FACT = ['In the encyclopedia,', 'According to the biology textbook,', 'In the field guide,', 'According to the scientific report,', 'In the zoology lecture,', 'According to the research paper,', 'In the university course,', 'According to the nature magazine,', 'In the veterinary manual,', 'According to the government survey,', 'In the science journal,', 'According to the lab notebook,', 'In the documentary,', 'According to the museum catalogue,', 'In the expert interview,', 'According to the official statistics,', 'In the wildlife census,', 'According to the dictionary,', 'In the atlas,', 'According to the almanac,']
# a kitartott kifejezések egyetlen tartalmi szava sem szerepel a tanítókban (ellenőrizve)
N_TRAIN_CTX = 12


@dataclass
class Stmt:
    text: str
    entity: str
    category: str
    prop: str
    polarity: bool
    true_in_world: bool
    template: int
    ctx: str = ""          # "fiction" | "fact" | ""
    ctx_idx: int = -1


def statements(seed=0, with_ctx=False):
    rng = random.Random(seed)
    ents = D.build_entities(seed)
    out = []
    for e in ents.values():
        for prop in D.PROPERTIES:
            truth = D.value(prop, e.category)
            for pol in (True, False):
                for ti, T in enumerate(STATEMENT_T):
                    art = D.article(e.name)
                    s = T.format(Art=art.capitalize(), art=art, X=e.name, P=PHRASE[prop][0 if pol else 1])
                    st = Stmt(s, e.name, e.category, prop, pol, pol == truth, ti)
                    if with_ctx:
                        kind = rng.choice(["fiction", "fact"])
                        pool = CTX_FICTION if kind == "fiction" else CTX_FACT
                        ci = rng.randrange(len(pool))
                        st.text = pool[ci] + " " + s[0].lower() + s[1:]
                        st.ctx, st.ctx_idx = kind, ci
                    out.append(st)
    rng.shuffle(out)
    return out


# ------------------------------------------------------------------ jellemzők
@torch.inference_mode()
def last_token_states(model, tok, texts, batch_size=16):
    """Rétegenkénti utolsó-token aktivációk és a statikus alapvonal (bemeneti beágyazások átlaga)."""
    L = len(get_layers(model))
    acts, static = None, []
    emb = model.get_input_embeddings().weight
    for b in range(0, len(texts), batch_size):
        enc = tok(texts[b:b + batch_size], return_tensors="pt", padding=True, add_special_tokens=False)
        out = model(**enc, output_hidden_states=True)
        last = enc["attention_mask"].sum(1) - 1
        hs = torch.stack(out.hidden_states[1:])                     # (L, B, T, d)
        sel = hs[:, torch.arange(hs.shape[1]), last]                # (L, B, d)
        acts = sel if acts is None else torch.cat([acts, sel], 1)
        for i in range(len(last)):
            ids = enc["input_ids"][i, : last[i] + 1]
            static.append(emb[ids].mean(0))
    return acts.float(), torch.stack(static).float()


def bow(texts, vocab=None):
    words = [t.lower().replace(".", " .").replace(",", " ,").split() for t in texts]
    if vocab is None:
        vocab = {w: i for i, w in enumerate(sorted({w for ws in words for w in ws}))}
    X = torch.zeros(len(texts), len(vocab))
    for i, ws in enumerate(words):
        for w in ws:
            if w in vocab:
                X[i, vocab[w]] = 1.0
    return X, vocab


def logreg(Xtr, ytr, Xte, n_cls, l2=1e-3, iters=200):
    mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    W = torch.zeros(Xtr.shape[1], n_cls, requires_grad=True)
    b = torch.zeros(n_cls, requires_grad=True)
    opt = torch.optim.LBFGS([W, b], max_iter=iters, line_search_fn="strong_wolfe")
    y = torch.as_tensor(ytr)

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(Xtr @ W + b, y) + l2 * (W ** 2).sum()
        loss.backward()
        return loss
    opt.step(closure)
    with torch.no_grad():
        return torch.softmax(Xte @ W + b, -1).numpy()


def auc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    return float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())


# ------------------------------------------------------------------ E0 + CTX
def e0_and_ctx(model, tok, n_max=3000, seed=0, batch_size=16):
    res = {}
    for task_name, with_ctx in (("E0", False), ("CTX", True)):
        S = statements(seed, with_ctx=with_ctx)[:n_max]
        if task_name == "E0":
            tr = [s for s in S if s.template < N_TRAIN_T]
            te = [s for s in S if s.template >= N_TRAIN_T]
            labels = {"polaritás": (lambda s: int(s.polarity), 2),
                      "tulajdonság": (lambda s: list(D.PROPERTIES).index(s.prop), len(D.PROPERTIES)),
                      "alany kategóriája": (lambda s: D.CATEGORIES.index(s.category), len(D.CATEGORIES)),
                      "igaz-e a világban": (lambda s: int(s.true_in_world), 2)}
        else:
            tr = [s for s in S if s.ctx_idx < N_TRAIN_CTX]
            te = [s for s in S if s.ctx_idx >= N_TRAIN_CTX]
            labels = {"fikció vs. tény (kitartott forráskifejezés)": (lambda s: int(s.ctx == "fact"), 2)}
        A_tr, St_tr = last_token_states(model, tok, [s.text for s in tr], batch_size)
        A_te, St_te = last_token_states(model, tok, [s.text for s in te], batch_size)
        B_tr, vocab = bow([s.text for s in tr])
        B_te, _ = bow([s.text for s in te], vocab)
        rng = np.random.default_rng(seed)
        idx = rng.permutation(len(tr))
        fit, val = idx[: int(0.8 * len(idx))], idx[int(0.8 * len(idx)):]
        out = {}
        for name, (lab, k) in labels.items():
            ytr = np.array([lab(s) for s in tr])
            yte = np.array([lab(s) for s in te])
            best_l, best = 0, -1.0
            for l in range(A_tr.shape[0]):
                p = logreg(A_tr[l][fit], ytr[fit], A_tr[l][val], k)
                a = float((p.argmax(1) == ytr[val]).mean())
                if a > best:
                    best_l, best = l, a
            r = {"best_layer": best_l}
            for feat, Xtr, Xte in (("aktiváció", A_tr[best_l], A_te[best_l]), ("statikus", St_tr, St_te),
                                   ("BoW", B_tr, B_te)):
                p = logreg(Xtr, ytr, Xte, k)
                r[feat] = {"acc": float((p.argmax(1) == yte).mean())}
                if k == 2:
                    r[feat]["auc"] = auc(p[:, 1], yte)
            if task_name == "CTX":
                for feat, Xtr, Xte in (("aktiváció", A_tr[best_l], A_te[best_l]), ("statikus", St_tr, St_te),
                                       ("BoW", B_tr, B_te)):
                    p = logreg(Xtr, ytr, Xte, k)[:, 1]
                    groups = {}
                    for s_, sc in zip(te, p):
                        groups.setdefault((s_.ctx, s_.ctx_idx), []).append(sc)
                    keys = sorted(groups)
                    g_sc = np.array([np.mean(groups[g]) for g in keys])
                    g_y = np.array([int(g[0] == "fact") for g in keys])
                    obs_auc = auc(g_sc, g_y)
                    rng_p = np.random.default_rng(1)
                    null = [auc(g_sc, rng_p.permutation(g_y)) for _ in range(2000)]
                    r[feat]["kifejezésszintű_auc"] = obs_auc
                    r[feat]["kifejezések_száma"] = len(keys)
                    r[feat]["permutációs_p"] = float(np.mean([x >= obs_auc for x in null]))
            out[name] = r
        res[task_name] = out
    return res


# ------------------------------------------------------------------ ISZB
def iszb(model, tok, layer, alpha=1.0, mode="subj_last", seed=0, n_per_cat=3, batch_size=16):
    """Minden (cél-kategória, tulajdonság) élre: a más kategóriájú entitásokat transzplantációval a
    célba visszük, és mérjük, hogy a tulajdonság a cél értéke felé fordul-e (IIA). Összevetés: a
    kategóriaszintű promptolás ('Does a fish have fins?') és a tulajdonságtábla."""
    ents = D.build_entities(seed)
    mu_items, owner = [], []
    for e in ents.values():
        if e.split == "mu":
            for r in D.render_neutral(e.name):
                mu_items.append(r)
                owner.append(e)
    st = subject_states(model, tok, mu_items, mode, batch_size)[layer]
    mu = {c: st[[i for i, o in enumerate(owner) if o.category == c]].mean(0) for c in D.CATEGORIES}
    test = [e for e in ents.values() if e.split == "test"]
    rows = []
    for target in D.CATEGORIES:
        for prop in D.PROPERTIES:
            tv = D.value(prop, target)
            srcs = [e for e in test if e.category != target and D.value(prop, e.category) != tv][: n_per_cat * 5]
            if not srcs:
                continue
            items, ops = [], []
            for e in srcs:
                ed = D.Edit(e.name, e.category, target, "test")
                q = D.Question("x", ed.key, "D", prop, D.value(prop, e.category), tv, e.name, D.PROPERTIES[prop][0])
                items.append(D.render(q, ed, "plain"))
                ops.append(Op("add", (alpha * (mu[target] - mu[e.category])).astype(np.float32), mode))
            m = margins(model, tok, items, Patch(layer, ops), batch_size)
            iia = float(np.mean([(mi > 0) == tv for mi in m]))
            cat_q = D.render_proto(prop, target)
            prompt_m = float(margins(model, tok, [cat_q], None, 1)[0])
            rows.append({"target": target, "prop": prop, "truth": tv, "iia": iia,
                         "prompt_correct": (prompt_m > 0) == tv})
    return rows


# ------------------------------------------------------------------ B4
def hysteresis(model, tok, entity="robin", old="bird", new="fish", prop="breathe_underwater", kmax=6,
               batch_size=8):
    """k ellentmondó állítás ('Source i says the robin is a fish.') egy kiinduló 'bird' állítás-sor
    után, majd fordítva. A válasz m-margója a 'Can a robin breathe underwater?' kérdésre."""
    q = D.PROPERTIES[prop][0].replace("{art}", D.article(entity)).replace("{X}", entity)

    def prompt(seq):
        lines = "".join(f"Source {i + 1} says the {entity} is a {c}.\n" for i, c in enumerate(seq))
        return D.Rendered(D.FEWSHOT + lines + "Question: " + q + "\nAnswer:", [])
    up = [prompt([old] * kmax + [new] * k) for k in range(0, 2 * kmax + 1)]
    down = [prompt([new] * (2 * kmax) + [old] * k) for k in range(0, 2 * kmax + 1)]
    m_up = margins(model, tok, up, None, batch_size).tolist()
    m_down = margins(model, tok, down, None, batch_size).tolist()
    return {"up": m_up, "down": m_down, "kmax": kmax}
