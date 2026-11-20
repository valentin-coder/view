"""101. kör elemzése (előregisztrált): python -m arlc.analyze_r101"""
import json
import math
import os
import statistics as st

from .run_r101 import VARIANTS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-101", "test")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 4) if x else None


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    out = {"n": len(R), "post (generátoronként)": {}, "target (típusonként)": {}}
    for v in VARIANTS:
        out["post (generátoronként)"][v] = {g: nm(r["post"] for r in R if r["variant"] == v and r["gen"] == g)
                                           for g in ("G1k", "G2", "G3", "G4")}
        out["target (típusonként)"][v] = {f"{g} {k}": nm(r["target"] for r in R if r["variant"] == v and r["gen"] == g and r["kind"] == k)
                                          for (g, k) in sorted({(r["gen"], r["kind"]) for r in R})}
    base = out["post (generátoronként)"]["alap"]
    out["Δpost az alaphoz"] = {v: {g: (None if d[g] is None else round(d[g] - base[g], 4)) for g in d}
                               for v, d in out["post (generátoronként)"].items()}
    liar = lambda v: nm(r["target"] for r in R if r["variant"] == v and r["kind"] == "hazug forrás")
    corr = lambda v: nm(r["target"] for r in R if r["variant"] == v and r["kind"] in ("szabály-helyesbítés", "jó új specialista"))
    order = ["π_új=0,8", "alap", "π_új=0,95", "π_új=0,99"]
    out["H101b hazug target π_új szerint"] = {v: liar(v) for v in order}
    out["H101b helyesbítés+specialista target π_új szerint"] = {v: corr(v) for v in order}
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
