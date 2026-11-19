"""82. kör: menekülőút-audit (előregisztrált, friss seedek 19000–19019).
    python -m arlc.run_r82
Elemzési terv: docs/korok/82-menekulout-audit.md (a futtatás előtt commitolva).
"""
import json
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit, world_g1, world_g2
from .core import Memory
from .generator2 import make_case2
from .procedural import accuracy, evaluate
from .run_r55 import is_garbage, make_case
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-82", "test")
SEEDS = range(19000, 19020)
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
V49 = {**V48, **V4.V49_SM}
VARIANTS = {"v3": None, "v4.9": V49, "v4.9+PK": {**V49, "priority_exceptions": True, "priority_code": True}}
CASES = [("G2", ""), ("G1", "A"), ("G1", "B")]
KIND = "hazug forrás"


def job(a):
    gen, pop, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}{pop}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, KIND)
        pi, w = {"book": 0.999}, world_g2(seed)
    else:
        sch, obs, new, pre, post, tq, _ = make_case(seed, KIND, pop)
        pi, w = PI_META[pop], world_g1(seed)
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(pi)
    for o in obs:
        m.observe(o)
    row = {"gen": gen, "pop": pop, "seed": seed, "variant": name, "pre": evaluate(m, pre),
           "audit_pre": audit(m, w, gen), "garbage": (pop == "B" and is_garbage(seed))}
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq),
                "liar_rejected": sum(1 for o in new if o.id in H.rej), "liar_n": len(new),
                "audit_post": audit(m, w, gen, obs_ids={o.id for o in obs}), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, p, s, vi) for (g, p) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
