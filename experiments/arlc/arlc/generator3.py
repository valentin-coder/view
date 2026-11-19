"""88. kör: harmadik, független benchmark-generátor (G3): időben változó világ.

A konfigurációt (v4.9+PK, illetve a 86. kör döntése szerinti változatát) a generátor megírása ELŐTT befagyasztottam
(docs/korok/88-befagyasztas-es-g3.md); a G3-on futtatott eredmények egyik kapcsolót sem hangolják.

Eltér a G1-től és a G2-től:
- **változó állapot:** minden entitásnak van egy állapota (st0, st1, st2; kölcsönösen kizárók, változó csoport). Az
  entitások egy része a folyam közben állapotot vált; a terepforrás különböző időpontokban jelenti az aktuálisat;
- **a világ szabálya is változhat:** egy kategória egy szabálya egy τ időpontban megfordul (nem tankönyvhiba, hanem
  valódi változás);
- **elavult forrás:** egy archívum a mostani időbélyeggel régi állapotokat közöl;
- **kalibrált források:** a deklarált hitelesség megegyezik a valódival (a 87. kör G1k-tanulsága miatt);
- **történeti kérdések:** az értékelés a τ előtti állapotra is kérdez (t = τ − 1).
Hierarchia: két csúcs (nem diszjunktak), hat levél, egy szülővel; így a világ a sémával mindig konzisztens.
"""
from __future__ import annotations

import itertools
import random

from .core import Lit, Obs, Rule, Schema

KINDS3 = ("állapotváltozás", "szabályváltozás", "elavult forrás", "hazug forrás")
STATES = ("st0", "st1", "st2")


class World3:
    def __init__(self, rng, n_leaf=6, n_props=6, n_ent=30, rules_per_cat=2, exc_rate=0.02, change_rate=0.3, T=30):
        self.tops = ["T0", "T1"]
        self.leaves = [f"L{i}" for i in range(n_leaf)]
        self.parent = {l: rng.choice(self.tops) for l in self.leaves}
        self.cats = self.tops + self.leaves
        self.props = [f"s{i}" for i in range(n_props)]
        self.rules = {c: {p: rng.random() < 0.5 for p in rng.sample(self.props, rules_per_cat)} for c in self.cats}
        self.rule_changes = {}                 # (c, p) -> (τ, új érték)
        self.members = {f"x{i}": rng.choice(self.leaves) for i in range(n_ent)}
        self.exceptions = {}
        for e in self.members:
            tr = self.static_truth(e, 0)
            if tr and rng.random() < exc_rate * n_props:
                p = rng.choice(sorted(tr))
                self.exceptions[e] = {p: not tr[p]}
        # állapot-pályák: [(kezdő idő, állapot), ...]
        self.state = {}
        for e in self.members:
            s0 = rng.choice(STATES)
            traj = [(0, s0)]
            if rng.random() < change_rate:
                traj.append((rng.randint(5, T), rng.choice([s for s in STATES if s != s0])))
            self.state[e] = traj
        self.book_errors = set()

    def rule_value(self, c, p, t):
        v = self.rules[c].get(p)
        ch = self.rule_changes.get((c, p))
        if v is not None and ch is not None and t >= ch[0]:
            v = ch[1]
        return v

    def static_truth(self, e, t):
        leaf = self.members[e]
        res = {}
        for p in self.props:
            v = self.rule_value(leaf, p, t)
            if v is None:
                v = self.rule_value(self.parent[leaf], p, t)
            if v is not None:
                res[p] = v
        for p, v in self.exceptions.get(e, {}).items():
            res[p] = v
        return res

    def state_at(self, e, t):
        s = None
        for t0, st in self.state[e]:
            if t0 <= t:
                s = st
        return s

    def truth(self, e, t):
        res = self.static_truth(e, t)
        res[self.state_at(e, t)] = True
        return res


