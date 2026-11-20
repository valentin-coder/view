"""116. kör elemzése (előregisztrált): python -m arlc.analyze_r116"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff
from .generator5 import KINDS5

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-116", "test")
V = ("v3", "FROZEN_91", "FROZEN_115")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 4) if x else None


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(116)

    def ps(v, m, kinds=None):
        d = defaultdict(list)
        for r in R:
            if r["variant"] == v and (kinds is None or r["kind"] in kinds) and not math.isnan(r[m]):
                d[r["seed"]].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"n": len(R), "táblázat": {}}
    for k in KINDS5:
        for v in V:
            rv = [r for r in R if r["kind"] == k and r["variant"] == v]
            if rv:
                out["táblázat"][f"{k} | {v}"] = {m: nm(r[m] for r in rv) for m in ("pre", "post", "target", "sec")} | \
                    {"n": len(rv), "kör": sum(1 for r in rv if r["cycle"]), "másolás": sum(1 for r in rv if r["dup"])}
    out["H116a pre: F115 − F91"] = boot_diff(ps("FROZEN_115", "pre"), ps("FROZEN_91", "pre"), rng)
    out["H116b hazug target: F115 − v3"] = boot_diff(ps("FROZEN_115", "target", {"hazug forrás"}), ps("v3", "target", {"hazug forrás"}), rng)
    out["H116c részleges másoló target: F115 − F91"] = boot_diff(ps("FROZEN_115", "target", {"részleges új másoló"}), ps("FROZEN_91", "target", {"részleges új másoló"}), rng)
    f = [r for r in R if r["variant"] == "FROZEN_115"]
    out["H116d körök aránya (F115)"] = round(sum(1 for r in f if r["cycle"]) / max(1, len(f)), 3)
    out["post: F115 − v3"] = boot_diff(ps("FROZEN_115", "post"), ps("v3", "post"), rng)
    out["post: F91 − v3"] = boot_diff(ps("FROZEN_91", "post"), ps("v3", "post"), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
