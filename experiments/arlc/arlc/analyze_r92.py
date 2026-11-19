"""92. kör elemzése (előregisztrált): python -m arlc.analyze_r92"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-92")


def main():
    bat = {n: json.load(open(os.path.join(B, "battery", f"{n}.json"))) for n in ("v4.4e", "FROZEN_88", "FROZEN_91")}
    R = [json.load(open(os.path.join(B, "test", f))) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    rng = random.Random(92)

    def ps(v, m, pop, garbage=None):
        d = defaultdict(list)
        for r in R:
            if r["variant"] == v and r["pop"] in pop and (garbage is None or r["garbage"] == garbage) and not math.isnan(r[m]):
                d[(r["pop"], r["seed"])].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"feladatcsomag": bat, "táblázat": {}}
    for pop in ("B", "C"):
        for v in ("v3", "FROZEN_88", "FROZEN_91"):
            rv = [r for r in R if r["pop"] == pop and r["variant"] == v]
            out["táblázat"][f"{pop} | {v}"] = {m: round(st.mean(r[m] for r in rv if not math.isnan(r[m])), 4) for m in ("pre", "post", "target")} | \
                {"sec": round(st.mean(r["sec"] for r in rv), 1), "n": len(rv)}
        if pop == "B":
            for v in ("v3", "FROZEN_88", "FROZEN_91"):
                rv = [r for r in R if r["pop"] == "B" and r["variant"] == v and r["garbage"]]
                out["táblázat"][f"B-szemét | {v}"] = {m: round(st.mean(r[m] for r in rv), 4) for m in ("post", "target")}
    out["H92b B post: F91 − F88"] = boot_diff(ps("FROZEN_91", "post", {"B"}), ps("FROZEN_88", "post", {"B"}), rng)
    out["H92b B-szemét post: F91 − F88"] = boot_diff(ps("FROZEN_91", "post", {"B"}, True), ps("FROZEN_88", "post", {"B"}, True), rng)
    out["H92c C post: F91 − F88"] = boot_diff(ps("FROZEN_91", "post", {"C"}), ps("FROZEN_88", "post", {"C"}), rng)
    out["H92d hazug target B∪C: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"B", "C"}), ps("v3", "target", {"B", "C"}), rng)
    json.dump(out, open(os.path.join(B, "analysis.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != "feladatcsomag"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
