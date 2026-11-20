"""116. kör: a FROZEN_115 az ötödik generátoron (G5: forrásfüggőségi hálózat a háttérben). Előregisztrált, friss seedek
43000–43009.
    python -m arlc.run_r116
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit
from .core import Memory
from .generator5 import KINDS5, make_case5
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-116", "test")
SEEDS = range(43000, 43010)
VARIANTS = {"v3": None, "FROZEN_91": V4.FROZEN_91, "FROZEN_115": V4.FROZEN_115}


def has_cycle(pairs):
    g = {}
    for a, b in pairs:
        g.setdefault(a, set()).add(b)

    def reach(x, y, seen):
        return any(n == y or (n not in seen and reach(n, y, seen | {n})) for n in g.get(x, ()))
    return any(reach(a, a, {a}) for a in g)


def job(a):
    kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{KINDS5.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, w = make_case5(seed, kind)
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
    for o in obs:
        m.observe(o)
    row = {"kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre), "audit_pre": audit(m, w, "G5"),
           "dup_pre": sorted(m.beam[0].dup)}
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq), "dup": sorted(H.dup), "cycle": has_cycle(H.dup),
                "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, s, vi) for vi in (2, 1, 0) for k in KINDS5 for s in SEEDS]   # a lassú változat előre
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
