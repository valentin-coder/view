"""50. kör: az előregisztrált ismétlés elemzése (H50a–c), a 44. kör módszerével."""
from __future__ import annotations

import json
import math
import os
import random
import statistics as st

from . import analyze_r44 as A
from .run_r50 import OUT, SEEDS

V = "v4.4-egyszintű"


def main():
    rows = A.load(OUT)
    T = A.table(rows)
    seeds = sorted({r["seed"] for r in rows})
    rng = random.Random(50)
    res = {"n_rows": len(rows), "seeds": [seeds[0], seeds[-1], len(seeds)], "means": {}}
    methods = sorted({r["method"] for r in rows})
    for m in methods:
        res["means"][m] = {k: A._nanmean(A.per_seed(T, m, k, seeds).values())
                           for k in ("pre_acc", "post_acc", "target_acc", "surprise_seconds")}
    post = {m: A.per_seed(T, m, "post_acc", seeds) for m in methods}
    res["H50a v4.4e - arlc (post)"] = A.boot_diff(post[V], post["arlc"], rng)
    res["H50b v4.4e - wms (post)"] = A.boot_diff(post[V], post["wms"], rng)
    bm = A.per_seed(T, V, "brier_map", seeds)
    ba = A.per_seed(T, V, "brier_avg", seeds)
    res["H50c Brier MAP - átlag (v4.4e)"] = A.boot_diff(bm, ba, rng)
    res["by_kind"] = {k: {m: {met: A._nanmean([T[(m, s, k)][met] for s in seeds if (m, s, k) in T])
                              for met in ("post_acc", "target_acc")} for m in methods} for k in A.KINDS}
    json.dump(res, open(os.path.join(os.path.dirname(OUT), "replication_analysis.json"), "w"),
              ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "by_kind"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
