"""57. kör: kombinált benchmark (A és B populáció), előregisztrált. Módszerek: v3, v4.4e, v4.7;
feltáróan a kétsebességű H2 a v3 és a v4.7 fölött. Esetenként részfájl, folytatható.
    python -m arlc.run_r57 --pop A --workers 4
"""
from __future__ import annotations

import argparse
import json
import os
from multiprocessing import Pool

from . import v4 as V4
from .run_r44 import KINDS
from .run_r55 import cone, dismissed, make_case, run_mem, score

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-57")
SEEDS = range(5000, 5030)
CFGS = {"v3": None, "v4.4e": V4.V44E_OVERRIDES, "v4.7": V4.V47_OVERRIDES}


def job(args):
    pop, seed, ki = args
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return args
    sch, obs, new, pre, post, tq, garbage = make_case(seed, KINDS[ki], pop)
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    keys = {(e, p) for e, p, _ in q} | {(e, p) for e, p, _ in tq}
    row = {"pop": pop, "seed": seed, "kind": KINDS[ki], "garbage": garbage}
    mems = {}
    for name, cfg in CFGS.items():
        if pop == "C" and name == "v4.7":
            cfg = {**cfg, "ctx_cost": {"book": 10.0, "book2": 10.0, "census": 10.0}}
        m, t = run_mem(sch, obs, new, cfg)
        mems[name] = m
        a = {k: m.answer(*k, record_use=False) for k in keys}
        row[f"post_{name}"] = score(a, q)
        row[f"target_{name}"] = score(a, tq)
        row[f"dismissed_{name}"] = dismissed(m)
        if pop == "C":   # melyik tankönyvet tette félre (≥ 90% elvetve vagy izolálva)
            for b in ("book", "book2"):
                ids = [o.id for o in m.obs if o.source == b]
                row[f"dismissed_{b}_{name}"] = (b in m.best.iso) or sum(i in m.best.rej for i in ids) >= 0.9 * len(ids)
        row[f"t_{name}"] = t
        row[f"_a_{name}"] = a
    C = cone(mems["v4.7"], new)
    h2 = row["_a_v3"] if row["dismissed_v4.7"] else {k: (row["_a_v4.7"][k] if k[0] in C else row["_a_v3"][k]) for k in keys}
    row["post_H2(v3+v4.7)"] = score(h2, q)
    row["target_H2(v3+v4.7)"] = score(h2, tq)
    for name in CFGS:
        del row[f"_a_{name}"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return args


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
