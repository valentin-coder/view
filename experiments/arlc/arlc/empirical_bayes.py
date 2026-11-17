"""45. kör: empirikus Bayes (II. típusú MAP / MDL) az ε és κ_S paraméterekre.

Egy világ megfigyeléseire minden (ε, κ_S) rácspontban lefut a v4, és a legjobb hipotézis kódhossza
L*(θ) = min_H L(H; θ) a −log2 P(D | θ) max-közelítése. A becslés θ̂ = argmin L*(θ). Ismert igazi
kivételarányú és zajú procedurális világokon ellenőrizhető, hogy θ̂ követi-e az igazit, és hogy a
θ̂-val mért pontosság jobb-e a befagyasztott v4-énél.
"""
from __future__ import annotations

import itertools
import random

from .core import Memory
from . import procedural as P
from . import v4 as V4

EPS_GRID = (0.01, 0.03, 0.05, 0.1, 0.2)
KAPPA_GRID = (10.0, 30.0, 100.0)


def world_case(seed, exc_rate, fact_noise, book_error=0.1):
    rng = random.Random(seed)
    w = P.generate_world(rng, exc_rate=exc_rate)
    obs, c, t = P.stream(w, rng, book_error=book_error, fact_noise=fact_noise)
    truth = {e: w.truth(e) for e in w.members}
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=len(w.members) + 2, n_categories=len(w.cats),
                   n_props=len(w.props))
    n_true_exc = sum(len(v) for v in w.exceptions.values())
    return sch, obs, truth, n_true_exc


def fit(sch, obs, truth):
    rows = []
    for eps, kap in itertools.product(EPS_GRID, KAPPA_GRID):
        with V4.configured({"exc_prior": eps, "kappa": kap}):
            mem = Memory(sch, mode="arlc")
        for o in obs:
            mem.observe(o)
        rows.append({"eps": eps, "kappa": kap, "L_star": mem.score(mem.best),
                     "acc": P.evaluate(mem, truth), "n_exc": len(mem.best.exc)})
    best = min(rows, key=lambda r: r["L_star"])
    frozen = next(r for r in rows if r["eps"] == 0.05 and r["kappa"] == 30.0)
    oracle = max(rows, key=lambda r: r["acc"])
    return {"grid": rows, "fitted": best, "frozen": frozen, "oracle_best_acc": oracle}


def run(seeds=range(2000, 2010), exc_rates=(0.005, 0.03, 0.1), noises=(0.02, 0.1)):
    out = []
    for seed, er, nz in itertools.product(seeds, exc_rates, noises):
        sch, obs, truth, n_true = world_case(seed, er, nz)
        r = fit(sch, obs, truth)
        out.append({"seed": seed, "exc_rate": er, "fact_noise": nz, "n_true_exceptions": n_true,
                    "fitted_eps": r["fitted"]["eps"], "fitted_kappa": r["fitted"]["kappa"],
                    "acc_fitted": r["fitted"]["acc"], "acc_frozen": r["frozen"]["acc"],
                    "acc_oracle": r["oracle_best_acc"]["acc"], "grid": r["grid"]})
        print({k: v for k, v in out[-1].items() if k != "grid"}, flush=True)
    return out
