"""96. kör elemzése (előregisztrált): python -m arlc.analyze_r96"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-96")
V = ("v3", "FROZEN_91", "F91_DK")
LIAR = {("G1k", "hazug forrás"), ("G2", "hazug forrás"), ("G3", "hazug forrás"), ("G4", "hazug forrás"),
        ("G2", "torzított forrás")}


def main():
    R = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(96)

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
    out["H96a G4 post: DK − F91"] = boot_diff(ps("F91_DK", "post", {"G4"}), ps("FROZEN_91", "post", {"G4"}), rng)
    for g in ("G1k", "G2", "G3"):
        out[f"H96b {g} post: DK − F91"] = boot_diff(ps("F91_DK", "post", {g}), ps("FROZEN_91", "post", {g}), rng)
    for g in ("G1k", "G2", "G3", "G4"):
        out[f"H96c {g} post: DK − v3"] = boot_diff(ps("F91_DK", "post", {g}), ps("v3", "post", {g}), rng)
    out["H96d hazug-szerű target: DK − F91"] = boot_diff(ps("F91_DK", "target", sets=LIAR), ps("FROZEN_91", "target", sets=LIAR), rng)
    bat = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("FROZEN_91", "F91_DK")}
    out["feladatcsomag"] = bat
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k not in ("táblázat",)}, ensure_ascii=False, indent=1, default=str))
    for k, v in out["táblázat"].items():
        print(k, v)


if __name__ == "__main__":
    main()
