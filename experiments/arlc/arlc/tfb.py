"""28. kör: TFB – Thagard-fokozat benchmark (szimbolikus változat).

Fokozatok: 1 új példány, 2 gyenge szabály kivétellel, 3 erős szabály, 5 új fajta-reláció,
7 megkülönböztetés feladása (két kategória egyesítése), 8 ágátugrás (átkategorizálás),
9 fafelcserélés (a hierarchia szervezőelvének cseréje, két előre adott fával).
A 4. (rész–egész) és a 6. (új fogalom grounding nélkül) fokozat itt nem értelmezett.
"""
from __future__ import annotations

import random

from .core import Lit, Memory, Obs, Rule, Schema

METHODS = {
    "recency": dict(mode="recency"),
    "wms": dict(mode="wms"),
    "arlc": dict(mode="arlc"),
    "arlc+forrás": dict(mode="arlc", source_moves=True),
    "arlc-beta30+forrás": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=30),
    "arlc-beta10+forrás": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=10),
    "arlc-beta3+forrás": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=3),
    "arlc-2szint(T3,S30)": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=30, theory_kappa=3),
    "arlc-2szint(T3,S100)": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=100, theory_kappa=3),
    "arlc-2szint(T1,S30)": dict(mode="arlc", source_moves=True, reliability="beta", prior_strength=30, theory_kappa=1),
}


class Ctr:
    def __init__(self):
        self.i = 0

    def __next__(self):
        self.i += 1
        return self.i


def make(method: str, schema: Schema) -> Memory:
    kw = dict(METHODS[method])
    sm = kw.pop("source_moves", None)
    tk = kw.pop("theory_kappa", "nincs megadva")
    mem = Memory(schema, **kw)
    if sm is not None:
        mem.source_moves = sm
    if tk != "nincs megadva":
        mem.theory_kappa = tk
    return mem


def acc(mem, queries):
    return sum(mem.answer(e, p, record_use=False) == v for e, p, v in queries) / len(queries)


# ------------------------------------------------------------------ 1, 2, 3, 5, 8
def deg1(method, seed):
    sch = Schema(n_entities=10, n_categories=3, n_props=4)
    m, c = make(method, sch), Ctr()
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)))
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "striped", False)))
    m.observe(Obs(next(c), "s", 1, 0.9, lit=Lit("isa", "e1", "dax")))
    return acc(m, [("e1", "poisonous", True), ("e1", "striped", False)]), {}


def deg2(method, seed):
    sch = Schema(n_entities=12, n_categories=3, n_props=4)
    m, c = make(method, sch), Ctr()
    m.observe(Obs(next(c), "blog", 0, 0.8, rule=Rule("dax", "has", "noisy", True)))
    for i in range(9):
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
    for i in range(5, 9):   # 4 alátámasztó tény (más daxokról)
        m.observe(Obs(next(c), "field", 8 + i, 0.9, lit=Lit("has", f"d{i}", "noisy", True)))
    m.observe(Obs(next(c), "field", 20, 0.9, lit=Lit("has", "d0", "noisy", False)))
    q = [("d0", "noisy", False)] + [(f"d{i}", "noisy", True) for i in range(1, 5)]
    return acc(m, q), {}


def deg3(method, seed):
    sch = Schema(n_entities=12, n_categories=3, n_props=4)
    m, c = make(method, sch), Ctr()
    for i in range(6):
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
    m.observe(Obs(next(c), "book", 10, 0.99, rule=Rule("dax", "has", "heavy", True)))
    return acc(m, [(f"d{i}", "heavy", True) for i in range(6)]), {}


def deg5(method, seed):
    sch = Schema(n_entities=12, n_categories=4, n_props=4)
    m, c = make(method, sch), Ctr()
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("wug", "has", "shiny", True)))
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("wug", "has", "slow", False)))
    for i in range(4):
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
    m.observe(Obs(next(c), "book2", 10, 0.95, rule=Rule("dax", "isa", "wug", True)))
    q = [(f"d{i}", "shiny", True) for i in range(4)] + [(f"d{i}", "slow", False) for i in range(4)]
    return acc(m, q), {}


def deg8(method, seed):
    rng = random.Random(seed)
    sch = Schema(n_entities=12, n_categories=4, n_props=6)
    m, c = make(method, sch), Ctr()
    for cat, props in (("dax", {"poisonous": True, "striped": False}), ("fep", {"poisonous": False, "striped": True})):
        for p, v in props.items():
            m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule(cat, "has", p, v)))
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "isa", "fep", False)))
    for i in range(4):
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"f{i}", "fep")))
    m.observe(Obs(next(c), "expert", 10, 0.99, lit=Lit("isa", "d0", "fep")))
    q = [("d0", "poisonous", False), ("d0", "striped", True)] + \
        [(f"d{i}", "poisonous", True) for i in range(1, 4)] + [(f"f{i}", "striped", True) for i in range(4)]
    return acc(m, q), {}


