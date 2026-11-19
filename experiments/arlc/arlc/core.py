"""ARLC v3 szimbolikus mag (15. kör specifikációja).

Feltevés-alapú revízió MDL-pontszámmal, kivételekkel, forrás-kontextusokkal,
frissítés (vágás) operátorral, indukcióval és B elemű nyalábbal. Gradiens és LLM nincs:
a bemenet orákulum-literál (opcionálisan mesterséges zajjal).
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field, fields, replace as _dc_replace
from itertools import combinations
from typing import Iterable, Optional

IND_BASE = 10 ** 6
CLOSURE_CACHE_MAX = 15000   # 30 entitásnál bejegyzésenként kb. 50–150 kB


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
    cond: Optional[tuple] = None   # második feltétel: (tulajdonság, előjel) explicit tényként (30. kör)


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
        k = self.__dict__.get("_key")
        if k is None:
            k = (self.rej, self.exc, self.iso, self.cut, tuple(o.rule for o in self.ind))
            object.__setattr__(self, "_key", k)
        return k


_HYP_FIELDS = ("rej", "exc", "iso", "cut", "ind")


def replace(obj, **kw):
    """Gyors dataclasses.replace a Hyp-re (46. kör): ugyanazokat a mezőket állítja be, __init__ és
    mezőellenőrzés nélkül. A gyorsítótárazott kulcsot (_key) nem másolja."""
    if type(obj) is not Hyp:
        return _dc_replace(obj, **kw)
    n = object.__new__(Hyp)
    d = n.__dict__
    src = obj.__dict__
    for f in _HYP_FIELDS:
        d[f] = kw[f] if f in kw else src[f]
    return n


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
                 induce: bool = True, induce_min: int = 3, use_decay: float = 1.0,
                 reliability: str = "fixed", prior_strength: float = 10.0):
        assert mode in MODES, mode
        self.s, self.mode, self.B, self.depth = schema, mode, beam, depth
        self.eta, self.delta, self.c_ctx = eta, delta, c_ctx
        self.induce_on = induce and mode.startswith("arlc")
        self.induce_min = induce_min
        self.use_decay = use_decay
        self.reliability = reliability          # 'fixed' | 'beta' (tanult forrás-megbízhatóság)
        self.kappa = prior_strength
        self.ctx_cost: dict = {}               # forrásonkénti szétválasztási költség (külső jelből)
        self.reinstate_all = True              # True (alapértelmezés a 36. kör óta): minden jelöltre fut a visszahelyezés; False: csak szerkezeti jelöltekre (gyorsabb, de a 36. kör szerint szuboptimális lehet)
        self.ctx_induction = False             # True: izolált kontextusban is indukál, oda szkópolva
        self.vetted: Optional[set] = None      # ha meg van adva: csak ezek a források kapják a deklarált q-t
        self.newcomer_q: float = 0.9           # a többi (nem ellenőrzött) forrás előzetes átlaga
        self.source_q: dict = {}               # forrásszintű felülírás (pl. hiteltelenítés után)
        self.source_moves = False              # True: forrásszintű elutasítás és indukált-szabály-elhagyás lépés
        self.age_discount = 1.0                # < 1: a régi evidencia log-esélye λ^kor szerint gyengül (nem normatív)
        self.class_exceptions = False          # True: osztályszintű kivétel (a szabály hatókörének szűkítése)
        self.invention = False                 # True: kategória-feltalálás anomáliákból (30. kör)
        self.invent_min = 2                    # legalább ennyi anomália kell a feltaláláshoz
        self.invent_revive = False             # True: egy már elvetett szabályt is visszavehet finomítva
        self.theory_kappa: Optional[float] = None  # ha meg van adva: a forrás szabályai külön, ilyen κ-jú paramétert kapnak (32. kör)
        self.summary: Counter = Counter()      # 37. kör: elfelejtett, szabály által jósolt tények: (rule_id, e, q) -> darab
        self.exc_prior: Optional[float] = None # 41. kör: ha meg van adva, a kivétel egy ε valószínűségű abnormalitás
        self.cheap_greedy = False              # 42. kör: a mohó befejezés helyi költségbecsléssel választ
        self.corroboration = False             # 43. kör (v4.1): csak a megerősített állítás épít múltat
        self.ind_exc_cost = False              # 45. kör (3. hiba): indukált/feltalált szabály kivétele is -log2 ε-ba kerül
        self.theory_mix: Optional[tuple] = None  # 48. kör: (π, κ1, q0, κ0) keverék-prior az elmélet-megbízhatóságra
        self.priority_exceptions = False         # 82. kör: osztálykivétel rivális (ellentétes) szabályú osztályra is
        self.priority_code = False               # 81. kör: a prioritás-kivétel ára a riválisok közüli választás
        self.source_newcomer: Optional[tuple] = None  # 86. kör: (π_új, π_bevált, κ1, Δ) a forrás első megjelenése szerint
        self.source_mix: Optional[dict] = None   # 80. kör: forrás -> (π, κ1) kétkomponensű megbízhatósági prior (típus-metaadatból)
        self.source_mix_default: Optional[tuple] = None  # 80. kör: a source_mix-ben nem szereplő (ismeretlen) források (π, κ1)-e
        self.q_groups = False                  # 48. kör: a forrás állításai deklarált hitelesség szerint külön csoport
        self.strict_specificity = False        # 48. kör: osztályszintű kivétel csak a szabály törzsének szigorú alosztályára
        self.auto_specificity = False          # 49. kör: a specifikusabb ellentétes szabály ingyen felülírja az általánosabbat
        self.ctx_override = False              # 53. kör: az izolált forrás a saját kontextusában felülír (lex specialis)
        self.latent_truth = False              # 53. kör: közös látens igazság az egyező jelentésekre
        self.theory_pi: dict = {}              # 60. kör: forrásonkénti π a keverék-priorhoz (metaadat)
        self.entity_memo = True                # 72. kör: entitásonként memoizált zárás (viselkedésmegőrző)
        self.ctx_override_sources = None       # 73. kör: ha halmaz, az elsőbbség csak ezekre a (jelzett) forrásokra érvényes
        self.ctx_induction_sources = None      # 78. kör: ha halmaz, kontextusfüggő indukció csak ezek (jelzett források) kontextusában
        self._emc: dict = {}
        self._inv_counter = 0
        self.obs: list[Obs] = []
        self.by_id: dict[int, Obs] = {}
        self.beam: list[Hyp] = [Hyp()]
        self.now = 0
        self.uses: Counter = Counter()
        self._ccache: dict = {}
        self._scache: dict = {}
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
        ctx_lits = None
        if self.ctx_override and ctx is not None and ctx in H.iso and (self.ctx_override_sources is None
                                                                     or ctx in self.ctx_override_sources):
            # 53. kör: kontextuson belüli elsőbbség (lex specialis). Az izolált forrás saját szabályai és
            # tényei a saját kontextusában felülírják az örökölt, ellentétes állításokat, ütközés helyett.
            own_r = {(o.rule.body, o.rule.pred, o.rule.obj, o.rule.pos) for o in rules if o.source == ctx}
            n0 = len(rules) + len(facts)
            rules = [o for o in rules if o.source == ctx or
                     (o.rule.body, o.rule.pred, o.rule.obj, not o.rule.pos) not in own_r]
            ctx_lits = {(o.lit.pred, o.lit.subj, o.lit.obj, o.lit.pos) for o in facts if o.source == ctx}
            facts = [o for o in facts if o.source == ctx or
                     (o.lit.pred, o.lit.subj, o.lit.obj, not o.lit.pos) not in ctx_lits]
            n_override = n0 - len(rules) - len(facts)
        cls_exc = {(x[0], x[1][4:]) for x in H.exc if isinstance(x[1], str) and x[1].startswith("cat:")}
        if self.entity_memo and use_rules:
            isa, has, ruled, n_ent_over = self._closure_by_entity(H, rules, facts, cls_exc, ctx_lits)
            if ctx_lits is not None:
                n_override += n_ent_over
        else:
            isa, has, ruled, n_ent_over = self._closure_all(H, rules, facts, cls_exc, ctx_lits, use_rules)
            if ctx_lits is not None:
                n_override += n_ent_over
        cl = Closure(isa, has, ruled)
        cl.n_override = n_override if ctx_lits is not None else 0
        cl.conflict = self._rule_conflict(rules) or self._conflict(cl)
        if len(self._ccache) >= CLOSURE_CACHE_MAX:
            # 44. kör (memória): egy nehéz megfigyelésen belül a gyorsítótár 12 GB fölé nőtt. A zárás
            # tiszta függvény, ezért az ürítés a viselkedést nem változtatja, csak az időt.
            self._ccache.clear()
        self._ccache[key] = cl
        return cl

    def _closure_all(self, H, rules, facts, cls_exc, ctx_lits, use_rules=True, ents=None):
        """A zárás magja (a 72. kör előtti kód változatlanul). ents: ha meg van adva, csak ezekre az entitásokra
        fut a szabály-alkalmazás (a tényeket a hívó szűri)."""
        n_over = 0
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
                if r.rule.cond is None:
                    by_body[r.rule.body].append(r)
            # kétfeltételes (feltalált) tagsági szabályok: explicit tagság + explicit tény
            for ro in rules:
                if ro.rule.cond is None:
                    continue
                for e in list(isa.keys()):
                    b = isa[e].get((ro.rule.body, True))
                    f = has.get(e, {}).get(ro.rule.cond)
                    if b is not None and f is not None and (ro.id, e) not in H.exc:
                        isa[e].setdefault((ro.rule.obj, ro.rule.pos), b | f | {("obs", ro.id), ("inst", ro.id, e)})
            auto = self.auto_specificity
            if auto:
                up = defaultdict(set)
                for ro in rules:
                    r = ro.rule
                    if r.pred == "isa" and r.pos:
                        if r.cond is None:
                            up[r.body].add(r.obj)
                        else:
                            up[r.obj].add(r.body)
                anc_memo: dict = {}

                def anc(c):
                    a = anc_memo.get(c)
                    if a is None:
                        a, st = set(), [c]
                        while st:
                            x = st.pop()
                            for y in up.get(x, ()):
                                if y not in a and y != c:
                                    a.add(y)
                                    st.append(y)
                        anc_memo[c] = a
                    return a
            for e in list(isa.keys()):
                pending = [] if auto else None
                queue = [c for (c, pos) in isa[e] if pos]
                seen = set(queue)
                while queue:
                    c = queue.pop(0)
                    base = isa[e][(c, True)]
                    for ro in by_body.get(c, []):
                        if (ro.id, e) in H.exc:
                            continue
                        if cls_exc and any((ro.id, c2) in cls_exc for (c2, p2) in isa[e] if p2):
                            continue
                        sup = base | {("obs", ro.id), ("inst", ro.id, e)}
                        r = ro.rule
                        k = (r.obj, r.pos)
                        if ctx_lits is not None and (r.pred, e, r.obj, not r.pos) in ctx_lits:
                            n_over += 1
                            continue
                        if r.pred == "isa":
                            isa[e].setdefault(k, sup)
                            if r.pos and r.obj not in seen:
                                seen.add(r.obj)
                                queue.append(r.obj)
                        elif auto:
                            pending.append((r.body, k, sup))
                        else:
                            has[e].setdefault(k, sup)
                            ruled[e].add(k)
                if auto and pending:
                    # 49. kör: specifikus öröklés (Touretzky). Egy alkalmazás kiesik, ha egy ellentétes
                    # előjelű alkalmazás törzse az ő törzsének szigorú alosztálya. Ingyenes, nem kivétel.
                    for body, k, sup in pending:
                        opp = (k[0], not k[1])
                        if any(k2 == opp and body in anc(b2) for b2, k2, _ in pending):
                            continue
                        has[e].setdefault(k, sup)
                        ruled[e].add(k)
        return isa, has, ruled, n_over

    def _closure_by_entity(self, H, rules, facts, cls_exc, ctx_lits):
        """72. kör: entitásonként memoizált zárás. Egy entitás eredménye csak a szabályhalmaztól, a saját
        tényeitől, a saját kivételeitől, a globális osztálykivételektől és (elsőbbségnél) a saját kontextus-
        literáljaitól függ. A szótárak beszúrási sorrendje azonos a _closure_all-éval, így a konfliktuskeresés
        sorrendje sem változik."""
        memo = self._emc
        # a megfigyelések objektumai élnek (self.obs), az id-jük biztonságos; az indukált/feltalált szabályok
        # objektumai eldobódhatnak, ezért azoknál tartalom-alapú kulcs
        gkey = (tuple(id(o) if o.id < IND_BASE else (o.id, o.rule) for o in rules), frozenset(cls_exc),
                self.auto_specificity)
        gid = memo.get(("g", gkey))
        if gid is None:
            gid = len(memo)
            memo[("g", gkey)] = gid
        by_e: dict = {}
        order_isa, order_has = [], []
        for o in sorted(facts, key=lambda o: (-o.time, o.id)):
            e = o.lit.subj
            lst = by_e.get(e)
            if lst is None:
                lst = by_e[e] = []
            lst.append(o)
        seen_i, seen_h = set(), set()
        for o in sorted(facts, key=lambda o: (-o.time, o.id)):
            e = o.lit.subj
            if o.lit.pred == "isa":
                if e not in seen_i:
                    seen_i.add(e)
                    order_isa.append(e)
            elif e not in seen_h:
                seen_h.add(e)
                order_has.append(e)
        exc_by_e: dict = {}
        for x in H.exc:
            if not (isinstance(x[1], str) and x[1].startswith("cat:")):
                exc_by_e.setdefault(x[1], []).append(x)
        res = {}
        n_over = 0
        for e, fl in by_e.items():
            ex = frozenset(exc_by_e.get(e, ()))
            cl_e = None if ctx_lits is None else frozenset(l for l in ctx_lits if l[1] == e)
            k = (gid, e, tuple(id(o) for o in fl), ex, cl_e)
            r = memo.get(k)
            if r is None:
                Hs = replace(H, exc=frozenset(ex) | frozenset(x for x in H.exc if isinstance(x[1], str) and x[1].startswith("cat:")))
                i_, h_, ru_, no_ = self._closure_all(Hs, rules, fl, cls_exc, cl_e if ctx_lits is not None else None)
                r = (dict(i_).get(e, {}), dict(h_).get(e, {}), dict(ru_).get(e, set()), no_)
                if len(memo) > 400000:
                    memo.clear()
                    memo[("g", gkey)] = gid
                memo[k] = r
            res[e] = r
            n_over += r[3]
        isa: dict = defaultdict(dict)
        has: dict = defaultdict(dict)
        ruled: dict = defaultdict(set)
        for e in order_isa:
            isa[e] = res[e][0]
        for e in order_has:
            has[e] = res[e][1]
        for e in order_isa:
            if e not in seen_h and res[e][1]:
                has[e] = res[e][1]
        for e, r in res.items():
            if r[2]:
                ruled[e] = r[2]
        return isa, has, ruled, n_over

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
        k = H.key()
        if k in self._scache:
            return self._scache[k]
        v = self._score(H)
        self._scache[k] = v
        return v

    def _score(self, H: Hyp) -> float:
        if self.mode == "wms":
            return sum(math.log2(self.by_id[i].q / (1 - self.by_id[i].q)) for i in H.rej)
        bits = 0.0
        has_cut = bool(H.cut)
        if self.reliability == "beta":
            bits += self._beta_bits(H)
        cl_cache: dict = {}
        seen_truth: set = set()

        def cl_for(ctx, t):
            k = (ctx, t)
            if k not in cl_cache:
                cl_cache[k] = self.closure(H, ctx, t)
            return cl_cache[k]
        for o in self.obs:
            q_o = self.source_q.get(o.source, o.q)
            if self.age_discount < 1.0:
                q_o = 0.5 + (q_o - 0.5) * self.age_discount ** max(0, self.now - o.time)
            if o.id in H.rej:
                if self.reliability != "beta":
                    bits += -math.log2(1 - q_o)
                if o.lit is not None and o.lit.pred == "has":
                    bits += 1.0
                continue
            if self.reliability != "beta":
                bits += -math.log2(q_o)
            if o.lit is not None and o.lit.pred == "has":
                ctx = o.source if o.source in H.iso else None
                tt = o.time if has_cut else self.now
                if self.latent_truth:
                    # 53. kör: közös látens igazság. Az igazság-tag literálonként egyszer fizetendő; egy további
                    # elfogadott, egyező jelentés a látens értékből determinisztikus (csak a megbízhatósága kerül).
                    lk = (ctx, tt, o.lit.subj, o.lit.obj, o.lit.pos)
                    if lk in seen_truth:
                        continue
                    seen_truth.add(lk)
                cl = cl_for(ctx, tt)
                pred = (o.lit.obj, o.lit.pos) in cl.ruled.get(o.lit.subj, ())
                bits += -math.log2(1 - self.delta) if pred else 1.0
        n_cls = sum(1 for x in H.exc if isinstance(x[1], str) and x[1].startswith("cat:"))
        if self.exc_prior is None:
            bits += (len(H.exc) - n_cls) * math.log2(max(2, self.s.n_entities))
        else:
            # minden (szabály, jelölt tag) pár egy abnormalitás-változó: kivétel -log2 ε, egyébként -log2(1-ε)
            eps = self.exc_prior
            for rid, e in self._candidate_applications():
                bits += -math.log2(eps) if (rid, e) in H.exc else -math.log2(1 - eps)
            if self.ind_exc_cost:
                # 45. kör: a jelöltlistán kívüli (indukált, feltalált, kétfeltételes) szabályok kivétele
                # ugyanazt a határköltséget kapja, mint egy tankönyvi szabályé: log2((1-ε)/ε).
                # A normál alkalmazásaik nem kapnak tagot (nem megfigyelt abnormalitás-változók
                # kimarginalizálva), így nem tér vissza a világméret-műtermék.
                cand = getattr(self, "_capp_set", None)
                if cand is None or getattr(self, "_capp_set_key", None) != self._capp_key:
                    cand = set(self._candidate_applications())
                    self._capp_set, self._capp_set_key = cand, self._capp_key
                for x in H.exc:
                    if not (isinstance(x[1], str) and x[1].startswith("cat:")) and x not in cand:
                        bits += math.log2((1 - eps) / eps)
        if self.priority_code and n_cls:
            for x in H.exc:
                if isinstance(x[1], str) and x[1].startswith("cat:"):
                    pb = self._prio_bits(H, x)
                    bits += (math.log2(max(2, self.s.n_categories)) + 1.0) if pb is None else pb
        else:
            bits += n_cls * (math.log2(max(2, self.s.n_categories)) + 1.0)
        bits += sum(self.ctx_cost.get(src, self.c_ctx) for src in H.iso)
        if self.ctx_override:
            # 53. kör: a kontextus a fő világ + kódolt eltérések; minden felülírás egy eltérés,
            # ára egy kivételé (ε nélkül a régi log2|E|-es kivételár)
            dev = math.log2((1 - self.exc_prior) / self.exc_prior) if self.exc_prior else math.log2(max(2, self.s.n_entities))
            for src in H.iso:
                bits += cl_for(src, self.now).n_override * dev
        if self.summary:
            for (rid, e, q), cnt in self.summary.items():
                active = rid not in H.rej and (rid, e) not in H.exc
                bits += cnt * (-math.log2(q) + (-math.log2(1 - self.delta) if active else 1.0))
        for oid, _ in H.cut:
            g = self._group(self.by_id[oid].lit)
            bits += -math.log2(self.s.update_prior.get(g, 1e-3))
        bits += len(H.ind) * math.log2(max(2, 2 * self.s.n_categories * self.s.n_props))
        if self.eta:
            bits += self.eta * sum(n for tok, n in self.uses.items() if self._lost(tok, H))
        return bits

    def _beta_bits(self, H: Hyp) -> float:
        """Forrásonként béta-binomiális kód az elfogadás/elutasítás sorozatra.
        Előzetes: Beta(κ·q, κ·(1−q)), q = a forrás deklarált hitelessége (átlag)."""
        stats: dict = {}
        corr = self._corroborated(H) if self.corroboration else None
        for o in self.obs:
            q0 = o.q if (self.vetted is None or o.source in self.vetted) else self.newcomer_q
            q0 = self.source_q.get(o.source, q0)
            key = (o.source, "elmélet") if (self.theory_kappa is not None and o.rule is not None) else o.source
            if self.q_groups:
                key = (key if isinstance(key, tuple) else (key, "adat")) + (round(q0, 6),)
            n, k, q = stats.get(key, (0, 0, q0))
            rej = o.id in H.rej
            if corr is not None and not rej and o.id not in corr:
                stats.setdefault(key, (n, k, q))        # semleges: nem épít múltat
                continue
            stats[key] = (n + 1, k + rej, q)
        first_seen = None
        if self.source_newcomer is not None:
            fk = len(self.obs)
            if getattr(self, "_fs_key", None) != fk:
                fs: dict = {}
                for o in self.obs:
                    if o.time < fs.get(o.source, float("inf")):
                        fs[o.source] = o.time
                self._fs, self._fs_key = fs, fk
            first_seen = self._fs
        bits = 0.0
        lb = lambda a, b: math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
        bb = lambda n, k, kap, q: (lb(kap * q, kap * (1 - q)) - lb(kap * q + n - k, kap * (1 - q) + k)) / math.log(2)
        for src, (n, k, q) in stats.items():
            theory = isinstance(src, tuple) and src[1] == "elmélet"
            sm = None
            if self.source_mix is not None:
                sname = src[0] if isinstance(src, tuple) else src
                sm = self.source_mix.get(sname, self.source_mix_default)
            elif self.source_newcomer is not None:
                # 86. kör: a forrástípus helyett a forrás megfigyelhető múltja: az új (most megjelent) forrás
                # szemét-esélye nagyobb, mint a bevált forrásé
                sname = src[0] if isinstance(src, tuple) else src
                pn, po, k1n, dlt = self.source_newcomer
                sm = (pn, k1n) if first_seen[sname] >= self.now - dlt else (po, k1n)
            if theory and self.theory_mix is not None:
                # 48. kör: „nagyjából helyes, néhány hibával” (κ1 a q körül) vagy „egészében téves” (q0, κ0)
                pi, k1, q0m, k0 = self.theory_mix[:4]
                pi = self.theory_pi.get(src[0], pi)   # 60. kör: forrás-metaadatból jövő területi π
                if sm is not None:
                    k1 = sm[1]                        # 80. kör: a becsületes komponens szélessége a forrástípusból
                # kalibrált változat: a magányos állítás helyességének valószínűsége a deklarált q marad,
                # π·q1 + (1−π)·q0 = q (ehhez π ≥ (q − q0)/(1 − q0) kell)
                q1 = min(1 - 1e-9, max(1e-9, (q - (1 - pi) * q0m) / pi)) if len(self.theory_mix) > 4 else q
                c1, c0 = bb(n, k, k1, q1), bb(n, k, k0, q0m)
                m = min(c1, c0)
                bits += m - math.log2(pi * 2 ** (m - c1) + (1 - pi) * 2 ** (m - c0))
                continue
            if sm is not None:
                # 80. kör: „becsületes, legfeljebb kissé kalibrálatlan” (κ1 a deklarált q körül) vagy „szemét” (Beta(1,1))
                pi, k1 = sm
                c1, c0 = bb(n, k, k1, q), bb(n, k, 2.0, 0.5)
                m = min(c1, c0)
                bits += m - math.log2(pi * 2 ** (m - c1) + (1 - pi) * 2 ** (m - c0))
                continue
            kap = self.theory_kappa if theory else self.kappa
            bits += bb(n, k, kap, q)
        return bits

    def _candidate_applications(self) -> list:
        """Minden (feltétel nélküli szabály, entitás) pár egy abnormalitás-változó (41. kör, a 43. körben
        javítva): a kivétel ára így akkor is -log2 ε, ha a tagság levezetett, nem állított. Ahol a
        szabály nem alkalmazható, a pár csak konstans -log2(1-ε) tagot ad."""
        key = len(self.obs)
        if getattr(self, "_capp_key", None) == key:
            return self._capp
        ents = sorted({o.lit.subj for o in self.obs if o.lit is not None})
        out = [(r.id, e) for r in self.obs if r.rule is not None and r.rule.cond is None for e in ents]
        self._capp_key, self._capp = key, out
        return out

    def _corroborated(self, H: Hyp) -> set:
        """Az elfogadott megfigyelések közül azok, amelyeket más forrás vagy egy szabály megerősít."""
        cl = self.closure(H, None, self.now)
        fact_src = defaultdict(set)
        isa_src = defaultdict(set)
        for o in self.obs:
            if o.lit is None or o.id in H.rej:
                continue
            key = (o.lit.subj, o.lit.obj, o.lit.pos)
            (fact_src if o.lit.pred == "has" else isa_src)[key].add(o.source)
        members = defaultdict(list)
        for e, d in cl.isa.items():
            for (c, pos) in d:
                if pos:
                    members[c].append(e)
        out = set()
        for o in self.obs:
            if o.id in H.rej:
                continue
            if o.lit is not None:
                key = (o.lit.subj, o.lit.obj, o.lit.pos)
                if o.lit.pred == "has":
                    if (fact_src[key] - {o.source}) or (o.lit.obj, o.lit.pos) in cl.ruled.get(o.lit.subj, ()):
                        out.add(o.id)
                elif isa_src[key] - {o.source}:
                    out.add(o.id)
            elif o.rule is not None and o.rule.pred == "has" and o.rule.cond is None:
                r = o.rule
                if any(fact_src.get((e, r.obj, r.pos), set()) - {o.source} for e in members.get(r.body, ())):
                    out.add(o.id)
        return out

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
                if self.class_exceptions:
                    body = self._get(tok[1], H).rule.body
                    cl = self.closure(H, None, self.now)
                    for (c2, p2) in cl.isa.get(tok[2], {}):
                        if p2 and c2 != body and (not self.strict_specificity or self._proper_sub(H, c2, body)
                                                  or (self.priority_exceptions and self._rival_rule(H, c2, tok[1]))):
                            yield replace(H, exc=H.exc | {(tok[1], "cat:" + c2)})

    def _rival_rule(self, H: Hyp, c2: str, rid: int) -> bool:
        """82. kör: prioritásos alapértelmezés (Brewka, 1989). A (rid, cat:c2) osztálykivétel akkor is megengedett, ha
        c2 nem alosztálya a szabály törzsének, de c2-nek van saját, elfogadott, ellentétes előjelű szabálya ugyanarra a
        tulajdonságra: ekkor a kivétel azt jelenti, hogy „c2 szabálya elsőbbséget élvez rid-del szemben”."""
        return c2 in self._rivals(H, rid)

    def _rivals(self, H: Hyp, rid: int) -> set:
        """82. kör: azok a kategóriák, amelyeknek elfogadott, ellentétes előjelű szabálya van rid tulajdonságára."""
        o = next((y for y in H.ind if y.id == rid), None) if rid >= IND_BASE else self.by_id.get(rid)
        if o is None or o.rule is None or o.rule.pred != "has":
            return set()
        r = o.rule
        return {o.rule.body for o in list(self.obs) + list(H.ind)
                if o.rule is not None and o.id not in H.rej and o.rule.cond is None and o.rule.pred == "has"
                and o.rule.obj == r.obj and o.rule.pos != r.pos and o.rule.body != r.body}

    def _prio_bits(self, H: Hyp, x) -> Optional[float]:
        """81. kör (priority_code): egy prioritás-típusú osztálykivétel ára. A rivális kategóriát a riválisok
        közül kell megnevezni (log2 |R|), nem az összes kategória közül, + 1 bit a kivétel létéért. None, ha x nem
        prioritás-típusú (alosztály-kivétel vagy nincs rivális)."""
        c2 = x[1][4:]
        o = next((y for y in H.ind if y.id == x[0]), None) if x[0] >= IND_BASE else self.by_id.get(x[0])
        if o is None or o.rule is None:
            return None                      # elárvult kivétel (a szabálya már nincs a hipotézisben)
        body = o.rule.body
        if self.strict_specificity and self._proper_sub(H, c2, body):
            return None
        R = self._rivals(H, x[0])
        if c2 not in R:
            return None
        return math.log2(max(2, len(R))) + 1.0

    def _proper_sub(self, H: Hyp, c2: str, body: str) -> bool:
        """48. kör: c2 a body szigorú alosztálya-e az elfogadott alosztály-szabályok
        szerint. A feltalált c′ = b ∧ F kategória definíció szerint b alosztálya."""
        up = defaultdict(set)
        for o in list(self.obs) + list(H.ind):
            r = o.rule
            if r is None or o.id in H.rej or r.pred != "isa" or not r.pos:
                continue
            if r.cond is None:
                up[r.body].add(r.obj)
            else:
                up[r.obj].add(r.body)
        seen, stack = {c2}, [c2]
        while stack:
            x = stack.pop()
            for y in up.get(x, ()):
                if y == body:
                    return True
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return False

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

    def _local_cost(self, H: Hyp, H2: Hyp) -> float:
        """Olcsó, helyi költségbecslés egy módosításra (42. kör): csak a megváltozott elemek."""
        c = 0.0
        for i in H2.rej - H.rej:
            o = self.by_id.get(i)
            if o is not None:
                q = min(max(self.source_q.get(o.source, o.q), 1e-6), 1 - 1e-6)
                c += math.log2(q / (1 - q))
        unit = (math.log2((1 - self.exc_prior) / self.exc_prior) if self.exc_prior
                else math.log2(max(2, self.s.n_entities)))
        for x in H2.exc - H.exc:
            pb = (self._prio_bits(H2, x) if (self.priority_code and isinstance(x[1], str) and x[1].startswith("cat:"))
                  else None)
            c += unit if pb is None else pb
        c += sum(self.ctx_cost.get(src, self.c_ctx) for src in H2.iso - H.iso)
        c += sum(-math.log2(self.s.update_prior.get(self._group(self.by_id[i].lit), 1e-3))
                 for i, _ in set(H2.cut) - set(H.cut))
        c -= 4.0 * (len(H.ind) - len(H2.ind))
        return c

    def _greedy(self, H: Hyp, max_steps: int = 80) -> Optional[Hyp]:
        """Mohó befejezés: a maradék konfliktusokat egyenként, a legolcsóbb lépéssel oldja fel."""
        for _ in range(max_steps):
            c = self.find_conflict(H)
            if c is None:
                return H
            opts = list(self._mods(H, c))
            if not opts:
                return None
            if self.cheap_greedy:
                # azonos a min(opts, key=(költség, str(kulcs)))-csal, de a drága str(kulcs) csak a
                # legolcsóbb holtversenyesekre számolódik (46. kör, viselkedésmegőrző gyorsítás)
                costs = [self._local_cost(H, h) for h in opts]
                cmin = min(costs)
                ties = [h for h, cv in zip(opts, costs) if cv == cmin]
                H = ties[0] if len(ties) == 1 else min(ties, key=lambda h: str(h.key()))
            else:
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
            cl = self.closure(H, None, self.now)
            moves = [replace(H, rej=H.rej - {i}) for i in sorted(H.rej)
                     if not self._surely_conflicts(cl, self.by_id[i], H)]
            moves += [replace(H, exc=H.exc - {x}) for x in sorted(H.exc)]
            moves += [replace(H, iso=H.iso - {s}) for s in sorted(H.iso)]
            if self.source_moves:
                moves += [replace(H, ind=tuple(x for x in H.ind if x is not o)) for o in H.ind]
                for src in sorted({o.source for o in self.obs}):
                    ids = frozenset(o.id for o in self.obs if o.source == src and o.q < 1.0)
                    if ids and not ids <= H.rej:
                        moves.append(replace(H, rej=H.rej | ids))
            for H2 in moves:
                if self.find_conflict(H2) is None:
                    sc = self.score(H2)
                    if sc < cur - 1e-9:
                        H, cur, improved = H2, sc, True
                        break
        return H

    def _surely_conflicts(self, cl: Closure, o: Obs, H: Hyp) -> bool:
        """Biztosan ütközne-e o visszavétele (csak a globális kontextusban, változó csoport
        és vágás nélkül ítélünk; minden más esetben a teljes ellenőrzés fut)."""
        if o.lit is None or o.source in H.iso or H.cut or self._mutable(o):
            return False
        l = o.lit
        if l.pred == "has":
            return (l.obj, not l.pos) in cl.has.get(l.subj, {})
        d = cl.isa.get(l.subj, {})
        if (l.obj, not l.pos) in d:
            return True
        if l.pos:
            return any(pos and frozenset((c, l.obj)) in self.s.disjoint for (c, pos) in d)
        return False

    def _invent(self, H: Hyp) -> list[Hyp]:
        """Kategória-feltalálás: ha egy c → p szabálynak legalább invent_min olyan tagja van,
        amelyről ¬p-t figyeltünk meg, és ezek mind osztoznak egy F tényben, amelyet a 'normális'
        tagok közül egyik sem mutat, javasolt: c' := c ∧ F, c' → ¬p, és a c → p szabály
        osztályszintű kivétele c'-re."""
        out = []
        facts: dict = defaultdict(dict)       # e -> {(prop, pos): obs_id}  (explicit, nem elutasított)
        members: dict = defaultdict(set)      # c -> explicit tagok
        for o in self.obs:
            if o.lit is None or (o.id in H.rej and o.lit.pred == "isa"):
                continue
            if o.lit.pred == "has":
                facts[o.lit.subj][(o.lit.obj, o.lit.pos)] = o.id
            elif o.lit.pos:
                members[o.lit.obj].add(o.lit.subj)
        for ro in self.obs:
            r = ro.rule
            if r is None or r.pred != "has" or r.cond is not None:
                continue
            if ro.id in H.rej and not self.invent_revive:
                continue
            anom = [e for e in members.get(r.body, ()) if (r.obj, not r.pos) in facts[e]]
            normal = [e for e in members.get(r.body, ()) if (r.obj, r.pos) in facts[e]]
            if len(anom) < self.invent_min:
                continue
            shared = set.intersection(*[set(facts[e]) for e in anom]) - {(r.obj, not r.pos)}
            for F in sorted(shared):
                if any(F in facts[e] for e in normal):
                    continue
                if any(o.rule and o.rule.cond == F and o.rule.body == r.body for o in H.ind):
                    continue
                self._inv_counter += 1
                new_cat = f"{r.body}&{F[0]}{'' if F[1] else '-'}"
                m_rule = Obs(IND_BASE + 500000 + 2 * self._inv_counter, "__invented__", self.now, 1.0,
                             rule=Rule(r.body, "isa", new_cat, True, cond=F))
                h_rule = Obs(IND_BASE + 500001 + 2 * self._inv_counter, "__invented__", self.now, 1.0,
                             rule=Rule(new_cat, "has", r.obj, not r.pos))
                exc = {x for x in H.exc if not (x[0] == ro.id and x[1] in anom)}
                exc.add((ro.id, "cat:" + new_cat))
                rej = H.rej - {facts[e][(r.obj, not r.pos)] for e in anom} - {ro.id}
                H2 = replace(H, ind=H.ind + (m_rule, h_rule), exc=frozenset(exc), rej=frozenset(rej))
                if self.find_conflict(H2) is None:
                    out.append(H2)
        return out

    # ------------------------------------------------------------ induction
    def _induce(self, H: Hyp, subj: str) -> list[Hyp]:
        out = []
        ctxs = [None] + (sorted(s for s in H.iso if self.ctx_induction_sources is None
                                or s in self.ctx_induction_sources) if self.ctx_induction else [])
        for ctx in ctxs:
            out.extend(self._induce_in(H, subj, ctx))
        return out

    def _induce_in(self, H: Hyp, subj: str, ctx: Optional[str]) -> list[Hyp]:
        cl = self.closure(H, ctx, self.now)
        cats = [c for (c, pos) in cl.isa.get(subj, {}) if pos]
        out = []
        for c in cats:
            members = [e for e, d in cl.isa.items() if (c, True) in d]
            if len(members) < self.induce_min:
                continue
            existing = {(o.rule.obj, o.rule.pos) for o in list(self.obs) + list(H.ind)
                        if o.rule and o.rule.body == c and o.id not in H.rej
                        and (o.source not in H.iso or o.source == ctx)}
            votes: Counter = Counter()
            for e in members:
                for (p, pos), sup in cl.has.get(e, {}).items():
                    if (p, pos) not in cl.ruled.get(e, ()):
                        votes[(p, pos)] += 1
            for (p, pos), n in votes.items():
                if n >= self.induce_min and votes.get((p, not pos), 0) == 0 and (p, pos) not in existing \
                        and (p, not pos) not in existing:
                    self._ind_counter += 1
                    o = Obs(IND_BASE + self._ind_counter, ctx or "__induced__", self.now, 1.0,
                            rule=Rule(c, "has", p, pos))
                    H2 = replace(H, ind=H.ind + (o,))
                    if self.find_conflict(H2) is None:
                        out.append(H2)
        return out

    # ------------------------------------------------------------ public API
    def observe(self, o: Obs) -> dict:
        self._ccache.clear()
        self._emc.clear()
        self._scache.clear()
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
        parent: dict = {}
        seen: set = set()
        for H in self.beam:
            for H2 in self._repair(H, self.depth, seen):
                cands[H2.key()] = H2
                parent.setdefault(H2.key(), H)
        if not cands:
            for H in self.beam:
                H2 = replace(H, rej=H.rej | {o.id})
                if self.find_conflict(H2) is None:
                    cands[H2.key()] = H2
        if self.induce_on and o.lit is not None:
            for H in sorted(cands.values(), key=self.score)[:2]:
                for H3 in self._induce(H, o.lit.subj):
                    cands[H3.key()] = H3
        def structural(h: Hyp) -> bool:
            p = parent.get(h.key())
            if p is None or self.reinstate_all:
                return True
            new_rej = h.rej - p.rej
            return (h.iso != p.iso or h.exc != p.exc or h.cut != p.cut or h.ind != p.ind
                    or any(self.by_id[i].rule is not None for i in new_rej))
        if self.invention:
            for H in sorted(cands.values(), key=self.score)[:2]:
                for H4 in self._invent(H):
                    cands[H4.key()] = H4
                    parent.setdefault(H4.key(), None)
        ranked = sorted({h.key(): h for h in (self._reinstate(h) if structural(h) else h
                                              for h in cands.values())}.values(),
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

    def consolidate(self, keep_summary: bool = True) -> int:
        """37. kör: a legjobb hipotézisben elfogadott, egyetlen szabály által jósolt 'has' tények
        törlése a memóriából. keep_summary=True: a pontszám megőrzi a hozzájárulásukat egy
        (szabály, entitás, hitelesség) számlálóban; False: naiv törlés."""
        H = self.best
        cl = self.closure(H, None, self.now)
        drop = []
        for o in self.obs:
            if o.lit is None or o.lit.pred != "has" or o.id in H.rej or o.source in H.iso:
                continue
            k = (o.lit.obj, o.lit.pos)
            if k not in cl.ruled.get(o.lit.subj, ()):
                continue
            cats = {c for (c, pos) in cl.isa.get(o.lit.subj, {}) if pos}
            rids = [r.id for r in self.obs if r.rule is not None and r.rule.cond is None and r.rule.pred == "has"
                    and r.id not in H.rej and r.rule.body in cats and (r.rule.obj, r.rule.pos) == k
                    and (r.id, o.lit.subj) not in H.exc]
            if len(rids) != 1:
                continue
            drop.append((o, rids[0]))
        ids = {o.id for o, _ in drop}
        self.obs = [o for o in self.obs if o.id not in ids]
        if keep_summary:
            for o, rid in drop:
                self.summary[(rid, o.lit.subj, o.q)] += 1
        self._ccache.clear()
        self._scache.clear()
        return len(drop)

    def set_source_q(self, source: str, q: float) -> dict:
        """Meta-információ egy forrásról (pl. 'a visszajelzés hamis volt'): a forrás előzetes
        megbízhatósága q lesz, majd a nyaláb újraoptimalizálódik."""
        self.source_q[source] = q
        return self.reoptimize()

    def reoptimize(self) -> dict:
        self._ccache.clear()
        self._scache.clear()
        prev = self.best
        cands = {h.key(): self._reinstate(h) for h in self.beam}
        self.beam = sorted({h.key(): h for h in cands.values()}.values(), key=self.score)[: self.B]
        return {"changed": self.best.key() != prev.key(), "rej_added": sorted(self.best.rej - prev.rej),
                "ind_dropped": [(o.rule.body, o.rule.obj, o.rule.pos) for o in prev.ind if o not in self.best.ind]}

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
            self._scache.clear()
        return ans
