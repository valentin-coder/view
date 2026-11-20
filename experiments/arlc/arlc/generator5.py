"""116. kör: ötödik benchmark-generátor (G5): forrásfüggőségi hálózat a háttérben.

A FROZEN_115 konfigurációt a generátor megírása ELŐTT befagyasztottam (115. kör). A G5-ön mért eredmények egyetlen
kapcsolót sem hangolhatnak.

Eltér a G4-től: a forrásfüggőség nem csak a meglepetésben, hanem **a háttérfolyamban** van.
- lapos kategóriák (8, egyenként 3 szabállyal), kevés valódi kivétel;
- három eredeti terepforrás (o1: 0,95; o2: 0,85; o3: 0,7 valódi megbízhatóság);
- **c1:** az o3 részleges másolója (jelentései 80%-a az o3 egy jelentésének szó szerinti másolata, a többi független, 0,9);
- **c2:** a c1 teljes másolója (lánc: o3 → c1 → c2);
- minden forrás 0,9-et deklarál.
Meglepetések:
  1. **részleges új másoló:** új forrás, 10 állításának fele az o3 jelentéseiből (a hibásakat előnyben részesítve), fele
     független valódi érték;
  2. **jó forrás visszhangja:** új forrás az o1 10 jelentését ismétli (ártalmatlan egyezés);
  3. **hazug forrás:** kontroll.
"""
from __future__ import annotations

import itertools
import random

from .core import Lit, Obs, Rule, Schema

KINDS5 = ("részleges új másoló", "jó forrás visszhangja", "hazug forrás")
ORIG = {"o1": 0.95, "o2": 0.85, "o3": 0.7}


class World5:
    def __init__(self, rng, n_cat=8, n_props=8, n_ent=30, rules_per_cat=3, exc_rate=0.02):
        self.cats = [f"K{i}" for i in range(n_cat)]
        self.props = [f"r{i}" for i in range(n_props)]
        self.rules = {c: {p: rng.random() < 0.5 for p in rng.sample(self.props, rules_per_cat)} for c in self.cats}
        self.members = {f"z{i}": rng.choice(self.cats) for i in range(n_ent)}
        self.exceptions = {}
        for e, c in self.members.items():
            if self.rules[c] and rng.random() < exc_rate * len(self.rules[c]):
                p = rng.choice(sorted(self.rules[c]))
                self.exceptions[e] = {p: not self.rules[c][p]}
        self.book_errors = set()
        self.reports = []            # (forrás, e, p, érték)

    def truth(self, e):
        res = dict(self.rules[self.members[e]])
        res.update(self.exceptions.get(e, {}))
        return res


def stream5(w: World5, rng, book_error=0.1, facts_per_ent=3):
    c = itertools.count(1)
    obs = []
    for cat, rs in w.rules.items():
        for p, v in rs.items():
            stated = v if rng.random() >= book_error else (not v)
            if stated != v:
                w.book_errors.add((cat, p))
            obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(cat, "has", p, stated)))
    t = 1
    o3_reports = []
    for e in sorted(w.members):
        obs.append(Obs(next(c), "census", t, 0.99, lit=Lit("isa", e, w.members[e], True)))
        tr = w.truth(e)
        for p in rng.sample(sorted(tr), min(facts_per_ent, len(tr))):
            src = rng.choice(sorted(ORIG))
            v = tr[p] if rng.random() < ORIG[src] else (not tr[p])
            w.reports.append((src, e, p, v))
            obs.append(Obs(next(c), src, t, 0.9, lit=Lit("has", e, p, v)))
            if src == "o3":
                o3_reports.append((e, p, v))
        # c1: az eddigi o3-jelentések 80%-ban másolata, egyébként független
        if rng.random() < 0.6:
            if o3_reports and rng.random() < 0.8:
                e2, p2, v2 = rng.choice(o3_reports)
            else:
                e2 = rng.choice(sorted(w.members))
                p2 = rng.choice(sorted(w.truth(e2)))
                v2 = w.truth(e2)[p2] if rng.random() < 0.9 else (not w.truth(e2)[p2])
            for src in ("c1", "c2"):            # c2 a c1 teljes másolója
                w.reports.append((src, e2, p2, v2))
                obs.append(Obs(next(c), src, t, 0.9, lit=Lit("has", e2, p2, v2)))
        t += 1
    return obs, c, t


def surprise5(kind, w: World5, rng, c, t):
    new, target = [], []
    ents = sorted(w.members)
    if kind == "részleges új másoló":
        o3 = sorted({(e, p, v) for (s, e, p, v) in w.reports if s == "o3"})
        wrong = [x for x in o3 if x[2] != w.truth(x[0]).get(x[1])]
        picks = rng.sample(wrong, min(5, len(wrong)))
        picks += rng.sample([x for x in o3 if x not in picks], min(5 - len(picks), len(o3) - len(picks)))
        for e, p, v in picks:
            new.append(Obs(next(c), "partial", t, 0.9, lit=Lit("has", e, p, v)))
            target.append((e, p))
        for e in rng.sample(ents, 5):
            p = rng.choice(sorted(w.truth(e)))
            new.append(Obs(next(c), "partial", t, 0.9, lit=Lit("has", e, p, w.truth(e)[p])))
            target.append((e, p))
    elif kind == "jó forrás visszhangja":
        o1 = sorted({(e, p, v) for (s, e, p, v) in w.reports if s == "o1"})
        for e, p, v in rng.sample(o1, min(10, len(o1))):
            new.append(Obs(next(c), "echo1", t, 0.9, lit=Lit("has", e, p, v)))
            target.append((e, p))
    elif kind == "hazug forrás":
        for e in rng.sample(ents, 8):
            p = rng.choice(sorted(w.truth(e)))
            new.append(Obs(next(c), "liar", t, 0.9, lit=Lit("has", e, p, not w.truth(e)[p])))
            target.append((e, p))
    return new, target


def make_case5(seed, kind):
    rng = random.Random(seed)
    w = World5(rng)
    obs, c, t = stream5(w, rng)
    pre = {e: w.truth(e) for e in w.members}
    new, target = surprise5(kind, w, rng, c, t + 1)
    post = {e: w.truth(e) for e in w.members}
    sch = Schema(disjoint=set(), n_entities=len(w.members) + 2, n_categories=len(w.cats), n_props=len(w.props))
    tq = [(e, p, post[e][p]) for e, p in target if p in post.get(e, {})]
    return sch, obs, new, pre, post, tq, w
