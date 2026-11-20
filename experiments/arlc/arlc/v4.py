"""43. kör: az ARLC v4 befagyasztott konfigurációja és az ablációs tábla.

A v4 a 26–42. kör túlélő mechanizmusait kapcsolja be egyszerre. A konfigurációt a 44. kör
procedurális benchmarkja előtt rögzítem; utána nem hangolom.
"""
from __future__ import annotations

import contextlib
import json
import math
import statistics as st

from . import core

V4 = {
    "reliability": "beta",        # 17. kör
    "kappa": 30.0,                # adatforrások (κ_S), 32. kör
    "theory_kappa": 1.0,          # elméletek (κ_T), 32. kör
    "exc_prior": 0.05,            # 41. kör
    "class_exceptions": True,     # 27. kör
    "invention": True,            # 30. kör
    "invent_revive": True,        # 30. kör
    "source_moves": True,         # 27. kör
    "ctx_induction": True,        # 21. kör
    "reinstate_all": True,        # 36. kör
    "cheap_greedy": True,         # 42. kör (kimerítő ellenőrzéssel igazolva)
    "depth": 2,                   # 42. kör (kimerítő ellenőrzéssel igazolva; kb. 25× gyorsabb)
}

V41_OVERRIDES = {"corroboration": True}   # v4.1: a 43. kör diagnózisa után, feltáró jelleggel
V42_OVERRIDES = {"ind_exc_cost": True}    # v4.2: a 45. körben talált 3. hiba javítása (nem a befagyasztott v4)
MIX = (0.9, 30.0, 0.5, 2.0)               # 48. kör: π, κ1, q0, κ0 (nem kalibrált; első javaslat)
MIX_CAL = (0.95, 30.0, 0.5, 2.0, "cal")   # 48. kör: kalibrált keverék (magányos állításra P(helyes) = q)
MIX_CAL99 = (0.99, 30.0, 0.5, 2.0, "cal")  # 49. kör: a „szemét elmélet” prioresélye 1%
MIX_CAL999 = (0.999, 30.0, 0.5, 2.0, "cal")  # 49. kör: 0,1%
V5_OVERRIDES = {"ind_exc_cost": True, "theory_mix": MIX_CAL, "q_groups": True,   # 48. kör: keverékes jelölt (ELVETVE)
                "strict_specificity": True}
V43_OVERRIDES = {"ind_exc_cost": True, "q_groups": True, "strict_specificity": True}  # 48. kör: a túlélő javítások
V44_OVERRIDES = {**V43_OVERRIDES, "auto_specificity": True}   # 49. kör: + specifikus öröklés
V45_OVERRIDES = {**V44_OVERRIDES, "ctx_override": True}        # 50. kör: + kontextuson belüli elsőbbség (ELVETVE)
V44E_OVERRIDES = {**V44_OVERRIDES, "theory_kappa": None}       # 50. kör: v4.4-egyszintű
V46_OVERRIDES = {**V44E_OVERRIDES, "latent_truth": True}       # 53. kör: + közös látens igazság
V47_OVERRIDES = {**V44E_OVERRIDES, "ctx_cost": {"book": 10.0, "census": 10.0}}  # 56. kör: gondozott forrás kontextusa 10 bit
# 80. kör: forrástípus-prior (a 78. kör bűnbak-forrás diagnózisára). A típus metaadat, a paraméterek a priori:
# gondozott forrás megbízhatósága kb. ±0,01 pontossággal ismert (κ1 = 300), szemét-esélye 0,1%; terepi forrás
# kalibrálatlan lehet (κ1 = 30), szemét-esélye 1%; ismeretlen (új, ellenőrizetlen) forrás: κ1 = 30, szemét-esélye 10%.
CURATED = (0.999, 300.0)
FIELD = (0.99, 30.0)
UNKNOWN = (0.9, 30.0)
SOURCE_TYPE_MIX = {"book": CURATED, "book2": CURATED, "census": CURATED, "review": CURATED, "expert": CURATED,
                   "field": FIELD, "fieldA": FIELD, "fieldB": FIELD}
V49_SM = {"source_mix": SOURCE_TYPE_MIX, "source_mix_default": UNKNOWN}
# 86. kör: metaadat nélküli változatok. U: minden forrás egyforma keverék-priort kap; N: az új (az aktuális időpontban
# megjelent) forrás szemét-esélye 10%, a bevált forrásé 0,1% (a forrás múltja megfigyelhető, nem orákulum).
V49_U = {"source_mix": {}, "source_mix_default": (0.9, 30.0)}
V49_N = {"source_newcomer": (0.9, 0.999, 30.0, 0)}
# 88. kör: BEFAGYASZTOTT konfiguráció a harmadik generátor (G3) előtt. A G3-on mért eredmények nem módosíthatják.
# v4.8-π (tankönyv-keverék, π a metaadatból; a G3-ban a tankönyv „normál”, π = 0,999) + PK (81. kör) + N (86. kör).
HYBRID_91 = None  # lent definiálva
FROZEN_88 = {**V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0),
             "priority_exceptions": True, "priority_code": True, **V49_N}

