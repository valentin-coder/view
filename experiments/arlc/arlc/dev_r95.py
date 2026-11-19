"""95. kör, fejlesztési ellenőrzés (NEM teszt): Tκ és TDκ a már felhasznált seedeken + a feladatcsomag."""
import json
import os
import statistics as st
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .g1k import make_case_k
from .generator4 import make_case4
from .procedural import accuracy, evaluate
from .run_r60 import PI_META

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-95", "dev")
V = {"F91": V4.FROZEN_91, "F91+Tκ": V4.F91_TK, "F91+TDκ": V4.F91_TDK}


def job(a):
    gen, seed, name = a
    path = os.path.join(OUT, f"{gen}_{seed}_{list(V).index(name)}.json")
    if os.path.exists(path):
        return a
    if gen == "G4":
        sch, obs, new, pre, post, tq, _ = make_case4(seed, "hazug forrás"); pi = {"book": 0.999}
    else:
        sch, obs, new, pre, post, tq, _ = make_case_k(seed, "hazug forrás", "C"); pi = PI_META["C"]
    with V4.configured(V[name]):
        m = Memory(sch, mode="arlc")
    m.theory_pi = dict(pi)
    for o in obs:
        m.observe(o)
    pa = evaluate(m, pre)
    for o in new:
        m.observe(o)
    json.dump({"gen": gen, "seed": seed, "variant": name, "pre": pa, "post": evaluate(m, post), "target": accuracy(m, tq)}, open(path, "w"))
    return a


def bat(name):
    path = os.path.join(OUT, f"battery_{list(V).index(name)}.json")
    if not os.path.exists(path):
        with V4.configured(V[name]) as c:
            json.dump(V4.battery(c), open(path, "w"), ensure_ascii=False, default=str)
    return name


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    jobs = [("G4", s, n) for s in range(28000, 28006) for n in V] + [("C", s, n) for s in (16000, 16001) for n in V]
    with Pool(4) as pool:
        list(pool.imap_unordered(bat, list(V)[1:]))
        list(pool.imap_unordered(job, jobs))
    rows = [json.load(open(os.path.join(OUT, f))) for f in os.listdir(OUT) if not f.startswith("battery")]
    for g in ("G4", "C"):
        for n in V:
            r = [x for x in rows if x["gen"] == g and x["variant"] == n]
            print(g, n, "pre %.3f post %.3f target %.3f" % tuple(st.mean(x[m] for x in r) for m in ("pre", "post", "target")))
    for i, n in enumerate(V):
        if i:
            b = json.load(open(os.path.join(OUT, f"battery_{i}.json")))
            print(n, {k: b[k] for k in ("E1 RR (átkat.+alosztály)", "E3 helyes döntés", "E4 pontosság (ε=0,05)", "TFB-9 pontosság (zaj 0,15)", "TFB-2 pontosság")})
