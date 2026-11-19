"""91. kör elemzése (előregisztrált): python -m arlc.analyze_r91"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-91", "test")
V = ("v3", "η=0", "η=1", "hibrid+V")
SRC = {("G1k", "hazug forrás"), ("G2", "hazug forrás"), ("G2", "torzított forrás"), ("G3", "hazug forrás"),
       ("G3", "elavult forrás")}


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(91)

    def ps(v, m, gens=None, sets=None):
        dd = defaultdict(list)
        for r in R:
            if r["variant"] == v and (gens is None or r["gen"] in gens) and (sets is None or (r["gen"], r["kind"]) in sets) \
                    and not math.isnan(r[m]):
                dd[(r["gen"], r["seed"])].append(r[m])
        return {k: st.mean(x) for k, x in dd.items()}
    out = {"n": len(R), "táblázat": {}}
    for g in ("G1k", "G2", "G3"):
        for v in V:
            rv = [r for r in R if r["gen"] == g and r["variant"] == v]
            out["táblázat"][f"{g} | {v}"] = {m: round(st.mean(x for x in (r[m] for r in rv) if not math.isnan(x)), 4)
                                             for m in ("pre", "post", "target")} | {"sec": round(st.mean(r["sec"] for r in rv), 1)}
        for k in sorted({r["kind"] for r in R if r["gen"] == g}):
            for v in V:
                rv = [r for r in R if r["gen"] == g and r["kind"] == k and r["variant"] == v]
                out["táblázat"][f"{g} {k} | {v}"] = {m: round(st.mean(x for x in (r[m] for r in rv) if not math.isnan(x)), 4)
                                                     for m in ("post", "target")}
    for g in ("G1k", "G2", "G3"):
        out[f"H91a {g}: η=0 − v3 (post)"] = boot_diff(ps("η=0", "post", {g}), ps("v3", "post", {g}), rng)
        out[f"H91b {g}: hibrid+V − v3 (post)"] = boot_diff(ps("hibrid+V", "post", {g}), ps("v3", "post", {g}), rng)
        out[f"{g}: hibrid+V − η=1 (post)"] = boot_diff(ps("hibrid+V", "post", {g}), ps("η=1", "post", {g}), rng)
    out["H91c forrás-célkérdések: hibrid+V − η=0"] = boot_diff(ps("hibrid+V", "target", sets=SRC), ps("η=0", "target", sets=SRC), rng)
    out["forrás-célkérdések: hibrid+V − η=1"] = boot_diff(ps("hibrid+V", "target", sets=SRC), ps("η=1", "target", sets=SRC), rng)
    out["H91d G3 pre: hibrid+V − η=1"] = boot_diff(ps("hibrid+V", "pre", {"G3"}), ps("η=1", "pre", {"G3"}), rng)
    st_ = [r["target"] for r in R if r["gen"] == "G3" and r["kind"] == "állapotváltozás" and r["variant"] == "hibrid+V"]
    out["H91e G3 állapotváltozás target (hibrid+V)"] = round(st.mean(st_), 4) if st_ else None
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "táblázat"}, ensure_ascii=False, indent=1))
    for k, v in out["táblázat"].items():
        print(k, v)


if __name__ == "__main__":
    main()
