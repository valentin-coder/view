"""55. kör: kétsebességű rendszer (előregisztrált).

Ugyanarra a folyamra két memória fut: a v3 (lassan változó, stabil) és a v4.4-egyszintű (gyorsan reagáló,
forrás- és kontextus-érzékeny). A válasz:
- H1 („kúp”): a meglepetés kúpjában a v4.4e válasza, máshol a v3-é. A kúp: a meglepetés megfigyeléseinek
  alanyai, és a meglepetésben szereplő szabályok törzskategóriáinak tagjai (a v4.4e zárása szerint).
- H2 („kúp + visszaesés”): mint H1, de ha a v4.4e a meglepetés után a tankönyv ≥ 90%-át elveti vagy
  izolálja, minden kérdésre a v3 válaszol.

Populációk: „A” (a 44. kör generátora változatlanul) és „B” (seedenként 30% eséllyel egészében téves
tankönyv, mint az 52. körben). Esetenként részfájl, folytatható.
    python -m arlc.run_r55 --pop A --seeds 4000 4030 --workers 4
"""
from __future__ import annotations

import argparse
import json
import os
import random
import time
from multiprocessing import Pool

from . import procedural as P
from . import v4 as V4
from .core import Memory, Obs, Rule
from .run_r44 import KINDS, beam_average

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-55")


def is_garbage(seed):
    return random.Random(seed * 7 + 13).random() < 0.3


def make_case(seed, kind, pop):
    """A procedural.make_case, B populációban egészében téves tankönyvvel (a szabályok előjele véletlen)."""
    sch, obs, new, pre, post, tq = P.make_case(seed, kind)
    if pop == "C":
        # 57. kör: két rivális tankönyv; seedenként véletlenül az egyik egészében téves (TFB-9-szerű)
        bad = "book" if random.Random(seed * 11 + 5).random() < 0.5 else "book2"
        grng = random.Random(seed + 7919)
        out, nid = [], 900000
        for o in obs:
            if o.rule is not None and o.rule.pred == "has" and o.source == "book":
                good_r = o.rule
                bad_r = Rule(good_r.body, good_r.pred, good_r.obj, grng.random() < 0.5)
                out.append(Obs(o.id, "book", o.time, o.q, rule=bad_r if bad == "book" else good_r))
                out.append(Obs(nid, "book2", o.time, o.q, rule=bad_r if bad == "book2" else good_r))
                nid += 1
            else:
                out.append(o)
        return sch, out, new, pre, post, tq, bad
    garbage = pop == "B" and is_garbage(seed)
    if garbage:
        grng = random.Random(seed + 7919)
        obs = [Obs(o.id, o.source, o.time, o.q, rule=Rule(o.rule.body, o.rule.pred, o.rule.obj, grng.random() < 0.5))
               if (o.rule is not None and o.rule.pred == "has" and o.source == "book") else o for o in obs]
    return sch, obs, new, pre, post, tq, garbage


def run_mem(sch, obs, new, cfg):
    if cfg is None:
        m = Memory(sch, mode="arlc")
    else:
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
    for o in obs:
        m.observe(o)
    t = time.perf_counter()
    for o in new:
        m.observe(o)
    return m, time.perf_counter() - t


def cone(mem, new):
    ents = {o.lit.subj for o in new if o.lit is not None}
    bodies = {o.rule.body for o in new if o.rule is not None}
    if bodies:
        cl = mem.closure(mem.best, None, mem.now)
        for e, d in cl.isa.items():
            if any((b, True) in d for b in bodies):
                ents.add(e)
    return ents


def dismissed(mem):
    H = mem.best
    book = [o.id for o in mem.obs if o.source == "book"]
    return ("book" in H.iso) or (sum(i in H.rej for i in book) >= 0.9 * max(1, len(book)))


def score(answers, queries):
    if not queries:
        return float("nan")
    return sum(answers[(e, p)] == v for e, p, v in queries) / len(queries)


def job(args):
    pop, seed, ki = args
    path = os.path.join(OUT, pop, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return args
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, garbage = make_case(seed, kind, pop)
    m3, t3 = run_mem(sch, obs, new, None)
    m4, t4 = run_mem(sch, obs, new, V4.V44E_OVERRIDES)
    q = [(e, p, v) for e, tr in post.items() for p, v in tr.items() if p != "marked"]
    keys = {(e, p) for e, p, _ in q} | {(e, p) for e, p, _ in tq}
    a3 = {k: m3.answer(*k, record_use=False) for k in keys}
    a4 = {k: m4.answer(*k, record_use=False) for k in keys}
    C = cone(m4, new)
    h1 = {k: (a4[k] if k[0] in C else a3[k]) for k in keys}
    fb = dismissed(m4)
    h2 = a3 if fb else h1
    row = {"pop": pop, "seed": seed, "kind": kind, "garbage": garbage, "cone_size": len(C), "fallback": fb,
           "v3_dismissed": dismissed(m3), "t_v3": t3, "t_v44e": t4}
    for name, a in (("v3", a3), ("v4.4e", a4), ("H1", h1), ("H2", h2)):
        row[f"post_{name}"] = score(a, q)
        row[f"target_{name}"] = score(a, tq)
    row.update({f"v44e_{k}": v for k, v in beam_average(m4, post, tq).items()})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return args


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pop", default="A")
    ap.add_argument("--seeds", type=int, nargs=2, default=(4000, 4030))
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = [(a.pop, s, ki) for s in range(*a.seeds) for ki in range(len(KINDS))
            if not os.path.exists(os.path.join(OUT, a.pop, f"{ki}_{s}.json"))]
    print("hátralévő:", len(jobs), flush=True)
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
