"""45. kör: empirikus Bayes (II. típusú MAP / MDL) az ε és κ_S paraméterekre.

L*(θ) = min_H L(H; θ) a −log2 P(D | θ) max-közelítése; a becslés θ̂ = argmin_θ L*(θ).

Olcsó, pontos újrapontozás: egy H pontszáma ε-ban és κ-ban zárt alakú. A többi tag nem függ
tőlük, így
    L(H; ε, κ) = R(H) + A(H; ε) + B(H; κ),
ahol A az abnormalitás-tag, B a béta-binomiális forráskód. R(H)-t egyszer számolom, egy
referencia-θ₀-nál. A jelölt hipotéziseket néhány valódi keresésből gyűjtöm (θ₀ és két szélső ε),
a teljes nyalábjukkal. L*(θ) így felső becslés: a minimum csak a gyűjtött jelöltek fölött van.

Két abnormalitás-tag:
  naiv (a mag pontszáma): minden (szabály, entitás) pár egy változó, a nem megfigyeltek is:
      A = k·(−log ε) + (N_all − k)·(−log(1−ε)), N_all ≈ |szabály|·|entitás|;
  marginális: a nem megfigyelt abnormalitás-változók kiösszegezve (a szorzójuk 1):
      A = k·(−log ε) + N_rel(H)·(−log(1−ε)), N_rel = az elfogadott, szabály által jósolt tények száma.
"""
from __future__ import annotations

import itertools
import math
import random

from .core import Lit, Memory, Obs
from . import procedural as P
from . import v4 as V4

EPS_FINE = tuple(round(x, 5) for x in (0.002, 0.003, 0.005, 0.0075, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05,
                                       0.07, 0.1, 0.13, 0.17, 0.22, 0.3))
KAPPA_FINE = (1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 1e4)
SEARCH_EPS = (0.01, 0.05, 0.2)
REF = {"exc_prior": 0.05, "kappa": 30.0}


# ------------------------------------------------------------------ világ
def world_case(seed, exc_rate, fact_noise, repeated=False, n_ent=20, book_error=0.1):
    """repeated=True: minden megfigyelt tényt két független terepforrás is jelent (ismételt mérés)."""
    rng = random.Random(seed)
    w = P.generate_world(rng, n_ent=n_ent, exc_rate=exc_rate)
    obs, c, t = P.stream(w, rng, book_error=book_error, fact_noise=fact_noise)
    n_flip = n_exc_vis = n_fact = 0
    extra = []
    for o in obs:
        if o.lit is not None and o.lit.pred == "has":
            e, p = o.lit.subj, o.lit.obj
            tr = w.truth(e)[p]
            n_fact += 1
            n_flip += o.lit.pos != tr
            n_exc_vis += p in w.exceptions.get(e, {})
            if repeated:
                v = tr if rng.random() >= fact_noise else (not tr)
                extra.append((o, Obs(next(c), "field2", o.time, 0.9, lit=Lit("has", e, p, v))))
    if repeated:
        out = []
        by = {id(a): b for a, b in extra}
        for o in obs:
            out.append(o)
            if id(o) in by:
                out.append(by[id(o)])
        obs = out
    truth = {e: w.truth(e) for e in w.members}
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=len(w.members) + 2, n_categories=len(w.cats),
                   n_props=len(w.props))
    stats = {"n_fact": n_fact, "eps_vis": n_exc_vis / max(1, n_fact), "noise_vis": n_flip / max(1, n_fact),
             "n_true_exc": sum(len(v) for v in w.exceptions.values())}
    return sch, obs, truth, stats


# ------------------------------------------------------------------ zárt alakú tagok
def _inst_exc(H):
    return [x for x in H.exc if not (isinstance(x[1], str) and x[1].startswith("cat:"))]


def ab_naive(mem, H, eps):
    cand = set(mem._candidate_applications())
    k_in = sum(1 for x in _inst_exc(H) if x in cand)
    k_out = sum(1 for x in _inst_exc(H) if x not in cand)
    a = k_in * -math.log2(eps) + (len(cand) - k_in) * -math.log2(1 - eps)
    if mem.ind_exc_cost:
        a += k_out * math.log2((1 - eps) / eps)
    return a


def n_rel(mem, H):
    cl = mem.closure(H, None, mem.now)
    n = 0
    for o in mem.obs:
        if o.lit is None or o.lit.pred != "has" or o.id in H.rej or o.source in H.iso:
            continue
        r = cl.ruled.get(o.lit.subj, ())
        if (o.lit.obj, True) in r or (o.lit.obj, False) in r:
            n += 1
    return n


def ab_marg(mem, H, eps):
    return len(_inst_exc(H)) * -math.log2(eps) + n_rel(mem, H) * -math.log2(1 - eps)


def beta_term(mem, H, kappa):
    old = mem.kappa
    mem.kappa = kappa
    try:
        return mem._beta_bits(H)
    finally:
        mem.kappa = old


