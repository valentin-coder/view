"""93. kör elemzése (előregisztrált): python -m arlc.analyze_r93"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff
from .generator4 import KINDS4

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-93", "test")
V = ("v3", "FROZEN_88", "FROZEN_91")


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(93)

    def ps(v, m, kinds=None):
        d = defaultdict(list)
        for r in R:
            if r["variant"] == v and (kinds is None or r["kind"] in kinds) and not math.isnan(r[m]):
                d[r["seed"]].append(r[m])
        return {k: st.mean(x) for k, x in d.items()}
    out = {"n": len(R), "táblázat": {}}
    for k in KINDS4 + ("összes",):
        for v in V:
            rv = [r for r in R if r["variant"] == v and (k == "összes" or r["kind"] == k)]
            row = {m: round(st.mean(r[m] for r in rv if not math.isnan(r[m])), 4) for m in ("pre", "post", "target")}
            if k != "összes":
                nr = defaultdict(int); nn = defaultdict(int)
                for r in rv:
                    for s, n in r["new_rejected"].items():
                        nr[s] += n
                    for s, n in r["new_n"].items():
                        nn[s] += n
                row["új félretéve"] = {s: round(nr[s] / nn[s], 3) for s in nn}
            out["táblázat"][f"{k} | {v}"] = row
    out["H93a post: F91 − v3"] = boot_diff(ps("FROZEN_91", "post"), ps("v3", "post"), rng)
    out["H93b hazug target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"hazug forrás"}), ps("v3", "target", {"hazug forrás"}), rng)
    t = lambda k: st.mean(r["target"] for r in R if r["variant"] == "FROZEN_91" and r["kind"] == k)
    out["H93c F91 target: visszhang − hazug"] = round(t("visszhang") - t("hazug forrás"), 4)
    out["H93d romló target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"romló forrás"}), ps("v3", "target", {"romló forrás"}), rng)
    out["H93e specialista target: F91 − v3"] = boot_diff(ps("FROZEN_91", "target", {"jó új specialista"}), ps("v3", "target", {"jó új specialista"}), rng)
    out["post: F91 − F88"] = boot_diff(ps("FROZEN_91", "post"), ps("FROZEN_88", "post"), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
