"""112. kör elemzése (előregisztrált): python -m arlc.analyze_r112"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-112")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 4) if x else None


def main():
    C = [json.load(open(os.path.join(B, "copy", f))) for f in os.listdir(os.path.join(B, "copy")) if f.endswith(".json")]
    T = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(112)
    out = {"n_copy": len(C), "n_test": len(T), "másoló/megerősítő": {}}
    for k in ("bevált másoló", "független megerősítő"):
        for v in ("v3", "FROZEN_91", "F91_D"):
            rv = [r for r in C if r["kind"] == k and r["variant"] == v]
            out["másoló/megerősítő"][f"{k} | {v}"] = {m: nm(r[m] for r in rv) for m in ("wrong_before", "wrong_after", "target_before", "target_after", "post")} | \
                {"észlelt másolás": sum(1 for r in rv if r["dup"])}
    ps = lambda rows, v, m: {r["seed"]: r[m] for r in rows if r["variant"] == v and not math.isnan(r[m])}
    cp = [r for r in C if r["kind"] == "bevált másoló"]
    ind = [r for r in C if r["kind"] == "független megerősítő"]
    out["H112a hibás részhalmaz utána: D − F91"] = boot_diff(ps(cp, "F91_D", "wrong_after"), ps(cp, "FROZEN_91", "wrong_after"), rng)
    out["H112b D utána − F91 előtte"] = round(nm(r["wrong_after"] for r in cp if r["variant"] == "F91_D") - nm(r["wrong_before"] for r in cp if r["variant"] == "FROZEN_91"), 4)
    out["H112c megerősítő target utána: D − F91"] = boot_diff(ps(ind, "F91_D", "target_after"), ps(ind, "FROZEN_91", "target_after"), rng)
    for g in ("G1k", "G2", "G3", "G4"):
        d = defaultdict(list); f = defaultdict(list)
        for r in T:
            if r["gen"] == g and not math.isnan(r["post"]):
                (d if r["variant"] == "F91_D" else f)[r["seed"]].append(r["post"])
        out[f"H112d {g} post: D − F91"] = boot_diff({k: st.mean(x) for k, x in d.items()}, {k: st.mean(x) for k, x in f.items()}, rng)
    bat = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("FROZEN_91", "F91_D")}
    out["feladatcsomag eltérések"] = {k: (bat["FROZEN_91"][k], bat["F91_D"][k]) for k in bat["FROZEN_91"] if bat["FROZEN_91"][k] != bat["F91_D"][k]}
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
