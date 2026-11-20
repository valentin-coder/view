"""98. kör: a G1 ritkábban mért meglepetéstípusai a FROZEN_91-gyel a G1k-n (előregisztrált, friss seedek 32000–32019).
    python -m arlc.run_r98
"""
import json
import math
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r60 import PI_META, RHO, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-98", "test")
SEEDS = range(32000, 32020)
KIND_IDX = (1, 2, 4)            # szabály-helyesbítés, kivételes alfaj, más régió
VARIANTS = ("v3", "FROZEN_91", "FROZEN_91+jel")


def job(a):
    ki, seed, vi = a
    name = VARIANTS[vi]
    path = os.path.join(OUT, f"{ki}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    t0 = time.time()
    if name == "v3":
        m = Memory(sch, mode="arlc")
    else:
        cfg = dict(V4.FROZEN_91)
        if name.endswith("+jel"):
            cc = ctx_costs({o.source for o in obs + new}, kind, seed, ki, 0.99)
            flagged = frozenset(s for s, c in cc.items() if c < -math.log2(RHO))
            cfg.update({"ctx_override": True, "ctx_cost": cc, "ctx_override_sources": flagged})
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
        if name.endswith("+jel"):
            m.c_ctx = 1e6
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post), "target": accuracy(m, tq),
               "iso": sorted(m.beam[0].iso), "sec": round(time.time() - t0, 1)}, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(ki, s, vi) for ki in KIND_IDX for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
