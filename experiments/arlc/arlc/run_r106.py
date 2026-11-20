"""106. kör: tartózkodás a pontszám-különbség alapján (előregisztrált, friss seedek 36000–36011, négy generátor).
    python -m arlc.run_r106
"""
import json
import math
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator2 import make_case2
from .generator3 import make_case3
from .generator4 import make_case4
from .run_r44 import beam_average
from .run_r60 import PI_META
from .run_r96 import CASES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-106", "test")
SEEDS = range(36000, 36012)
VARIANTS = {"FROZEN_91": V4.FROZEN_91, "F91_Q": V4.F91_Q}
TAUS = (0.0, 1.0, 2.0, 4.0)


def ans(cl, e, p):
    d = cl.has.get(e, {})
    pos, neg = (p, True) in d, (p, False) in d
    return True if pos and not neg else False if neg and not pos else None


def abstain_metrics(m, queries):
    """τ-nként: lefedettség, szelektív pontosság, pontosság (tartózkodás = hibás), Brier (tartózkodás = ½)."""
    L = [m.score(H) for H in m.beam]
    cls = [m.closure(H, None, m.now) for H in m.beam]
    out = {}
    for tau in TAUS:
        n = ans_n = corr = 0
        brier = 0.0
        for e, p, v in queries:
            a0 = ans(cls[0], e, p)
            gap = min((L[i] - L[0] for i in range(1, len(L)) if ans(cls[i], e, p) != a0), default=float("inf"))
            a = None if (tau > 0 and gap < tau) else a0
            n += 1
            y = 1.0 if v else 0.0
            pa = 1.0 if a is True else 0.0 if a is False else 0.5
            brier += (pa - y) ** 2
            if a is not None:
                ans_n += 1
                corr += (a == v)
        out[str(tau)] = {"n": n, "answered": ans_n, "correct": corr, "brier": brier / max(1, n)}
    return out


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
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
    with V4.configured(VARIANTS[name]):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META["A"])
    for o in obs + new:
        m.observe(o)
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    ba = beam_average(m, post, tq)
    row = {"gen": gen, "kind": kind, "seed": seed, "variant": name, "beam_n": len(m.beam),
           "post": abstain_metrics(m, q), "target": abstain_metrics(m, tq),
           "brier_avg": ba["brier_avg"], "brier_avg_target": ba["brier_avg_target"], "sec": round(time.time() - t0, 1)}
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
