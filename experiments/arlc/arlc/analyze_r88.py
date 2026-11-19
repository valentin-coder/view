"""88. kör elemzése (előregisztrált): python -m arlc.analyze_r88"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff
from .generator3 import KINDS3

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-88", "test")
V = ("v3", "v4.4e", "befagyasztott")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 4) if x else None


def per_seed(R, v, m, kinds=None):
    d = defaultdict(list)
    for r in R:
        if r["variant"] == v and (kinds is None or r["kind"] in kinds) and not math.isnan(r[m]):
            d[r["seed"]].append(r[m])
    return {s: st.mean(x) for s, x in d.items()}


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(88)
    out = {"n": len(R), "táblázat": {}}
    for k in KINDS3:
        for v in V:
            rv = [r for r in R if r["kind"] == k and r["variant"] == v]
            out["táblázat"][f"{k} | {v}"] = {"pre": nm(r["pre"] for r in rv), "post": nm(r["post"] for r in rv),
                                             "target": nm(r["target"] for r in rv), "hist": nm(r["hist"] for r in rv),
                                             "új félretéve": round(sum(r["new_rejected"] for r in rv) / max(1, sum(r["new_n"] for r in rv)), 3),
                                             "vágás/eset": round(st.mean(r["cuts"] for r in rv), 2),
                                             "izolál": sum(1 for r in rv if r["iso"]), "sec": nm(r["sec"] for r in rv)}
    for v in V:
        rv = [r for r in R if r["variant"] == v]
        out["táblázat"][f"összes | {v}"] = {"pre": nm(r["pre"] for r in rv), "post": nm(r["post"] for r in rv)}
    out["H88a post: befagyasztott − v3"] = boot_diff(per_seed(R, "befagyasztott", "post"), per_seed(R, "v3", "post"), rng)
    out["H88b hazug target: befagyasztott − v3"] = boot_diff(per_seed(R, "befagyasztott", "target", {"hazug forrás"}), per_seed(R, "v3", "target", {"hazug forrás"}), rng)
    out["H88e elavult target: befagyasztott − v3"] = boot_diff(per_seed(R, "befagyasztott", "target", {"elavult forrás"}), per_seed(R, "v3", "target", {"elavult forrás"}), rng)
    out["post: befagyasztott − v4.4e"] = boot_diff(per_seed(R, "befagyasztott", "post"), per_seed(R, "v4.4e", "post"), rng)
    out["post: v4.4e − v3"] = boot_diff(per_seed(R, "v4.4e", "post"), per_seed(R, "v3", "post"), rng)
    out["pre: befagyasztott − v3"] = boot_diff(per_seed(R, "befagyasztott", "pre"), per_seed(R, "v3", "pre"), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
