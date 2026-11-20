"""106. kör elemzése (előregisztrált): python -m arlc.analyze_r106"""
import json
import math
import os
import random
import statistics as st
from collections import defaultdict

from .analyze_r44 import boot_diff
from .run_r106 import TAUS

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-106", "test")


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    rng = random.Random(106)
    out = {"n": len(R)}
    for v in ("FROZEN_91", "F91_Q"):
        rv = [r for r in R if r["variant"] == v]
        tab = {}
        for part in ("post", "target"):
            for tau in TAUS:
                t = str(tau)
                n = sum(r[part][t]["n"] for r in rv)
                a = sum(r[part][t]["answered"] for r in rv)
                c = sum(r[part][t]["correct"] for r in rv)
                tab[f"{part} τ={tau}"] = {"lefedettség": round(a / n, 4), "szelektív pontosság": round(c / max(1, a), 4),
                                          "pontosság": round(c / n, 4),
                                          "Brier": round(st.mean(r[part][t]["brier"] for r in rv if r[part][t]["n"]), 4)}
        tab["nyaláb-átlag Brier (post)"] = round(st.mean(r["brier_avg"] for r in rv), 4)
        tab["nyaláb-átlag Brier (target)"] = round(st.mean(r["brier_avg_target"] for r in rv if not math.isnan(r["brier_avg_target"])), 4)

        def ps(f):
            d = defaultdict(list)
            for r in rv:
                x = f(r)
                if x is not None and not math.isnan(x):
                    d[(r["gen"], r["seed"])].append(x)
            return {k: st.mean(x) for k, x in d.items()}
        sel = lambda part, t: (lambda r: r[part][t]["correct"] / r[part][t]["answered"] if r[part][t]["answered"] else None)
        acc0 = lambda r: r["post"]["0.0"]["correct"] / r["post"]["0.0"]["answered"] if r["post"]["0.0"]["answered"] else None
        tab["H106a szelektív(τ=2) − szelektív(τ=0)"] = boot_diff(ps(sel("post", "2.0")), ps(acc0), rng)
        tab["H106c Brier(τ=2) − Brier(τ=0)"] = boot_diff(ps(lambda r: r["post"]["2.0"]["brier"]), ps(lambda r: r["post"]["0.0"]["brier"]), rng)
        tab["H106d Brier(τ=2) − nyaláb-átlag"] = boot_diff(ps(lambda r: r["post"]["2.0"]["brier"]), ps(lambda r: r["brier_avg"]), rng)
        out[v] = tab
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
