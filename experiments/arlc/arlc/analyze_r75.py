"""A 75. és 77. kör előregisztrált elemzése."""
import json
import math
import os
import random
import statistics as st
import sys

from .analyze_r44 import boot_diff

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    if not os.path.isdir(path):
        return []
    return [json.load(open(os.path.join(path, f))) for f in sorted(os.listdir(path)) if f.endswith(".json")]


def ps(rows, key, kinds=None):
    out = {}
    for r in rows:
        if kinds and r["kind"] not in kinds:
            continue
        v = r.get(key)
        if v is None or (isinstance(v, float) and math.isnan(v)):
            continue
        out.setdefault((r.get("pop", "-"), r["seed"]), []).append(v)
    return {k: st.mean(v) for k, v in out.items()}


def mean(rows, key, kinds=None):
    v = [x for x in ps(rows, key, kinds).values()]
    return round(st.mean(v), 4) if v else None


def r75():
    base = os.path.join(HERE, "..", "results", "kor-75")
    A, C = load(os.path.join(base, "A")), load(os.path.join(base, "C"))
    rng = random.Random(75)
    M = ("v3", "v4.4e", "v4.8-π", "v4.8-π+jel")
    res = {"n": {"A": len(A), "C": len(C)}}
    for pop, R in (("A", A), ("C", C), ("A∪C", A + C)):
        res[pop] = {m: {k: mean(R, f"{k}_{m}") for k in ("post", "target", "brier")} for m in M}
        res[pop]["v4.8-π+jel nyaláb-Brier"] = mean(R, "brier_avg_v4.8-π+jel")
    AC = A + C
    res["H75a v4.8-π+jel − v3 (A∪C)"] = boot_diff(ps(AC, "post_v4.8-π+jel"), ps(AC, "post_v3"), rng)
    res["H75b v4.8-π+jel − v4.4e (A∪C)"] = boot_diff(ps(AC, "post_v4.8-π+jel"), ps(AC, "post_v4.4e"), rng)
    res["H75c v4.8-π+jel − v4.4e (A)"] = boot_diff(ps(A, "post_v4.8-π+jel"), ps(A, "post_v4.4e"), rng)
    res["H75d Brier v3 − nyaláb-átlag (A∪C)"] = boot_diff(ps(AC, "brier_v3"), ps(AC, "brier_avg_v4.8-π+jel"), rng)
    json.dump(res, open(os.path.join(base, "analysis.json"), "w"), ensure_ascii=False, indent=1)
    return res


def r77():
    base = os.path.join(HERE, "..", "results", "kor-77")
    R = load(base)
    rng = random.Random(77)
    M = ("wms", "v3", "v4.4e", "v4.8-π")
    res = {"n": len(R), "összes": {m: {k: mean(R, f"{k}_{m}") for k in ("pre", "post", "target", "brier")} for m in M}}
    for k in sorted({r["kind"] for r in R}):
        res[k] = {m: {x: mean(R, f"{x}_{m}", (k,)) for x in ("post", "target")} for m in M}
    res["H77a v4.8-π − v3 (post)"] = boot_diff(ps(R, "post_v4.8-π"), ps(R, "post_v3"), rng)
    res["H77b v4.4e − wms (post)"] = boot_diff(ps(R, "post_v4.4e"), ps(R, "post_wms"), rng)
    res["H77c hazug target v4.8-π − v3"] = boot_diff(ps(R, "target_v4.8-π", ("hazug forrás",)), ps(R, "target_v3", ("hazug forrás",)), rng)
    res["H77d prioritás-szakértő target"] = {m: mean(R, f"target_{m}", ("prioritás-szakértő",)) for m in M}
    json.dump(res, open(os.path.join(base, "analysis.json"), "w"), ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    res = r75() if sys.argv[1] == "75" else r77()
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
