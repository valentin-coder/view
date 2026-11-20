"""107. kör, fejlesztési ellenőrzés (NEM teszt): szabályok időbeli vágása."""
import json
import math
import os
import statistics as st
from collections import defaultdict
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator3 import make_case3
from .procedural import accuracy, evaluate
from .run_r60 import PI_META
from .run_r88 import acc_at

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-107", "dev")
V = {"v3": None, "FROZEN_91": V4.FROZEN_91, "F91_R": V4.F91_R}
SETS = [("G3", "szabályváltozás", range(23000, 23006)), ("G3", "állapotváltozás", range(23000, 23004)),
        ("G3", "hazug forrás", range(23000, 23004)), ("G1k", "szabály-helyesbítés", range(16000, 16004))]


def job(a):
    gen, kind, seed, name = a
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{list(V).index(name)}.json")
    if os.path.exists(path):
        return a
    hq = tau = None
    if gen == "G3":
        sch, obs, new, pre, post, tq, hq, tau, _ = make_case3(seed, kind, 0.3)
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, kind, "A")
    if V[name] is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(V[name]):
            m = Memory(sch, mode="arlc")
        m.theory_pi = dict(PI_META["A"])
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post),
               "target": accuracy(m, tq), "hist": acc_at(m, hq, tau - 1) if hq else float("nan"),
               "cuts": len(m.beam[0].cut)}, open(path, "w"))
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, n) for (g, k, ss) in SETS for s in ss for n in V]
    with Pool(4) as pool:
        list(pool.imap_unordered(job, jobs))
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT)]
    g = defaultdict(list)
    for r in rows:
        g[(r["gen"], r["kind"], r["variant"])].append(r)
    nm = lambda xs: st.mean([x for x in xs if not math.isnan(x)]) if any(not math.isnan(x) for x in xs) else float("nan")
    for k in sorted(g):
        v = g[k]
        print(k, "pre %.3f post %.3f target %.3f hist %.3f vágás %.1f" % (nm([r["pre"] for r in v]), nm([r["post"] for r in v]),
              nm([r["target"] for r in v]), nm([r["hist"] for r in v]), st.mean(r["cuts"] for r in v)), flush=True)
