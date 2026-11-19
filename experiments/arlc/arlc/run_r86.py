"""86. kör: a forrástípus-prior tanulható (metaadat nélküli) változata (előregisztrált, friss seedek 22000–22019).
    python -m arlc.run_r86
Elemzési terv: docs/korok/86-tanulhato-forrastipus.md (a futtatás előtt commitolva).
"""
import json
import os
import time
from collections import Counter
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit, world_g1, world_g2
from .core import Memory
from .g1k import make_case_k
from .generator2 import make_case2
from .procedural import accuracy, evaluate
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-86", "test")
SEEDS = range(22000, 22020)
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
PK = {"priority_exceptions": True, "priority_code": True}
VARIANTS = {"T nélkül": {**V48, **PK}, "T (metaadat)": {**V48, **PK, **V4.V49_SM},
            "N (új forrás)": {**V48, **PK, **V4.V49_N}, "U (egyforma)": {**V48, **PK, **V4.V49_U}}
CASES = [("G1k", "A", "hazug forrás"), ("G1k", "A", "átkategorizálás"), ("G1k", "C", "hazug forrás"),
         ("G2", "", "hazug forrás"), ("G2", "", "torzított forrás")]


def job(a):
    gen, pop, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}{pop}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
        pi, w = {"book": 0.999}, world_g2(seed)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, pop)
        pi, w = PI_META[pop], world_g1(seed)
    t0 = time.time()
    with V4.configured(VARIANTS[name]):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(pi)
    for o in obs:
        m.observe(o)
    row = {"gen": gen, "pop": pop, "kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre)}
    if pop != "C":
        row["audit_pre"] = audit(m, w, "G2" if gen == "G2" else "G1")
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq),
                "new_rejected": sum(1 for o in new if o.id in H.rej), "new_n": len(new),
                "rej_post": dict(Counter(m.by_id[i].source for i in H.rej if i in m.by_id)),
                "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, p, k, s, vi) for (g, p, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))
            if not (p == "C" and list(VARIANTS)[vi].startswith("U"))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
