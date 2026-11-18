"""57. kör, feltáró: a kétszintű v4.4 (κ_T = 1) a C populáción (rivális tankönyvek). Nem előregisztrált."""
import json
import os
import sys
from multiprocessing import Pool

from . import procedural as P
from . import v4 as V4
from .run_r44 import KINDS
from .run_r55 import make_case, run_mem

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-57", "C_v4.4")


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, bad = make_case(seed, KINDS[ki], "C")
    m, t = run_mem(sch, obs, new, V4.V44_OVERRIDES)
    row = {"seed": seed, "kind": KINDS[ki], "garbage": bad, "post_v4.4": P.evaluate(m, post),
           "target_v4.4": P.accuracy(m, tq), "t": t}
    for b in ("book", "book2"):
        ids = [o.id for o in m.obs if o.source == b]
        row[f"dismissed_{b}"] = (b in m.best.iso) or sum(i in m.best.rej for i in ids) >= 0.9 * len(ids)
        row[f"iso_{b}"] = b in m.best.iso
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in range(5000, 5030) for ki in range(len(KINDS))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as pool:
        for a in pool.imap_unordered(job, jobs):
            print(*a, flush=True)
