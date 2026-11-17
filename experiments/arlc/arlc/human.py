"""27. kör: emberi hiedelemrevíziós jelenségek szimbolikus megfelelői.

(a) Elio–Pelletier-típusú választás: szabály + tény + ellentmondás -> mit ad fel a rendszer?
(b) Sorrendhatás (Hogarth–Einhorn): ugyanazok az evidenciák más sorrendben.
(c) Chinn–Brewer: az anomáliákra adott hét válaszfajta mint az ARLC operátorai.
(d) Hiedelem-kitartás (Ross–Lepper–Hubbard): hiteltelenítés után.
"""
from __future__ import annotations

import itertools
import math
import random

from .core import Hyp, Lit, Memory, Obs, Rule, Schema


class Ctr:
    def __init__(self):
        self.i = 0

    def __next__(self):
        self.i += 1
        return self.i


# ---------------------------------------------------------------------------------- (a)
def elio_pelletier(n_entities_list=(4, 8, 16, 64, 256), q_rule_list=(0.8, 0.9, 0.95),
                   q_fact_list=(0.8, 0.9, 0.95), q_contra=0.9, support_list=(0, 2, 5)):
    """Szabály ('a dax mérges'), tény ('x dax'), ellentmondás ('x nem mérges'). Melyik esik?"""
    rows = []
    for nE, qr, qf, sup in itertools.product(n_entities_list, q_rule_list, q_fact_list, support_list):
        sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=nE, n_categories=2, n_props=2)
        mem = Memory(sch, mode="arlc", induce=False)
        c = Ctr()
        r = Obs(next(c), "rulesrc", 0, qr, rule=Rule("dax", "has", "poisonous", True))
        mem.observe(r)
        for i in range(sup):
            mem.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
            mem.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
        f = Obs(next(c), "factsrc", 50, qf, lit=Lit("isa", "x", "dax"))
        mem.observe(f)
        k = Obs(next(c), "contrasrc", 51, q_contra, lit=Lit("has", "x", "poisonous", False))
        mem.observe(k)
        b = mem.best
        if r.id in b.rej:
            choice = "szabály feladása"
        elif any(e[0] == r.id for e in b.exc):
            choice = "szabály gyengítése (kivétel)"
        elif f.id in b.rej:
            choice = "tény feladása"
        elif k.id in b.rej:
            choice = "ellentmondás elutasítása"
        else:
            choice = "egyéb"
        rows.append({"n_entities": nE, "q_rule": qr, "q_fact": qf, "support": sup, "choice": choice})
    return rows


# ---------------------------------------------------------------------------------- (b)
def order_effects(age_discounts=(1.0, 0.9, 0.7, 0.5), etas=(0.0, 0.3), reliabilities=("fixed", "beta")):
    """x tagsága A vagy B (diszjunkt). Erős és gyenge evidenciák két sorrendben:
    'erős A elöl' (A A a b b b) vs 'erős A hátul' (b b b A A ... ugyanazok)."""
    strong, weak = 0.95, 0.7
    seq_A = [("A", strong), ("A", strong)]
    seq_B = [("B", weak), ("B", weak), ("B", weak), ("B", weak)]
    rows = []
    for rel in reliabilities:
        for lam in age_discounts:
            for eta in etas:
                res = {}
                for order_name, seq in (("A-elöl", seq_A + seq_B), ("A-hátul", seq_B + seq_A)):
                    sch = Schema(disjoint={frozenset(("A", "B"))}, n_entities=2, n_categories=2, n_props=2)
                    kw = {"reliability": "beta", "prior_strength": 30} if rel == "beta" else {}
                    mem = Memory(sch, mode="arlc", eta=eta, induce=False, **kw)
                    mem.age_discount = lam
                    c = Ctr()
                    mem.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("A", "has", "pa", True)))
                    mem.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("B", "has", "pb", True)))
                    for t, (cat, q) in enumerate(seq, start=1):
                        mem.observe(Obs(next(c), f"src{t}", t, q, lit=Lit("isa", "x", cat)))
                        mem.answer("x", "pa"), mem.answer("x", "pb")
                    res[order_name] = "A" if mem.answer_isa("x", "A") else ("B" if mem.answer_isa("x", "B") else "?")
                rows.append({"reliability": rel, "age_discount": lam, "eta": eta, **res,
                             "order_effect": res["A-elöl"] != res["A-hátul"]})
    return rows


