"""Az 55. és 57. kör előregisztrált elemzése (világok szerinti klaszteres bootstrap, mint a 44. körben).
    python -m arlc.analyze_r55 55
    python -m arlc.analyze_r55 57
"""
from __future__ import annotations

import json
import math
import os
import random
import statistics as st
import sys

from .analyze_r44 import boot_diff

HERE = os.path.dirname(os.path.abspath(__file__))


def load(rnd, pop):
    d = os.path.join(HERE, "..", "results", f"kor-{rnd}", pop)
    if not os.path.isdir(d):
        return []
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".json")]


def per_seed(rows, key, filt=lambda r: True):
    out = {}
    for r in rows:
        if not filt(r):
            continue
        v = r[key]
        if isinstance(v, float) and math.isnan(v):
            continue
        out.setdefault(r["seed"], []).append(v)
    return {s: st.mean(v) for s, v in out.items()}


def summary(rows, methods):
    return {m: {k: round(st.mean(per_seed(rows, f"{k}_{m}").values()), 4)
                for k in ("post", "target")} for m in methods}


def r55():
    rng = random.Random(55)
    A, B = load(55, "A"), load(55, "B")
    M = ("v3", "v4.4e", "H1", "H2")
    res = {"n": {"A": len(A), "B": len(B)}, "A": summary(A, M) if A else None, "B": summary(B, M) if B else None}
    if A:
        p = {m: per_seed(A, f"post_{m}") for m in M}
        t = {m: per_seed(A, f"target_{m}") for m in M}
        res["H55a H2 − v3 (A, post)"] = boot_diff(p["H2"], p["v3"], rng)
        res["H55b H2 − v4.4e (A, post)"] = boot_diff(p["H2"], p["v4.4e"], rng)
        res["H55c H2 − v4.4e (A, target)"] = boot_diff(t["H2"], t["v4.4e"], rng)
        res["A visszaesés aránya"] = sum(r["fallback"] for r in A) / len(A)
    if B:
        p = {m: per_seed(B, f"post_{m}") for m in M}
        res["H55d H1 − v3 (B, post)"] = boot_diff(p["H1"], p["v3"], rng)
        res["H55e H2 − H1 (B, post)"] = boot_diff(p["H2"], p["H1"], rng)
        for g in (True, False):
            sub = [r for r in B if r["garbage"] == g]
            res[f"B {'szemét' if g else 'jó'} tankönyv"] = {"n": len(sub), **summary(sub, M),
                                                           "visszaesés": sum(r["fallback"] for r in sub) / max(1, len(sub))}
    return res


def r57():
    rng = random.Random(57)
    A, B = load(57, "A"), load(57, "B")
    M = ("v3", "v4.4e", "v4.7", "H2(v3+v4.7)")
    res = {"n": {"A": len(A), "B": len(B)}, "A": summary(A, M) if A else None, "B": summary(B, M) if B else None}
    if A and B:
        AB = [dict(r, seed=(r["pop"], r["seed"])) for r in A + B]
        p = {m: per_seed(AB, f"post_{m}") for m in M}
        res["H57a v4.7 − v3 (A∪B, post)"] = boot_diff(p["v4.7"], p["v3"], rng)
    if A:
        p = {m: per_seed(A, f"post_{m}") for m in M}
        res["H57b v4.7 − v4.4e (A, post)"] = boot_diff(p["v4.7"], p["v4.4e"], rng)
        res["feltáró: H2 − v3 (A, post)"] = boot_diff(p["H2(v3+v4.7)"], p["v3"], rng)
    if B:
        p = {m: per_seed(B, f"post_{m}") for m in M}
        res["H57c v4.7 − v3 (B, post)"] = boot_diff(p["v4.7"], p["v3"], rng)
    for r in A + B:   # H3: v4.7, katasztrófánál v3 (57. kör kiegészítés)
        r["post_H3"] = r["post_v3"] if r["dismissed_v4.7"] else r["post_v4.7"]
        r["target_H3"] = r["target_v3"] if r["dismissed_v4.7"] else r["target_v4.7"]
    if A:
        p = {m: per_seed(A, f"post_{m}") for m in ("v3", "v4.7", "H3")}
        res["H57e H3 − v4.7 (A, post)"] = boot_diff(p["H3"], p["v4.7"], rng)
        res["H57e H3 − v3 (A, post)"] = boot_diff(p["H3"], p["v3"], rng)
    if B:
        bad = [r for r in B if r["garbage"]]
        p = {m: per_seed(bad, f"post_{m}") for m in ("v4.7", "H3")}
        res["H57f H3 − v4.7 (B szemét, post)"] = boot_diff(p["H3"], p["v4.7"], rng)
    C = load(57, "C")
    if C:
        M3 = ("v3", "v4.4e", "v4.7")
        for r in C:
            fb = r["dismissed_book_v4.7"] or r["dismissed_book2_v4.7"]
            r["post_H3"] = r["post_v3"] if fb else r["post_v4.7"]
        res["C"] = summary(C, M3)
        p = {m: per_seed(C, f"post_{m}") for m in M3 + ("H3",)}
        res["H57g v4.7 − v3 (C, post)"] = boot_diff(p["v4.7"], p["v3"], rng)
        res["H57i H3 − v4.7 (C, post)"] = boot_diff(p["H3"], p["v4.7"], rng)
        res["H57h helyes gestalt-váltás (a szemét félretéve, a jó nem)"] = {
            m: sum(r[f"dismissed_{r['garbage']}_{m}"] and not r[f"dismissed_{'book2' if r['garbage'] == 'book' else 'book'}_{m}"]
                   for r in C) for m in M3} | {"n": len(C)}
    good = [r for r in A + B if not r["garbage"]]
    bad = [r for r in B if r["garbage"]]
    res["H57d félretevés"] = {
        "jó tankönyv": {m: sum(r[f"dismissed_{m}"] for r in good) for m in ("v3", "v4.4e", "v4.7")} | {"n": len(good)},
        "szemét tankönyv": {m: sum(r[f"dismissed_{m}"] for r in bad) for m in ("v3", "v4.4e", "v4.7")} | {"n": len(bad)}}
    return res


if __name__ == "__main__":
    rnd = sys.argv[1]
    res = r55() if rnd == "55" else r57()
    out = os.path.join(HERE, "..", "results", f"kor-{rnd}", "analysis.json")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))
