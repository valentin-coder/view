"""Viselkedésmegőrző gyorsítások ellenőrzése: kis procedurális világokon a teljes nyaláb
(kulcsok és pontszámok) és a válaszok bitre egyeznek-e egy elmentett referenciával."""
from __future__ import annotations

import json
import random
import sys
import time

from . import procedural as P
from . import v4 as V4
from .core import Memory


def canon(H):
    """A hash-seedtől független kulcs: minden halmaz rendezett repr-listaként."""
    return [sorted(map(repr, H.rej)), sorted(map(repr, H.exc)), sorted(map(repr, H.iso)), list(map(repr, H.cut)),
            [repr(o.rule) for o in H.ind]]


def fingerprint(seeds=(11, 12, 13, 14), n_ent=8, overrides=None):
    out = []
    t0 = time.perf_counter()
    for seed in seeds:
        rng = random.Random(seed)
        w = P.generate_world(rng, n_ent=n_ent)
        obs, c, t = P.stream(w, rng)
        sch = P.Schema(disjoint=set(w.disjoint), n_entities=n_ent + 2, n_categories=len(w.cats), n_props=len(w.props))
        with V4.configured(overrides or {}):
            m = Memory(sch, mode="arlc")
        for o in obs:
            m.observe(o)
        beam = [[canon(H), round(m.score(H), 9)] for H in m.beam]
        ans = [[e, p, m.answer(e, p, record_use=False)] for e in sorted(w.members) for p in w.props]
        out.append({"seed": seed, "beam": beam, "answers": ans})
    return out, time.perf_counter() - t0


if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    fp, sec = fingerprint()
    if mode == "save":
        json.dump(fp, open(path, "w"))
        print("mentve", round(sec, 1), "s")
    else:
        ref = json.load(open(path))
        print("EGYEZIK" if json.loads(json.dumps(fp)) == ref else "ELTÉR", round(sec, 1), "s")
