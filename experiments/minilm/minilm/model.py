"""Kis GPT CPU-n: betanítás, befagyasztás, rétegenkénti aktivációk."""
from __future__ import annotations

import math
import time

import torch
import torch.nn as nn
import torch.nn.functional as F


class Vocab:
    def __init__(self, texts: list[str]):
        words = sorted({w for t in texts for w in t.split()})
        self.itos = ["<pad>", "<bos>", "<unk>"] + words
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    def encode(self, text: str) -> list[int]:
        return [1] + [self.stoi.get(w, 2) for w in text.split()]

    def __len__(self):
        return len(self.itos)


class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.att = nn.MultiheadAttention(d, h, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x, mask):
        a = self.ln1(x)
        x = x + self.att(a, a, a, attn_mask=mask, need_weights=False)[0]
        return x + self.mlp(self.ln2(x))


class TinyGPT(nn.Module):
    def __init__(self, vocab: int, d=128, layers=3, heads=4, ctx=40):
        super().__init__()
        self.tok, self.pos = nn.Embedding(vocab, d), nn.Embedding(ctx, d)
        self.blocks = nn.ModuleList([Block(d, heads) for _ in range(layers)])
        self.ln, self.head = nn.LayerNorm(d), nn.Linear(d, vocab, bias=False)
        self.ctx = ctx

    def forward(self, idx, return_hidden=False):
        T = idx.shape[1]
        mask = torch.triu(torch.full((T, T), float("-inf")), diagonal=1)
        x = self.tok(idx) + self.pos(torch.arange(T))
        hs = [x]
        for b in self.blocks:
            x = b(x, mask)
            hs.append(x)
        logits = self.head(self.ln(x))
        return (logits, hs) if return_hidden else logits


def batchify(seqs: list[list[int]], ctx: int):
    L = min(ctx, max(len(s) for s in seqs))
    x = torch.zeros(len(seqs), L, dtype=torch.long)
    lens = []
    for i, s in enumerate(seqs):
        s = s[:L]
        x[i, :len(s)] = torch.tensor(s)
        lens.append(len(s))
    return x, lens


def train(model: TinyGPT, seqs: list[list[int]], steps=1500, bs=64, lr=3e-3, seed=0, log_every=250):
    torch.manual_seed(seed)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    g = torch.Generator().manual_seed(seed)
    t0 = time.time()
    hist = []
    for step in range(steps):
        idx = torch.randint(len(seqs), (bs,), generator=g).tolist()
        x, lens = batchify([seqs[i] for i in idx], model.ctx)
        logits = model(x[:, :-1])
        tgt = x[:, 1:].clone()
        tgt[tgt == 0] = -100
        loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), tgt.reshape(-1), ignore_index=-100)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps - 1:
            hist.append((step, float(loss.detach())))
            print(f"  lépés {step:5d}  veszteség {float(loss.detach()):.3f}  ({time.time() - t0:.0f}s)", flush=True)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)       # befagyasztás
    return hist


@torch.inference_mode()
def activations(model: TinyGPT, seqs: list[list[int]], positions: list[int], bs=256):
    """Minden rétegre (beágyazás + blokkok) a megadott pozíció aktivációja: (L+1, n, d)."""
    out = None
    for b in range(0, len(seqs), bs):
        chunk = seqs[b:b + bs]
        x, lens = batchify(chunk, model.ctx)
        _, hs = model(x, return_hidden=True)
        if out is None:
            out = torch.zeros(len(hs), len(seqs), hs[0].shape[-1])
        for j in range(len(chunk)):
            p = min(positions[b + j], lens[j] - 1)
            for l, h in enumerate(hs):
                out[l, b + j] = h[j, p]
    return out