# ------------------------------------------------------------------ illesztés
def collect(sch, obs, overrides, truth):
    """Valódi keresések a SEARCH_EPS pontokban; visszaadja a kiértékelő memóriát és a jelölteket."""
    runs, cands = [], {}
    evaluator = None
    for eps in SEARCH_EPS:
        with V4.configured({**overrides, "exc_prior": eps, "kappa": REF["kappa"]}):
            mem = Memory(sch, mode="arlc")
        for o in obs:
            mem.observe(o)
        runs.append({"eps": eps, "acc": P.evaluate(mem, truth), "key": mem.best.key()})
        for H in mem.beam:
            cands.setdefault(H.key(), H)
        if eps == REF["exc_prior"]:
            evaluator = mem
    return evaluator, list(cands.values()), runs


def profile(mem, cands):
    rows = []
    for H in cands:
        mem._scache.clear()
        mem.exc_prior, mem.kappa = REF["exc_prior"], REF["kappa"]
        total = mem.score(H)
        R = total - ab_naive(mem, H, REF["exc_prior"]) - beta_term(mem, H, REF["kappa"])
        rows.append({"H": H, "R": R, "k": len(_inst_exc(H)), "n_rel": n_rel(mem, H),
                     "n_rej_field": sum(1 for i in H.rej if mem.by_id[i].source.startswith("field")),
                     "naive": {e: ab_naive(mem, H, e) for e in EPS_FINE},
                     "marg": {e: ab_marg(mem, H, e) for e in EPS_FINE},
                     "beta": {k: beta_term(mem, H, k) for k in KAPPA_FINE}})
    out = {}
    for kind in ("naive", "marg"):
        best = None
        for e, k in itertools.product(EPS_FINE, KAPPA_FINE):
            L, r = min(((r["R"] + r[kind][e] + r["beta"][k], r) for r in rows), key=lambda z: z[0])
            if best is None or L < best[0]:
                best = (L, e, k, r)
        # ε-profil rögzített κ₀ mellett is (a κ-tól független állítás ellenőrzéséhez)
        prof_e = {e: min(r["R"] + r[kind][e] + r["beta"][REF["kappa"]] for r in rows) for e in EPS_FINE}
        e_at_k0 = min(prof_e, key=prof_e.get)
        out[kind] = {"eps": best[1], "kappa": best[2], "k": best[3]["k"], "n_rel": best[3]["n_rel"],
                     "n_rej_field": best[3]["n_rej_field"], "eps_at_kappa0": e_at_k0, "H": best[3]["H"]}
    return out


def acc_of(sch, obs, overrides, truth, eps, kappa):
    with V4.configured({**overrides, "exc_prior": eps, "kappa": kappa}):
        mem = Memory(sch, mode="arlc")
    for o in obs:
        mem.observe(o)
    return P.evaluate(mem, truth)


def run_world(seed, exc_rate, noise, repeated, overrides=None, refit_acc=True):
    overrides = dict(V4.V44_OVERRIDES if overrides is None else overrides)
    sch, obs, truth, stats = world_case(seed, exc_rate, noise, repeated)
    mem, cands, runs = collect(sch, obs, overrides, truth)
    prof = profile(mem, cands)
    row = {"seed": seed, "exc_rate": exc_rate, "noise": noise, "repeated": repeated, **stats,
           "n_cands": len(cands), "n_all": len(mem._candidate_applications()),
           "runs": runs}
    for kind in ("naive", "marg"):
        p = prof[kind]
        row[kind] = {k: v for k, v in p.items() if k != "H"}
    if refit_acc:
        m = prof["marg"]
        row["acc_frozen"] = next(r["acc"] for r in runs if r["eps"] == REF["exc_prior"])
        row["acc_eb_marg"] = acc_of(sch, obs, overrides, truth, m["eps"], m["kappa"])
    return row


def run(seeds=range(2000, 2004), exc_rates=(0.005, 0.03, 0.1), noises=(0.02, 0.1), repeated=(False, True)):
    out = []
    for args in itertools.product(seeds, exc_rates, noises, repeated):
        out.append(run_world(*args))
        print({k: v for k, v in out[-1].items() if k != "runs"}, flush=True)
    return out


# ------------------------------------------------------------------ folytatható párhuzamos futtatás
def _job(args):
    import json, os
    path, a = args
    row = run_world(*a)
    tmp = path + ".tmp"
    json.dump(row, open(tmp, "w"), default=str, indent=1)
    os.replace(tmp, path)
    return a


def main():
    import argparse, json, os
    from multiprocessing import Pool
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=3)
    a = ap.parse_args()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-45")
    parts = os.path.join(out, "parts")
    os.makedirs(parts, exist_ok=True)
    jobs = []
    for args in itertools.product(range(2000, 2000 + a.seeds), (0.005, 0.03, 0.1), (0.02, 0.1), (False, True)):
        p = os.path.join(parts, "_".join(str(x) for x in args) + ".json")
        if not os.path.exists(p):
            jobs.append((p, args))
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_job, jobs):
            print("kész", r, flush=True)
    rows = [json.load(open(os.path.join(parts, f))) for f in sorted(os.listdir(parts)) if f.endswith(".json")]
    json.dump(rows, open(os.path.join(out, "results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
