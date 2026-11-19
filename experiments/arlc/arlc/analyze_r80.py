"""80. kör elemzése (előregisztrált): python -m arlc.analyze_r80"""
import json
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-80", "test")


def main():
    rows = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(80)
    out = {"n": len(rows)}
    V = ("v3", "v4.8-π", "v4.8-π+T")
    for gen in ("G1A", "G2"):
        R = [r for r in rows if r["gen"] + r["pop"] == gen]
        tab = {}
        for v in V:
            rv = [r for r in R if r["variant"] == v]
            tab[v] = {m: round(st.mean(r[m] for r in rv), 4) for m in ("pre", "post", "target")}
            tab[v]["n"] = len(rv)
            for src in ("book", "census", "fieldB", "field", "liar"):
                tab[v][f"rej_pre_{src}"] = round(st.mean(r["rej_pre"].get(src, 0) for r in rv), 2)
        out[gen] = tab

        def per_seed(v, m, kinds=None):
            d = defaultdict(list)
            for r in R:
                if r["variant"] == v and (kinds is None or r["kind"] in kinds):
                    d[r["seed"]].append(r[m])
            return {s: st.mean(x) for s, x in d.items()}
        for m in ("pre", "post"):
            out[gen][f"+T − v4.8-π ({m})"] = boot_diff(per_seed("v4.8-π+T", m), per_seed("v4.8-π", m), rng)
            out[gen][f"+T − v3 ({m})"] = boot_diff(per_seed("v4.8-π+T", m), per_seed("v3", m), rng)
        out[gen]["hazug target: +T − v4.8-π"] = boot_diff(per_seed("v4.8-π+T", "target", {"hazug forrás"}),
                                                          per_seed("v4.8-π", "target", {"hazug forrás"}), rng)
        if gen == "G2":
            rt = [r for r in R if r["variant"] == "v4.8-π+T"]
            out[gen]["valódi tankönyvhiba (átlag/eset)"] = round(st.mean(r["book_errors"] for r in rt), 2)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
