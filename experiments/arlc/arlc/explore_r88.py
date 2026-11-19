"""88. kör, FELTÁRÓ (nem előregisztrált): a G3-kudarc két komponensének szétválasztása ugyanazokon a seedeken.
(a) a séma állapotváltozási priorja (0,05 vs. a valódi gyakorisághoz közelebbi 0,3); (b) az N keverék-prior.
    python -m arlc.explore_r88
"""
import json
import os
from multiprocessing import Pool

from . import v4 as V4
from .audit_truth import audit
from .core import Memory
from .generator3 import KINDS3, make_case3
from .procedural import accuracy, evaluate
from .run_r88 import SEEDS, acc_at

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-88", "explore")
NO_N = {k: v for k, v in V4.FROZEN_88.items() if k != "source_newcomer"}
VARIANTS = {("befagyasztott − N", 0.05): NO_N, ("v3", 0.3): None, ("befagyasztott", 0.3): V4.FROZEN_88,
            ("befagyasztott − N", 0.3): NO_N}


def job(a):
    kind, seed, vi = a
    (name, upd), cfg = list(VARIANTS.items())[vi]
    path = os.path.join(OUT, f"{KINDS3.index(kind)}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, hq, tau, w = make_case3(seed, kind, upd)
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
    for o in obs:
        m.observe(o)
    row = {"kind": kind, "seed": seed, "variant": name, "upd": upd, "pre": evaluate(m, pre), "audit_pre": audit(m, w, "G3")}
    for o in new:
        m.observe(o)
    H = m.beam[0]
    row.update({"post": evaluate(m, post), "target": accuracy(m, tq), "hist": acc_at(m, hq, tau - 1),
                "new_rejected": sum(1 for o in new if o.id in H.rej), "new_n": len(new), "cuts": len(H.cut)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(k, s, vi) for k in KINDS3 for s in SEEDS for vi in range(len(VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