ABLATIONS = {
    "v4": {},
    "− tanult megbízhatóság": {"reliability": "fixed", "theory_kappa": None},
    "− kétszintű (egyszintű κ=30)": {"theory_kappa": None},
    "− kivétel-prior (log₂|E|)": {"exc_prior": None},
    "− osztályszintű kivétel": {"class_exceptions": False},
    "− feltalálás": {"invention": False, "invent_revive": False},
    "− forrásszintű lépés": {"source_moves": False},
    "− olcsó mohó lépés (mélység 3)": {"cheap_greedy": False, "depth": 3},
}


@contextlib.contextmanager
def configured(overrides: dict):
    """Minden 'arlc' módú Memory a v4 (+felülírások) beállításaival jön létre."""
    cfg = dict(V4)
    cfg.update(overrides)
    orig = core.Memory.__init__

    def init(self, *a, **k):
        orig(self, *a, **k)
        if self.mode.startswith("arlc"):
            self.reliability = cfg["reliability"]
            self.kappa = cfg["kappa"]
            for key in ("theory_kappa", "exc_prior", "class_exceptions", "invention", "invent_revive",
                        "source_moves", "ctx_induction", "reinstate_all", "cheap_greedy", "depth"):
                setattr(self, key, cfg[key])
            self.corroboration = cfg.get("corroboration", False)
            self.ind_exc_cost = cfg.get("ind_exc_cost", False)
            self.theory_mix = cfg.get("theory_mix", None)
            self.q_groups = cfg.get("q_groups", False)
            self.strict_specificity = cfg.get("strict_specificity", False)
            self.auto_specificity = cfg.get("auto_specificity", False)
            self.ctx_override = cfg.get("ctx_override", False)
            self.latent_truth = cfg.get("latent_truth", False)
            self.ctx_cost.update(cfg.get("ctx_cost", {}))
            if "ctx_override_sources" in cfg:
                self.ctx_override_sources = cfg["ctx_override_sources"]
            self.priority_exceptions = cfg.get("priority_exceptions", False)
            self.priority_code = cfg.get("priority_code", False)
            self.source_newcomer = cfg.get("source_newcomer", None)
            self.rel_temper = cfg.get("rel_temper", None)
            self.rel_hybrid = cfg.get("rel_hybrid", False)
            self.cut_per_event = cfg.get("cut_per_event", False)
            self.rel_hybrid_kappa = cfg.get("rel_hybrid_kappa", None)
            self.source_changepoints = cfg.get("source_changepoints", False)
            self.chg_prior = cfg.get("chg_prior", 0.01)
            self.newcomer_corrob = cfg.get("newcomer_corrob", False)
            self.q_temper = cfg.get("q_temper", 1.0)
            self.rule_cuts = cfg.get("rule_cuts", False)
            self.rule_change_prior = cfg.get("rule_change_prior", 0.01)
            self.copy_detection = cfg.get("copy_detection", False)
            self.copy_prior = cfg.get("copy_prior", 0.01)
            self.reopen_search = cfg.get("reopen_search", False)
            self.copy_acyclic = cfg.get("copy_acyclic", False)
            if "source_mix" in cfg:
                self.source_mix = cfg["source_mix"]
                self.source_mix_default = cfg.get("source_mix_default")
            if "ctx_induction_sources" in cfg:
                self.ctx_induction_sources = cfg["ctx_induction_sources"]
    core.Memory.__init__ = init
    try:
        yield cfg
    finally:
        core.Memory.__init__ = orig


