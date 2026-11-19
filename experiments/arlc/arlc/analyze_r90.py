"""90. kör elemzése (előregisztrált): python -m arlc.analyze_r90"""
import json
import math
import os
import random
import statistics as st
from collections import Counter, defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-90", "test")
ETAS = ("η=0.0", "η=0.5", "η=1.0")
SRC = {("G1k", "hazug forrás"), ("G2", "hazug forrás"), ("G2", "torzított forrás"), ("G3", "hazug forrás"),
       ("G3", "elavult forrás")}
TOL = 0.5


def choose(cands):
    """A legkisebb prequential veszteségű η; TOL biten belüli holtversenynél a legnagyobb η."""
    best = min(r["preq_loss"] for r in cands)
    ok = [r for r in cands if r["preq_loss"] <= best + TOL]
    return max(ok, key=lambda r: float(r["variant"][2:]))


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    by = defaultdict(dict)
    for r in R:
        by[(r["gen"], r["kind"], r["seed"])][r["variant"]] = r
    rows = []
    chosen = Counter()
    for key, d in by.items():
        if all(e in d for e in ETAS) and "v3" in d:
            sb = dict(choose([d[e] for e in ETAS]))
            chosen[(key[0], sb["variant"])] += 1
            sb["variant"] = "SB"
            rows += [d["v3"], *[d[e] for e in ETAS], sb]
    rng = random.Random(90)
    V = ("v3",) + ETAS + ("SB",)

    def ps(v, m, gens=None, sets=None):
        dd = defaultdict(list)
        for r in rows:
            if r["variant"] == v and (gens is None or r["gen"] in gens) and (sets is None or (r["gen"], r["kind"]) in sets) \
                    and not math.isnan(r[m]):
                dd[(r["gen"], r["seed"])].append(r[m])
        return {k: st.mean(x) for k, x in dd.items()}
    out = {"n_eset": len(rows) // 5, "η-választás": {f"{g} {v}": n for (g, v), n in sorted(chosen.items())}, "táblázat": {}}
    for g in ("G1k", "G2", "G3"):
        for v in V:
            rv = [r for r in rows if r["gen"] == g and r["variant"] == v]
            out["táblázat"][f"{g} | {v}"] = {m: round(st.mean(x for x in (r[m] for r in rv) if not math.isnan(x)), 4)
                                             for m in ("pre", "post", "target")}
    for g in ("G1k", "G2", "G3"):
        a = ps("SB", "post", {g})
        b3, b1 = ps("v3", "post", {g}), ps("η=1.0", "post", {g})
        best = {k: max(b3[k], b1[k]) for k in a}
        out[f"H90a {g}: SB − max(v3, η=1) (post)"] = boot_diff(a, best, rng)
    out["H90b forrás-célkérdések: SB − v3"] = boot_diff(ps("SB", "target", sets=SRC), ps("v3", "target", sets=SRC), rng)
    out["H90c G3 pre: SB − η=1"] = boot_diff(ps("SB", "pre", {"G3"}), ps("η=1.0", "pre", {"G3"}), rng)
    out["H90d G1k∪G2 post: SB − η=1"] = boot_diff(ps("SB", "post", {"G1k", "G2"}), ps("η=1.0", "post", {"G1k", "G2"}), rng)
    for g in ("G1k", "G2", "G3"):
        out[f"{g} post: SB − v3"] = boot_diff(ps("SB", "post", {g}), ps("v3", "post", {g}), rng)
        out[f"{g} post: η=0 − v3"] = boot_diff(ps("η=0.0", "post", {g}), ps("v3", "post", {g}), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
