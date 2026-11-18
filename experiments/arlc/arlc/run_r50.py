"""50. kör: előregisztrált ismétlés friss seedeken (3000–3029) a v4.4-egyszintű változatra.

Generátor, mérőszámok, elemzés: mint a 44. körben. Módszerek: lookup, recency, wms, arlc (v3),
v4.4-egyszintű (nyaláb-átlaggal). A v4-et a költsége miatt nem futtatom újra.
    python -m arlc.run_r50 --workers 4
"""
import argparse
import json
import os
from multiprocessing import Pool

from .procedural import run_case
from .run_r44 import KINDS, run_variant

SEEDS = range(3000, 3030)
METHODS = ("lookup", "recency", "wms", "arlc", "v4.4-egyszintű")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-50", "replication")


def path(ki, seed):
    return os.path.join(OUT, f"{ki}_{seed}.json")


def job(a):
    ki, seed = a
    rows = [run_case(seed, KINDS[ki], m) if m != "v4.4-egyszintű" else run_variant(seed, KINDS[ki], m) for m in METHODS]
    json.dump(rows, open(path(ki, seed) + ".tmp", "w"), indent=1)
    os.replace(path(ki, seed) + ".tmp", path(ki, seed))
    return ki, seed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    todo = [(ki, s) for s in SEEDS for ki in range(len(KINDS)) if not os.path.exists(path(ki, s))]
    print("hátralévő:", len(todo), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, todo):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
