"""113. kör: a másolásfelismerés hamis riasztása – független tanúk egy hibás tankönyvi szabály ellen. Előregisztrált,
friss seedek 40000–40029.
    python -m arlc.run_r113
"""
import json
import math
import os
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator4 import make_case4
from .procedural import accuracy, evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-113", "test")
VARIANTS = {"v3": None, "FROZEN_91": V4.FROZEN_91, "FROZEN_112": V4.FROZEN_112}


def job(a):
    seed, vi = a
    name = list(VARIANTS)[vi]
    path = os.path.join(OUT, f"{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, w = make_case4(seed, "független tanúk")
    cfg = VARIANTS[name]
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
    for o in obs:
        m.observe(o)
    row = {"seed": seed, "variant": name, "n_target": len(tq), "target_before": accuracy(m, tq)}
    for o in new:
        m.observe(o)
    row.update({"target_after": accuracy(m, tq), "post": evaluate(m, post), "dup": sorted(m.beam[0].dup),
                "witness_rejected": sum(1 for o in new if o.id in m.beam[0].rej)})
    json.dump(row, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, [(s, vi) for s in range(40000, 40030) for vi in range(3)]):
            print(*r, flush=True)
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT) if f.endswith(".json")]
    out = {}
    for v in VARIANTS:
        rv = [r for r in rows if r["variant"] == v and r["n_target"]]
        out[v] = {"esetek": len(rv), "target előtte": round(sum(r["target_before"] for r in rv) / len(rv), 4),
                  "target utána": round(sum(r["target_after"] for r in rv) / len(rv), 4),
                  "post": round(sum(r["post"] for r in rv) / len(rv), 4),
                  "másolásnak minősítve": sum(1 for r in rv if r["dup"]),
                  "tanú félretett állításai (átlag)": round(sum(r["witness_rejected"] for r in rv) / len(rv), 2)}
    json.dump(out, open(os.path.join(OUT, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print("KÉSZ", flush=True)
