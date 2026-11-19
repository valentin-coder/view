"""70. kör: típusbizonytalanságot továbbító π (előregisztrált).
Kemény: π = π(becsült típus) (66. kör). Lágy: π_eff = Σ_t P(t | becslés) π(t), kalibrált osztályozóval:
P(becsült | becslés) = a, a többi típusé (1 − a)/3. A keverék-prior komponensei típusonként közösek, ezért a
típusok keveréke pontosan egyetlen π_eff-re esik össze.
    python -m arlc.run_r70 --pop C --workers 4
"""
import argparse
import json
import os
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case, run_mem
from .run_r66 import SRC_PI, TRUE_TYPE, classify

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-70")
SEEDS = range(11000, 11015)
KIND_IDX = (0, 1, 3)
ACCS = (0.8, 0.9)


def soft_pi(t_hat, acc):
    others = [t for t in SRC_PI if t != t_hat]
    return acc * SRC_PI[t_hat] + sum((1 - acc) / len(others) * SRC_PI[t] for t in others)


def run_v48(sch, obs, new, pis):
    with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = pis
    for o in obs + new:
        m.observe(o)
    return m


def job(a):
    pop, seed, ki = a
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case(seed, KINDS[ki], pop)
    row = {"pop": pop, "seed": seed, "kind": KINDS[ki], "garbage": g}
    m, _ = run_mem(sch, obs, new, V4.V44E_OVERRIDES)
    row["post_v4.4e"], row["target_v4.4e"] = evaluate(m, post), accuracy(m, tq)
    for acc in ACCS:
        types = classify(pop, seed, ki, acc)
        row[f"types_a{acc}"] = types
        for mode, pis in (("kemény", {s: SRC_PI[t] for s, t in types.items()}),
                          ("lágy", {s: soft_pi(t, acc) for s, t in types.items()})):
            m = run_v48(sch, obs, new, pis)
            tag = f"{mode}_a{acc}"
            row[f"pi_{tag}"] = pis
            row[f"post_{tag}"], row[f"target_{tag}"] = evaluate(m, post), accuracy(m, tq)
            for b in ("book", "book2"):
                ids = [o.id for o in m.obs if o.source == b]
                if ids:
                    row[f"dismissed_{b}_{tag}"] = (b in m.best.iso) or sum(i in m.best.rej for i in ids) >= 0.9 * len(ids)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="C")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in SEEDS for ki in KIND_IDX if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
