"""101. kör: prior-érzékenységi protokoll a FROZEN_91-re (előregisztrált, friss seedek 33000–33011).
    python -m arlc.run_r101
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory, Obs
from .g1k import make_case_k
from .generator2 import make_case2
from .generator3 import make_case3
from .generator4 import make_case4
from .procedural import accuracy, evaluate
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-101", "test")
SEEDS = range(33000, 33012)
F = V4.FROZEN_91
NC = F["source_newcomer"]
VARIANTS = {
    "alap": ({}, 1.0, None),
    "π_új=0,8": ({"source_newcomer": (0.8,) + NC[1:]}, 1.0, None),
    "π_új=0,95": ({"source_newcomer": (0.95,) + NC[1:]}, 1.0, None),
    "π_új=0,99": ({"source_newcomer": (0.99,) + NC[1:]}, 1.0, None),
    "ε×½": ({"exc_prior": 0.025}, 1.0, None),
    "ε×2": ({"exc_prior": 0.1}, 1.0, None),
    "(1−q)×½": ({}, 0.5, None),
    "(1−q)×2": ({}, 2.0, None),
    "upd×½": ({}, 1.0, 0.15),
    "upd×2": ({}, 1.0, 0.6),
}
CASES = [("G1k", "hazug forrás"), ("G1k", "szabály-helyesbítés"), ("G2", "hazug forrás"), ("G3", "hazug forrás"),
         ("G3", "állapotváltozás"), ("G4", "hazug forrás"), ("G4", "jó új specialista")]


def scale_q(obs, f):
    if f == 1.0:
        return obs
    return [Obs(o.id, o.source, o.time, min(0.999, max(0.501, 1 - (1 - o.q) * f)), o.lit, o.rule) for o in obs]


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    ov, f, upd = VARIANTS[name]
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    elif gen == "G3":
        sch, obs, new, pre, post, tq, *_ = make_case3(seed, kind, upd or 0.3)
    elif gen == "G4":
        sch, obs, new, pre, post, tq, _ = make_case4(seed, kind)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    obs, new = scale_q(obs, f), scale_q(new, f)
    t0 = time.time()
    with V4.configured({**F, **ov}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META["A"])
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post),
               "target": accuracy(m, tq), "sec": round(time.time() - t0, 1)}, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in CASES for s in SEEDS for vi, n in enumerate(VARIANTS)
            if not (n.startswith("upd") and g != "G3")]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
