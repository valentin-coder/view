"""115. kör elemzése (előregisztrált): python -m arlc.analyze_r115"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-115")
V = ("v3", "FROZEN_112", "F112_RO")
RC = {("G3", "szabályváltozás")}


def main():
    R = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(115)

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
    out["H115a szabályváltozás target: RO − F112"] = boot_diff(ps("F112_RO", "target", sets=RC), ps("FROZEN_112", "target", sets=RC), rng)
    out["H115b szabályváltozás hist: RO − F112"] = boot_diff(ps("F112_RO", "hist", sets=RC), ps("FROZEN_112", "hist", sets=RC), rng)
    for g in ("G1k", "G2", "G3", "G4"):
        out[f"H115d {g} post (szabályváltozás nélkül): RO − F112"] = boot_diff(ps("F112_RO", "post", {g}, exclude=RC), ps("FROZEN_112", "post", {g}, exclude=RC), rng)
    HK = {("G1k", "szabály-helyesbítés")}
    out["H115c helyesbítés (revízió) target: RO − F112"] = boot_diff(ps("F112_RO", "target", sets=HK), ps("FROZEN_112", "target", sets=HK), rng)
    out["szabályváltozás target: RO − v3"] = boot_diff(ps("F112_RO", "target", sets=RC), ps("v3", "target", sets=RC), rng)
    out["feladatcsomag"] = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("FROZEN_112", "F112_RO")}
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ("táblázat",)}, ensure_ascii=False, indent=1, default=str))
    for k, v in out["táblázat"].items():
        print(k, v)


if __name__ == "__main__":
    main()