# ---------------------------------------------------------------------------------- (c)
def classify(mem: Memory, pre: Hyp, rule_id: int, anomaly_ids: set, isa_ids: set) -> str:
    b = mem.best
    if rule_id in b.rej:
        return "elmélet-csere" if b.ind else "elmélet feladása"
    if b.iso - pre.iso:
        return "kizárás (más kontextus)"
    if any(e[0] == rule_id for e in b.exc - pre.exc):
        return "perifériás módosítás (kivétel)"
    if anomaly_ids & b.rej and not (isa_ids & b.rej):
        return "adat elutasítása"
    if isa_ids & b.rej:
        return "újraértelmezés (nem is tartozik ide)"
    if b.cut != pre.cut:
        return "frissítés (a világ változott)"
    return "egyéb"


def chinn_brewer(Ns=(0, 2, 6, 12), n_anom_list=(1, 2, 3, 4, 5, 6, 8), q_list=(0.7, 0.9, 0.99),
                 tagged_list=(False, True), seeds=range(3), membership_from=("same", "survey")):
    """Az anomáliák forrása és száma, a szabály beágyazottsága és az, hogy az anomáliák egy
    másik kontextusból (saját, következetes forrásból) jönnek-e."""
    rows = []
    for N, m, q, tagged, seed, mf in itertools.product(Ns, n_anom_list, q_list, tagged_list, seeds,
                                                        membership_from):
        rng = random.Random(seed)
        sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + m + 2, n_categories=2, n_props=2)
        mem = Memory(sch, mode="arlc", reliability="beta", prior_strength=30, depth=3, beam=6)
        c = Ctr()
        r = Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True))
        mem.observe(r)
        t = 0
        for i in range(N):
            t += 1
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
            mem.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
        pre = mem.best
        an, isa = set(), set()
        for j in range(m):
            t += 1
            src = "valley" if tagged else f"obs{seed}_{j}_{rng.randrange(10**6)}"
            a = Obs(next(c), src if mf == "same" else "survey", t, q if mf == "same" else 0.9,
                    lit=Lit("isa", f"x{j}", "dax"))
            k = Obs(next(c), src, t, q, lit=Lit("has", f"x{j}", "poisonous", False))
            mem.observe(a)
            mem.observe(k)
            isa.add(a.id)
            an.add(k.id)
        rows.append({"N": N, "anomalies": m, "q": q, "one_consistent_source": tagged, "seed": seed,
                     "membership_from": mf,
                     "response": classify(mem, pre, r.id, an, isa)})
    return rows


# ---------------------------------------------------------------------------------- (d)
def perseverance(independents=(0, 2, 4, 6), reliabilities=("fixed", "beta")):
    rows = []
    for rel in reliabilities:
        for sm in (False, True):
            for ind in independents:
                sch = Schema(n_entities=4 + 6 + ind, n_categories=2, n_props=2)
                kw = {"reliability": "beta", "prior_strength": 30} if rel == "beta" else {}
                mem = Memory(sch, mode="arlc", **kw)
                mem.source_moves = sm
                c = Ctr()
                t = 0
                mem.observe(Obs(next(c), "survey", 0, 0.9, lit=Lit("isa", "probe", "dax")))
                for i in range(6):
                    t += 1
                    mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
                    mem.observe(Obs(next(c), "feedback", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
                for i in range(ind):
                    t += 1
                    mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"z{i}", "dax")))
                    mem.observe(Obs(next(c), "other", t, 0.9, lit=Lit("has", f"z{i}", "poisonous", True)))
                before = mem.answer("probe", "poisonous", record_use=False)
                mem.set_source_q("feedback", 0.1)
                after = mem.answer("probe", "poisonous", record_use=False)
                rows.append({"reliability": rel, "source_moves": sm, "independent_support": ind,
                             "before": before, "after": after, "persevered": after is True})
    return rows


