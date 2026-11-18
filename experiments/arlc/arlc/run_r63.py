"""63. kör: nyaláb-átlagolt, bizonytalanságot jelző válasz a v4.8-π-ben (metaadat-π, jel nélkül), előregisztrált.
Esetenként egy futás; a MAP és a nyaláb poszterior-súlyú átlaga (w_H ∝ 2^(−L)) ugyanabból a memóriából.
    python -m arlc.run_r63 --pop A --workers 4
"""
import argparse
import json
import os
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .run_r44 import KINDS, beam_average
from .run_r55 import make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-63")
SEEDS = range(7000, 7015)


def probs(mem, queries):
    L = [mem.score(H) for H in mem.beam]
    lmin = min(L)
    w = [2 ** -(x - lmin) for x in L]
    z = sum(w)
    cls = [mem.closure(H, None, mem.now) for H in mem.beam]
    out = []
    for e, p, v in queries:
        acc = 0.0
        for wi, cl in zip(w, cls):
            d = cl.has.get(e, {})
            pos, neg = (p, True) in d, (p, False) in d
            acc += wi * (1.0 if pos and not neg else 0.0 if neg and not pos else 0.5)
        out.append(acc / z)
    return out


def job(a):
    pop, seed, ki = a
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case(seed, KINDS[ki], pop)
    with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META[pop])
    for o in obs + new:
        m.observe(o)
    row = {"pop": pop, "seed": seed, "kind": KINDS[ki], **beam_average(m, post, tq)}
    from .procedural import evaluate, accuracy
    row["post_map"] = evaluate(m, post)
    row["target_map"] = accuracy(m, tq)
    pt = probs(m, tq)
    row["target_frac_uncertain"] = (sum(0.2 < x < 0.8 for x in pt) / len(pt)) if pt else float("nan")
    row["target_mean_abs_from_half"] = (sum(abs(x - 0.5) for x in pt) / len(pt)) if pt else float("nan")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="A")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in SEEDS for ki in range(len(KINDS))
            if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
