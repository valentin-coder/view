"""A 63. kör előregisztrált elemzése (H63a–c)."""
import json
import math
import os
import random
import statistics as st

from .analyze_r44 import boot_diff

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    rows = []
    for pop in ("A", "C"):
        d = os.path.join(HERE, "..", "results", "kor-63", pop)
        if os.path.isdir(d):
            rows += [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".json")]
    return rows


def per_seed(rows, key, kinds=None):
    out = {}
    for r in rows:
        if kinds and r["kind"] not in kinds:
            continue
        v = r[key]
        if isinstance(v, float) and math.isnan(v):
            continue
        out.setdefault((r["pop"], r["seed"]), []).append(v)
    return {k: st.mean(v) for k, v in out.items()}


def main():
    rows = load()
    rng = random.Random(63)
    tie = ("más régió", "hazug forrás")
    res = {"n": len(rows)}
    res["H63a target Brier MAP − átlag (más régió, hazug forrás)"] = boot_diff(
        per_seed(rows, "brier_map_target", tie), per_seed(rows, "brier_avg_target", tie), rng)
    res["H63b post Brier MAP − átlag"] = boot_diff(per_seed(rows, "brier_map"), per_seed(rows, "brier_avg"), rng)
    reg = [r for r in rows if r["kind"] == "más régió" and not math.isnan(r["target_frac_uncertain"])]
    res["H63c más régió: bizonytalan célkérdések aránya"] = st.mean(r["target_frac_uncertain"] for r in reg) if reg else None
    by = {}
    for k in sorted({r["kind"] for r in rows}):
        sub = [r for r in rows if r["kind"] == k]
        f = lambda key: round(st.mean(x for x in (r[key] for r in sub) if not (isinstance(x, float) and math.isnan(x))), 4)
        by[k] = {"target MAP pont.": f("target_map"), "target átlag pont.": f("avg_target_acc"),
                 "target Brier MAP": f("brier_map_target"), "target Brier átlag": f("brier_avg_target"),
                 "bizonytalan arány": f("target_frac_uncertain"), "nyaláb-szórás (bit)": f("beam_spread_bits")}
    res["típusonként"] = by
    json.dump(res, open(os.path.join(HERE, "..", "results", "kor-63", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
