"""88. kör, feltáró rész elemzése: python -m arlc.analyze_x88"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff
from .generator3 import KINDS3

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-88")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 3) if x else None


def main():
    R = [json.load(open(os.path.join(B, "explore", f))) for f in os.listdir(os.path.join(B, "explore")) if f.endswith(".json")]
    R += [dict(json.load(open(os.path.join(B, "test", f))), upd=0.05) for f in os.listdir(os.path.join(B, "test")) if f.endswith(".json")]
    g = defaultdict(list)
    for r in R:
        g[(r["variant"], r["upd"])].append(r)
    out = {}
    for k in sorted(g):
        rv = g[k]
        row = {"n": len(rv), "pre": nm(r["pre"] for r in rv), "post": nm(r["post"] for r in rv),
               "field téves félretevés/eset": round(st.mean(r["audit_pre"].get("field:F:téves_félretevés", 0) for r in rv), 1)}
        for kd in KINDS3:
            row[f"{kd}: target / hist"] = (nm(r["target"] for r in rv if r["kind"] == kd), nm(r["hist"] for r in rv if r["kind"] == kd))
        out[f"{k[0]} | upd={k[1]}"] = row

    def ps(v, upd, m):
        d = defaultdict(list)
        for r in g[(v, upd)]:
            if not math.isnan(r[m]):
                d[r["seed"]].append(r[m])
        return {s: st.mean(x) for s, x in d.items()}
    rng = random.Random(881)
    out["upd=0,3: befagyasztott − v3 (post)"] = boot_diff(ps("befagyasztott", 0.3, "post"), ps("v3", 0.3, "post"), rng)
    out["upd=0,3: befagyasztott − v3 (pre)"] = boot_diff(ps("befagyasztott", 0.3, "pre"), ps("v3", 0.3, "pre"), rng)
    out["upd=0,05: (befagyasztott − N) − v3 (post)"] = boot_diff(ps("befagyasztott − N", 0.05, "post"), ps("v3", 0.05, "post"), rng)
    out["upd=0,3: (befagyasztott − N) − v3 (post)"] = boot_diff(ps("befagyasztott − N", 0.3, "post"), ps("v3", 0.3, "post"), rng)
    json.dump(out, open(os.path.join(B, "explore_analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
