"""103. kör elemzése (előregisztrált): python -m arlc.analyze_r103"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-103")
V = ("FROZEN_91", "V5_CORE")
SRC = {("G1k", "hazug forrás"), ("G2", "hazug forrás"), ("G3", "hazug forrás"), ("G4", "hazug forrás"),
       ("G2", "torzított forrás"), ("G4", "jó új specialista")}


def main():
    R = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(103)

    def ps(v, m, gens=None, sets=None):
        d = defaultdict(list)
        for r in R:
            if r["variant"] == v and (gens is None or r["gen"] in gens) and (sets is None or (r["gen"], r["kind"]) in sets) \
                    and not math.isnan(r[m]):
                d[(r["gen"], r["seed"])].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"n": len(R), "táblázat": {}}
    for key in sorted({(r["gen"], r["kind"]) for r in R}) + [(g, "összes") for g in ("G1k", "G2", "G3", "G4")]:
        for v in V:
            rv = [r for r in R if r["variant"] == v and r["gen"] == key[0] and (key[1] == "összes" or r["kind"] == key[1])]
            out["táblázat"][f"{key[0]} {key[1]} | {v}"] = {m: round(st.mean(x for x in (r[m] for r in rv) if not math.isnan(x)), 4)
                                                          for m in ("pre", "post", "target")}
    for g in ("G1k", "G2", "G3", "G4"):
        out[f"H103a {g} post: V5 − F91"] = boot_diff(ps("V5_CORE", "post", {g}), ps("FROZEN_91", "post", {g}), rng)
    out["H103b forrás-célkérdések: V5 − F91"] = boot_diff(ps("V5_CORE", "target", sets=SRC), ps("FROZEN_91", "target", sets=SRC), rng)
    out["feladatcsomag"] = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("FROZEN_91", "V5_CORE")}
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != "táblázat"}, ensure_ascii=False, indent=1, default=str))
    for k, v in out["táblázat"].items():
        if "összes" in k:
            print(k, v)


if __name__ == "__main__":
    main()
