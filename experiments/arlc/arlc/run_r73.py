"""73. kör: jelhez kötött kontextuson belüli elsőbbség (előregisztrált).
Változatok (mind v4.8-π + kontextusjel a = 0,99): elsőbbség nélkül; elsőbbség minden izolált forrásra (71. kör);
elsőbbség csak a jel által „más kontextusnak” jelzett forrásra.
    python -m arlc.run_r73 4
"""
import json
import math
import os
import random
import sys
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META, RHO, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-73")
SEEDS = range(13000, 13020)


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, g = make_case(seed, kind, "A")
    sources = {o.source for o in obs + new}
    cc = ctx_costs(sources, kind, seed, ki, 0.99)
    flagged = {s for s, c in cc.items() if c < -math.log2(RHO)}      # a jel „más kontextus”-t mond
    row = {"seed": seed, "kind": kind, "flagged": sorted(flagged)}
    for name, ov, srcs in (("jel", False, None), ("jel+elsőbbség", True, None), ("jel+jelzett elsőbbség", True, flagged)):
        with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0),
                            "ctx_override": ov, "ctx_cost": cc}):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
        m.c_ctx = 1e6
        m.ctx_override_sources = srcs
        for o in obs + new:
            m.observe(o)
        row[f"post_{name}"], row[f"target_{name}"] = evaluate(m, post), accuracy(m, tq)
        row[f"iso_{name}"] = sorted(m.best.iso)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in SEEDS for ki in (3, 4) if not os.path.exists(os.path.join(OUT, f"{ki}_{s}.json"))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as pool:
        for x in pool.imap_unordered(job, jobs):
            print(*x, flush=True)
