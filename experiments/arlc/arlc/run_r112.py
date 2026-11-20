"""112. kör: másolásfelismerés (F91_D) – előregisztrált. Másoló/megerősítő: friss seedek 39000–39019; a többi típus
(károsodás-ellenőrzés): 39100–39111; feladatcsomag.
    python -m arlc.run_r112
"""
import json
import os
import time
from multiprocessing import Pool

from . import run_r96 as R96
from . import v4 as V4
from .core import Memory
from .generator4 import KINDS4_EXTRA, make_case4
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-112")
V_COPY = {"v3": None, "FROZEN_91": V4.FROZEN_91, "F91_D": V4.F91_D}


def job_copy(a):
    kind, seed, vi = a
    name = list(V_COPY)[vi]
    path = os.path.join(OUT, "copy", f"{KINDS4_EXTRA.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, w = make_case4(seed, kind)
    f4wrong = {(e, p) for (src, e, p, v) in w.reports if src == "f4" and v != w.truth(e).get(p)}
    tqw = [x for x in tq if (x[0], x[1]) in f4wrong]
    cfg = V_COPY[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
    t0 = time.time()
    for o in obs:
        m.observe(o)
    row = {"kind": kind, "seed": seed, "variant": name, "wrong_before": accuracy(m, tqw), "target_before": accuracy(m, tq)}
    for o in new:
        m.observe(o)
    row.update({"wrong_after": accuracy(m, tqw), "target_after": accuracy(m, tq), "post": evaluate(m, post),
                "dup": sorted(m.beam[0].dup), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    for d in ("copy", "test", "battery"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    R96.OUT = OUT
    R96.VARIANTS = {"FROZEN_91": V4.FROZEN_91, "F91_D": V4.F91_D}
    jobs_c = [(k, s, vi) for k in KINDS4_EXTRA for s in range(39000, 39020) for vi in range(3)]
    jobs_t = [(g, k, s, vi) for (g, k) in R96.CASES for s in range(39100, 39112) for vi in range(2)]
    with Pool(4) as pool:
        for r in pool.imap_unordered(R96.bat, ["FROZEN_91", "F91_D"]):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(job_copy, jobs_c):
            print(*r, flush=True)
        for r in pool.imap_unordered(R96.job, jobs_t):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
