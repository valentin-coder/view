"""86. kör elemzése (előregisztrált): python -m arlc.analyze_r86"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-86", "test")
V = ("T nélkül", "T (metaadat)", "N (új forrás)", "U (egyforma)")
LIARLIKE = {("G1kA", "hazug forrás"), ("G2", "hazug forrás"), ("G2", "torzított forrás")}


def per_seed(R, v, m, sets):
    d = defaultdict(list)
    for r in R:
        key = (r["gen"] + r["pop"], r["kind"])
        if r["variant"] == v and key in sets and not math.isnan(r[m]):
            d[(key, r["seed"])].append(r[m])
    # seedenként (a halmazokon átlagolva)
    by = defaultdict(list)
    for (key, s), x in d.items():
        by[s].append(st.mean(x))
    return {s: st.mean(x) for s, x in by.items()}


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(86)
    out = {"n": len(R), "táblázat": {}}
    for key in sorted({(r["gen"] + r["pop"], r["kind"]) for r in R}):
        for v in V:
            rv = [r for r in R if (r["gen"] + r["pop"], r["kind"]) == key and r["variant"] == v]
            if rv:
                out["táblázat"][f"{key[0]} {key[1]} | {v}"] = {
                    "n": len(rv), "pre": round(st.mean(r["pre"] for r in rv), 4), "post": round(st.mean(r["post"] for r in rv), 4),
                    "target": round(st.mean(r["target"] for r in rv if not math.isnan(r["target"])), 4),
                    "új forrás félretéve": round(sum(r["new_rejected"] for r in rv) / max(1, sum(r["new_n"] for r in rv)), 3),
                    "sec": round(st.mean(r["sec"] for r in rv), 1)}
    gen_sets = {("G1kA", "hazug forrás"), ("G1kA", "átkategorizálás"), ("G2", "hazug forrás"), ("G2", "torzított forrás")}
    C = {("G1kC", "hazug forrás")}
    out["H86a hazug-szerű target: N − (T nélkül)"] = boot_diff(per_seed(R, "N (új forrás)", "target", LIARLIKE), per_seed(R, "T nélkül", "target", LIARLIKE), rng)
    out["H86b hazug-szerű target: T − N"] = boot_diff(per_seed(R, "T (metaadat)", "target", LIARLIKE), per_seed(R, "N (új forrás)", "target", LIARLIKE), rng)
    out["H86c G1k-C post: N − (T nélkül)"] = boot_diff(per_seed(R, "N (új forrás)", "post", C), per_seed(R, "T nélkül", "post", C), rng)
    out["H86d pre (G1k-A ∪ G2): N − (T nélkül)"] = boot_diff(per_seed(R, "N (új forrás)", "pre", gen_sets), per_seed(R, "T nélkül", "pre", gen_sets), rng)
    out["H86e hazug-szerű target: N − U"] = boot_diff(per_seed(R, "N (új forrás)", "target", LIARLIKE), per_seed(R, "U (egyforma)", "target", LIARLIKE), rng)
    out["G1k-C post: T − N"] = boot_diff(per_seed(R, "T (metaadat)", "post", C), per_seed(R, "N (új forrás)", "post", C), rng)
    out["post (G1k-A ∪ G2): N − T"] = boot_diff(per_seed(R, "N (új forrás)", "post", gen_sets), per_seed(R, "T (metaadat)", "post", gen_sets), rng)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
