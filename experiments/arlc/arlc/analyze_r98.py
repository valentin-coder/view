"""98. kör elemzése (előregisztrált): python -m arlc.analyze_r98"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-98", "test")
V = ("v3", "FROZEN_91", "FROZEN_91+jel")


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(98)

    def ps(v, m, kinds=None):
        d = defaultdict(list)
        for r in R:
            if r["variant"] == v and (kinds is None or r["kind"] in kinds) and not math.isnan(r[m]):
                d[r["seed"]].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"n": len(R), "táblázat": {}}
    for k in sorted({r["kind"] for r in R}):
        for v in V:
            rv = [r for r in R if r["kind"] == k and r["variant"] == v]
            out["táblázat"][f"{k} | {v}"] = {m: round(st.mean(x for x in (r[m] for r in rv) if not math.isnan(x)), 4)
                                             for m in ("pre", "post", "target")} | {"izolál": sum(1 for r in rv if r["iso"])}
    out["H98a post: F91 − v3"] = boot_diff(ps("FROZEN_91", "post"), ps("v3", "post"), rng)
    out["H98b kivételes alfaj target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"kivételes alfaj"}), ps("v3", "target", {"kivételes alfaj"}), rng)
    out["H98c más régió target: jel − F91"] = boot_diff(ps("FROZEN_91+jel", "target", {"más régió"}), ps("FROZEN_91", "target", {"más régió"}), rng)
    out["H98d más régió target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"más régió"}), ps("v3", "target", {"más régió"}), rng)
    out["szabály-helyesbítés target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"szabály-helyesbítés"}), ps("v3", "target", {"szabály-helyesbítés"}), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
