"""92. kör: a FROZEN_91 biztonsági ellenőrzése (előregisztrált).
(1) a korábbi körök feladatcsomagja (v4.battery) három konfigurációra;
(2) G1k-B (szemét-tankönyv) és G1k-C (rivális elméletek), hazug forrás, friss seedek 27000–27019.
    python -m arlc.run_r92
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .procedural import accuracy, evaluate
from .run_r55 import is_garbage
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-92")
CFGS = {"v4.4e": V4.V44E_OVERRIDES, "FROZEN_88": V4.FROZEN_88, "FROZEN_91": V4.FROZEN_91}
VARIANTS = {"v3": None, "FROZEN_88": V4.FROZEN_88, "FROZEN_91": V4.FROZEN_91}
SEEDS = range(27000, 27020)


def bat(name):
    path = os.path.join(OUT, "battery", f"{name}.json")
    if os.path.exists(path):
        return name
    t0 = time.time()
    with V4.configured(CFGS[name]) as c:
        out = V4.battery(c)
    out["sec"] = round(time.time() - t0, 1)
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    return name


def job(a):
    pop, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, "test", f"{pop}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case_k(seed, "hazug forrás", pop)
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META[pop])
    for o in obs:
        m.observe(o)
    row = {"pop": pop, "seed": seed, "variant": name, "garbage": bool(g) if pop == "B" else None, "pre": evaluate(m, pre)}
    for o in new:
        m.observe(o)
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "battery"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "test"), exist_ok=True)
    jobs = [("B", s, vi) for s in SEEDS for vi in range(3)] + [("C", s, vi) for s in SEEDS for vi in range(3)]
    with Pool(4) as pool:
        for r in pool.imap_unordered(bat, list(CFGS)):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
