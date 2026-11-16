"""Fagyasztott modell köré írt mag: batch-elt igen/nem margó, rejtett állapotok,
és a reziduális áramba író beavatkozó hook. Gradiens sehol nincs."""
from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
import torch

from .data import Rendered


def load_model(name: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float32)
    model.eval()
    return prepare(model, tok)


def prepare(model, tok):
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "right"
    for p in model.parameters():
        p.requires_grad_(False)
    return model, tok


def get_layers(model):
    for path in ("model.layers", "transformer.h", "gpt_neox.layers"):
        obj = model
        try:
            for attr in path.split("."):
                obj = getattr(obj, attr)
            return obj
        except AttributeError:
            continue
    raise ValueError("ismeretlen modellarchitektúra: nem találom a rétegeket")


def yes_no_ids(tok) -> tuple[int, int]:
    ids = []
    for w in (" Yes", " No"):
        enc = tok.encode(w, add_special_tokens=False)
        if len(enc) != 1:
            warnings.warn(f"'{w}' nem egyetlen token ({enc}); az elsőt használom")
        ids.append(enc[0])
    return ids[0], ids[1]


@dataclass
class Encoded:
    input_ids: torch.Tensor
    attention_mask: torch.Tensor
    subj_pos: list[list[int]]  # X-említések tokenpozíciói (minden említés, minden tokenje)
    subj_last: list[list[int]]  # említésenként az utolsó token
    last: list[int]            # a prompt utolsó (nem pad) tokenje


def encode(tok, items: Sequence[Rendered]) -> Encoded:
    enc = tok([r.text for r in items], return_tensors="pt", padding=True,
              return_offsets_mapping=True, add_special_tokens=False)
    offsets = enc.pop("offset_mapping").tolist()
    subj_pos, subj_last, last = [], [], []
    for i, r in enumerate(items):
        n = int(enc["attention_mask"][i].sum())
        last.append(n - 1)
        allpos, lastpos = [], []
        for (s, e) in r.spans:
            toks = [t for t in range(n) if offsets[i][t][1] > s and offsets[i][t][0] < e]
            if not toks:
                raise ValueError(f"az említés nem képezhető tokenekre: {r.text[s:e]!r}")
            allpos.extend(toks)
            lastpos.append(toks[-1])
        subj_pos.append(allpos)
        subj_last.append(lastpos)
    return Encoded(enc["input_ids"], enc["attention_mask"], subj_pos, subj_last, last)


@dataclass
class Op:
    """Egy batch-elem beavatkozása az adott rétegben.

    kind='add':     h <- h + vec
    kind='replace': h <- h + Q Q^T (vec - h)   (a kategória-altér cseréje)
    """
    kind: str
    vec: np.ndarray
    site: str  # 'subj_last' | 'subj_all' | 'final'


@dataclass
class Patch:
    layer: int
    ops: list[Optional[Op]]           # batch-elemenként (None = nincs beavatkozás)
    Q: Optional[np.ndarray] = None    # (d, k) ortonormált bázis a 'replace'-hez
    norm_keep: bool = False


def _positions(enc: Encoded, i: int, site: str) -> list[int]:
    if site == "subj_last":
        return enc.subj_last[i]
    if site == "subj_all":
        return enc.subj_pos[i]
    if site == "final":
        return [enc.last[i]]
    raise ValueError(site)


def _make_hook(enc: Encoded, patch: Patch, offset: int):
    Q = None if patch.Q is None else torch.as_tensor(patch.Q, dtype=torch.float32)

    def hook(module, inputs, output):
        hs = output[0] if isinstance(output, tuple) else output
        hs = hs.clone()
        for j in range(hs.shape[0]):
            op = patch.ops[offset + j]
            if op is None:
                continue
            pos = _positions(enc, offset + j, op.site)
            h = hs[j, pos, :]
            v = torch.as_tensor(op.vec, dtype=hs.dtype)
            if op.kind == "add":
                h2 = h + v
            elif op.kind == "replace":
                h2 = h + ((v - h) @ Q) @ Q.T
            else:
                raise ValueError(op.kind)
            if patch.norm_keep:
                h2 = h2 * (h.norm(dim=-1, keepdim=True) / h2.norm(dim=-1, keepdim=True).clamp_min(1e-6))
            hs[j, pos, :] = h2
        if isinstance(output, tuple):
            return (hs,) + tuple(output[1:])
        return hs

    return hook


@torch.inference_mode()
def margins(model, tok, items: Sequence[Rendered], patch: Optional[Patch] = None,
            batch_size: int = 16) -> np.ndarray:
    """m = logit(' Yes') - logit(' No') a válasz pozíciójában, opcionális beavatkozással."""
    yid, nid = yes_no_ids(tok)
    layers = get_layers(model)
    out = np.zeros(len(items), dtype=np.float64)
    for b in range(0, len(items), batch_size):
        chunk = items[b:b + batch_size]
        enc = encode(tok, chunk)
        handle = None
        if patch is not None:
            sub = Patch(patch.layer, patch.ops[b:b + batch_size], patch.Q, patch.norm_keep)
            handle = layers[patch.layer].register_forward_hook(_make_hook(enc, sub, 0))
        try:
            logits = model(input_ids=enc.input_ids, attention_mask=enc.attention_mask).logits
        finally:
            if handle is not None:
                handle.remove()
        idx = torch.tensor(enc.last)
        lg = logits[torch.arange(len(chunk)), idx]
        out[b:b + len(chunk)] = (lg[:, yid] - lg[:, nid]).double().numpy()
    return out


@torch.inference_mode()
def subject_states(model, tok, items: Sequence[Rendered], mode: str,
                   batch_size: int = 16) -> np.ndarray:
    """Rétegenkénti szubjektum-reprezentáció: (L, n, d).

    Az l-edik elem az l-edik réteg KIMENETE (hidden_states[l+1]), ugyanaz a
    hely, ahová a hook ír. mode: 'subj_last' (az utolsó említés utolsó tokenje)
    vagy 'subj_all' (az összes szubjektum-token átlaga).
    """
    n_layers = len(get_layers(model))
    res = None
    for b in range(0, len(items), batch_size):
        chunk = items[b:b + batch_size]
        enc = encode(tok, chunk)
        hs = model(input_ids=enc.input_ids, attention_mask=enc.attention_mask,
                   output_hidden_states=True).hidden_states
        if res is None:
            res = np.zeros((n_layers, len(items), hs[0].shape[-1]), dtype=np.float32)
        for j in range(len(chunk)):
            pos = enc.subj_last[j][-1:] if mode == "subj_last" else enc.subj_pos[j]
            for l in range(n_layers):
                res[l, b + j] = hs[l + 1][j, pos, :].mean(0).float().numpy()
    return res


def category_subspace(mu: dict[str, np.ndarray]) -> np.ndarray:
    """A centrált kategóriaátlagok által kifeszített altér ortonormált bázisa (d, k)."""
    M = np.stack(list(mu.values()))
    M = M - M.mean(0, keepdims=True)
    U, S, _ = np.linalg.svd(M.T, full_matrices=False)
    k = int((S > S.max() * 1e-6).sum())
    return U[:, :k].astype(np.float32)
