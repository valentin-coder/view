"""68. kör: azonosíthatóság az igaz hipotézisből.
Esetenként az „igazhoz horgonyzott” hipotézis: a tankönyv hibásan közölt szabályai, a zajos terepi tények és a hamis
meglepetés-tények elvetve, a régióforrás kontextusba izolálva; a maradék ütközéseket mohó befejezés oldja fel.
rés = L(H_igaz) − L(MAP): > 0: a modell egy hamis magyarázatot tart olcsóbbnak (modell-hiba); < 0: a keresés nem
találta meg az olcsóbb igaz magyarázatot (keresési hiba); |rés| kicsi: alulhatározott.
    python -m arlc.run_r68 --workers 4
"""
import argparse
import json
import os
import random
from multiprocessing import Pool

from . import procedural as P
from . import v4 as V4
from .core import Hyp, Memory
from .run_r44 import KINDS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-68")
SEEDS = range(10000, 10015)


def world_and_case(seed, kind):
    rng = random.Random(seed)
    w = P.generate_world(rng)
    obs, c, t = P.stream(w, rng)
    pre = {e: w.truth(e) for e in w.members}
    book_errors = set(w.book_errors)
    new, target = P.surprise(kind, w, rng, c, t + 1)
    post = {e: w.truth(e) for e in w.members}
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=len(pre) + 2, n_categories=len(w.cats), n_props=len(w.props))
    tq = [(e, p, post[e][p]) for e, p in target if p in post.get(e, {})]
    return sch, obs, new, pre, post, tq, book_errors


def job(a):
    seed, ki = a
    path = os.path.join(OUT, f"{ki}_{seed}.json")
    if os.path.exists(path):
        return a
    kind = KINDS[ki]
    sch, obs, new, pre, post, tq, book_errors = world_and_case(seed, kind)
    with V4.configured(V4.V44E_OVERRIDES):
        m = Memory(sch, mode="arlc")
    for o in obs + new:
        m.observe(o)
    Hmap = m.best
    rej = {o.id for o in obs if o.rule is not None and o.rule.pred == "has" and (o.rule.body, o.rule.obj) in book_errors}
    rej |= {o.id for o in obs if o.lit is not None and o.lit.pred == "has" and o.source == "field"
            and pre.get(o.lit.subj, {}).get(o.lit.obj) is not None and pre[o.lit.subj][o.lit.obj] != o.lit.pos}
    rej |= {o.id for o in new if o.lit is not None and o.lit.pred == "has" and o.source == "liar"}
    iso = frozenset({"region2"}) if kind == "más régió" else frozenset()
    Hg0 = m._greedy(Hyp(rej=frozenset(rej), iso=iso))
    # a mohó befejezés felesleges elutasításokat is ad; a visszahelyezés (36. kör) ezeket kidobja, a valódi hibák
    # elutasítása megmarad (visszavéve ütköznének)
    Hg = m._reinstate(Hg0) if Hg0 is not None else None
    row = {"seed": seed, "kind": kind, "n_true_rej": len(rej), "L_map": m.score(Hmap)}
    m.beam = [Hmap]
    row["target_map"] = P.accuracy(m, tq)
    row["post_map"] = P.evaluate(m, post)
    if Hg is not None:
        row["L_true"] = m.score(Hg)
        row["gap"] = row["L_true"] - row["L_map"]
        m.beam = [Hg]
        row["target_true"] = P.accuracy(m, tq)
        row["post_true"] = P.evaluate(m, post)
        row["extra_rej_true"] = len(Hg.rej - frozenset(rej))
        row["anchor_rej_dropped"] = len(frozenset(rej) - Hg.rej)
        row["L_true_greedy_only"] = m.score(Hg0)
    json.dump(row, open(path + ".tmp", "w"), indent=1)
    os.replace(path + ".tmp", path)
    return a


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    w = ap.parse_args().workers
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, ki) for s in SEEDS for ki in range(len(KINDS)) if not os.path.exists(os.path.join(OUT, f"{ki}_{s}.json"))]
    with Pool(w) as pool:
        for r in pool.imap_unordered(job, jobs):
            print(*r, flush=True)
