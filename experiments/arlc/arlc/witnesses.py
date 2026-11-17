"""40. kör: tanúk függetlensége (Condorcet, hallomás, rémhír).

Egy szabályt ('dax mérges', N alátámasztással) ellenpéldák támadnak. Az ellenpéldákat k eredeti
forrás figyelte meg, és mindegyiket r további forrás 'továbbadja' (hallomás). Naiv módban minden
továbbadó új, független forrásnak számít; származás-tudatos módban a továbbadott állítás az eredeti
forrás állítása (ugyanaz a tartalom, ugyanaz a forrás -> nem számít újra)."""
from __future__ import annotations

import itertools

from .core import Lit, Memory, Obs, Rule, Schema


def run_one(N, k, r, provenance, q=0.9, q_membership=0.999, exc_prior=None):
    sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + k + 2, n_categories=2, n_props=2)
    mem = Memory(sch, mode="arlc")
    mem.exc_prior = exc_prior
    c = itertools.count(1)
    mem.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)))
    mem.observe(Obs(next(c), "survey", 1, 0.9, lit=Lit("isa", "probe", "dax")))
    t = 1
    for i in range(N):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        mem.observe(Obs(next(c), f"s{i}", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
    seen = set()
    for j in range(k):
        t += 1
        mem.observe(Obs(next(c), "census", t, q_membership, lit=Lit("isa", f"x{j}", "dax")))
        claim = Lit("has", f"x{j}", "poisonous", False)
        for rep in range(r + 1):                    # az eredeti + r továbbadás
            src = f"orig{j}" if (rep == 0 or provenance) else f"relay{j}_{rep}"
            if provenance and (src, claim) in seen:
                continue
            seen.add((src, claim))
            mem.observe(Obs(next(c), src, t, q, lit=claim))
    return mem.answer("probe", "poisonous", record_use=False) is not True


def min_originals(N, r, provenance, kmax=20, q_membership=0.999, exc_prior=None):
    for k in range(1, kmax + 1):
        if run_one(N, k, r, provenance, q_membership=q_membership, exc_prior=exc_prior):
            return k
    return None


def run(Ns=(4, 8, 16), rs=(0, 1, 3, 7), q_memberships=(0.9, 0.999)):
    rows = []
    for qm in q_memberships:
        for N in Ns:
            for r in rs:
                for prov in (False, True):
                    rows.append({"N": N, "relays_per_original": r, "provenance": prov, "q_membership": qm,
                                 "originals_needed": min_originals(N, r, prov, q_membership=qm)})
    return rows
