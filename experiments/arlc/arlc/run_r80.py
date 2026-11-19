"""80. kör: forrástípus-prior (előregisztrált teszt, friss seedek 17000–17019).
    python -m arlc.run_r80
Elemzési terv: docs/korok/80-forrastipus-prior.md (a futtatás előtt commitolva).
"""
import json
import os
import random
from collections import Counter
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator2 import World2, make_case2, stream2
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-80", "test")
SEEDS = range(17000, 17020)
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
VARIANTS = {"v3": None, "v4.8-π": V48, "v4.8-π+T": {**V48, **V4.V49_SM}}
CASES = [("G1", "A", k) for k in ("átkategorizálás", "hazug forrás")] + \
        [("G2", "", k) for k in ("hazug forrás", "szabály-helyesbítés")]


def n_book_errors2(seed):
    rng = random.Random(seed)
    w = World2(rng)
    stream2(w, rng)
    return len(w.book_errors)


def job(a):
    gen, pop, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}{pop}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
        pi = {"book": 0.999}
    else:
        sch, obs, new, pre, post, tq, _ = make_case(seed, kind, pop)
        pi = PI_META[pop]
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(pi)
    for o in obs:
        m.observe(o)
    pre_acc = evaluate(m, pre)
    rej_pre = Counter(m.by_id[i].source for i in m.beam[0].rej if i in m.by_id)
    for o in new:
        m.observe(o)
    rej = Counter(m.by_id[i].source for i in m.beam[0].rej if i in m.by_id)
    row = {"gen": gen, "pop": pop, "kind": kind, "seed": seed, "variant": name, "pre": pre_acc,
           "post": evaluate(m, post), "target": accuracy(m, tq), "rej_pre": dict(rej_pre), "rej": dict(rej),
           "book_errors": n_book_errors2(seed) if gen == "G2" else None}
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, p, k, s, vi) for (g, p, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
