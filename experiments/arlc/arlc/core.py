"""ARLC v3 szimbolikus mag (15. kör specifikációja).

Feltevés-alapú revízió MDL-pontszámmal, kivételekkel, forrás-kontextusokkal,
frissítés (vágás) operátorral, indukcióval és B elemű nyalábbal. Gradiens és LLM nincs:
a bemenet orákulum-literál (opcionálisan mesterséges zajjal).
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
from itertools import combinations
from typing import Iterable, Optional

IND_BASE = 10 ** 6


@dataclass(frozen=True)
class Lit:
    pred: str          # 'isa' | 'has'
    subj: str
    obj: str
    pos: bool = True


@dataclass(frozen=True)
class Rule:
    body: str          # isa(X, body) ->
    pred: str          # 'isa' | 'has'
    obj: str
    pos: bool = True


@dataclass(frozen=True)
class Obs:
    id: int
    source: str
    time: int
    q: float
    lit: Optional[Lit] = None
    rule: Optional[Rule] = None


@dataclass
class Schema:
    disjoint: set = field(default_factory=set)          # frozenset({c1, c2})
    groups: dict = field(default_factory=dict)          # prop -> group
    update_prior: dict = field(default_factory=dict)    # group|'isa' -> pi
    n_entities: int = 10
    n_categories: int = 5
    n_props: int = 10


@dataclass(frozen=True)
class Hyp:
    rej: frozenset = frozenset()
    exc: frozenset = frozenset()
    iso: frozenset = frozenset()
    cut: tuple = ()           # ((obs_id, end_time), ...) rendezve
    ind: tuple = ()           # indukált Obs-ok

    def key(self):
        return (self.rej, self.exc, self.iso, self.cut, tuple(o.rule for o in self.ind))


@dataclass
class Closure:
    isa: dict      # e -> {(c, pos): support}
    has: dict      # e -> {(p, pos): support}
    ruled: dict    # e -> set((p, pos)) szabályból levezetett has-literálok
    conflict: Optional[frozenset] = None


MODES = ("lookup", "recency", "wms", "arlc", "arlc-nocut", "arlc-noctx", "arlc-noexc")


class Memory:
    def __init__(self, schema: Schema, mode: str = "arlc", beam: int = 8, depth: int = 3,
                 eta: float = 0.0, delta: float = 0.05, c_ctx: float = 6.0,
                 induce: bool = True, induce_min: int = 3, use_decay: float = 1.0):
        assert mode in MODES, mode
        self.s, self.mode, self.B, self.depth = schema, mode, beam, depth
        self.eta, self.delta, self.c_ctx = eta, delta, c_ctx
        self.induce_on = induce and mode.startswith("arlc")
        self.induce_min = induce_min
        self.use_decay = use_decay
        self.obs: list[Obs] = []
        self.by_id: dict[int, Obs] = {}
        self.beam: list[Hyp] = [Hyp()]
        self.now = 0
        self.uses: Counter = Counter()
        self._ccache: dict = {}
        self._ind_counter = 0
        self.events: list[dict] = []

    # ------------------------------------------------------------ helpers
    @property
    def best(self) -> Hyp:
        return self.beam[0]

    def _get(self, oid: int, H: Hyp) -> Obs:
        if oid >= IND_BASE:
            for o in H.ind:
                if o.id == oid:
                    return o
        return self.by_id[oid]

    def _mutable(self, o: Obs) -> bool:
        """Változó csoportú tény a megfigyelés idejétől érvényes; a többi tény időtlen."""
        return o.lit is not None and self.s.update_prior.get(self._group(o.lit), 0.0) >= 0.01

    def _group(self, lit: Lit) -> Optional[str]:
        return "isa" if lit.pred == "isa" else self.s.groups.get(lit.obj)

    # ------------------------------------------------------------ closure
    def closure(self, H: Hyp, ctx: Optional[str], t: int, use_rules: bool = True) -> Closure:
        key = (H.key(), ctx, t, use_rules, len(self.obs))
        if key in self._ccache:
            return self._ccache[key]
        cut = dict(H.cut)
        rules, facts = [], []
        for o in list(self.obs) + list(H.ind):
            if o.id in H.rej:
                continue
            if o.time > t and (o.rule is not None or self._mutable(o)):
                continue
            if o.id in cut and t >= cut[o.id]:
                continue
            if o.source in H.iso and o.source != ctx:
                continue
            (rules if o.rule else facts).append(o)
        isa: dict = defaultdict(dict)
        has: dict = defaultdict(dict)
        ruled: dict = defaultdict(set)
        for o in sorted(facts, key=lambda o: (-o.time, o.id)):   # a legfrissebb támasz elöl
            l = o.lit
            tok = frozenset([("obs", o.id)])
            (isa if l.pred == "isa" else has)[l.subj].setdefault((l.obj, l.pos), tok)
        if use_rules:
            by_body = defaultdict(list)
            for r in rules:
                by_body[r.rule.body].append(r)
            for e in list(isa.keys()):
                queue = [c for (c, pos) in isa[e] if pos]
                seen = set(queue)
                while queue:
                    c = queue.pop(0)
                    base = isa[e][(c, True)]
                    for ro in by_body.get(c, []):
                        if (ro.id, e) in H.exc:
                            continue
                        sup = base | {("obs", ro.id), ("inst", ro.id, e)}
                        r = ro.rule
                        k = (r.obj, r.pos)
                        if r.pred == "isa":
                            isa[e].setdefault(k, sup)
                            if r.pos and r.obj not in seen:
                                seen.add(r.obj)
                                queue.append(r.obj)
                        else:
                            has[e].setdefault(k, sup)
                            ruled[e].add(k)
        cl = Closure(isa, has, ruled)
        cl.conflict = self._rule_conflict(rules) or self._conflict(cl)
        self._ccache[key] = cl
        return cl

    def _rule_conflict(self, rules: list) -> Optional[frozenset]:
        """Azonos törzsű és fejű, ellentétes előjelű szabályok közvetlenül ütköznek."""
        seen = {}
        for o in rules:
            r = o.rule
            k = (r.body, r.pred, r.obj)
            if k in seen and seen[k].rule.pos != r.pos:
                return frozenset([("obs", seen[k].id), ("obs", o.id)])
            seen.setdefault(k, o)
        return None

    def _conflict(self, cl: Closure) -> Optional[frozenset]:
        for e, d in cl.isa.items():
            for (c, pos), sup in d.items():
                if pos and (c, False) in d:
                    return sup | d[(c, False)]
            pos_c = [(c, sup) for (c, pos), sup in d.items() if pos]
            for (c1, s1), (c2, s2) in combinations(pos_c, 2):
                if frozenset((c1, c2)) in self.s.disjoint:
                    return s1 | s2
        for e, d in cl.has.items():
            by_group = defaultdict(list)
            for (p, pos), sup in d.items():
                if pos and (p, False) in d:
                    return sup | d[(p, False)]
                g = self.s.groups.get(p)
                if pos and g is not None:
                    by_group[g].append(sup)
            for g, sups in by_group.items():
                if len(sups) > 1:
                    return sups[0] | sups[1]
        return None

    def contexts(self, H: Hyp) -> list[Optional[str]]:
        return [None] + sorted(H.iso)

    def find_conflict(self, H: Hyp) -> Optional[frozenset]:
        times = {self.now} | {end - 1 for (_, end) in H.cut if end - 1 >= 0}
        for ctx in self.contexts(H):
            for t in sorted(times, reverse=True):
                c = self.closure(H, ctx, t).conflict
                if c is not None:
                    return c
        return None

    # ------------------------------------------------------------ score
    def score(self, H: Hyp) -> float:
        if self.mode == "wms":
            return sum(math.log2(self.by_id[i].q / (1 - self.by_id[i].q)) for i in H.rej)
        bits = 0.0
        has_cut = bool(H.cut)
        for o in self.obs:
            if o.id in H.rej:
                bits += -math.log2(1 - o.q)
                if o.lit is not None and o.lit.pred == "has":
                    bits += 1.0
                continue
            bits += -math.log2(o.q)
            if o.lit is not None and o.lit.pred == "has":
                ctx = o.source if o.source in H.iso else None
                cl = self.closure(H, ctx, o.time if has_cut else self.now)
                pred = (o.lit.obj, o.lit.pos) in cl.ruled.get(o.lit.subj, ())
                bits += -math.log2(1 - self.delta) if pred else 1.0
        bits += len(H.exc) * math.log2(max(2, self.s.n_entities))
        bits += len(H.iso) * self.c_ctx
        for oid, _ in H.cut:
            g = self._group(self.by_id[oid].lit)
            bits += -math.log2(self.s.update_prior.get(g, 1e-3))
        bits += len(H.ind) * math.log2(max(2, 2 * self.s.n_categories * self.s.n_props))
        if self.eta:
            bits += self.eta * sum(n for tok, n in self.uses.items() if self._lost(tok, H))
        return bits

    def _lost(self, tok, H: Hyp) -> bool:
        if tok[0] == "obs":
            return tok[1] in H.rej or (tok[1] >= IND_BASE and all(o.id != tok[1] for o in H.ind))
        if tok[0] == "inst":
            return (tok[1], tok[2]) in H.exc or tok[1] in H.rej
        return False

    # ------------------------------------------------------------ repair
    def _mods(self, H: Hyp, conflict: frozenset) -> Iterable[Hyp]:
        full = self.mode.startswith("arlc")
        obs_in = [self._get(t[1], H) for t in conflict if t[0] == "obs"]
        for tok in sorted(conflict, key=str):
            if tok[0] == "obs":
                o = self._get(tok[1], H)
                if o.id >= IND_BASE:
                    yield replace(H, ind=tuple(x for x in H.ind if x.id != o.id))
                    continue
                if o.q < 1.0:
                    yield replace(H, rej=H.rej | {o.id})
                if full and self.mode != "arlc-noctx" and o.source not in H.iso:
                    yield replace(H, iso=H.iso | {o.source})
                if full and self.mode != "arlc-nocut" and o.lit is not None:
                    g = self._group(o.lit)
                    if self.s.update_prior.get(g, 0) > 0:
                        later = [x.time for x in obs_in if x.lit is not None and x.lit.subj == o.lit.subj
                                 and self._group(x.lit) == g and x.time > o.time]
                        if later and o.id not in dict(H.cut):
                            yield replace(H, cut=tuple(sorted(H.cut + ((o.id, min(later)),))))
            elif tok[0] == "inst" and full and self.mode != "arlc-noexc":
                yield replace(H, exc=H.exc | {(tok[1], tok[2])})

    def _repair(self, H: Hyp, depth: int, seen: set) -> list[Hyp]:
        k = H.key()
        if k in seen:
            return []
        seen.add(k)
        c = self.find_conflict(H)
        if c is None:
            return [H]
        if depth == 0:
            g = self._greedy(H)
            return [] if g is None else [g]
        out = []
        for H2 in self._mods(H, c):
            out.extend(self._repair(H2, depth - 1, seen))
        return out

    def _greedy(self, H: Hyp, max_steps: int = 80) -> Optional[Hyp]:
        """Mohó befejezés: a maradék konfliktusokat egyenként, a legolcsóbb lépéssel oldja fel."""
        for _ in range(max_steps):
            c = self.find_conflict(H)
            if c is None:
                return H
            opts = list(self._mods(H, c))
            if not opts:
                return None
            H = min(opts, key=self.score)
        return None

    def _recency_repair(self, H: Hyp) -> Hyp:
        for _ in range(50):
            c = self.find_conflict(H)
            if c is None:
                return H
            olds = [self._get(t[1], H) for t in c if t[0] == "obs" and t[1] < IND_BASE]
            olds = [o for o in olds if o.q < 1.0]
            if not olds:
                break
            victim = min(olds, key=lambda o: (o.time, o.id))
            H = replace(H, rej=H.rej | {victim.id})
        return H

    def _reinstate(self, H: Hyp) -> Hyp:
        """Anytime-javítás: korábban elutasított megfigyelések / kivételek / elszigetelések
        visszavétele, ha konzisztens marad és a pontszám csökken."""
        improved = True
        cur = self.score(H)
        while improved:
            improved = False
            moves = [replace(H, rej=H.rej - {i}) for i in sorted(H.rej)]
            moves += [replace(H, exc=H.exc - {x}) for x in sorted(H.exc)]
            moves += [replace(H, iso=H.iso - {s}) for s in sorted(H.iso)]
            for H2 in moves:
                if self.find_conflict(H2) is None:
                    sc = self.score(H2)
                    if sc < cur - 1e-9:
                        H, cur, improved = H2, sc, True
                        break
        return H

    # ------------------------------------------------------------ induction
    def _induce(self, H: Hyp, subj: str) -> list[Hyp]:
        cl = self.closure(H, None, self.now)
        cats = [c for (c, pos) in cl.isa.get(subj, {}) if pos]
        out = []
        for c in cats:
            members = [e for e, d in cl.isa.items() if (c, True) in d]
            if len(members) < self.induce_min:
                continue
            existing = {(o.rule.obj, o.rule.pos) for o in list(self.obs) + list(H.ind)
                        if o.rule and o.rule.body == c and o.id not in H.rej}
            votes: Counter = Counter()
            for e in members:
                for (p, pos), sup in cl.has.get(e, {}).items():
                    if (p, pos) not in cl.ruled.get(e, ()):
                        votes[(p, pos)] += 1
            for (p, pos), n in votes.items():
                if n >= self.induce_min and votes.get((p, not pos), 0) == 0 and (p, pos) not in existing \
                        and (p, not pos) not in existing:
                    self._ind_counter += 1
                    o = Obs(IND_BASE + self._ind_counter, "__induced__", self.now, 1.0,
                            rule=Rule(c, "has", p, pos))
                    H2 = replace(H, ind=H.ind + (o,))
                    if self.find_conflict(H2) is None:
                        out.append(H2)
        return out

    # ------------------------------------------------------------ public API
    def observe(self, o: Obs) -> dict:
        self._ccache.clear()
        if self.use_decay < 1.0:
            for k in list(self.uses):
                self.uses[k] *= self.use_decay
        self.obs.append(o)
        self.by_id[o.id] = o
        self.now = max(self.now, o.time)
        prev = self.best
        if self.mode == "lookup":
            return {}
        if self.mode == "recency":
            self.beam = [self._recency_repair(self.best)]
            return self._event(prev, self.best, o)
        cands: dict = {}
        seen: set = set()
        for H in self.beam:
            for H2 in self._repair(H, self.depth, seen):
                cands[H2.key()] = H2
        if not cands:
            for H in self.beam:
                H2 = replace(H, rej=H.rej | {o.id})
                if self.find_conflict(H2) is None:
                    cands[H2.key()] = H2
        if self.induce_on and o.lit is not None:
            for H in sorted(cands.values(), key=self.score)[:2]:
                for H3 in self._induce(H, o.lit.subj):
                    cands[H3.key()] = H3
        ranked = sorted({h.key(): h for h in (self._reinstate(h) for h in cands.values())}.values(),
                        key=lambda h: (self.score(h), len(h.rej) + len(h.exc) + len(h.iso) + len(h.cut)))
        self.beam = ranked[: self.B] if ranked else self.beam
        return self._event(prev, self.best, o)

    def _event(self, prev: Hyp, new: Hyp, o: Obs) -> dict:
        ev = {
            "t": o.time, "obs": o.id,
            "rejected_old": sorted(i for i in new.rej - prev.rej if i != o.id),
            "new_rejected": o.id in new.rej,
            "rules_dropped": sorted(i for i in new.rej - prev.rej if self.by_id[i].rule is not None)
            + [x.id for x in prev.ind if x not in new.ind],
            "exc_added": sorted(new.exc - prev.exc),
            "iso_added": sorted(new.iso - prev.iso),
            "cut_added": sorted(set(new.cut) - set(prev.cut)),
            "ind_added": [(x.rule.body, x.rule.obj, x.rule.pos) for x in new.ind if x not in prev.ind],
        }
        self.events.append(ev)
        return ev

    def answer(self, e: str, p: str, ctx: Optional[str] = None, t: Optional[int] = None,
               record_use: bool = True) -> Optional[bool]:
        return self._ans("has", e, p, ctx, t, record_use)

    def answer_isa(self, e: str, c: str, ctx: Optional[str] = None, t: Optional[int] = None,
                   record_use: bool = False) -> Optional[bool]:
        return self._ans("isa", e, c, ctx, t, record_use)

    def _ans(self, pred, e, x, ctx, t, record_use):
        H = self.best
        t = self.now if t is None else t
        if self.mode == "lookup":
            best = None
            for o in self.obs:
                if o.lit and o.lit.pred == pred and o.lit.subj == e and o.lit.obj == x and o.time <= t:
                    if best is None or o.time >= best.time:
                        best = o
            return None if best is None else best.lit.pos
        cl = self.closure(H, ctx if ctx in H.iso else None, t)
        d = (cl.isa if pred == "isa" else cl.has).get(e, {})
        pos, neg = d.get((x, True)), d.get((x, False))
        if pos is not None and neg is None:
            ans, sup = True, pos
        elif neg is not None and pos is None:
            ans, sup = False, neg
        else:
            return None
        if record_use and self.eta:
            for tok in sup:
                self.uses[tok] += 1
        return ans
