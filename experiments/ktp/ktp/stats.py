"""Mérőszámok és statisztika: RR, CR, F, entitás szerint klaszterezett bootstrap."""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np

RR_KINDS = ("D", "I")
CR_KINDS = ("S1", "S2")


def hmean(a: float, b: float) -> float:
    return 0.0 if a + b == 0 else 2 * a * b / (a + b)


def per_edit(rows: Iterable[dict], method: str, kinds_rr=RR_KINDS, kinds_cr=CR_KINDS) -> dict[str, dict]:
    """rows: {'edit','entity','kind','before','after', method: m}. Szerkesztésenkénti RR, CR, CR_T."""
    acc: dict[str, dict] = defaultdict(lambda: {"rr": [], "cr": [], "crt": [], "entity": None})
    for r in rows:
        if method not in r:
            continue
        e = acc[r["edit"]]
        e["entity"] = r["entity"]
        pred = r[method] > 0
        if r["kind"] in kinds_rr:
            e["rr"].append(float(pred == r["after"]))
        elif r["kind"] in kinds_cr:
            e["cr"].append(float(pred != r["before"]))
        elif r["kind"] == "T":
            e["crt"].append(float(pred != r["before"]))
    out = {}
    for k, e in acc.items():
        out[k] = {
            "entity": e["entity"],
            "rr": float(np.mean(e["rr"])) if e["rr"] else np.nan,
            "cr": float(np.mean(e["cr"])) if e["cr"] else np.nan,
            "crt": float(np.mean(e["crt"])) if e["crt"] else np.nan,
        }
    return out


def aggregate(pe: dict[str, dict], keys: Iterable[str] | None = None) -> dict:
    keys = list(pe) if keys is None else list(keys)
    rr_vals = [pe[k]["rr"] for k in keys if not np.isnan(pe[k]["rr"])]
    cr_vals = [pe[k]["cr"] for k in keys if not np.isnan(pe[k]["cr"])]
    rr = float(np.mean(rr_vals)) if rr_vals else np.nan
    cr = float(np.mean(cr_vals)) if cr_vals else np.nan
    crt_vals = [pe[k]["crt"] for k in keys if not np.isnan(pe[k]["crt"])]
    crt = float(np.mean(crt_vals)) if crt_vals else np.nan
    f = hmean(rr, 1 - cr) if not (np.isnan(rr) or np.isnan(cr)) else np.nan
    return {"rr": float(rr), "cr": float(cr), "crt": crt, "f": f,
            "n_edits": len(keys)}


def cluster_bootstrap_diff(pes: dict[str, dict[str, dict]], target: str, rivals: list[str],
                           n_boot: int = 2000, seed: int = 0) -> dict:
    """F(target) - max_r F(rival), entitásonként újramintavételezve (konzervatív: a max a
    mintán belül számolódik)."""
    rng = np.random.default_rng(seed)
    keys = [k for k in pes[target] if all(k in pes[r] for r in rivals)]
    by_ent: dict[str, list[str]] = defaultdict(list)
    for k in keys:
        by_ent[pes[target][k]["entity"]].append(k)
    ents = sorted(by_ent)

    def stat(sample_keys):
        ft = aggregate(pes[target], sample_keys)["f"]
        fr = max(aggregate(pes[r], sample_keys)["f"] for r in rivals)
        return ft - fr

    point = stat(keys)
    boots = []
    for _ in range(n_boot):
        pick = rng.choice(len(ents), size=len(ents), replace=True)
        sample = [k for i in pick for k in by_ent[ents[i]]]
        boots.append(stat(sample))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"diff": float(point), "ci95": [float(lo), float(hi)], "n_edits": len(keys),
            "n_entities": len(ents)}


def wilcoxon_edits(pe_a: dict[str, dict], pe_b: dict[str, dict]) -> dict:
    from scipy.stats import wilcoxon
    keys = [k for k in pe_a if k in pe_b]
    fa = np.array([hmean(pe_a[k]["rr"], 1 - pe_a[k]["cr"]) for k in keys])
    fb = np.array([hmean(pe_b[k]["rr"], 1 - pe_b[k]["cr"]) for k in keys])
    ok = ~(np.isnan(fa) | np.isnan(fb))
    d = fa[ok] - fb[ok]
    if len(d) < 5 or np.allclose(d, 0):
        return {"n": int(len(d)), "median_diff": float(np.median(d)) if len(d) else np.nan, "p": np.nan}
    res = wilcoxon(d)
    return {"n": int(len(d)), "median_diff": float(np.median(d)), "p": float(res.pvalue)}
