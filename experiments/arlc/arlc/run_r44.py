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


VARIANT = None   # None: az előregisztrált futás; "v4.3": másodlagos, címkézett változat (45., 48. kör)


def part_path(ki, seed):
    d = PARTS if VARIANT is None else PARTS + "_" + VARIANT
    return os.path.join(d, f"{ki}_{seed}.json")


def run_variant(seed, kind, name):
    """A v4 helyett egy későbbi javított változat, ugyanazzal a mérőszámmal (procedural.run_case mintájára)."""
    import time
    from .core import Memory
    from . import procedural as PR
    from . import v4 as V4
    ov = {"v4.3": V4.V43_OVERRIDES}[name]
    sch, obs, new, pre, post, tq = PR.make_case(seed, kind)
    t0 = time.perf_counter()
    with V4.configured(ov):
        mem = Memory(sch, mode="arlc")
    for o in obs:
        mem.observe(o)
    pre_acc = PR.evaluate(mem, pre)
    t1 = time.perf_counter()
    for o in new:
        mem.observe(o)
    sec_total, sec_surprise = time.perf_counter() - t0, time.perf_counter() - t1
    row = {"seed": seed, "kind": kind, "method": name, "pre_acc": pre_acc, "post_acc": PR.evaluate(mem, post),
           "target_acc": PR.accuracy(mem, tq), "n_target": len(tq), "seconds": sec_total,
           "surprise_seconds": sec_surprise}
    row.update(beam_average(mem, post, tq))
    return row


def beam_average(mem, truth, tq):
    """49. kör (feltáró, nem előregisztrált): válasz a nyaláb poszterior-súlyú átlagából a MAP helyett.
    w_H ∝ 2^(−L(H)); P(igaz) = Σ w·[igaz] + ½·Σ w·[nem tudom]. Brier-pontszám a MAP-pal szemben."""
    import math
    L = [mem.score(H) for H in mem.beam]
    lmin = min(L)
    w = [2 ** -(x - lmin) for x in L]
    z = sum(w)
    cls = [mem.closure(H, None, mem.now) for H in mem.beam]

    def p_true(e, p):
        acc = 0.0
        for wi, cl in zip(w, cls):
            d = cl.has.get(e, {})
            pos, neg = (p, True) in d, (p, False) in d
            acc += wi * (1.0 if pos and not neg else 0.0 if neg and not pos else 0.5)
        return acc / z

    def scores(qs):
        if not qs:
            return float("nan"), float("nan"), float("nan"), float("nan")
        acc_a = acc_m = br_a = br_m = 0.0
        for e, p, v in qs:
            pa = p_true(e, p)
            m = mem.answer(e, p, record_use=False)
            pm = 1.0 if m is True else 0.0 if m is False else 0.5
            y = 1.0 if v else 0.0
            acc_a += (pa > 0.5) == v if pa != 0.5 else 0
            acc_m += (m == v)
            br_a += (pa - y) ** 2
            br_m += (pm - y) ** 2
        n = len(qs)
        return acc_a / n, acc_m / n, br_a / n, br_m / n
    q = [(e, p, v) for e, tr in truth.items() for p, v in tr.items() if p != "marked"]
    a, m, ba, bm = scores(q)
    ta, tm, tba, tbm = scores(tq)
    return {"avg_post_acc": a, "brier_avg": ba, "brier_map": bm, "avg_target_acc": ta,
            "brier_avg_target": tba, "brier_map_target": tbm, "beam_spread_bits": max(L) - lmin,
            "beam_n": len(L)}


def job(args):
    ki, seed = args
    if VARIANT is None:
        rows = [run_case(seed, KINDS[ki], m) for m in METHODS]
    else:
        rows = [run_variant(seed, KINDS[ki], VARIANT)]
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
    ap.add_argument("--variant", default=None)
    a = ap.parse_args()
    global VARIANT
    VARIANT = a.variant
    os.makedirs(PARTS if VARIANT is None else PARTS + "_" + VARIANT, exist_ok=True)
    if VARIANT is not None:
        todo = [(ki, s) for s in SEEDS for ki in range(len(KINDS)) if not os.path.exists(part_path(ki, s))]
        print(f"{VARIANT}: hátralévő esetek: {len(todo)}", flush=True)
        with Pool(a.workers) as pool:
            for ki, seed, sec in pool.imap_unordered(job, todo):
                print(ki, seed, round(sec), flush=True)
        return
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