# ------------------------------------------------------------------ 7
def deg7(method, seed, n_support=3, q_merge=0.99):
    """Előzmény: a dax és a fep diszjunkt (visszavonható negatív szabályokkal), mindkettőnek
    saját tulajdonságai. Kiváltó: 'a dax és a fep ugyanaz' (két pozitív szabály). Várt: a
    diszjunktság feladása, és minden tag mindkét kategória tulajdonságait örökli."""
    sch = Schema(n_entities=20, n_categories=2, n_props=4)
    m, c = make(method, sch), Ctr()
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)))
    m.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("fep", "has", "striped", True)))
    neg = [Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "isa", "fep", False)),
           Obs(next(c), "book", 0, 0.95, rule=Rule("fep", "isa", "dax", False))]
    for o in neg:
        m.observe(o)
    for i in range(n_support):
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        m.observe(Obs(next(c), "s", i + 1, 0.9, lit=Lit("isa", f"f{i}", "fep")))
    m.observe(Obs(next(c), "expert", 20, q_merge, rule=Rule("dax", "isa", "fep", True)))
    m.observe(Obs(next(c), "expert", 20, q_merge, rule=Rule("fep", "isa", "dax", True)))
    q = [(f"d{i}", "striped", True) for i in range(n_support)] + \
        [(f"f{i}", "poisonous", True) for i in range(n_support)] + \
        [(f"d{i}", "poisonous", True) for i in range(n_support)]
    return acc(m, q), {"disjointness_dropped": all(o.id in m.best.rej for o in neg)}


# ------------------------------------------------------------------ 9
TREE_H = {  # élőhely szerinti fa (a régi, "book_h" forrás)
    "isa": [("dax", "aquatic"), ("fep", "terrestrial"), ("zorb", "aquatic"), ("blick", "terrestrial")],
    "has": [("aquatic", "gills", True), ("aquatic", "warm", False), ("terrestrial", "gills", False),
            ("terrestrial", "warm", True), ("aquatic", "fins", True), ("terrestrial", "legs", True)],
}
TREE_L = {  # leszármazás szerinti fa (az új, "book_l" forrás)
    "isa": [("dax", "mammalian"), ("fep", "reptilian"), ("zorb", "reptilian"), ("blick", "mammalian")],
    "has": [("mammalian", "warm", True), ("mammalian", "gills", False), ("reptilian", "warm", False),
            ("reptilian", "gills", False), ("mammalian", "fur", True), ("reptilian", "scales", True)],
}


def deg9(method, seed, n_facts=8, q_h=0.95, q_l=0.9, truth_tree="L", noise=0.0):
    """Két teljes fa két forrásból. A megfigyelt tények a leszármazási fát támasztják alá, az
    élőhelyit cáfolják. Mérés: pontosság a leszármazási igazság szerint, és koherencia: a
    vesztes (élőhelyi) fa szabályaiból hány marad aktív."""
    rng = random.Random(seed)
    sch = Schema(disjoint={frozenset(("aquatic", "terrestrial")), frozenset(("mammalian", "reptilian"))},
                 n_entities=40, n_categories=6, n_props=6)
    m, c = make(method, sch), Ctr()
    h_ids, l_ids = [], []
    for src, tree, q, ids in (("book_h", TREE_H, q_h, h_ids), ("book_l", TREE_L, q_l, l_ids)):
        for a, b in tree["isa"]:
            o = Obs(next(c), src, 0, q, rule=Rule(a, "isa", b, True))
            m.observe(o)
            ids.append(o.id)
        for a, p, v in tree["has"]:
            o = Obs(next(c), src, 0, q, rule=Rule(a, "has", p, v))
            m.observe(o)
            ids.append(o.id)
    ents = []
    for cat in ("dax", "fep", "zorb", "blick"):
        for i in range(3):
            e = f"{cat}{i}"
            ents.append((e, cat))
            m.observe(Obs(next(c), "survey", 1, 0.9, lit=Lit("isa", e, cat)))
    # az igazság a választott fa szerint (alapból a leszármazási)
    T = TREE_L if truth_tree == "L" else TREE_H
    truth = {}
    for e, cat in ents:
        sup = dict(T["isa"])[cat]
        truth[e] = {p: v for a, p, v in T["has"] if a == sup}
    t = 2
    observed = set()
    for _ in range(n_facts):
        e, cat = rng.choice(ents)
        p = rng.choice(sorted(truth[e]))
        observed.add((e, p))
        t += 1
        v = truth[e][p] if rng.random() >= noise else (not truth[e][p])
        m.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", e, p, v)))
    queries = [(e, p, v) for e, _ in ents for p, v in truth[e].items() if (e, p) not in observed]
    active_h = sum(1 for i in h_ids if i not in m.best.rej) / len(h_ids)
    active_l = sum(1 for i in l_ids if i not in m.best.rej) / len(l_ids)
    return acc(m, queries), {"h_rules_active": active_h, "l_rules_active": active_l,
                             "n_queries": len(queries)}


DEGREES = {1: deg1, 2: deg2, 3: deg3, 5: deg5, 7: deg7, 8: deg8, 9: deg9}


def run(seeds=range(5), n_facts_list=(2, 4, 8, 16)):
    rows = []
    for deg, fn in DEGREES.items():
        for method in METHODS:
            for seed in (seeds if deg in (8, 9) else [0]):
                if deg == 9:
                    for nf in n_facts_list:
                        a, extra = fn(method, seed, n_facts=nf)
                        rows.append({"degree": deg, "method": method, "seed": seed, "n_facts": nf,
                                     "acc": a, **extra})
                else:
                    a, extra = fn(method, seed)
                    rows.append({"degree": deg, "method": method, "seed": seed, "acc": a, **extra})
    return rows
