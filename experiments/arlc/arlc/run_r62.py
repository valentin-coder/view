"""62. kör: a 60. kör H60d-kudarcának szétbontása a „más régió” eseteken (A, B, C × 6000–6019).
Változatok: v4.8-π (metaadat-π, jel nélkül, minden forrás kontextusa 6 bit), v4.8-a0.99 (jel 0,99 pontossággal)."""
import json
import os
import sys
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .run_r44 import KINDS
from .run_r55 import make_case
from .run_r60 import PI_META, SEEDS, answers_metrics, ctx_costs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-62")
KI = KINDS.index("más régió")


def run(sch, obs, new, pop, cc, c_ctx):
    with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0), "ctx_cost": cc}):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(PI_META[pop])
    m.c_ctx = c_ctx
    for o in obs + new:
        m.observe(o)
    return m


def job(a):
    pop, seed = a
    path = os.path.join(OUT, f"{pop}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case(seed, KINDS[KI], pop)
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    keys = {(e, p) for e, p, _ in q} | {(e, p) for e, p, _ in tq}
    sources = {o.source for o in obs + new}
    row = {"pop": pop, "seed": seed}
    for name, cc, c in (("v4.8-π", {}, 6.0), ("v4.8-a0.99", ctx_costs(sources, KINDS[KI], seed, KI, 0.99), 1e6)):
        m = run(sch, obs, new, pop, cc, c)
        mp, mt = answers_metrics(m, keys, q, tq)
        row.update({f"post_{name}": mp["acc"], f"target_{name}": mt.get("acc"), f"iso_{name}": sorted(m.best.iso),
                    f"region2_rejected_{name}": sum(1 for i in m.best.rej if m.by_id[i].source == "region2")})
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(p, s) for p in ("A", "B", "C") for s in SEEDS]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as pool:
        for a in pool.imap_unordered(job, jobs):
            print(*a, flush=True)