def battery(cfg):
    """A korábbi körök feladataiból összeállított ellenőrző csomag (csak az 'arlc' sorok)."""
    from . import experiments as X, tfb, quine as Q, invention as I
    out = {}
    e1 = [r for r in X.e1(seeds=range(5)) if r["mode"] == "arlc"]
    out["E1 RR (átkat.+alosztály)"] = st.mean(r["rr"] for r in e1)
    out["E1 kollaterális"] = st.mean(r["collateral"] for r in e1)
    e2a = [r for r in X.e2a(Ns=(2, 8, 16), M=25) if r["mode"] == "arlc"]
    flips = [r["flip_at"] or 26 for r in e2a]
    out["E2a átfordulás N=2/8/16"] = "/".join(str(f) for f in flips)
    out["E2a monoton"] = all(a <= b for a, b in zip(flips, flips[1:]))
    e3 = []
    for n in (8, 16):
        for sysm in (True, False):
            r = [x for x in X.e3(n=n, systematic=sysm) if x["mode"] == "arlc"][0]
            e3.append(bool(r["isolated"]) == sysm)
    out["E3 helyes döntés"] = sum(e3) / len(e3)
    e4 = [r for r in X.e4(eps_list=(0.05,), seeds=range(3)) if r["mode"] == "arlc"]
    out["E4 pontosság (ε=0,05)"] = st.mean(r["acc"] for r in e4)
    out["E4 hamis átrendezés/50"] = st.mean(r["struct_events_per50"] for r in e4)
    a7 = [r for r in X.a7() if r["mode"] == "arlc"][0]
    out["A7 (frissítés/revízió) pontosság"] = st.mean(a7[k] for k in ("loc_now", "loc_past", "cat_now", "cat_past"))
    d9 = []
    for truth in ("L", "H"):
        for s in range(3):
            a, ex = tfb.deg9("arlc", s, n_facts=8, truth_tree=truth, noise=0.15)
            d9.append((a, ex["h_rules_active"] if truth == "L" else ex["l_rules_active"]))
    out["TFB-9 pontosság (zaj 0,15)"] = st.mean(a for a, _ in d9)
    out["TFB-9 vesztes fa aktív"] = st.mean(c for _, c in d9)
    out["TFB-2 pontosság"] = tfb.deg2("arlc", 0)[0]
    out["TFB-8 pontosság"] = tfb.deg8("arlc", 0)[0]
    qn = [Q.run_one(nS, nG, m, class_exc=cfg["class_exceptions"]) for nS in (2, 12) for nG in (2, 12) for m in (1, 6)]
    out["Quine: G sosem esik"] = all("G (" not in r["choice"] for r in qn)
    inv = [I.run_one(8, m, cfg["invention"], s, revive=cfg["invent_revive"], class_exc=cfg["class_exceptions"])
           for m in (4, 6) for s in range(2)]
    out["Feltalálás: általánosítás"] = st.mean((r["gen_striped_not_poisonous"] + r["gen_plain_poisonous"]) / 2
                                               for r in inv)
    return out


def run_ablation():
    rows = {}
    for name, ov in ABLATIONS.items():
        with configured(ov) as cfg:
            rows[name] = battery(cfg)
        print(name, json.dumps(rows[name], ensure_ascii=False, default=float), flush=True)
    return rows

# 91. kör: hibrid megbízhatósági kód a befagyasztott szerkezettel
HYBRID_91 = {**FROZEN_88, "rel_hybrid": True}
HYBRID_V_91 = {**HYBRID_91, "cut_per_event": True}
# 91. kör: ÚJ BEFAGYASZTOTT konfiguráció (az előregisztrált 91. kör alapján). A 93. kori negyedik generátor ezt méri.
FROZEN_91 = HYBRID_V_91
# 95. kör: lassan tanuló becsületes komponens (κ₁ = 300) az elmélet-keverékben (Tκ) és a bevált adatforrásokon (Dκ)
F91_TK = {**FROZEN_91, "theory_mix": (0.9, 300.0, 0.5, 2.0)}
F91_TDK = {**F91_TK, "rel_hybrid_kappa": 300.0}
# 96. kör: a hibrid bevált adatforrása lassan tanuló béta-kóddal (κ = 300) a rögzített helyett (jelölt)
F91_DK = {**FROZEN_91, "rel_hybrid_kappa": 300.0}
# 100. kör: megerősítés-függő új-forrás bizalom (jelölt)
F91_C = {**FROZEN_91, "newcomer_corrob": True}
# 102. kör: óvatos hitelesség (jelölt)
F91_Q = {**FROZEN_91, "q_temper": 2.0}
V3_Q = {"q_temper": 2.0}   # csak a temperálás a v3-hoz (a configured() a v4-alapot is beállítja, ezért külön kezelendő)
# 103. kör: egyszerűsített mag (a 95. kori LOO szerint a mért világokban hatástalan vagy enyhén káros kapcsolók nélkül)
V5_CORE = {**FROZEN_91, "q_groups": False, "ind_exc_cost": False, "source_moves": False}
# 107. kör: szabályok időbeli vágása (jelölt)
F91_R = {**FROZEN_91, "rule_cuts": True}
# 112. kör: másolásfelismerés (jelölt)
F91_D = {**FROZEN_91, "copy_detection": True}
# 112. kör: ÚJ BEFAGYASZTOTT konfiguráció (az előregisztrált 112. kör minden kritériumán átment)
FROZEN_112 = F91_D
# 115. kör: általános újranyitó keresés (jelöltek)
F112_O = {**FROZEN_112, "reopen_search": True}
F112_RO = {**F112_O, "rule_cuts": True}
F112_CPO = {**F112_O, "source_changepoints": True}
# 115. kör: ÚJ BEFAGYASZTOTT konfiguráció (az előregisztrált 115. kör minden kritériumán átment)
FROZEN_115 = F112_RO
# 117. kör: aciklikus másolási gráf (jelölt)
F115_A = {**FROZEN_115, "copy_acyclic": True}
