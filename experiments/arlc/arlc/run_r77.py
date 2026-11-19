"""77. kör: a második, független generátoron (generator2.py) mért összevetés (előregisztrált).
Módszerek: wms, v3, v4.4e, v4.8-π (a tankönyv π-je 0,999: gondozott). Egyetlen kapcsolót sem hangolok erre a generátorra.
    python -m arlc.run_r77 4
"""
import json
import os
import sys
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator2 import KINDS2, make_case2
from .procedural import accuracy, evaluate
from .run_r75 import brier_map

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-77")
SEEDS = range(15000, 15020)


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq = make_case2(seed, KINDS2[ki])
    row = {"seed": seed, "kind": KINDS2[ki]}
    for name in ("wms", "v3", "v4.4e", "v4.8-π"):
        if name in ("wms", "v3"):
            m = Memory(sch, mode="wms" if name == "wms" else "arlc")
        else:
            cfg = dict(V4.V44E_OVERRIDES)
            if name == "v4.8-π":
                cfg.update({"theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)})
            with V4.configured(cfg):
                m = Memory(sch, mode="arlc")
            if name == "v4.8-π":
                m.theory_pi = {"book": 0.999}
        for o in obs:
            m.observe(o)
        row[f"pre_{name}"] = evaluate(m, pre)
        for o in new:
            m.observe(o)
        row[f"post_{name}"], row[f"target_{name}"], row[f"brier_{name}"] = evaluate(m, post), accuracy(m, tq), brier_map(m, post)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in SEEDS for ki in range(len(KINDS2)) if not os.path.exists(os.path.join(OUT, f"{ki}_{s}.json"))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as pool:
        for x in pool.imap_unordered(job, jobs):
            print(*x, flush=True)
