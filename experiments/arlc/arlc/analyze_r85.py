"""85. kör elemzése (előregisztrált): python -m arlc.analyze_r85"""
import json
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-85", "test")
V = ("v3", "v4.9", "v4.9+PK")


def per_seed(R, gen, v, m):
    d = defaultdict(list)
    for r in R:
        if r["gen"] == gen and r["variant"] == v:
            d[r["seed"]].append(r[m] if not callable(m) else m(r))
    return {s: st.mean(x) for s, x in d.items()}


def isa_false(r):
    return sum(n for k, n in r["audit_pre"].items() if k.endswith(":I:téves_félretevés"))


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(85)
    out = {"n": len(R)}
    for g in ("G1", "G1k"):
        out[g] = {}
        for v in V:
            rv = [r for r in R if r["gen"] == g and r["variant"] == v]
            a = defaultdict(float)
            for r in rv:
                for k, n in r["audit_pre"].items():
                    a[k] += n / len(rv)
            out[g][v] = {m: round(st.mean(r[m] for r in rv), 4) for m in ("pre", "post", "target")} | \
                        {"n": len(rv), "isa téves félretevés/eset": round(st.mean(isa_false(r) for r in rv), 2),
                         "audit": {k: round(x, 2) for k, x in sorted(a.items())}}
    for v in V:
        out[f"H85a {v}: G1k − G1 (pre)"] = boot_diff(per_seed(R, "G1k", v, "pre"), per_seed(R, "G1", v, "pre"), rng)
    for g in ("G1", "G1k"):
        for a, b in (("v4.9+PK", "v3"), ("v4.9", "v3"), ("v4.9+PK", "v4.9")):
            out[f"{g}: {a} − {b} (post)"] = boot_diff(per_seed(R, g, a, "post"), per_seed(R, g, b, "post"), rng)
    dk = {s: per_seed(R, "G1k", "v4.9+PK", "post")[s] - per_seed(R, "G1k", "v3", "post")[s] for s in per_seed(R, "G1k", "v3", "post")}
    d1 = {s: per_seed(R, "G1", "v4.9+PK", "post")[s] - per_seed(R, "G1", "v3", "post")[s] for s in per_seed(R, "G1", "v3", "post")}
    out["H85d: [(PK − v3)_G1k] − [(PK − v3)_G1] (post)"] = boot_diff(dk, d1, rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("G1", "G1k")}, ensure_ascii=False, indent=1))
    for g in ("G1", "G1k"):
        for v in V:
            print(g, v, {k: x for k, x in out[g][v].items() if k != "audit"})


if __name__ == "__main__":
    main()
