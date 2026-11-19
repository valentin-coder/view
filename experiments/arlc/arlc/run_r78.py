"""78. kör: kontextusfüggő indukció – ki, be, vagy csak jelzett forrásra (előregisztrált), mindkét generátoron.
    python -m arlc.run_r78 4
"""
import json
import math
import os
import sys
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator2 import KINDS2, make_case2
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import RHO, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-78")
SEEDS = range(16000, 16020)
JOBS = [("G2", s, ki) for s in SEEDS for ki in (0, 1, 3)] + [("G1", s, ki) for s in SEEDS for ki in (0, 1, 3)]


def flagged_sources(sources, kind, seed, ki):
    cc = ctx_costs(sources, kind, seed, ki, 0.99)
    return frozenset(s for s, c in cc.items() if c < -math.log2(RHO))


def job(a):
    gen, seed, ki = a
    path = os.path.join(OUT, gen, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        kind = KINDS2[ki]
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    else:
        kind = KINDS[ki]
        sch, obs, new, pre, post, tq, _ = make_case(seed, kind, "A")
    fl = flagged_sources({o.source for o in obs + new}, kind, seed, ki)
    row = {"gen": gen, "seed": seed, "kind": kind, "flagged": sorted(fl)}
    for name, ov in (("v4.4e", {}), ("v4.4e−ki", {"ctx_induction": False}),
                     ("v4.4e jelzett ki", {"ctx_induction_sources": fl})):
        with V4.configured({**V4.V44E_OVERRIDES, **ov}):
            m = Memory(sch, mode="arlc")
        for o in obs:
            m.observe(o)
        row[f"pre_{name}"] = evaluate(m, pre)
        for o in new:
            m.observe(o)
        row[f"post_{name}"], row[f"target_{name}"] = evaluate(m, post), accuracy(m, tq)
        row[f"iso_{name}"] = sorted(m.best.iso)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    jobs = [j for j in JOBS if not os.path.exists(os.path.join(OUT, j[0], f"{j[2]}_{j[1]}.json"))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as pool:
        for x in pool.imap_unordered(job, jobs):
            print(*x, flush=True)
