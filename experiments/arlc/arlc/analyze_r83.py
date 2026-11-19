"""83. kör elemzése (előregisztrált): python -m arlc.analyze_r83"""
import json
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-83", "test")
V = ("v4.9", "v4.9+PK", "v4.8-π+PK", "v4.4e+PK")


def per_seed(R, v, m, sets=None):
    d = defaultdict(list)
    for r in R:
        if r["variant"] == v and (sets is None or (r["gen"] + r["pop"], r["kind"]) in sets):
            d[(r["gen"] + r["pop"], r["seed"])].append(r[m])
    return {s: st.mean(x) for s, x in d.items()}


def main():
    rows = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(83)
    out = {"n": len(rows)}
    for gen in ("G1A", "G1C", "G2"):
        R = [r for r in rows if r["gen"] + r["pop"] == gen]
        out[gen] = {v: {m: round(st.mean(r[m] for r in R if r["variant"] == v), 4) for m in ("pre", "post", "target")}
                    | {"n": sum(1 for r in R if r["variant"] == v),
                       "sec": round(st.mean(r["sec"] for r in R if r["variant"] == v), 1)} for v in V}
    G2 = [r for r in rows if r["gen"] == "G2"]
    C = [r for r in rows if r["pop"] == "C"]
    liar = {("G1A", "hazug forrás"), ("G2", "hazug forrás")}
    out["H83a G2 pre: (v4.8-π+PK) − (v4.9+PK)"] = boot_diff(per_seed(G2, "v4.8-π+PK", "pre"), per_seed(G2, "v4.9+PK", "pre"), rng)
    out["H83b hazug target G1A∪G2: (v4.9+PK) − (v4.8-π+PK)"] = boot_diff(per_seed(rows, "v4.9+PK", "target", liar), per_seed(rows, "v4.8-π+PK", "target", liar), rng)
    out["H83c G1C post: (v4.9+PK) − v4.9"] = boot_diff(per_seed(C, "v4.9+PK", "post"), per_seed(C, "v4.9", "post"), rng)
    out["H83d G1C post: (v4.4e+PK) − (v4.9+PK)"] = boot_diff(per_seed(C, "v4.4e+PK", "post"), per_seed(C, "v4.9+PK", "post"), rng)
    out["G2 post: (v4.8-π+PK) − (v4.9+PK)"] = boot_diff(per_seed(G2, "v4.8-π+PK", "post"), per_seed(G2, "v4.9+PK", "post"), rng)
    out["G2 pre: (v4.4e+PK) − (v4.9+PK)"] = boot_diff(per_seed(G2, "v4.4e+PK", "pre"), per_seed(G2, "v4.9+PK", "pre"), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
