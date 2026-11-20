"""115. kör, fejlesztési ellenőrzés (NEM teszt): általános újranyitó keresés a 97. és 107. kör jelöltjeivel."""
import json
import math
import os
import statistics as st
from collections import defaultdict
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .generator3 import make_case3
from .generator4 import make_case4
from .procedural import accuracy, evaluate
from .run_r88 import acc_at

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-115", "dev")
V = {"F112": V4.FROZEN_112, "F112+R": {**V4.FROZEN_112, "rule_cuts": True}, "F112+R+O": V4.F112_RO,
     "F112+CP": {**V4.FROZEN_112, "source_changepoints": True}, "F112+CP+O": V4.F112_CPO, "F112+O": V4.F112_O}
SETS = [("G3", "szabályváltozás", range(23000, 23006), ("F112", "F112+R", "F112+R+O", "F112+O")),
        ("G3", "állapotváltozás", range(23000, 23004), ("F112", "F112+R+O", "F112+O")),
        ("G4", "romló forrás", range(28000, 28006), ("F112", "F112+CP", "F112+CP+O", "F112+O")),
        ("G4", "hazug forrás", range(28000, 28004), ("F112", "F112+CP+O", "F112+O"))]


def job(a):
    gen, kind, seed, name = a
    path = os.path.join(OUT, f"{gen}_{kind.replace(' ', '_')}_{seed}_{list(V).index(name)}.json")
    if os.path.exists(path):
        return a
    hq = tau = None
    if gen == "G3":
        sch, obs, new, pre, post, tq, hq, tau, _ = make_case3(seed, kind, 0.3)
    else:
        sch, obs, new, pre, post, tq, _ = make_case4(seed, kind)
    with V4.configured(V[name]):
        m = Memory(sch, mode="arlc")
    m.theory_pi = {"book": 0.999}
    for o in obs + new:
        m.observe(o)
    json.dump({"gen": gen, "kind": kind, "seed": seed, "variant": name, "post": evaluate(m, post), "target": accuracy(m, tq),
               "hist": acc_at(m, hq, tau - 1) if hq else float("nan")}, open(path, "w"))
    return a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [(g, k, s, n) for (g, k, ss, ns) in SETS for s in ss for n in ns]
    with Pool(4) as pool:
        list(pool.imap_unordered(job, jobs))
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT)]
    g = defaultdict(list)
    for r in rows:
        g[(r["gen"], r["kind"], r["variant"])].append(r)
    nm = lambda xs: st.mean([x for x in xs if not math.isnan(x)]) if any(not math.isnan(x) for x in xs) else float("nan")
    for k in sorted(g):
        v = g[k]
        print(k, "post %.3f target %.3f hist %.3f" % (nm([r["post"] for r in v]), nm([r["target"] for r in v]), nm([r["hist"] for r in v])), flush=True)
    print("KÉSZ")