def stream3(w: World3, rng, book_error=0.1, field_noise=0.1, facts_per_ent=3, T=30):
    c = itertools.count(1)
    obs = []
    for l in w.leaves:
        obs.append(Obs(next(c), "book", 0, 0.95, rule=Rule(l, "isa", w.parent[l], True)))
    for cat, rs in w.rules.items():
        for p, v in rs.items():
            stated = v if rng.random() >= book_error else (not v)
            if stated != v:
                w.book_errors.add((cat, p))
            obs.append(Obs(next(c), "book", 0, 1 - book_error / 2, rule=Rule(cat, "has", p, stated)))
    ents = sorted(w.members)
    for i, e in enumerate(ents):
        t = 1 + i * T // len(ents)
        obs.append(Obs(next(c), "census", t, 0.99, lit=Lit("isa", e, w.members[e], True)))
        tr = w.static_truth(e, t)
        for p in rng.sample(sorted(tr), min(facts_per_ent, len(tr))):
            v = tr[p] if rng.random() >= field_noise else (not tr[p])
            obs.append(Obs(next(c), "field", t, 1 - field_noise, lit=Lit("has", e, p, v)))
        for ts in sorted({t, rng.randint(t, T)}):
            obs.append(Obs(next(c), "field", ts, 1 - field_noise, lit=Lit("has", e, w.state_at(e, ts), True)))
    obs.sort(key=lambda o: (o.time, o.id))
    return obs, c, T + 1


def surprise3(kind, w: World3, rng, c, tau):
    """(új megfigyelések, célkérdések [(e, p)], történeti kérdések [(e, p)] a τ − 1 időpontra)"""
    new, target, htarget = [], [], []
    ents = sorted(w.members)
    if kind == "állapotváltozás":
        for e in rng.sample(ents, 6):
            old = w.state_at(e, tau - 1)
            ns = rng.choice([s for s in STATES if s != old])
            w.state[e].append((tau, ns))
            new.append(Obs(next(c), "field", tau, 0.9, lit=Lit("has", e, ns, True)))
            target.append((e, ns))
            htarget.append((e, old))
    elif kind == "szabályváltozás":
        cands = [(l, p) for l in w.leaves for p in w.rules[l] if any(m == l for m in w.members.values())]
        cat, p = rng.choice(sorted(cands))
        w.rule_changes[(cat, p)] = (tau, not w.rules[cat][p])
        new.append(Obs(next(c), "review", tau, 0.995, rule=Rule(cat, "has", p, not w.rules[cat][p])))
        mem = [e for e in ents if w.members[e] == cat and p not in w.exceptions.get(e, {})]
        for e in rng.sample(mem, min(4, len(mem))):
            new.append(Obs(next(c), "field", tau, 0.9, lit=Lit("has", e, p, w.static_truth(e, tau)[p])))
        target = [(e, p) for e in mem]
        htarget = list(target)
    elif kind == "elavult forrás":
        changed = [e for e in ents if len(w.state[e]) > 1]
        for e in rng.sample(changed, min(6, len(changed))):
            new.append(Obs(next(c), "archive", tau, 0.9, lit=Lit("has", e, w.state[e][0][1], True)))
            target.append((e, w.state_at(e, tau)))
            htarget.append((e, w.state_at(e, tau - 1)))
    elif kind == "hazug forrás":
        for e in rng.sample(ents, 8):
            tr = w.static_truth(e, tau)
            if tr:
                p = rng.choice(sorted(tr))
                new.append(Obs(next(c), "liar", tau, 0.9, lit=Lit("has", e, p, not tr[p])))
                target.append((e, p))
                htarget.append((e, p))
    return new, target, htarget


def make_case3(seed, kind):
    """(séma, megfigyelések, meglepetés, pre-igazság, post-igazság, célkérdések, történeti kérdések, τ)"""
    rng = random.Random(seed)
    w = World3(rng)
    obs, c, tau = stream3(w, rng)
    pre = {e: w.truth(e, tau - 1) for e in w.members}
    new, target, htarget = surprise3(kind, w, rng, c, tau)
    post = {e: w.truth(e, tau) for e in w.members}
    hist = {e: w.truth(e, tau - 1) for e in w.members}
    sch = Schema(disjoint=set(), groups={s: "status" for s in STATES}, update_prior={"status": 0.05},
                 n_entities=len(w.members) + 2, n_categories=len(w.cats), n_props=len(w.props) + len(STATES))
    tq = [(e, p, post[e][p]) for e, p in target if p in post.get(e, {})]
    hq = [(e, p, hist[e][p]) for e, p in htarget if p in hist.get(e, {})]
    return sch, obs, new, pre, post, tq, hq, tau, w
