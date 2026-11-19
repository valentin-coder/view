"""85. kör: a G1 generátorhiba hatása (G1 vs. a javított G1k), előregisztrált, friss seedek 21000–21019.
    python -m arlc.run_r85
Elemzési terv: docs/korok/85-g1k.md (a futtatás előtt commitolva).
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit, world_g1
from .core import Memory
from .g1k import make_case_k
from .procedural import accuracy, evaluate
from .run_r55 import make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-85", "test")
SEEDS = range(21000, 21020)
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
V49 = {**V48, **V4.V49_SM}
VARIANTS = {"v3": None, "v4.9": V49, "v4.9+PK": {**V49, "priority_exceptions": True, "priority_code": True}}
GENS = {"G1": make_case, "G1k": make_case_k}
KINDS = ("átkategorizálás", "szabály-helyesbítés", "hazug forrás")


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}_{KINDS.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, _ = GENS[gen](seed, kind, "A")
    w = world_g1(seed)
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
    for o in obs:
        m.observe(o)
    row = {"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre), "audit_pre": audit(m, w, "G1")}
    for o in new:
        m.observe(o)
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for g in GENS for k in KINDS for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
