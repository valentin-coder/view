"""71. kör: kontextuson belüli elsőbbség (árazott eltérésekkel) a v4.8-π-ben, jellel és jel nélkül (előregisztrált).
Változatok: v4.8-π; v4.8-π + elsőbbség; v4.8-π + elsőbbség + kontextusjel (a = 0,99).
    python -m arlc.run_r71 --workers 4
"""
import json
import os
import sys
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-71")
SEEDS = range(12000, 12020)


def run(sch, obs, new, override, cc, c_ctx):
    with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0),
                        "ctx_override": override, "ctx_cost": cc}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META["A"])
    m.c_ctx = c_ctx
    for o in obs + new:
        m.observe(o)
    return m


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, g = make_case(seed, kind, "A")
    sources = {o.source for o in obs + new}
    row = {"seed": seed, "kind": kind}
    for name, ov, cc, c in (("v4.8-π", False, {}, 6.0), ("+elsőbbség", True, {}, 6.0),
                            ("+elsőbbség+jel", True, ctx_costs(sources, kind, seed, ki, 0.99), 1e6)):
        m = run(sch, obs, new, ov, cc, c)
        row[f"post_{name}"], row[f"target_{name}"] = evaluate(m, post), accuracy(m, tq)
        row[f"iso_{name}"] = sorted(m.best.iso)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in SEEDS for ki in (1, 3, 4) if not os.path.exists(os.path.join(OUT, f"{ki}_{s}.json"))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as pool:
        for a in pool.imap_unordered(job, jobs):
            print(*a, flush=True)
