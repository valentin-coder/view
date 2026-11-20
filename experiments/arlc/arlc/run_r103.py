"""103. kör: egyszerűsített mag (V5_CORE) vs. FROZEN_91 – előregisztrált, friss seedek 35000–35011.
    python -m arlc.run_r103
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator2 import make_case2
from .generator3 import make_case3
from .generator4 import make_case4
from .procedural import accuracy, evaluate
from .run_r60 import PI_META
from .run_r96 import CASES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-103")
SEEDS = range(35000, 35012)
VARIANTS = {"FROZEN_91": (V4.FROZEN_91, 1.0), "V5_CORE": (V4.V5_CORE, 1.0)}


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    cfg, qt = VARIANTS[name]
    path = os.path.join(OUT, "test", f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    elif gen == "G3":
        sch, obs, new, pre, post, tq, *_ = make_case3(seed, kind, 0.3)
    elif gen == "G4":
        sch, obs, new, pre, post, tq, _ = make_case4(seed, kind)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    t0 = time.time()
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
    m.q_temper = qt
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post),
               "target": accuracy(m, tq), "sec": round(time.time() - t0, 1)}, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


def bat(name):
    path = os.path.join(OUT, "battery", f"{name}.json")
    if not os.path.exists(path):
        cfg = V4.FROZEN_91 if name == "FROZEN_91" else V4.V5_CORE
        with V4.configured(cfg) as c:
            json.dump(V4.battery(c), open(path, "w"), ensure_ascii=False, default=str)
    return name


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "test"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "battery"), exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(bat, ["FROZEN_91", "V5_CORE"]):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
