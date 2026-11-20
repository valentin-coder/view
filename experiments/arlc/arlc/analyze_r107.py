"""107. kör elemzése (előregisztrált): python -m arlc.analyze_r107"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-107")
V = ("v3", "FROZEN_91", "F91_R")
RC = {("G3", "szabályváltozás")}


def main():
    R = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(107)

    def ps(v, m, gens=None, sets=None, exclude=None):
        d = defaultdict(list)
        for r in R:
            k = (r["gen"], r["kind"])
            if r["variant"] == v and (gens is None or r["gen"] in gens) and (sets is None or k in sets) \
                    and (exclude is None or k not in exclude) and not math.isnan(r[m]):
                d[(r["gen"], r["seed"])].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"n": len(R), "táblázat": {}}
    for key in sorted({(r["gen"], r["kind"]) for r in R}):
        for v in V:
            rv = [r for r in R if r["variant"] == v and (r["gen"], r["kind"]) == key]
            nm = lambda m: round(st.mean([r[m] for r in rv if not math.isnan(r[m])]), 4) if any(not math.isnan(r[m]) for r in rv) else None
            out["táblázat"][f"{key[0]} {key[1]} | {v}"] = {m: nm(m) for m in ("pre", "post", "target", "hist")}
    out["H107a szabályváltozás target: R − F91"] = boot_diff(ps("F91_R", "target", sets=RC), ps("FROZEN_91", "target", sets=RC), rng)
    out["H107b szabályváltozás hist: R − F91"] = boot_diff(ps("F91_R", "hist", sets=RC), ps("FROZEN_91", "hist", sets=RC), rng)
    for g in ("G1k", "G2", "G3", "G4"):
        out[f"H107c {g} post (szabályváltozás nélkül): R − F91"] = boot_diff(ps("F91_R", "post", {g}, exclude=RC), ps("FROZEN_91", "post", {g}, exclude=RC), rng)
    out["szabályváltozás target: R − v3"] = boot_diff(ps("F91_R", "target", sets=RC), ps("v3", "target", sets=RC), rng)
    out["feladatcsomag"] = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("FROZEN_91", "F91_R")}
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ("táblázat",)}, ensure_ascii=False, indent=1, default=str))
    for k, v in out["táblázat"].items():
        print(k, v)


if __name__ == "__main__":
    main()
