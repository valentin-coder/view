"""44. kör: procedurálisan generált, előre rögzített benchmark.

ELŐREGISZTRÁCIÓ: ez a fájl és a docs/korok/44-procedurialis-benchmark.md elemzési terve a
benchmark futtatása ELŐTT kerül commitba. A generátor paraméterei utána nem változnak.

Igazság-szemantika: specifikus öröklés. Egy entitás tulajdonsága a legspecifikusabb
(a kategória-DAG-ban legközelebbi) olyan kategória szabálya, amely a tulajdonságról szól;
ha több, egyformán közeli kategória ellentmond (Nixon-gyémánt), az érték nem definiált, és a
kérdés kimarad. Az entitás saját (valódi) kivétele mindent felülír.
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field

from .core import Lit, Obs, Rule, Schema

SURPRISES = ("átkategorizálás", "szabály-helyesbítés", "kivételes alfaj", "hazug forrás", "más régió")


@dataclass
class World:
    cats: list
    parents: dict                 # c -> [szülők]
    rules: dict                   # c -> {p: bool}
    members: dict                 # e -> levélkategória
    exceptions: dict              # e -> {p: bool} valódi kivételek
    props: list
    disjoint: set = field(default_factory=set)

    def ancestors_by_depth(self, c):
        """(távolság, kategória) párok BFS szerint."""
        out, frontier, seen, d = [], [c], {c}, 0
        while frontier:
            out += [(d, x) for x in frontier]
            nxt = []
            for x in frontier:
                for p in self.parents.get(x, []):
                    if p not in seen:
                        seen.add(p)
                        nxt.append(p)
            frontier, d = nxt, d + 1
        return out

    def truth(self, e):
        res = {}
        anc = self.ancestors_by_depth(self.members[e])
        for p in self.props:
            if p in self.exceptions.get(e, {}):
                res[p] = self.exceptions[e][p]
                continue
            best_d, vals = None, set()
            for d, c in anc:
                if p in self.rules.get(c, {}):
                    if best_d is None:
                        best_d = d
                    if d == best_d:
                        vals.add(self.rules[c][p])
            if len(vals) == 1:
                res[p] = vals.pop()
        return res


def generate_world(rng, n_top=3, n_mid=5, n_leaf=8, n_props=10, n_ent=30, multi_parent=0.25,
                   rules_per_cat=2, exc_rate=0.03):
    top = [f"T{i}" for i in range(n_top)]
    mid = [f"M{i}" for i in range(n_mid)]
    leaf = [f"L{i}" for i in range(n_leaf)]
    parents = {c: [] for c in top}
    for c in mid:
        ps = [rng.choice(top)]
        if rng.random() < multi_parent:
            ps.append(rng.choice([t for t in top if t not in ps]))
        parents[c] = ps
    for c in leaf:
        ps = [rng.choice(mid)]
        if rng.random() < multi_parent:
            ps.append(rng.choice([m for m in mid if m not in ps]))
        parents[c] = ps
    cats = top + mid + leaf
    props = [f"p{i}" for i in range(n_props)]
    rules = {c: {p: rng.random() < 0.5 for p in rng.sample(props, rules_per_cat)} for c in cats}
    members = {f"e{i}": rng.choice(leaf) for i in range(n_ent)}
    w = World(cats, parents, rules, members, {}, props)
    for e in members:
        if rng.random() < exc_rate * n_props:
            tr = w.truth(e)
            if tr:
                p = rng.choice(sorted(tr))
                w.exceptions[e] = {p: not tr[p]}
    w.disjoint = {frozenset((a, b)) for a in top for b in top if a < b}
    return w


def stream(w: World, rng, book_error=0.1, fact_noise=0.05, facts_per_ent=3):
    """Megfigyelések: tankönyvi szabályok (néha hibásak), tagságok, zajos tények."""
    c = itertools.count(1)
    obs = []
    for x, ps in w.parents.items():
        for p in ps:
            obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(x, "isa", p, True)))
    w.book_errors = []
    for x, rs in w.rules.items():
        for p, v in rs.items():
            stated = v if rng.random() >= book_error else (not v)
            if stated != v:
                w.book_errors.append((x, p))
            obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(x, "has", p, stated)))
    t = 1
    for e, leaf in w.members.items():
        obs.append(Obs(next(c), "census", t, 0.95, lit=Lit("isa", e, leaf, True)))
        tr = w.truth(e)
        for p in rng.sample(sorted(tr), min(facts_per_ent, len(tr))):
            v = tr[p] if rng.random() >= fact_noise else (not tr[p])
            obs.append(Obs(next(c), "field", t, 0.9, lit=Lit("has", e, p, v)))
        t += 1
    return obs, c, t


def _members_of(w, cat):
    """Az entitások, amelyeknek cat őse (vagy maguk a levél)."""
    out = []
    for e, leaf in w.members.items():
        if cat in {x for _, x in w.ancestors_by_depth(leaf)}:
            out.append(e)
    return sorted(out)


def surprise(kind, w: World, rng, c, t):
    """Visszaadja: (új megfigyelések, célkérdések [(e, p)]). A célkérdések a meglepetés típusára
    jellemző kérdések; az értékelés a meglepetés utáni igazság szerint történik."""
    new, target = [], []
    if kind == "átkategorizálás":
        e = rng.choice(sorted(w.members))
        others = [l for l in w.cats if l.startswith("L") and l != w.members[e]]
        nl = rng.choice(others)
        w.members[e] = nl
        new.append(Obs(next(c), "expert", t, 0.99, lit=Lit("isa", e, nl, True)))
        target = [(e, p) for p in w.truth(e)]
    elif kind == "szabály-helyesbítés":
        # a tankönyv egy szabályt hibásan közölt; egy ellenőrzés a helyeset közli. A világ változatlan.
        if w.book_errors:
            cat, p = rng.choice(sorted(w.book_errors))
        else:
            cat = rng.choice([x for x in w.cats if w.rules[x]])
            p = rng.choice(sorted(w.rules[cat]))
        new.append(Obs(next(c), "review", t, 0.995, rule=Rule(cat, "has", p, w.rules[cat][p])))
        target = [(e, p) for e in _members_of(w, cat) if p in w.truth(e)]
    elif kind == "kivételes alfaj":
        cands = []
        for leaf_ in [x for x in w.cats if x.startswith("L")]:
            w.members["_probe_"] = leaf_
            tr = w.truth("_probe_")
            del w.members["_probe_"]
            cands += [(leaf_, p_) for p_, v in tr.items() if v is False]
        leaf, p = rng.choice(sorted(cands)) if cands else (rng.choice([x for x in w.cats if x.startswith("L")]),
                                                         rng.choice(w.props))
        if "marked" not in w.props:
            w.props.append("marked")
        for i in range(4):
            e = f"z{i}"
            w.members[e] = leaf
            w.exceptions[e] = {p: True, "marked": True}
            new.append(Obs(next(c), "census", t, 0.95, lit=Lit("isa", e, leaf, True)))
            new.append(Obs(next(c), "census", t, 0.95, lit=Lit("has", e, "marked", True)))
            new.append(Obs(next(c), f"lab{i}", t, 0.9, lit=Lit("has", e, p, True)))
        target = [(e, p) for e in sorted(w.members) if w.members[e] == leaf]
    elif kind == "hazug forrás":
        for e in rng.sample(sorted(w.members), 8):
            tr = w.truth(e)
            if tr:
                p = rng.choice(sorted(tr))
                new.append(Obs(next(c), "liar", t, 0.9, lit=Lit("has", e, p, not tr[p])))
                target.append((e, p))
    elif kind == "más régió":
        cands = [x for x in w.cats if x.startswith("L") and w.rules[x] and _members_of(w, x)]
        cat = rng.choice(cands) if cands else rng.choice([x for x in w.cats if w.rules[x]])
        p = rng.choice(sorted(w.rules[cat]))
        for e in _members_of(w, cat):
            if p in w.truth(e):
                new.append(Obs(next(c), "region2", t, 0.9, lit=Lit("has", e, p, not w.truth(e)[p])))
                target.append((e, p))
        new.append(Obs(next(c), "region2", t, 0.9, rule=Rule(cat, "has", p, not w.rules[cat][p])))
    return new, target


def make_case(seed, kind):
    rng = random.Random(seed)
    w = generate_world(rng)
    obs, c, t = stream(w, rng)
    pre_truth = {e: w.truth(e) for e in w.members}
    new, target = surprise(kind, w, rng, c, t + 1)
    post_truth = {e: w.truth(e) for e in w.members}
    n_ent = len(w.members)
    sch = Schema(disjoint=set(w.disjoint), n_entities=n_ent + 2, n_categories=len(w.cats),
                 n_props=len(w.props))
    target_q = [(e, p, post_truth[e][p]) for e, p in target if p in post_truth.get(e, {})]
    return sch, obs, new, pre_truth, post_truth, target_q


def evaluate(mem, truth):
    q = [(e, p, v) for e, tr in truth.items() for p, v in tr.items() if p != "marked"]
    if not q:
        return float("nan")
    return sum(mem.answer(e, p, record_use=False) == v for e, p, v in q) / len(q)


def accuracy(mem, queries):
    if not queries:
        return float("nan")
    return sum(mem.answer(e, p, record_use=False) == v for e, p, v in queries) / len(queries)


def run_case(seed, kind, method):
    """method: 'lookup' | 'recency' | 'wms' | 'arlc' (v3-alapértelmezés) | 'v4'."""
    import time
    from .core import Memory
    from . import v4 as V4
    sch, obs, new, pre, post, tq = make_case(seed, kind)
    t0 = time.perf_counter()
    if method == "v4":
        with V4.configured({}):
            mem = Memory(sch, mode="arlc")
    else:
        mem = Memory(sch, mode=method)
    for o in obs:
        mem.observe(o)
    pre_acc = evaluate(mem, pre)
    t1 = time.perf_counter()
    for o in new:
        mem.observe(o)
    t_surprise = time.perf_counter() - t1
    return {"seed": seed, "kind": kind, "method": method, "pre_acc": pre_acc, "post_acc": evaluate(mem, post),
            "target_acc": accuracy(mem, tq), "n_target": len(tq), "seconds": time.perf_counter() - t0,
            "surprise_seconds": t_surprise}


METHODS = ("lookup", "recency", "wms", "arlc", "v4")
SEEDS = range(1000, 1030)
