"""37. kör: tömörítés és felejtés."""
from __future__ import annotations

import itertools

from .core import Lit, Memory, Obs, Rule, Schema


def flip_point(N, variant, M=30, contradict_old=False):
    """variant: 'nincs' | 'összesítő' | 'naiv'. contradict_old: az anomáliák a már elfelejtett,
    alátámasztó daxokról szólnak (nem új entitásokról)."""
    sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + M + 2, n_categories=2, n_props=2)
    mem = Memory(sch, mode="arlc")
    c = itertools.count(1)
    mem.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)))
    mem.observe(Obs(next(c), "survey", 1, 0.9, lit=Lit("isa", "probe", "dax")))
    t = 1
    for i in range(N):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        mem.observe(Obs(next(c), f"s{i}", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
    n_before = len(mem.obs)
    dropped = 0
    if variant != "nincs":
        dropped = mem.consolidate(keep_summary=(variant == "összesítő"))
    flip = None
    for j in range(1, M + 1):
        t += 1
        ent = f"d{(j - 1) % N}" if contradict_old else f"x{j}"
        if not contradict_old:
            mem.observe(Obs(next(c), f"a{j}", t, 0.9, lit=Lit("isa", ent, "dax")))
        mem.observe(Obs(next(c), f"a{j}", t, 0.9, lit=Lit("has", ent, "poisonous", False)))
        if mem.answer("probe", "poisonous", record_use=False) is not True:
            flip = j
            break
    return {"N": N, "variant": variant, "contradict_old": contradict_old, "flip_at": flip,
            "obs_before": n_before, "dropped": dropped}


def run(Ns=(2, 4, 8, 12, 16)):
    return [flip_point(N, v, contradict_old=co) for N in Ns for v in ("nincs", "összesítő", "naiv")
            for co in (False, True)]
