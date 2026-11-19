"""87. kör: generátor-egységteszt. Egy világ akkor megengedett, ha létezik olyan ütközésmentes hipotézis, amely
pontosan a hamis megfigyeléseket teszi félre, és ezen túl csak kivételeket használ (igaz megfigyelést nem tesz félre,
kontextust nem izolál). Ha nincs ilyen, a generátor a sémájával ellentmondásos világot gyártott.
    python -m arlc.gen_check
"""
import json
import os
import sys
from collections import Counter

from .audit_truth import obs_true, world_g1, world_g2
from .core import Hyp, Memory, replace
from .g1k import make_case_k
from .generator2 import make_case2
from .run_r55 import make_case

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-87")


def admissible(m, w, gen, max_iter=400):
    """(megengedett-e, felhasznált kivételek száma, az első nem feloldható ütközés fajtái)"""
    H = Hyp(rej=frozenset(o.id for o in m.obs if obs_true(o, w, gen) is False))
    for _ in range(max_iter):
        c = m.find_conflict(H)
        if c is None:
            return True, len(H.exc), None
        insts = sorted((t for t in c if t[0] == "inst" and m._get(t[1], H).rule.pred == "has"), key=str)
        if not insts:
            kinds = sorted({("obs:" + m.by_id[t[1]].source) if t[0] == "obs" else ("inst:" + m._get(t[1], H).rule.pred)
                            for t in c})
            return False, len(H.exc), kinds
        wrong = []
        for t in insts:
            r = m._get(t[1], H).rule
            tv = w.truth(t[2]).get(r.obj) if t[2] in w.members else None
            if tv is not None and tv != r.pos:
                wrong.append(t)
        t = (wrong or insts)[0]            # rossz jóslat kivétele; ha az igazság nem definiált (Nixon), bármelyik
        H = replace(H, exc=H.exc | {(t[1], t[2])})
    return False, len(H.exc), ["iterációs korlát"]


def check(gen, seed, pop="A"):
    if gen == "G2":
        sch, obs, *_ = make_case2(seed, "hazug forrás")
        w, g = world_g2(seed), "G2"
    else:
        mk = make_case if gen == "G1" else make_case_k
        sch, obs, *_ = mk(seed, "hazug forrás", pop)
        w, g = world_g1(seed), "G1"
    m = Memory(sch, mode="arlc")
    m.obs = list(obs)                       # a megfigyelések keresés nélkül (csak a zárás és az ütközés kell)
    m.by_id = {o.id: o for o in obs}
    m.now = max(o.time for o in obs)
    ok, n_exc, kinds = admissible(m, w, g)
    return {"gen": gen, "pop": pop, "seed": seed, "ok": ok, "n_exc": n_exc, "conflict": kinds}


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    seeds = [int(x) for x in sys.argv[1:]] or list(range(44000, 44030)) + list(range(16000, 16020)) + list(range(22000, 22020))
    rows = []
    for gen in ("G1", "G1k", "G2"):
        for s in seeds:
            rows.append(check(gen, s))
            print(rows[-1], flush=True)
    summ = {}
    for gen in ("G1", "G1k", "G2"):
        R = [r for r in rows if r["gen"] == gen]
        summ[gen] = {"n": len(R), "megengedett": sum(r["ok"] for r in R),
                     "ütközés-fajták": Counter(tuple(r["conflict"]) for r in R if not r["ok"]).most_common(5),
                     "kivétel/világ (megengedettnél)": round(sum(r["n_exc"] for r in R if r["ok"]) / max(1, sum(r["ok"] for r in R)), 2)}
    json.dump({"rows": rows, "összesítés": summ}, open(os.path.join(OUT, "gen_check.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(summ, ensure_ascii=False, indent=1, default=str))
