"""95. kör (konszolidáció, FELTÁRÓ, fejlesztési seedeken): egyet-elhagyó abláció a FROZEN_91-ből négy generátoron.
    python -m arlc.loo_r95
"""
import json
import math
import os
import statistics as st
from collections import defaultdict
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator2 import make_case2
from .generator3 import make_case3
from .generator4 import make_case4
from .procedural import accuracy, evaluate
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-95", "loo")
F = V4.FROZEN_91
LOO = {
    "v3": None,
    "FROZEN_91": {},
    "− tankönyv-keverék": {"theory_mix": None, "theory_kappa": None},
    "− PK": {"priority_exceptions": False, "priority_code": False},
    "− N": {"source_newcomer": None},
    "− hibrid": {"rel_hybrid": False},
    "− V": {"cut_per_event": False},
    "− aut. specifikusság": {"auto_specificity": False},
    "− szigorú specifikusság": {"strict_specificity": False},
    "− kivétel-prior": {"exc_prior": None},
    "− osztálykivétel": {"class_exceptions": False},
    "− feltalálás": {"invention": False, "invent_revive": False},
    "− forráslépés": {"source_moves": False},
    "− kontextusindukció": {"ctx_induction": False},
    "− q-csoportok": {"q_groups": False},
    "− ind. kivétel-ár": {"ind_exc_cost": False},
}
SETS = [("G1k", "hazug forrás", range(16000, 16005)), ("G2", "hazug forrás", range(16000, 16005)),
        ("G3", "hazug forrás", range(23000, 23005)), ("G3", "állapotváltozás", range(23000, 23005)),
        ("G4", "hazug forrás", range(28000, 28005))]


def job(a):
    gen, kind, seed, vi = a
    name = list(LOO)[vi]
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{vi}.json")
    if os.path.exists(path):
        return a
    if gen == "G2":
        sch, obs, new, pre, post, tq = make_case2(seed, kind)
    elif gen == "G3":
        sch, obs, new, pre, post, tq, *_ = make_case3(seed, kind, 0.3)
    elif gen == "G4":
        sch, obs, new, pre, post, tq, _ = make_case4(seed, kind)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    ov = LOO[name]
    if ov is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured({**F, **ov}):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post),
               "target": accuracy(m, tq)}, open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return a


def summarize():
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT) if f.endswith(".json")]
    tab = defaultdict(dict)
    for n in LOO:
        for gen in ("G1k", "G2", "G3", "G4"):
            r = [x for x in rows if x["variant"] == n and x["gen"] == gen]
            if r:
                tab[n][gen] = (round(st.mean(x["post"] for x in r), 3),
                               round(st.mean(x["target"] for x in r if not math.isnan(x["target"])), 3))
    return tab


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k, ss) in SETS for s in ss for vi in range(len(LOO))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
    tab = summarize()
    json.dump(tab, open(os.path.join(OUT, "..", "loo_summary.json"), "w"), ensure_ascii=False, indent=1)
    for n, d in tab.items():
        print(f"{n:28s}", "  ".join(f"{g}: {v[0]:.3f}/{v[1]:.3f}" for g, v in d.items()), flush=True)
    print("KÉSZ", flush=True)
