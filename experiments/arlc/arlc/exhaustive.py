"""36. kör (előkészítés): kimerítő ellenőrzés kis feladatokon. A legjobb online hipotézis
pontszámát összevetjük az összes (elutasítás-részhalmaz × példányszintű kivétel-részhalmaz)
hipotézis globális optimumával, a saját célfüggvényünk szerint."""
from __future__ import annotations

import itertools
import random

from .core import Hyp, Lit, Memory, Obs, Rule, Schema


def all_instance_tokens(mem: Memory) -> list:
    toks = set()
    H = Hyp()
    for ctx in (None,):
        cl = mem.closure(H, ctx, mem.now)
        for d in list(cl.isa.values()) + list(cl.has.values()):
            for sup in d.values():
                for t in sup:
                    if t[0] == "inst":
                        toks.add((t[1], t[2]))
    return sorted(toks)


def exhaustive_best(mem: Memory, max_rej=None):
    obs_ids = [o.id for o in mem.obs if o.q < 1.0]
    insts = all_instance_tokens(mem)
    best = (float("inf"), None)
    n = 0
    for k in range(0, (max_rej or len(obs_ids)) + 1):
        for rej in itertools.combinations(obs_ids, k):
            for j in range(0, len(insts) + 1):
                for exc in itertools.combinations(insts, j):
                    H = Hyp(rej=frozenset(rej), exc=frozenset(exc))
                    n += 1
                    if mem.find_conflict(H) is None:
                        sc = mem.score(H)
                        if sc < best[0] - 1e-9:
                            best = (sc, H)
    return best, n


def random_problem(seed, n_ent=3, n_facts=4, n_rules=2):
    rng = random.Random(seed)
    cats, props = ["dax", "fep"], ["p", "r"]
    sch = Schema(disjoint={frozenset(("dax", "fep"))}, n_entities=n_ent + 1, n_categories=2, n_props=2)
    obs, c, t = [], itertools.count(1), 0
    for _ in range(n_rules):
        obs.append(Obs(next(c), rng.choice(["b1", "b2"]), 0, rng.choice([0.8, 0.9, 0.95]),
                       rule=Rule(rng.choice(cats), "has", rng.choice(props), rng.random() < 0.5)))
    for i in range(n_ent):
        t += 1
        obs.append(Obs(next(c), rng.choice(["s1", "s2"]), t, rng.choice([0.8, 0.9]),
                       lit=Lit("isa", f"e{i}", rng.choice(cats))))
    for _ in range(n_facts):
        t += 1
        obs.append(Obs(next(c), rng.choice(["s1", "s2", "s3"]), t, rng.choice([0.7, 0.8, 0.9, 0.95]),
                       lit=Lit("has", f"e{rng.randrange(n_ent)}", rng.choice(props), rng.random() < 0.5)))
    return sch, obs


def check(seeds=range(40), modes=("arlc", "arlc-noctx")):
    rows = []
    for seed in seeds:
        sch, obs = random_problem(seed)
        mem = Memory(sch, mode="arlc-noctx", induce=False)
        mem.mode = "arlc-noctx"
        for o in obs:
            mem.observe(o)
        online = mem.score(mem.best)
        (opt, Hopt), n = exhaustive_best(mem)
        rows.append({"seed": seed, "n_obs": len(obs), "n_hyp": n, "online": online, "optimum": opt,
                     "gap": online - opt, "online_has_cut_or_iso": bool(mem.best.cut or mem.best.iso)})
    return rows
