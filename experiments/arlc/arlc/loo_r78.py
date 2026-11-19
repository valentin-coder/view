"""78. kör, feltáró: egyet-elhagyó abláció a teljes v4.4e-ből a második generátoron (pre-acc, 20 seed)."""
import json
import os
import statistics as st
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator2 import make_case2
from .procedural import evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-78", "loo")
VARIANTS = {
    "v3": None,
    "v4.4e": {},
    "− tanult megbízhatóság": {"reliability": "fixed"},
    "− kivétel-prior": {"exc_prior": None},
    "− osztálykivétel": {"class_exceptions": False},
    "− aut. specifikusság": {"auto_specificity": False},
    "− feltalálás": {"invention": False, "invent_revive": False},
    "− forráslépés": {"source_moves": False},
    "− q-csoportok": {"q_groups": False},
    "− mohó/mélység2 (mélység 3)": {"cheap_greedy": False, "depth": 3},
}


def job(a):
    seed, vi = a
    path = os.path.join(OUT, f"{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    name = list(VARIANTS)[vi]
    sch, obs, new, pre, post, tq = make_case2(seed, "hazug forrás")
    if VARIANTS[name] is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured({**V4.V44E_OVERRIDES, **VARIANTS[name]}):
            m = Memory(sch, mode="arlc")
    for o in obs:
        m.observe(o)
    json.dump({"seed": seed, "variant": name, "pre": evaluate(m, pre)}, open(path, "w"))
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, i) for s in range(16000, 16020) for i in range(len(VARIANTS))]
    with Pool(4) as pool:
        for _ in pool.imap_unordered(job, jobs):
            pass
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT)]
    for n in VARIANTS:
        v = [r["pre"] for r in rows if r["variant"] == n]
        print(f"{n:32s} pre-acc {st.mean(v):.4f} (n={len(v)})", flush=True)
