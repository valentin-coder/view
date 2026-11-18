"""67. kör (feltáró): döntési margó mint azonosíthatósági mérték.
margó = L(H*) − L(MAP), ahol H* a nyaláb legjobb olyan hipotézise, amely legalább egy célkérdésre mást válaszol,
mint a MAP. Ha nincs ilyen a nyalábban, a margó alsó becslése a nyaláb teljes szórása („≥”).
    python -m arlc.run_r67 --workers 4
"""
import argparse
import json
import os
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-67")
SEEDS = range(9000, 9015)


def answers(mem, H, qs):
    cl = mem.closure(H, None, mem.now)
    out = []
    for e, p, v in qs:
        d = cl.has.get(e, {})
        pos, neg = (p, True) in d, (p, False) in d
        out.append(True if pos and not neg else False if neg and not pos else None)
    return out


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case(seed, KINDS[ki], "A")
    with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META["A"])
    for o in obs + new:
        m.observe(o)
    L = [m.score(H) for H in m.beam]
    a0 = answers(m, m.beam[0], tq)
    alt = [L[i] - L[0] for i, H in enumerate(m.beam) if answers(m, H, tq) != a0]
    row = {"seed": seed, "kind": KINDS[ki], "target_acc": accuracy(m, tq), "n_target": len(tq),
           "margin": min(alt) if alt else None, "margin_lower_bound": max(L) - L[0], "beam_n": len(L)}
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    w = ap.parse_args().workers
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in SEEDS for ki in range(len(KINDS))]
    with Pool(w) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
