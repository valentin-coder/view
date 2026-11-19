"""82. kör: menekülőút-audit. A generátor igazsága alapján minden megfigyelésről eldönti, hogy igaz-e
(a meglepetés előtti világban), és ebből a végső hipotézis félretevéseinek minőségét méri forrásonként."""
import random
from collections import Counter

from . import procedural as P
from .generator2 import World2, stream2


def world_g1(seed):
    rng = random.Random(seed)
    w = P.generate_world(rng)
    P.stream(w, rng)
    return w


def world_g2(seed):
    rng = random.Random(seed)
    w = World2(rng)
    stream2(w, rng)
    return w


def obs_true(o, w, gen):
    """True/False: igaz-e a megfigyelés a meglepetés előtti világban; None: nem definiált.
    G3: időfüggő világ, a megfigyelés a saját időbélyegén igaz-e."""
    if gen == "G3":
        return obs_true_g3(o, w)
    if o.rule is not None:
        r = o.rule
        if r.cond is not None:
            return None
        if r.pred == "isa":
            return (r.obj in w.parents.get(r.body, [])) if gen == "G1" else None
        rs = w.rules.get(r.body, {})
        return (r.obj in rs and rs[r.obj] == r.pos)
    l = o.lit
    if l.pred == "isa":
        if l.subj not in w.members:
            return None
        cats = w.members[l.subj] if gen == "G2" else [w.members[l.subj]]
        return (l.obj in cats) == l.pos
    v = w.truth(l.subj).get(l.obj) if l.subj in w.members else None
    return None if v is None else (v == l.pos)


def audit(m, w, gen, obs_ids=None):
    """Forrásonként: helyes félretevés (hamis állítás félretéve), téves félretevés (igaz állítás félretéve),
    elmulasztott (hamis állítás elfogadva). A nem definiált állítások kimaradnak."""
    H = m.beam[0]
    out = Counter()
    for o in m.obs:
        if obs_ids is not None and o.id not in obs_ids:
            continue
        t = obs_true(o, w, gen)
        if t is None:
            continue
        rej = o.id in H.rej
        kind = ("I" if o.rule.pred == "isa" else "R") if o.rule is not None else "F"
        if rej and not t:
            out[f"{o.source}:{kind}:helyes_félretevés"] += 1
        elif rej and t:
            out[f"{o.source}:{kind}:téves_félretevés"] += 1
        elif not rej and not t:
            out[f"{o.source}:{kind}:elmulasztott"] += 1
    out["izolált_források"] = len(H.iso)
    out["osztálykivétel"] = sum(1 for x in H.exc if isinstance(x[1], str) and x[1].startswith("cat:"))
    out["egyedi_kivétel"] = sum(1 for x in H.exc if not (isinstance(x[1], str) and x[1].startswith("cat:")))
    out["indukált"] = len(H.ind)
    return dict(out)


def obs_true_g3(o, w):
    t = o.time
    if o.rule is not None:
        r = o.rule
        if r.cond is not None:
            return None
        if r.pred == "isa":
            return w.parent.get(r.body) == r.obj
        v = w.rule_value(r.body, r.obj, t)
        return v is not None and v == r.pos
    l = o.lit
    if l.subj not in w.members:
        return None
    if l.pred == "isa":
        return (w.members[l.subj] == l.obj) == l.pos
    if l.obj.startswith("st"):
        return (w.state_at(l.subj, t) == l.obj) == l.pos
    v = w.static_truth(l.subj, t).get(l.obj)
    return None if v is None else (v == l.pos)
