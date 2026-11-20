"""111. kör: forrásmásolás bevált forrásról (a függetlenségi feltevés próbája). Előregisztrált, friss seedek 38000–38019.
    python -m arlc.run_r111
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator4 import KINDS4_EXTRA, make_case4
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-111", "test")
SEEDS = range(38000, 38020)
VARIANTS = {"v3": None, "FROZEN_91": V4.FROZEN_91, "F91_Q": V4.F91_Q}


def job(a):
    kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{KINDS4_EXTRA.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, w = make_case4(seed, kind)
    f4wrong = {(e, p) for (src, e, p, v) in w.reports if src == "f4" and v != w.truth(e).get(p)}
    tq_wrong = [(e, p, v) for (e, p, v) in tq if (e, p) in f4wrong]
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
    row = {"kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre),
           "target_before": accuracy(m, tq), "wrong_before": accuracy(m, tq_wrong), "n_wrong": len(tq_wrong)}
    for o in new:
        m.observe(o)
    row.update({"post": evaluate(m, post), "target_after": accuracy(m, tq), "wrong_after": accuracy(m, tq_wrong),
                "new_rejected": sum(1 for o in new if o.id in m.beam[0].rej), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, s, vi) for k in KINDS4_EXTRA for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
