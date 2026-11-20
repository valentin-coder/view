"""93. kör: negyedik, független benchmark-generátor (G4): forrásfüggőség és forrásváltozás.

A FROZEN_91 konfigurációt a generátor megírása ELŐTT befagyasztottam (91. kör, v4.FROZEN_91). A G4-en futtatott
eredmények egyetlen kapcsolót sem hangolhatnak.

Eltér az eddigiektől:
- **lapos kategóriarendszer** (nincs hierarchia, nincs diszjunktság), kis valódi kivételaránnyal;
- **négy terepforrás eltérő valódi megbízhatósággal** (0,97; 0,9; 0,8; 0,65), mind 0,9-et deklarál;
- meglepetések, amelyek a forrás-modell feltevéseit feszegetik:
  1. **visszhang:** egy hazug forrás és egy másoló, amely a hazug állításait ismétli (korrelált hibák; az ARLC a
     forrásokat függetlennek tekinti);
  2. **romló forrás:** a legjobb, régóta jelenlévő terepforrás hirtelen 60%-os hibaaránnyal jelent;
  3. **jó új specialista:** új forrás 0,99-es valódi megbízhatósággal, amely a leggyengébb terepforrás hibáit
     helyesbíti (a „gyanús új forrás” ára);
  4. **hazug forrás:** kontroll.
"""
from __future__ import annotations

import itertools
import random

from .core import Lit, Obs, Rule, Schema

KINDS4 = ("visszhang", "romló forrás", "jó új specialista", "hazug forrás")
KINDS4_EXTRA = ("bevált másoló", "független megerősítő")   # 111. kör: a függetlenségi feltevés próbája
FIELD_REL = {"f1": 0.97, "f2": 0.9, "f3": 0.8, "f4": 0.65}


class World4:
    def __init__(self, rng, n_cat=8, n_props=8, n_ent=30, rules_per_cat=3, exc_rate=0.02):
        self.cats = [f"K{i}" for i in range(n_cat)]
        self.props = [f"r{i}" for i in range(n_props)]
        self.rules = {c: {p: rng.random() < 0.5 for p in rng.sample(self.props, rules_per_cat)} for c in self.cats}
        self.members = {f"y{i}": rng.choice(self.cats) for i in range(n_ent)}
        self.exceptions = {}
        for e, c in self.members.items():
            if self.rules[c] and rng.random() < exc_rate * len(self.rules[c]):
                p = rng.choice(sorted(self.rules[c]))
                self.exceptions[e] = {p: not self.rules[c][p]}
        self.book_errors = set()
        self.reports = []            # (source, e, p, érték) a terepi jelentések

    def truth(self, e):
        res = dict(self.rules[self.members[e]])
        res.update(self.exceptions.get(e, {}))
        return res


def stream4(w: World4, rng, book_error=0.1, facts_per_ent=4):
    c = itertools.count(1)
    obs = []
    for cat, rs in w.rules.items():
        for p, v in rs.items():
            stated = v if rng.random() >= book_error else (not v)
            if stated != v:
                w.book_errors.add((cat, p))
            obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(cat, "has", p, stated)))
    t = 1
    for e in sorted(w.members):
        obs.append(Obs(next(c), "census", t, 0.99, lit=Lit("isa", e, w.members[e], True)))
        tr = w.truth(e)
        for p in rng.sample(sorted(tr), min(facts_per_ent, len(tr))):
            src = rng.choice(sorted(FIELD_REL))
            v = tr[p] if rng.random() < FIELD_REL[src] else (not tr[p])
            w.reports.append((src, e, p, v))
            obs.append(Obs(next(c), src, t, 0.9, lit=Lit("has", e, p, v)))
        t += 1
    return obs, c, t


def surprise4(kind, w: World4, rng, c, t):
    new, target = [], []
    ents = sorted(w.members)
    if kind in ("visszhang", "hazug forrás"):
        picks = []
        for e in rng.sample(ents, 8):
            p = rng.choice(sorted(w.truth(e)))
            picks.append((e, p))
            new.append(Obs(next(c), "liar", t, 0.9, lit=Lit("has", e, p, not w.truth(e)[p])))
            target.append((e, p))
        if kind == "visszhang":
            for e, p in picks:
                new.append(Obs(next(c), "echo", t, 0.9, lit=Lit("has", e, p, not w.truth(e)[p])))
            for e in rng.sample([x for x in ents if x not in {a for a, _ in picks}], 2):
                p = rng.choice(sorted(w.truth(e)))
                new.append(Obs(next(c), "echo", t, 0.9, lit=Lit("has", e, p, not w.truth(e)[p])))
                target.append((e, p))
    elif kind == "romló forrás":
        for e in rng.sample(ents, 10):
            p = rng.choice(sorted(w.truth(e)))
            v = w.truth(e)[p] if rng.random() >= 0.6 else (not w.truth(e)[p])
            new.append(Obs(next(c), "f1", t, 0.9, lit=Lit("has", e, p, v)))
            target.append((e, p))
    elif kind == "jó új specialista":
        wrong = [(e, p) for (s, e, p, v) in w.reports if v != w.truth(e).get(p)]
        rest = [(e, p) for e in ents for p in sorted(w.truth(e))]
        picks = sorted(set(rng.sample(wrong, min(5, len(wrong)))))
        for e, p in rng.sample(rest, 10 - len(picks)):
            if (e, p) not in picks:
                picks.append((e, p))
        for e, p in picks:
            v = w.truth(e)[p] if rng.random() < 0.99 else (not w.truth(e)[p])
            new.append(Obs(next(c), "spec", t, 0.9, lit=Lit("has", e, p, v)))
            target.append((e, p))
    elif kind in KINDS4_EXTRA:
        # 111. kör: a leggyengébb bevált terepforrás (f4) 10 jelentése, köztük (ha van) legfeljebb 5 hibás. A „másoló”
        # ugyanazt ismétli (korrelált hiba), a „független megerősítő” a valódi értéket közli ugyanazokra a kérdésekre.
        f4 = sorted({(e, p, v) for (src, e, p, v) in w.reports if src == "f4"})
        wrong = [x for x in f4 if x[2] != w.truth(x[0]).get(x[1])]
        right = [x for x in f4 if x[2] == w.truth(x[0]).get(x[1])]
        picks = rng.sample(wrong, min(5, len(wrong)))
        picks += rng.sample(right, min(10 - len(picks), len(right)))
        for e, p, v in picks:
            val = v if kind == "bevált másoló" else w.truth(e)[p]
            new.append(Obs(next(c), "mirror" if kind == "bevált másoló" else "indep", t, 0.9, lit=Lit("has", e, p, val)))
            target.append((e, p))
    return new, target


def make_case4(seed, kind):
    rng = random.Random(seed)
    w = World4(rng)
    obs, c, t = stream4(w, rng)
    pre = {e: w.truth(e) for e in w.members}
    new, target = surprise4(kind, w, rng, c, t + 1)
    post = {e: w.truth(e) for e in w.members}
    sch = Schema(disjoint=set(), n_entities=len(w.members) + 2, n_categories=len(w.cats), n_props=len(w.props))
    tq = [(e, p, post[e][p]) for e, p in target if p in post.get(e, {})]
    return sch, obs, new, pre, post, tq, w
