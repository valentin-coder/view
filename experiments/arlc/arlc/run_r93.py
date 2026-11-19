"""93. kör: a FROZEN_91 a negyedik generátoron (G4: forrásfüggőség és forrásváltozás). Előregisztrált, friss seedek
29000–29019.
    python -m arlc.run_r93
Elemzési terv: docs/korok/93-g4.md (a G4 első rendszerfuttatása előtt commitolva).
"""
import json
import os
import time
from collections import Counter
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit
from .core import Memory
from .generator4 import KINDS4, make_case4
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-93", "test")
SEEDS = range(29000, 29020)
VARIANTS = {"v3": None, "FROZEN_88": V4.FROZEN_88, "FROZEN_91": V4.FROZEN_91}


def job(a):
    kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{KINDS4.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, w = make_case4(seed, kind)
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
    for o in obs:
        m.observe(o)
    row = {"kind": kind, "seed": seed, "variant": name, "pre": evaluate(m, pre), "audit_pre": audit(m, w, "G4")}
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq),
                "new_rejected": dict(Counter(o.source for o in new if o.id in H.rej)),
                "new_n": dict(Counter(o.source for o in new)), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, s, vi) for k in KINDS4 for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
