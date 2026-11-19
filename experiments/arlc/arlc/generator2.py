"""77. kör: egy második, független benchmark-generátor (kereszt-osztályozás).

Eltér a 44. kör generátorától (procedural.py):
- **nincs hierarchia:** minden entitás F családból egy-egy kategóriába tartozik (kereszt-osztályozás); a kategóriák
  szabályai ütközhetnek, és az igazságot egy *rejtett* családprioritás dönti el (az ARLC ezt nem ismeri);
- **rosszul kalibrált források:** két terepforrás, mindkettő deklarált hitelessége 0,9, a valódi 0,97, illetve 0,8;
- **torzított forrás:** egy „optimista” forrás minden általa jelentett tényt igaznak mond;
- meglepetések: hazug forrás; tankönyvi szabály helyesbítése; egy rejtett-prioritású ütközés feloldását mutató
  szakértői szabály; a torzított forrás tömeges jelentése.
Az elemzési terv és a hipotézisek a docs/korok/77-masodik-generator.md-ben vannak, a futtatás előtt rögzítve.
"""
from __future__ import annotations

import itertools
import random

from .core import Lit, Obs, Rule, Schema

KINDS2 = ("hazug forrás", "szabály-helyesbítés", "prioritás-szakértő", "torzított forrás")


class World2:
    def __init__(self, rng, n_fam=3, n_per_fam=3, n_props=8, n_ent=30, rules_per_cat=2, book_error=0.1):
        self.fams = [[f"F{f}c{k}" for k in range(n_per_fam)] for f in range(n_fam)]
        self.cats = [c for fam in self.fams for c in fam]
        self.props = [f"q{i}" for i in range(n_props)]
        self.rules = {c: {p: rng.random() < 0.5 for p in rng.sample(self.props, rules_per_cat)} for c in self.cats}
        self.members = {f"x{i}": [rng.choice(fam) for fam in self.fams] for i in range(n_ent)}
        self.priority = list(range(n_fam))
        rng.shuffle(self.priority)                      # rejtett családprioritás
        self.book_errors = set()
        self.book_error = book_error

    def truth(self, e):
        res = {}
        cats = self.members[e]
        for p in self.props:
            for f in self.priority:                     # a legmagasabb prioritású család dönt
                c = cats[f]
                if p in self.rules[c]:
                    res[p] = self.rules[c][p]
                    break
        return res


def stream2(w: World2, rng, facts_per_ent=4):
    c = itertools.count(1)
    obs = []
    for cat, rs in w.rules.items():
        for p, v in rs.items():
            stated = v if rng.random() >= w.book_error else (not v)
            if stated != v:
                w.book_errors.add((cat, p))
            obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(cat, "has", p, stated)))
    t = 1
    for e, cats in w.members.items():
        for cat in cats:
            obs.append(Obs(next(c), "census", t, 0.95, lit=Lit("isa", e, cat, True)))
        tr = w.truth(e)
        for p in rng.sample(sorted(tr), min(facts_per_ent, len(tr))):
            src, rel = ("fieldA", 0.97) if rng.random() < 0.5 else ("fieldB", 0.8)
            v = tr[p] if rng.random() < rel else (not tr[p])
            obs.append(Obs(next(c), src, t, 0.9, lit=Lit("has", e, p, v)))       # mindkettő 0,9-et deklarál
        t += 1
    return obs, c, t


def surprise2(kind, w: World2, rng, c, t):
    new, target = [], []
    if kind == "hazug forrás":
        for e in rng.sample(sorted(w.members), 8):
            tr = w.truth(e)
            if tr:
                p = rng.choice(sorted(tr))
                new.append(Obs(next(c), "liar", t, 0.9, lit=Lit("has", e, p, not tr[p])))
                target.append((e, p))
    elif kind == "szabály-helyesbítés":
        if w.book_errors:
            cat, p = rng.choice(sorted(w.book_errors))
        else:
            cat = rng.choice(w.cats); p = rng.choice(sorted(w.rules[cat]))
        new.append(Obs(next(c), "review", t, 0.995, rule=Rule(cat, "has", p, w.rules[cat][p])))
        target = [(e, p) for e, cats in w.members.items() if cat in cats and p in w.truth(e)]
    elif kind == "prioritás-szakértő":
        # egy szakértő a rejtett prioritás szerint helyes értékeket közli azokra a tagokra, ahol két család ütközik
        conflicts = []
        for e, cats in w.members.items():
            tr = w.truth(e)
            for p, v in tr.items():
                vals = {w.rules[c][p] for c in cats if p in w.rules[c]}
                if len(vals) > 1:
                    conflicts.append((e, p, v))
        for e, p, v in rng.sample(conflicts, min(8, len(conflicts))):
            new.append(Obs(next(c), "expert", t, 0.95, lit=Lit("has", e, p, v)))
            target.append((e, p))
    elif kind == "torzított forrás":
        for e in rng.sample(sorted(w.members), 10):
            tr = w.truth(e)
            falses = [p for p, v in tr.items() if v is False]
            if falses:
                p = rng.choice(falses)
                new.append(Obs(next(c), "optimist", t, 0.9, lit=Lit("has", e, p, True)))
                target.append((e, p))
    return new, target


def make_case2(seed, kind):
    rng = random.Random(seed)
    w = World2(rng)
    obs, c, t = stream2(w, rng)
    pre = {e: w.truth(e) for e in w.members}
    new, target = surprise2(kind, w, rng, c, t + 1)
    post = {e: w.truth(e) for e in w.members}
    sch = Schema(disjoint=set(), n_entities=len(w.members) + 2, n_categories=len(w.cats), n_props=len(w.props))
    tq = [(e, p, post[e][p]) for e, p in target if p in post.get(e, {})]
    return sch, obs, new, pre, post, tq
