"""81. kör elemzése (előregisztrált): python -m arlc.analyze_r81"""
import json
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-81", "test")
V = ("v3", "v4.9", "v4.9+PK")


def per_seed(R, v, m, kinds=None):
    d = defaultdict(list)
    for r in R:
        if r["variant"] == v and (kinds is None or r["kind"] in kinds):
            d[r["seed"]].append(r[m])
    return {s: st.mean(x) for s, x in d.items()}


def main():
    rows = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(81)
    out = {"n": len(rows)}
    for gen in ("G1A", "G2"):
        R = [r for r in rows if r["gen"] + r["pop"] == gen]
        tab = {}
        for v in V:
            rv = [r for r in R if r["variant"] == v]
            tab[v] = {m: round(st.mean(r[m] for r in rv), 4) for m in ("pre", "post", "target")}
            tab[v]["n"] = len(rv)
            tab[v]["sec"] = round(st.mean(r["sec"] for r in rv), 1)
            for src in ("book", "census", "fieldA", "fieldB", "field"):
                tab[v][f"rej_pre_{src}"] = round(st.mean(r["rej_pre"].get(src, 0) for r in rv), 2)
            for k in sorted({r["kind"] for r in R}):
                rk = [r for r in rv if r["kind"] == k]
                tab[v][f"post[{k}]"] = round(st.mean(r["post"] for r in rk), 4)
                tab[v][f"target[{k}]"] = round(st.mean(r["target"] for r in rk), 4)
        out[gen] = tab
        for m in ("pre", "post"):
            for a, b in (("v4.9+PK", "v4.9"), ("v4.9+PK", "v3"), ("v4.9", "v3")):
                out[gen][f"{a} − {b} ({m})"] = boot_diff(per_seed(R, a, m), per_seed(R, b, m), rng)
        if gen == "G2":
            out[gen]["valódi tankönyvhiba (átlag/eset)"] = round(st.mean(r["book_errors"] for r in R if r["variant"] == "v3"), 2)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