# ---------------------------------------------------------------------------------- (c2)
def alternative_availability(Ns=(2, 6, 12), n_anom_list=(1, 2, 3, 4, 5, 6, 8), q_anom=0.9,
                             q_alt_list=(None, 0.6, 0.8), seeds=range(3)):
    """Chinn–Brewer 2. faktor: elérhető-e egy alternatív elmélet ('a daxok nem mérgesek',
    gyenge forrásból, előre közölve). A tagságot egy régi, hiteles forrás közli."""
    rows = []
    for N, m, qa, seed in itertools.product(Ns, n_anom_list, q_alt_list, seeds):
        sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + m + 2, n_categories=2, n_props=2)
        mem = Memory(sch, mode="arlc", reliability="beta", prior_strength=30, depth=3, beam=6)
        c = Ctr()
        r = Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True))
        mem.observe(r)
        alt = None
        if qa is not None:
            alt = Obs(next(c), "altbook", 0, qa, rule=Rule("dax", "has", "poisonous", False))
            mem.observe(alt)
        t = 0
        for i in range(N):
            t += 1
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
            mem.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
        for j in range(m):
            t += 1
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"x{j}", "dax")))
            mem.observe(Obs(next(c), f"lab{seed}_{j}", t, q_anom, lit=Lit("has", f"x{j}", "poisonous", False)))
        b = mem.best
        rows.append({"N": N, "anomalies": m, "q_alt": qa, "seed": seed,
                     "theory_dropped": r.id in b.rej,
                     "alternative_adopted": alt is not None and alt.id not in b.rej,
                     "induced_replacement": bool(b.ind)})
    return rows


# ---------------------------------------------------------------------------------- (c3)
def reconciling_alternative(Ns=(2, 6, 12), n_anom_list=(1, 2, 3, 4, 6, 8), q_alt_list=(None, 0.7, 0.9),
                            class_exc_list=(False, True), seeds=range(2)):
    """Összebékítő alternatíva: 'a laboratóriumi dax (ldax) a dax alfaja, és nem mérges'.
    Az anomáliák: 'x egy ldax' és 'x nem mérges'. Specifikussági elv nélkül az alfaj szabálya
    minden tagnál ütközik az általános szabállyal."""
    rows = []
    for N, m, qa, ce, seed in itertools.product(Ns, n_anom_list, q_alt_list, class_exc_list, seeds):
        sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + m + 2, n_categories=3, n_props=2)
        mem = Memory(sch, mode="arlc", reliability="beta", prior_strength=30, depth=3, beam=6)
        mem.class_exceptions = ce
        c = Ctr()
        r = Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True))
        mem.observe(r)
        alt = []
        if qa is not None:
            alt = [Obs(next(c), "altbook", 0, qa, rule=Rule("ldax", "isa", "dax", True)),
                   Obs(next(c), "altbook", 0, qa, rule=Rule("ldax", "has", "poisonous", False))]
            for o in alt:
                mem.observe(o)
        t = 0
        for i in range(N):
            t += 1
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
            mem.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
        for j in range(m):
            t += 1
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"x{j}", "ldax" if qa else "dax")))
            mem.observe(Obs(next(c), f"lab{seed}_{j}", t, 0.9, lit=Lit("has", f"x{j}", "poisonous", False)))
        b = mem.best
        cls = [x for x in b.exc if isinstance(x[1], str) and x[1].startswith("cat:")]
        rows.append({"N": N, "anomalies": m, "q_alt": qa, "class_exceptions": ce, "seed": seed,
                     "theory_dropped": r.id in b.rej,
                     "alternative_adopted": bool(alt) and all(o.id not in b.rej for o in alt),
                     "class_exception_used": bool(cls),
                     "old_data_kept": all(mem.answer(f"d{i}", "poisonous", record_use=False) is True for i in range(N)),
                     "anomalies_explained": all(mem.answer(f"x{j}", "poisonous", record_use=False) is False for j in range(m))})
    return rows
