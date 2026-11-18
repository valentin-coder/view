"""A 44. kör előregisztrált elemzése: világ (seed) szerinti klaszteres bootstrap 95% CI.

Fő végpont: a post-acc átlaga mind a 150 esetre. Egy bootstrap-minta a 30 seedből húz
visszatevéssel; egy seed mind az öt meglepetéstípusát viszi magával (klaszter).
"""
from __future__ import annotations

import json
import math
import os
import random
import statistics as st
import sys

from .run_r44 import KINDS, PARTS

B = 10000


def load(parts=PARTS, extra=None):
    rows = []
    for f in sorted(os.listdir(parts)):
        if f.endswith(".json"):
            rows += json.load(open(os.path.join(parts, f)))
    if extra and os.path.isdir(extra):
        for f in sorted(os.listdir(extra)):
            if f.endswith(".json"):
                rows += json.load(open(os.path.join(extra, f)))
    return rows


def table(rows):
    """(method, seed, kind) -> sor"""
    return {(r["method"], r["seed"], r["kind"]): r for r in rows}


def _nanmean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return st.mean(xs) if xs else float("nan")


def per_seed(T, method, metric, seeds, kinds=KINDS):
    """seed -> az adott seed típusainak átlaga (klaszterérték); csak teljes cellák."""
    out = {}
    for s in seeds:
        vals = [T[(method, s, k)][metric] for k in kinds if (method, s, k) in T]
        if len(vals) == len(kinds):
            out[s] = _nanmean(vals)
    return out


def boot_diff(a: dict, b: dict, rng):
    seeds = sorted(set(a) & set(b))
    d = [a[s] - b[s] for s in seeds if not (math.isnan(a[s]) or math.isnan(b[s]))]
    if not d:
        return None
    m = st.mean(d)
    bs = []
    for _ in range(B):
        smp = [d[rng.randrange(len(d))] for _ in d]
        bs.append(st.mean(smp))
    bs.sort()
    return {"n_seeds": len(d), "mean_diff": m, "ci95": [bs[int(0.025 * B)], bs[int(0.975 * B) - 1]]}


def analyze(rows):
    rng = random.Random(44)
    T = table(rows)
    methods = sorted({r["method"] for r in rows})
    seeds = sorted({r["seed"] for r in rows})
    res = {"n_rows": len(rows), "methods": methods, "seeds": [seeds[0], seeds[-1], len(seeds)]}
    res["means"] = {}
    for m in methods:
        res["means"][m] = {}
        for metric in ("pre_acc", "post_acc", "target_acc", "surprise_seconds", "seconds"):
            ps = per_seed(T, m, metric, seeds)
            res["means"][m][metric] = _nanmean(ps.values()) if ps else None
        res["means"][m]["n_complete_seeds"] = len(per_seed(T, m, "post_acc", seeds))
    res["by_kind"] = {}
    for k in KINDS:
        res["by_kind"][k] = {m: {met: _nanmean([T[(m, s, k)][met] for s in seeds if (m, s, k) in T])
                                 for met in ("pre_acc", "post_acc", "target_acc", "surprise_seconds")}
                             for m in methods}
    post = {m: per_seed(T, m, "post_acc", seeds) for m in methods}
    res["H44a v4 - wms (post)"] = boot_diff(post["v4"], post["wms"], rng)
    res["H44b v4 - arlc (post)"] = boot_diff(post["v4"], post["arlc"], rng)
    for k in ("hazug forrás", "más régió"):
        a = per_seed(T, "v4", "target_acc", seeds, kinds=(k,))
        b = per_seed(T, "wms", "target_acc", seeds, kinds=(k,))
        res[f"H44c v4 - wms (target, {k})"] = boot_diff(a, b, rng)
    # kiegészítő (nem előregisztrált) összevetések
    extra = {}
    for m in methods:
        if m in ("v4",):
            continue
        extra[f"v4 - {m} (post)"] = boot_diff(post["v4"], post[m], rng)
    for vx in ("v4.3", "v4.4"):
        if vx in methods:
            for other in ("v4", "wms", "arlc"):
                extra[f"{vx} - {other} (post)"] = boot_diff(post[vx], post[other], rng)
    pre = {m: per_seed(T, m, "pre_acc", seeds) for m in methods}
    extra["v4 - wms (pre)"] = boot_diff(pre["v4"], pre["wms"], rng)
    extra["v4 - arlc (pre)"] = boot_diff(pre["v4"], pre["arlc"], rng)
    res["kiegészítő"] = extra
    return res


if __name__ == "__main__":
    rows = load()
    for vx in ("v4.3", "v4.4"):
        rows += load(PARTS + "_" + vx) if os.path.isdir(PARTS + "_" + vx) else []
    res = analyze(rows)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(PARTS), "analysis.json")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "by_kind"}, ensure_ascii=False, indent=1))
