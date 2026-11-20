"""107. kör: szabályok időbeli vágása (F91_R) – előregisztrált, friss seedek 37000–37014.
    python -m arlc.run_r107
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
from .run_r88 import acc_at
from .run_r96 import CASES as BASE

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-107")
SEEDS = range(37000, 37015)
VARIANTS = {"v3": None, "FROZEN_91": V4.FROZEN_91, "F91_R": V4.F91_R}
CASES = BASE + [("G3", "szabályváltozás"), ("G1k", "szabály-helyesbítés")]


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, "test", f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    hq = tau = None
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    elif gen == "G3":
        sch, obs, new, pre, post, tq, hq, tau, _ = make_case3(seed, kind, 0.3)
    elif gen == "G4":
        sch, obs, new, pre, post, tq, _ = make_case4(seed, kind)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
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
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post),
               "target": accuracy(m, tq), "hist": acc_at(m, hq, tau - 1) if hq else float("nan"),
               "sec": round(time.time() - t0, 1)}, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


def bat(name):
    path = os.path.join(OUT, "battery", f"{name}.json")
    if not os.path.exists(path):
        with V4.configured(VARIANTS[name]) as c:
            json.dump(V4.battery(c), open(path, "w"), ensure_ascii=False, default=str)
    return name


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "test"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "battery"), exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(bat, ["FROZEN_91", "F91_R"]):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
