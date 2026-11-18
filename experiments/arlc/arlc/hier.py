"""52. kör: a „szemét elmélet” arányának (1 − π) becslése sok világ együtteséből, kemény EM-mel.

A deklarált q itt feltételes: „ha az elmélet ép, egy állítása q valószínűséggel helyes”. A keverék
ezért nem kalibrált (q1 = q); a populáció B-ben (30% szemét tankönyv) a kalibráció nem is volna
teljesíthető (π < (q − q0)/(1 − q0)).
"""
from __future__ import annotations

import json
import random
import sys

from . import procedural as P
from . import v4 as V4
from .core import Lit, Memory, Obs, Rule


def world(seed, n_ent, garbage):
    rng = random.Random(seed)
    w = P.generate_world(rng, n_ent=n_ent)
    obs, c, t = P.stream(w, rng)
    if garbage:
        # egészében téves tankönyv: minden tulajdonság-szabály előjele véletlen (az állítások fele téves)
        grng = random.Random(seed + 7919)
        new = []
        for o in obs:
            if o.rule is not None and o.rule.pred == "has":
                r = o.rule
                o = Obs(o.id, o.source, o.time, o.q, rule=Rule(r.body, r.pred, r.obj, grng.random() < 0.5))
            new.append(o)
        obs = new
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=n_ent + 2, n_categories=len(w.cats), n_props=len(w.props))
    return sch, obs, {e: w.truth(e) for e in w.members}


def run_world(sch, obs, truth, pi, ctx_bits):
    mix = (pi, 30.0, 0.5, 2.0)                       # nem kalibrált: q1 = q
    with V4.configured({**V4.V44_OVERRIDES, "theory_mix": mix}):
        m = Memory(sch, mode="arlc")
    m.ctx_cost.update({"book": ctx_bits})
    for o in obs:
        m.observe(o)
    H = m.best
    book = [o.id for o in m.obs if o.source == "book"]
    frac = sum(1 for i in book if i in H.rej) / max(1, len(book))
    judged_garbage = frac >= 0.9 or "book" in H.iso
    return {"acc": P.evaluate(m, truth), "book_rejected_frac": frac, "book_iso": "book" in H.iso,
            "judged_garbage": judged_garbage}


def ctx_bits_for(pi):
    """Közös hiperprior (49. kör): a kontextus-izolálás prioresélye a szemét-arány fele."""
    import math
    return -math.log2(max(1e-6, (1 - pi) / 2))


def _train_job(args):
    population, s, pi = args
    garbage = population == "B" and random.Random(s).random() < 0.3
    sch, obs, truth = world(s, 30, garbage)
    return {"seed": s, "true_garbage": garbage, **run_world(sch, obs, truth, pi, ctx_bits_for(pi))}


def em(population, train_seeds, pi0, iters=3, log=print, workers=int(__import__("os").environ.get("W", "2"))):
    from multiprocessing import Pool
    pi = pi0
    hist = []
    for it in range(iters):
        with Pool(workers) as pool:
            judged = pool.map(_train_job, [(population, s, pi) for s in train_seeds])
        for j in judged:
            log({"pop": population, "iter": it, "pi": pi, **j})
        n_g = sum(j["judged_garbage"] for j in judged)
        new_pi = (len(judged) - n_g + 1) / (len(judged) + 2)
        hist.append({"iter": it, "pi": pi, "n_judged_garbage": n_g, "n": len(judged), "new_pi": new_pi})
        if abs(new_pi - pi) < 1e-9:
            break
        pi = new_pi
    return pi, hist


def test(population, test_seeds, pi, log=print):
    out = []
    for s in test_seeds:
        garbage = population == "B" and random.Random(s).random() < 0.3
        sch, obs, truth = world(s, 12, garbage)
        r = run_world(sch, obs, truth, pi, ctx_bits_for(pi))
        out.append({"seed": s, "true_garbage": garbage, **r})
        log({"pop": population, "test_pi": pi, **out[-1]})
    return out


def main(out_path, population, pi0):
    rows = []

    def log(x):
        rows.append(x)
        print(json.dumps(x), flush=True)
    pi, hist = em(population, range(300, 324), pi0, log=log)
    res = {"population": population, "pi0": pi0, "pi_hat": pi, "em": hist,
           "test_hat": test(population, range(21, 29), pi, log=log), "log": rows}
    json.dump(res, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
