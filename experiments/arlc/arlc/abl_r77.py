"""77. kör, feltáró: melyik v4.x-komponens rontja a pre-acc-ot a második generátoron (a v3-hoz egyenként hozzáadva)."""
import json
import os
import sys
from multiprocessing import Pool

from . import core
from .generator2 import make_case2
from .procedural import evaluate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-77", "ablacio")
BASE = {"reliability": "beta", "kappa": 30.0}
STEPS = {
    "v3": {},
    "+béta (κ=30)": BASE,
    "+béta+kivétel-prior": {**BASE, "exc_prior": 0.05},
    "+béta+osztálykivétel": {**BASE, "class_exceptions": True},
    "+béta+aut. specifikusság": {**BASE, "auto_specificity": True},
    "+béta+feltalálás": {**BASE, "invention": True, "invent_revive": True},
    "+béta+forráslépés": {**BASE, "source_moves": True},
    "+béta+kontextusindukció": {**BASE, "ctx_induction": True},
    "+béta+q-csoportok": {**BASE, "q_groups": True},
}


def job(a):
    seed, name = a
    path = os.path.join(OUT, f"{seed}_{list(STEPS).index(name)}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq = make_case2(seed, "hazug forrás")
    m = core.Memory(sch, mode="arlc")
    for k, v in STEPS[name].items():
        setattr(m, k, v)
    for o in obs:
        m.observe(o)
    json.dump({"seed": seed, "variant": name, "pre": evaluate(m, pre)}, open(path, "w"))
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, n) for s in range(15000, 15020) for n in STEPS]
    with Pool(4) as pool:
        for x in pool.imap_unordered(job, jobs):
            pass
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT)]
    import statistics as st
    for n in STEPS:
        v = [r["pre"] for r in rows if r["variant"] == n]
        print(f"{n:28s} pre-acc {st.mean(v):.4f} (n={len(v)})")
