"""88. kör: a befagyasztott konfiguráció (V4.FROZEN_88) a harmadik generátoron (G3), előregisztrált, friss seedek
24000–24019.
    python -m arlc.run_r88
Elemzési terv: docs/korok/88-befagyasztas-es-g3.md (a G3 első futtatása előtt commitolva).
"""
import json
import math
import os
import time
from collections import Counter
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit
from .core import Memory
from .generator3 import KINDS3, make_case3
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-88", "test")
SEEDS = range(24000, 24020)
VARIANTS = {"v3": None, "v4.4e": V4.V44E_OVERRIDES, "befagyasztott": V4.FROZEN_88}


def acc_at(m, queries, t):
    if not queries:
        return float("nan")
    return sum(m._ans("has", e, p, None, t, False) == v for e, p, v in queries) / len(queries)


def job(a):
    kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{KINDS3.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, hq, tau, w = make_case3(seed, kind)
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
    row = {"kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre), "audit_pre": audit(m, w, "G3")}
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq), "hist": acc_at(m, hq, tau - 1),
                "new_rejected": sum(1 for o in new if o.id in H.rej), "new_n": len(new),
                "cuts": len(H.cut), "iso": sorted(H.iso),
                "rej_post": dict(Counter(m.by_id[i].source for i in H.rej if i in m.by_id)),
                "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, s, vi) for k in KINDS3 for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
