"""75. kör: a legjobb konfiguráció nagy, előregisztrált összevetése (A + C).
Módszerek: v3; v4.4e; v4.8-π (metaadat-π); v4.8-π+jel (a = 0,99, jelzett elsőbbség). A legjobbnál a nyaláb-átlag is.
    python -m arlc.run_r75 --pop A --workers 4
"""
import argparse
import json
import math
import os
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy, evaluate
from .run_r44 import KINDS, beam_average
from .run_r55 import make_case, run_mem
from .run_r60 import PI_META, RHO, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-75")
SEEDS = {"A": range(14000, 14030), "C": range(14000, 14020)}
KIND_IDX = (0, 3, 4)          # átkategorizálás, hazug forrás, más régió


def brier_map(m, post):
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    s = 0.0
    for e, p, v in q:
        a = m.answer(e, p, record_use=False)
        pa = 1.0 if a is True else 0.0 if a is False else 0.5
        s += (pa - (1.0 if v else 0.0)) ** 2
    return s / len(q)


def job(a):
    pop, seed, ki = a
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, g = make_case(seed, kind, pop)
    row = {"pop": pop, "seed": seed, "kind": kind, "garbage": g}
    for name, cfg in (("v3", None), ("v4.4e", V4.V44E_OVERRIDES)):
        m, _ = run_mem(sch, obs, new, cfg)
        row[f"post_{name}"], row[f"target_{name}"], row[f"brier_{name}"] = evaluate(m, post), accuracy(m, tq), brier_map(m, post)
    sources = {o.source for o in obs + new}
    cc = ctx_costs(sources, kind, seed, ki, 0.99)
    flagged = frozenset(s for s, c in cc.items() if c < -math.log2(RHO))
    for name, sig in (("v4.8-π", False), ("v4.8-π+jel", True)):
        cfg = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
        if sig:
            cfg.update({"ctx_override": True, "ctx_cost": cc, "ctx_override_sources": flagged})
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META[pop])
        if sig:
            m.c_ctx = 1e6
        for o in obs + new:
            m.observe(o)
        row[f"post_{name}"], row[f"target_{name}"], row[f"brier_{name}"] = evaluate(m, post), accuracy(m, tq), brier_map(m, post)
        if sig:
            ba = beam_average(m, post, tq)
            row["brier_avg_v4.8-π+jel"], row["post_avg_v4.8-π+jel"] = ba["brier_avg"], ba["avg_post_acc"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="A")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in SEEDS[a.pop] for ki in KIND_IDX if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
