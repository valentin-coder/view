"""36. kör: a célfüggvény valószínűségi jelentése. Az ARLC-pontszámot (rögzített megbízhatóság,
kivétel, kontextus, vágás és indukció nélkül) egy ProbLog-programként felírt generatív modell
−log2 P(hipotézis, jelentések) értékével vetjük össze."""
from __future__ import annotations

import math
import random

from problog.program import PrologString
from problog import get_evaluatable

from .core import Hyp, Memory


def to_problog(mem: Memory, H: Hyp, delta: float) -> str:
    L = []
    eps = mem.exc_prior
    for o in mem.obs:
        L.append(f"{o.q}::rel({o.id}).")
        L.append(f"evidence(rel({o.id}), {'false' if o.id in H.rej else 'true'}).")
    for o in mem.obs:
        if o.rule is not None:
            r = o.rule
            guard = "" if eps is None else f", \\+ ab({o.id}, X)"
            if r.pred == "has":
                L.append(f"rule_has(X, {r.obj}, {int(r.pos)}) :- rel({o.id}), isa(X, {r.body}){guard}.")
            elif r.pos:
                L.append(f"isa(X, {r.obj}) :- rel({o.id}), isa(X, {r.body}){guard}.")
            else:
                L.append(f"nisa(X, {r.obj}) :- rel({o.id}), isa(X, {r.body}){guard}.")
        elif o.lit.pred == "isa":
            L.append(f"isa({o.lit.subj}, {o.lit.obj}) :- rel({o.id}).")
        else:
            l = o.lit
            L.append(f"fact_has({l.subj}, {l.obj}, {int(l.pos)}) :- rel({o.id}).")
            L.append(f"{1 - delta}::lp({o.id}).  0.5::lu({o.id}).  0.5::lr({o.id}).")
            L.append(f"ok({o.id}) :- rel({o.id}), rule_has({l.subj}, {l.obj}, {int(l.pos)}), lp({o.id}).")
            L.append(f"ok({o.id}) :- rel({o.id}), \\+ rule_has({l.subj}, {l.obj}, {int(l.pos)}), lu({o.id}).")
            L.append(f"ok({o.id}) :- \\+ rel({o.id}), lr({o.id}).")
            L.append(f"evidence(ok({o.id}), true).")
    if eps is not None:
        for rid, e in mem._candidate_applications():
            L.append(f"{eps}::ab({rid}, {e}).")
            L.append(f"evidence(ab({rid}, {e}), {'true' if (rid, e) in H.exc else 'false'}).")
        L.append("ab(dummy, dummy) :- fail.")
    L += ["rule_has(dummy, dummy, 0) :- fail.", "fact_has(dummy, dummy, 0) :- fail.", "isa(dummy, dummy) :- fail.",
          "conflict :- rule_has(E, P, 1), rule_has(E, P, 0).",
          "conflict :- rule_has(E, P, V), fact_has(E, P, W), V \\= W.",
          "conflict :- fact_has(E, P, 1), fact_has(E, P, 0).",
          "conflict :- isa(E, dax), isa(E, fep).",
          "nisa(dummy, dummy) :- fail.",
          "conflict :- isa(E, C), nisa(E, C).",
          "evidence(conflict, false).", "query(conflict)."]
    return "\n".join(L)


def logp_evidence(program: str) -> float:
    """log2 P(evidence): a ProbLog normalizálatlan feltételes értékéből. A get_evaluatable
    az evidenciára feltételezett lekérdezést adja; P(evidence)-t a súlyozott modellszámlálóból
    olvassuk ki."""
    from problog.formula import LogicFormula
    from problog.sdd_formula import SDD  # noqa: F401  (ha nincs SDD, a ddnnf-et használja)
    lf = LogicFormula.create_from(PrologString(program))
    ev = get_evaluatable().create_from(lf)
    e = ev.get_evaluator()
    return math.log2(e.evaluate_evidence())


def check(problems, n_assign=20, seed=0, delta=0.05, exc_prior=None):
    rng = random.Random(seed)
    rows = []
    for pid, (sch, obs) in enumerate(problems):
        mem = Memory(sch, mode="arlc-noctx", induce=False)
        mem.exc_prior = exc_prior
        for o in obs:
            mem.observe(o)
        ids = [o.id for o in obs]
        apps = mem._candidate_applications() if exc_prior else []
        tried = 0
        while tried < n_assign:
            rej = frozenset(i for i in ids if rng.random() < 0.3)
            exc = frozenset(a for a in apps if rng.random() < 0.3)
            H = Hyp(rej=rej, exc=exc)
            if mem.find_conflict(H) is not None:
                continue
            tried += 1
            arlc = mem.score(H)
            pl = -logp_evidence(to_problog(mem, H, delta))
            rows.append({"problem": pid, "rej": sorted(rej), "arlc_bits": arlc, "problog_bits": pl,
                         "diff": arlc - pl})
    return rows


def problems_with_isa(n, seed=0):
    """Véletlen feladatok alosztály- és negatív (diszjunkt) szabályokkal is."""
    import itertools
    from .core import Lit, Obs, Rule, Schema
    rng = random.Random(seed)
    out = []
    for k in range(n):
        c = itertools.count(1)
        sch = Schema(disjoint={frozenset(("dax", "fep"))}, n_entities=5, n_categories=4, n_props=2)
        obs = [Obs(next(c), "b1", 0, rng.choice([0.9, 0.95]), rule=Rule("dax", "isa", "animal", True)),
               Obs(next(c), "b1", 0, 0.9, rule=Rule("animal", "has", "p", True)),
               Obs(next(c), "b2", 0, 0.9, rule=Rule("fep", "has", "p", False))]
        if rng.random() < 0.5:
            obs.append(Obs(next(c), "b2", 0, 0.8, rule=Rule("animal", "isa", "fep", False)))
        for i in range(3):
            obs.append(Obs(next(c), rng.choice(["s1", "s2"]), i + 1, 0.9, lit=Lit("isa", f"e{i}", rng.choice(["dax", "fep"]))))
        for i in range(3):
            obs.append(Obs(next(c), "f", i + 5, rng.choice([0.8, 0.9]),
                           lit=Lit("has", f"e{rng.randrange(3)}", "p", rng.random() < 0.5)))
        out.append((sch, obs))
    return out
