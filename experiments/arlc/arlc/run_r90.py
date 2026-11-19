"""90. kör: temperált megbízhatósági kód (SafeBayes-szerű), prequential η-választással. Előregisztrált, friss seedek
25000–25019; G1k-A, G2, G3 (kalibrált változási prior, upd = 0,3).
    python -m arlc.run_r90
Elemzési terv: docs/korok/90-temperalt-kod.md (a futtatás előtt commitolva).
"""
import json
import math
import os
import time
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator2 import make_case2
from .generator3 import make_case3
from .procedural import accuracy, evaluate
from .run_r60 import PI_META
from .run_r88 import acc_at

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-90", "test")
SEEDS = range(25000, 25020)
ETAS = (0.0, 0.5, 1.0)
VARIANTS = {"v3": None, **{f"η={e}": {**V4.FROZEN_88, "rel_temper": e} for e in ETAS}}
CASES = [("G1k", "hazug forrás"), ("G1k", "átkategorizálás"), ("G2", "hazug forrás"), ("G2", "torzított forrás"),
         ("G3", "hazug forrás"), ("G3", "állapotváltozás"), ("G3", "elavult forrás")]
L_HIT, L_UNK, L_MISS = -math.log2(0.9), 1.0, -math.log2(0.1)


def preq_loss(m, o):
    """A következő megfigyelés előrejelzésének vesztesége (bit), mielőtt a rendszer látná."""
    if o.lit is None or o.lit.pred != "has":
        return 0.0
    a = m.answer(o.lit.subj, o.lit.obj, record_use=False)
    return L_UNK if a is None else (L_HIT if a == o.lit.pos else L_MISS)


def job(a):
    gen, kind, seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    hq, tau = None, None
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    elif gen == "G3":
        sch, obs, new, pre, post, tq, hq, tau, _ = make_case3(seed, kind, 0.3)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    t0 = time.time()
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
    loss = 0.0
    for o in obs:
        loss += preq_loss(m, o)
        m.observe(o)
    row = {"gen": gen, "kind": kind, "seed": seed, "variant": name, "preq_loss": loss, "pre": evaluate(m, pre)}
    for o in new:
        m.observe(o)
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq),
                "hist": acc_at(m, hq, tau - 1) if hq is not None else float("nan"), "sec": round(time.time() - t0, 1)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in CASES for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
