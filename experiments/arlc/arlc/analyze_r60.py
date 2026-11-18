"""A 60. kör előregisztrált elemzése (H60a–e), világok szerinti klaszteres bootstrappal."""
from __future__ import annotations

import json
import math
import os
import random
import statistics as st

from .analyze_r44 import boot_diff
from .analyze_r55 import per_seed

HERE = os.path.dirname(os.path.abspath(__file__))
M = ("v3", "v4.4e", "v4.8")


def load(pop):
    d = os.path.join(HERE, "..", "results", "kor-60", pop)
    if not os.path.isdir(d):
        return []
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".json")]


def _m(rows, key):
    v = [r[key] for r in rows if not (isinstance(r[key], float) and math.isnan(r[key]))]
    return round(st.mean(v), 4) if v else None


def summary(rows):
    return {m: {k: _m(rows, f"{k}_{m}") for k in ("post", "target", "brier", "cov", "sel")} for m in M}


def main():
    rng = random.Random(60)
    P = {pop: load(pop) for pop in ("A", "B", "C")}
    res = {"n": {k: len(v) for k, v in P.items()}}
    for pop, rows in P.items():
        if rows:
            res[pop] = summary(rows)
    if P["A"]:
        p = {m: per_seed(P["A"], f"post_{m}") for m in M}
        res["H60a v4.8 − v4.4e (A, post)"] = boot_diff(p["v4.8"], p["v4.4e"], rng)
        res["H60a v4.8 − v3 (A, post)"] = boot_diff(p["v4.8"], p["v3"], rng)
    if P["C"]:
        p = {m: per_seed(P["C"], f"post_{m}") for m in M}
        res["H60b v4.8 − v4.4e (C, post)"] = boot_diff(p["v4.8"], p["v4.4e"], rng)
        good = lambda r: "book2" if r["garbage"] == "book" else "book"
        res["H60b helyes gestalt-váltás (C)"] = {
            m: sum(r.get(f"dismissed_{r['garbage']}_{m}", False) and not r.get(f"dismissed_{good(r)}_{m}", False)
                   for r in P["C"]) for m in M} | {"n": len(P["C"])}
    if P["B"]:
        p = {m: per_seed(P["B"], f"post_{m}") for m in M}
        res["H60c v4.8 − v3 (B, post)"] = boot_diff(p["v4.8"], p["v3"], rng)
    reg = [r for rows in P.values() for r in rows if r["kind"] == "más régió"]
    if reg:
        for r in reg:
            r["_k"] = (r["pop"], r["seed"])
        t = {m: {r["_k"]: r[f"target_{m}"] for r in reg} for m in M}
        res["H60d más régió target: v4.8 − v4.4e"] = boot_diff(t["v4.8"], t["v4.4e"], rng)
    allr = [dict(r, seed=(r["pop"], r["seed"])) for rows in P.values() for r in rows]
    if allr:
        b = {m: per_seed(allr, f"brier_{m}") for m in M}
        res["H60e Brier v4.4e − v4.8 (összes)"] = boot_diff(b["v4.4e"], b["v4.8"], rng)
    out = os.path.join(HERE, "..", "results", "kor-60", "analysis.json")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
