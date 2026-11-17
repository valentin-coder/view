"""30. kör: kategória-feltalálás anomáliákból (Thagard 6. fokozat, predikátum-invenció)."""
from __future__ import annotations

import itertools
import random

from .core import Lit, Memory, Obs, Rule, Schema

OTHER_ATTRS = ["heavy", "shiny", "slow", "warm", "noisy"]


def run_one(N, m, invention, seed, q_anom=0.9, distractor_rate=0.4, mixed=0, revive=False, class_exc=True):
    """N normál dax (mérges, nem csíkos), m anomális dax (csíkos, nem mérges), véletlen egyéb
    attribútumokkal. mixed: ennyi normál dax is csíkos (a jel nem tiszta)."""
    rng = random.Random(seed)
    sch = Schema(n_entities=N + m + 10, n_categories=4, n_props=8)
    mem = Memory(sch, mode="arlc", reliability="beta", prior_strength=30, depth=3, beam=6)
    mem.class_exceptions = class_exc
    mem.invention = invention
    mem.invent_revive = revive
    c = itertools.count(1)
    mem.observe(Obs(next(c), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True)))
    t = 0
    ents = [(f"n{i}", False) for i in range(N)] + [(f"a{j}", True) for j in range(m)]
    rng.shuffle(ents)
    for idx, (e, is_anom) in enumerate(ents):
        t += 1
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", e, "dax")))
        striped = is_anom or (not is_anom and int(e[1:]) < mixed)
        mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("has", e, "striped", striped)))
        for a in OTHER_ATTRS:
            if rng.random() < distractor_rate:
                mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("has", e, a, True)))
        mem.observe(Obs(next(c), "field" if not is_anom else f"lab{e}", t, 0.9 if not is_anom else q_anom,
                        lit=Lit("has", e, "poisonous", not is_anom)))
    # általánosítási teszt: új, nem látott entitások
    t += 1
    tests = []
    for k in range(4):
        for striped in (True, False):
            e = f"new{k}{'s' if striped else 'p'}"
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("isa", e, "dax")))
            mem.observe(Obs(next(c), "survey", t, 0.9, lit=Lit("has", e, "striped", striped)))
            tests.append((e, striped))
    b = mem.best
    invented = [o.rule for o in b.ind if o.rule.cond is not None]
    gen_striped = sum(mem.answer(e, "poisonous", record_use=False) is False for e, s in tests if s) / 4
    gen_plain = sum(mem.answer(e, "poisonous", record_use=False) is True for e, s in tests if not s) / 4
    seen_anom = sum(mem.answer(e, "poisonous", record_use=False) is False for e, a in ents if a) / max(1, m)
    return {"N": N, "m": m, "invention": invention, "revive": revive, "seed": seed, "mixed": mixed,
            "invented": [f"{r.body}&{r.cond}" for r in invented],
            "rule_kept": 1 not in b.rej, "n_instance_exc": sum(1 for x in b.exc if not str(x[1]).startswith("cat:")),
            "gen_striped_not_poisonous": gen_striped, "gen_plain_poisonous": gen_plain,
            "seen_anomalies_explained": seen_anom}


def run(Ns=(4, 8), ms=(1, 2, 3, 4, 6), seeds=range(3), mixed_list=(0, 1)):
    rows = []
    for N, m, (inv, rev), seed, mixed in itertools.product(Ns, ms, ((False, False), (True, False), (True, True)),
                                                         seeds, mixed_list):
        rows.append(run_one(N, m, inv, seed, mixed=mixed, revive=rev))
    return rows
