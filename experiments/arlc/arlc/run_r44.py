"""A 44. kör benchmarkjának folytatható futtatója.

Minden (típus, seed) eset egy külön részfájlba kerül (results/kor-44/parts/), és a futtató a
már kész eseteket kihagyja. Így egy konténer-újraindítás után ott folytatódik, ahol abbamaradt.
A generátor, a módszerek és a mérőszámok változatlanok (procedural.py).

    python -m arlc.run_r44 --workers 3          # futtatás / folytatás
    python -m arlc.run_r44 --merge              # részfájlok -> results_0..4.json
"""
import argparse
import json
import os
from multiprocessing import Pool

from .procedural import METHODS, SEEDS, run_case

KINDS = ("átkategorizálás", "szabály-helyesbítés", "kivételes alfaj", "hazug forrás", "más régió")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "kor-44")
PARTS = os.path.join(OUT, "parts")


def part_path(ki, seed):
    return os.path.join(PARTS, f"{ki}_{seed}.json")


def job(args):
    ki, seed = args
    rows = [run_case(seed, KINDS[ki], m) for m in METHODS]
    tmp = part_path(ki, seed) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(rows, f, indent=1)
    os.replace(tmp, part_path(ki, seed))
    return ki, seed, sum(r["seconds"] for r in rows)


def import_existing():
    """A korábbi (megszakadt) futás teljes seedjeit részfájlokká alakítja."""
    for ki in range(len(KINDS)):
        p = os.path.join(OUT, f"results_{ki}.json")
        if not os.path.exists(p):
            continue
        rows = json.load(open(p))
        by_seed = {}
        for r in rows:
            by_seed.setdefault(r["seed"], []).append(r)
        for seed, rs in by_seed.items():
            if len(rs) == len(METHODS) and not os.path.exists(part_path(ki, seed)):
                json.dump(rs, open(part_path(ki, seed), "w"), indent=1)


def merge():
    n = 0
    for ki in range(len(KINDS)):
        rows = []
        for seed in SEEDS:
            p = part_path(ki, seed)
            if os.path.exists(p):
                rows += json.load(open(p))
                n += 1
        json.dump(rows, open(os.path.join(OUT, f"results_{ki}.json"), "w"), indent=1)
    print(f"{n} / {len(KINDS) * len(SEEDS)} eset összefésülve")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--merge", action="store_true")
    a = ap.parse_args()
    os.makedirs(PARTS, exist_ok=True)
    if a.merge:
        merge()
        return
    import_existing()
    # seed szerint haladunk, típusok között váltakozva, hogy egy részeredmény is kiegyensúlyozott legyen
    todo = [(ki, s) for s in SEEDS for ki in range(len(KINDS)) if not os.path.exists(part_path(ki, s))]
    print(f"hátralévő esetek: {len(todo)}", flush=True)
    with Pool(a.workers) as pool:
        for ki, seed, sec in pool.imap_unordered(job, todo):
            print(ki, seed, round(sec), flush=True)
    merge()


if __name__ == "__main__":
    main()
