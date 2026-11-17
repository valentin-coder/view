"""42. kör: mennyire 'azonnali' az átrendezés? Megfigyelésenkénti idő és a meglepetés
feldolgozási ideje a tudásbázis és a függőségi kúp méretének függvényében."""
from __future__ import annotations

import random
import statistics as st
import time

from .core import Lit, Memory, Obs, Rule
from .experiments import Counter_, Taxo, stream_base


def run_one(n_roots, branching, per_leaf, seed=0, surprise="subclass"):
    tx = Taxo(seed, n_roots=n_roots, branching=branching, levels=3, per_leaf=per_leaf)
    ctr = Counter_()
    obs, t = stream_base(tx, ctr, rng=random.Random(seed))
    mem = Memory(tx.schema(), mode="arlc")
    times = []
    for o in obs:
        t0 = time.perf_counter()
        mem.observe(o)
        times.append(time.perf_counter() - t0)
    rng = random.Random(seed + 1)
    leaf = rng.choice(tx.leaves)
    if surprise == "subclass":
        root = tx.chain(leaf)[-1]
        newpar = rng.choice([c for c in tx.cats if tx.level[c] == 1 and tx.chain(c)[-1] != root])
        s = Obs(next(ctr), "expert", t, 0.999, rule=Rule(leaf, "isa", newpar, True))
        cone = sum(1 for e, l in tx.entities.items() if l == leaf)
    else:
        e = next(x for x, l in tx.entities.items() if l == leaf)
        other = rng.choice([l for l in tx.leaves if tx.chain(l)[-1] != tx.chain(leaf)[-1]])
        s = Obs(next(ctr), "expert", t, 0.999, lit=Lit("isa", e, other, True))
        cone = 1
    t0 = time.perf_counter()
    mem.observe(s)
    t_surprise = time.perf_counter() - t0
    return {"categories": len(tx.cats), "entities": len(tx.entities), "n_obs": len(obs), "surprise": surprise,
            "members_affected": cone, "obs_time_median_ms": 1000 * st.median(times),
            "obs_time_p95_ms": 1000 * sorted(times)[int(0.95 * len(times))], "obs_time_total_s": sum(times),
            "surprise_time_ms": 1000 * t_surprise}


def run(configs=((3, 2, 2), (3, 2, 4), (3, 3, 2), (3, 3, 4), (4, 3, 3), (3, 4, 2))):
    rows = []
    for nr, br, pl in configs:
        for sp in ("recat", "subclass"):
            rows.append(run_one(nr, br, pl, surprise=sp))
            print(rows[-1], flush=True)
    return rows
