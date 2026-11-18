"""60. kör: metaadatból jövő területi π és külső jelhez kötött kontextus (előregisztrált).

v4.8 = v4.4e + keverék-prior az elméletekre (κ1 = 30, q0 = 0,5, κ0 = 2, nem kalibrált), forrásonkénti π a
populáció metaadatából (A: 0,999; B: 0,7; C: 0,5), + kontextusár egy szimulált külső jelből:
    P(más kontextus | jel) Bayes-szerint, ρ = 1/64 priorral és a pontosságú jellel; ár = −log2 P.
A jel a „más régió” típus régióforrását a valószínűséggel jelzi, minden más forrást 1 − a valószínűséggel.
Esetenként részfájl, folytatható.
    python -m arlc.run_r60 --pop A --workers 4
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
from multiprocessing import Pool

from . import v4 as V4
from .run_r44 import KINDS
from .run_r55 import make_case, run_mem

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-60")
SEEDS = range(6000, 6020)
PI_META = {"A": {"book": 0.999}, "B": {"book": 0.7}, "C": {"book": 0.5, "book2": 0.5}}
RHO = 1 / 64


def ctx_costs(sources, kind, seed, ki, acc):
    rng = random.Random(seed * 31 + ki)
    costs = {}
    for s in sorted(sources):
        truly_other = (s == "region2")
        flagged = (rng.random() < acc) if truly_other else (rng.random() < 1 - acc)
        if flagged:
            p = RHO * acc / (RHO * acc + (1 - RHO) * (1 - acc))
        else:
            p = RHO * (1 - acc) / (RHO * (1 - acc) + (1 - RHO) * acc)
        costs[s] = -math.log2(p)
    return costs


def answers_metrics(m, keys, q, tq):
    a = {k: m.answer(*k, record_use=False) for k in keys}

    def met(qs):
        if not qs:
            return {}
        n = len(qs)
        ans = [(a[(e, p)], v) for e, p, v in qs]
        answered = [(x, v) for x, v in ans if x is not None]
        brier = sum(((1.0 if x is True else 0.0 if x is False else 0.5) - (1.0 if v else 0.0)) ** 2 for x, v in ans) / n
        return {"acc": sum(x == v for x, v in ans) / n, "brier": brier, "coverage": len(answered) / n,
                "sel_acc": (sum(x == v for x, v in answered) / len(answered)) if answered else float("nan")}
    return met(q), met(tq)


def job(args):
    pop, seed, ki = args
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return args
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, garbage = make_case(seed, kind, pop)
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    keys = {(e, p) for e, p, _ in q} | {(e, p) for e, p, _ in tq}
    sources = {o.source for o in obs + new}
    cc = ctx_costs(sources, kind, seed, ki, 0.9)
    v48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0), "ctx_cost": cc}
    row = {"pop": pop, "seed": seed, "kind": kind, "garbage": garbage, "ctx_cost": cc}
    for name, cfg in (("v3", None), ("v4.4e", V4.V44E_OVERRIDES), ("v4.8", v48)):
        if name == "v4.8":
            with V4.configured(cfg):
                from .core import Memory
                m = Memory(sch, mode="arlc")
            m.theory_pi = dict(PI_META[pop])
            m.c_ctx = 1e6      # minden forrásnak van jel szerinti ára (ctx_cost); ez csak biztonsági érték
            for o in obs:
                m.observe(o)
            for o in new:
                m.observe(o)
        else:
            m, _ = run_mem(sch, obs, new, cfg)
        mp, mt = answers_metrics(m, keys, q, tq)
        row.update({f"post_{name}": mp["acc"], f"brier_{name}": mp["brier"], f"cov_{name}": mp["coverage"],
                    f"sel_{name}": mp["sel_acc"], f"target_{name}": mt.get("acc", float("nan")),
                    f"tbrier_{name}": mt.get("brier", float("nan"))})
        for b in ("book", "book2"):
            ids = [o.id for o in m.obs if o.source == b]
            if ids:
                row[f"dismissed_{b}_{name}"] = (b in m.best.iso) or sum(i in m.best.rej for i in ids) >= 0.9 * len(ids)
        row[f"iso_{name}"] = sorted(m.best.iso)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return args


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="A")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in SEEDS for ki in range(len(KINDS))
            if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
