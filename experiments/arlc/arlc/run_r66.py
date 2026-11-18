"""66. kör: szimulált forrástípus-felismerés pontossága (előregisztrált).
Minden elméleti forrás valódi típusa: A-ban a tankönyv „gondozott”; C-ben mindkét tankönyv „rivális iskola”
(a terület alapgyakorisága szerint: két versengő tankönyv). A szimulált osztályozó a pontossággal a valódi típust adja,
különben a másik három egyikét (egyenletesen); π a felismert típusból (61. kör SRC_PI). A pontosságszintek
beágyazottak: ugyanaz az u ~ U(0,1) húzás dönti el, hogy helyes-e (u < a).
    python -m arlc.run_r66 --pop C --workers 4
"""
import argparse
import json
import os
import random
import zlib
from multiprocessing import Pool

from . import v4 as V4
from .core import Memory
from .procedural import accuracy, evaluate
from .run_r44 import KINDS
from .run_r55 import make_case, run_mem

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-66")
SEEDS = range(8000, 8010)
KIND_IDX = (0, 1, 3)                    # átkategorizálás, szabály-helyesbítés, hazug forrás
ACCS = (0.8, 0.9, 1.0)
SRC_PI = {"gondozott": 0.999, "rivális iskola": 0.5, "szakértő": 0.95, "pletyka": 0.7}
TRUE_TYPE = {"A": {"book": "gondozott"}, "C": {"book": "rivális iskola", "book2": "rivális iskola"}}


def classify(pop, seed, ki, acc):
    out = {}
    for src, t in TRUE_TYPE[pop].items():
        rng = random.Random(zlib.crc32(f"{pop}|{seed}|{ki}|{src}".encode()))   # folyamatfüggetlen (nem hash())
        u, wrong = rng.random(), rng.choice(sorted(k for k in SRC_PI if k != t))
        out[src] = t if u < acc else wrong
    return out


def job(a):
    pop, seed, ki = a
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    sch, obs, new, pre, post, tq, g = make_case(seed, KINDS[ki], pop)
    row = {"pop": pop, "seed": seed, "kind": KINDS[ki], "garbage": g}
    m, _ = run_mem(sch, obs, new, V4.V44E_OVERRIDES)
    row["post_v4.4e"], row["target_v4.4e"] = evaluate(m, post), accuracy(m, tq)
    for acc in ACCS:
        types = classify(pop, seed, ki, acc)
        with V4.configured({**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {s: SRC_PI[t] for s, t in types.items()}
        for o in obs + new:
            m.observe(o)
        tag = f"a{acc}"
        row[f"types_{tag}"] = types
        row[f"post_{tag}"], row[f"target_{tag}"] = evaluate(m, post), accuracy(m, tq)
        for b in ("book", "book2"):
            ids = [o.id for o in m.obs if o.source == b]
            if ids:
                row[f"dismissed_{b}_{tag}"] = (b in m.best.iso) or sum(i in m.best.rej for i in ids) >= 0.9 * len(ids)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="C")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in SEEDS for ki in KIND_IDX if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
