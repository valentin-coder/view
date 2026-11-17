"""38. kör: Quine hiedelemhálója – melyik szabályt adja fel az ARLC egy lánc mentén?

Szabályok: dax ⊂ állat (S), állat → élő (G). Alátámasztás: n_S megfigyelt dax 'élő' ténnyel
(ezt S és G együtt jósolja), n_G megfigyelt nem-dax állat 'élő' ténnyel (csak G jósolja).
Anomália: m darab 'x_j egy dax, és nem élő'. Lehetséges revíziók: S elvetése, G elvetése,
kivételek, vagy az anomáliák elutasítása."""
from __future__ import annotations

import itertools
import math

from .core import Lit, Memory, Obs, Rule, Schema


def run_one(n_S, n_G, m, q_S=0.95, q_G=0.95, class_exc=True):
    sch = Schema(disjoint=set(), n_entities=n_S + n_G + m + 2, n_categories=3, n_props=2)
    mem = Memory(sch, mode="arlc", induce=False)
    mem.class_exceptions = class_exc
    c = itertools.count(1)
    S = Obs(next(c), "taxonomy", 0, q_S, rule=Rule("dax", "isa", "animal", True))
    G = Obs(next(c), "biology", 0, q_G, rule=Rule("animal", "has", "alive", True))
    mem.observe(S)
    mem.observe(G)
    t = 0
    for i in range(n_S):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        mem.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", f"d{i}", "alive", True)))
    for i in range(n_G):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"a{i}", "animal")))
        mem.observe(Obs(next(c), "field", t, 0.9, lit=Lit("has", f"a{i}", "alive", True)))
    for j in range(m):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"x{j}", "dax")))
        mem.observe(Obs(next(c), f"lab{j}", t, 0.9, lit=Lit("has", f"x{j}", "alive", False)))
    b = mem.best
    cls = [x for x in b.exc if isinstance(x[1], str) and x[1].startswith("cat:")]
    if S.id in b.rej and G.id in b.rej:
        choice = "mindkettő"
    elif S.id in b.rej:
        choice = "S (dax ⊂ állat) feladva"
    elif G.id in b.rej:
        choice = "G (állat → élő) feladva"
    elif cls:
        choice = "G hatókör-szűkítése (osztályszintű kivétel)"
    elif b.exc:
        choice = "példány-kivétel"
    else:
        choice = "anomália elutasítva / újraértelmezve"
    return {"n_S": n_S, "n_G": n_G, "m": m, "choice": choice}


def predicted(n_S, n_G, m, q=0.95, delta=0.05, nE=None):
    """Zárt alakú becslés: a jelöltek költségkülönbsége a 'mindent megtart, anomáliákat elutasít'
    hipotézishez képest (bitben)."""
    lo = math.log2(q / (1 - q))                     # egy szabály elvetésének forrásköltsége
    lost = 1 + math.log2(1 - delta)                 # egy jósolt tény jóslatának elvesztése
    rej_anom = math.log2(0.9 / 0.1)                 # egy anomália elutasítása
    nE = nE or (n_S + n_G + m + 2)
    costs = {
        "anomália elutasítva / újraértelmezve": m * rej_anom,
        # S elvetése: a daxok nem állatok -> a d_i 'élő' tényei jóslat nélkül maradnak
        "S (dax ⊂ állat) feladva": lo + n_S * lost,
        # G elvetése: senki 'élő' ténye nincs jósolva
        "G (állat → élő) feladva": lo + (n_S + n_G) * lost,
        "példány-kivétel": m * math.log2(nE),
        "G hatókör-szűkítése (osztályszintű kivétel)": math.log2(3) + 1 + n_S * lost,
    }
    return min(costs, key=costs.get), costs


def run(n_S_list=(0, 2, 6, 12), n_G_list=(0, 2, 6, 12), m_list=(1, 3, 6), class_exc=True):
    rows = []
    for n_S, n_G, m in itertools.product(n_S_list, n_G_list, m_list):
        r = run_one(n_S, n_G, m, class_exc=class_exc)
        p, _ = predicted(n_S, n_G, m)
        r["predicted"] = p
        rows.append(r)
    return rows
