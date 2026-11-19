"""80. kör, fejlesztési ellenőrzés (NEM teszt): a forrástípus-prior a már felhasznált 78. köri seedeken."""
import json
import os
import sys
from collections import Counter
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator2 import make_case2
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-80", "dev")
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
VARIANTS = {"v3": None, "v4.4e": V4.V44E_OVERRIDES, "v4.4e+T": {**V4.V44E_OVERRIDES, **V4.V49_SM},
            "v4.8-π": V48, "v4.8-π+T": {**V48, **V4.V49_SM}}


def run(sch, obs, new, cfg, pi):
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(pi)
    return m


def job(a):
    gen, pop, seed, kind, name = a
    path = os.path.join(OUT, f"{gen}{pop}_{KINDS.index(kind) if gen == 'G1' else 0}_{seed}_{list(VARIANTS).index(name)}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
        pi = {"book": 0.999}
    else:
        sch, obs, new, pre, post, tq, _ = make_case(seed, kind, pop)
        pi = PI_META[pop]
    m = run(sch, obs, new, VARIANTS[name], pi)
    for o in obs:
        m.observe(o)
    pre_acc = evaluate(m, pre)
    for o in new:
        m.observe(o)
    H = m.beam[0]
    rej = Counter(m.by_id[i].source for i in H.rej if i in m.by_id)
    row = {"gen": gen, "pop": pop, "seed": seed, "kind": kind, "variant": name, "pre": pre_acc,
           "post": evaluate(m, post), "target": accuracy(m, tq), "rej": dict(rej)}
    json.dump(row, open(path, "w"))
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [("G2", "", s, "hazug forrás", n) for s in range(16000, 16020) for n in VARIANTS]
    jobs += [("G1", p, s, "hazug forrás", n) for p in ("A", "B") for s in range(16000, 16006) for n in VARIANTS]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
