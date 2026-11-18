"""49. kör: megfigyelési ekvivalencia-audit („álcázott elutasítás” keresése).

Egy elfogadott o állítás elutasítása (H + rej{o}) egy meghatározott hiedelemállapotot ad: a fő
kontextus zárását. Ha egy MÁS lépés (osztályszintű kivétel, a forrás kontextusba izolálása,
példányszintű kivételek az összes alkalmazásra) ugyanezt a zárást adja, akkor ugyanazt a
hiedelemállapotot más áron fejezi ki. Ha olcsóbb, az elutasítás hitelesség-ellenőrzése
megkerülhető. A 19., 26. (helyi kiút) és 48. (felső osztályos kivétel) kör hibái ilyenek voltak.

A zárás-aláírás: minden entitás összes levezetett (isa, has) literálja a fő kontextusban.
Példányszintű kivételeknél az ekvivalencia csak a meglévő entitásokra igaz (egy új tagra a szabály
továbbra is vonatkozik), ezért ezeket külön, „gyenge ekvivalencia” címkével jelentem.
"""
from __future__ import annotations

from dataclasses import replace

from .core import IND_BASE, Memory


def signature(mem: Memory, H) -> frozenset:
    cl = mem.closure(H, None, mem.now)
    out = []
    for e, d in cl.isa.items():
        out += [("isa", e, c, p) for (c, p) in d]
    for e, d in cl.has.items():
        out += [("has", e, c, p) for (c, p) in d]
    return frozenset(out)


def _apps(mem, H, o):
    """Az o szabály alkalmazásai a zárásban: (o.id, e) párok."""
    cl = mem.closure(H, None, mem.now)
    r = o.rule
    return [(o.id, e) for e, d in cl.isa.items() if (r.body, True) in d and (o.id, e) not in H.exc]


def audit(mem: Memory, H=None, max_claims=None):
    H = H or mem.best
    rows = []
    claims = [o for o in mem.obs if o.id not in H.rej and o.q < 1.0 and o.source not in H.iso]
    if max_claims:
        claims = claims[:max_claims]
    base_score = mem.score(H)
    for o in claims:
        Hr = replace(H, rej=H.rej | {o.id})
        if mem.closure(Hr, None, mem.now).conflict is not None and mem.closure(H, None, mem.now).conflict is None:
            continue
        sig_r = signature(mem, Hr)
        if sig_r == signature(mem, H):
            continue                       # az állítás nem hat semmire: nincs mit neutralizálni
        cost_rej = mem.score(Hr) - base_score
        alts = []
        if o.rule is not None and o.rule.cond is None:
            # osztályszintű kivétel bármely kategóriára (szigorú specifikusságtól függetlenül vizsgálva)
            cats = {c for e, d in mem.closure(H, None, mem.now).isa.items() for (c, p) in d if p}
            for c in sorted(cats):
                if c == o.rule.body:
                    continue
                Hc = replace(H, exc=H.exc | {(o.id, "cat:" + c)})
                if signature(mem, Hc) == sig_r:
                    proper = mem._proper_sub(H, c, o.rule.body)
                    # erős ekvivalencia csak akkor, ha c nem szigorú alosztály (minden jövőbeli tagra is
                    # hatástalanítja a szabályt); egy szigorú alosztályra vonatkozó kivétel gyenge
                    alts.append(("osztálykivétel" + ("" if proper else " (nem alosztály)"), mem.score(Hc) - base_score,
                                 not proper))
            apps = _apps(mem, H, o)
            if apps:
                He = replace(H, exc=H.exc | set(apps))
                if signature(mem, He) == sig_r:
                    alts.append((f"{len(apps)} példánykivétel", mem.score(He) - base_score, False))
        if o.source not in H.iso:
            Hi = replace(H, iso=H.iso | {o.source})
            same_src = [x for x in mem.obs if x.source == o.source and x.id not in H.rej]
            if len(same_src) == 1 and signature(mem, Hi) == sig_r:
                alts.append(("kontextus-izolálás", mem.score(Hi) - base_score, True))
        for name, cost, strong in alts:
            rows.append({"claim": o.id, "kind": "szabály" if o.rule is not None else "tény", "source": o.source,
                         "q": o.q, "alt": name, "strong": strong, "cost_rej": cost_rej, "cost_alt": cost,
                         "cheaper": cost < cost_rej - 1e-9})
    return rows


def whole_source(mem: Memory, H=None):
    """Egy egész forrás elutasítása vs. kontextusba izolálása (mindkettő a fő kontextusban a forrás
    összes állítását hatástalanítja)."""
    H = H or mem.best
    base = mem.score(H)
    out = []
    for src in sorted({o.source for o in mem.obs}):
        ids = {o.id for o in mem.obs if o.source == src and o.q < 1.0}
        if not ids or src in H.iso:
            continue
        Hr = replace(H, rej=H.rej | ids)
        Hi = replace(H, iso=H.iso | {src})
        out.append({"source": src, "n": len(ids), "same_signature": signature(mem, Hr) == signature(mem, Hi),
                    "cost_reject_all": mem.score(Hr) - base, "cost_isolate": mem.score(Hi) - base})
    return out
