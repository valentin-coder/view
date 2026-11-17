"""39. kör: ellentényes (hű) magyarázatok egy átrendezési döntésre.

szükséges okok: azok a megfigyelések, amelyek egyenkénti elhagyása megfordítja a döntést
elégséges magyarázat: a háttéren (szabályok) felüli megfigyelések egy mohón minimalizált
  részhalmaza, amely önmagában is előidézi a döntést
"""
from __future__ import annotations

import itertools

from .core import Lit, Memory, Obs, Rule, Schema


def replay(schema, obs, mem_kw=None):
    mem = Memory(schema, **(mem_kw or {}))
    for o in obs:
        mem.observe(o)
    return mem


def explain(schema, obs, decision, background=lambda o: o.rule is not None, mem_kw=None):
    full = decision(replay(schema, obs, mem_kw))
    cand = [o for o in obs if not background(o)]
    necessary = []
    for o in cand:
        if decision(replay(schema, [x for x in obs if x.id != o.id], mem_kw)) != full:
            necessary.append(o)
    keep = list(cand)
    for o in sorted(cand, key=lambda x: (x in necessary, x.id)):   # előbb a nem szükségeseket próbálja elhagyni
        trial = [x for x in keep if x.id != o.id]
        sub = [x for x in obs if background(x)] + trial
        if decision(replay(schema, sorted(sub, key=lambda x: x.id), mem_kw)) == full:
            keep = trial
    return {"decision": full, "n_candidates": len(cand), "necessary": [o.id for o in necessary],
            "sufficient": [o.id for o in keep]}


def e2a_case(N, m):
    sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + m + 2, n_categories=2, n_props=2)
    c = itertools.count(1)
    obs = [Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)),
           Obs(next(c), "survey", 1, 0.9, lit=Lit("isa", "probe", "dax"))]
    t = 1
    for i in range(N):
        t += 1
        obs.append(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        obs.append(Obs(next(c), f"s{i}", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
    for j in range(m):
        t += 1
        obs.append(Obs(next(c), f"a{j}", t, 0.9, lit=Lit("isa", f"x{j}", "dax")))
        obs.append(Obs(next(c), f"a{j}", t, 0.9, lit=Lit("has", f"x{j}", "poisonous", False)))
    return sch, obs


def kind(o):
    if o.lit is None:
        return "szabály"
    if o.lit.subj == "probe":
        return "próba-tagság"
    if o.lit.subj.startswith("d"):
        return "alátámasztás:" + o.lit.pred
    return "anomália:" + o.lit.pred


def run(cases=((4, 3), (4, 6), (8, 4), (8, 7), (12, 5), (12, 8))):
    rows = []
    for N, m in cases:
        sch, obs = e2a_case(N, m)
        byid = {o.id: o for o in obs}
        r = explain(sch, obs, lambda mem: 1 in mem.best.rej)
        rows.append({"N": N, "m": m, "rule_dropped": r["decision"], "n_candidates": r["n_candidates"],
                     "necessary": [kind(byid[i]) for i in r["necessary"]],
                     "sufficient": [kind(byid[i]) for i in r["sufficient"]]})
    return rows
