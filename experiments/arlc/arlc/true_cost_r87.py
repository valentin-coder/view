"""87. kör: az igaz hipotézis ára a talált hipotéziséhez képest (G1k, G2; 22000–22004).
    python -m arlc.true_cost_r87
"""


from . import v4 as V4
from .core import Memory, Hyp, replace
from .audit_truth import obs_true, world_g1, world_g2
from .g1k import make_case_k
from .generator2 import make_case2
from .procedural import evaluate
V48 = {**V4.V44E_OVERRIDES, "theory_kappa": 1.0, "theory_mix": (0.9, 30.0, 0.5, 2.0)}
cfg = {**V48, **V4.V49_SM, "priority_exceptions": True, "priority_code": True}

def true_hyp(m, w, gen, prio):
    H = Hyp(rej=frozenset(o.id for o in m.obs if obs_true(o, w, gen) is False))
    for _ in range(400):
        c = m.find_conflict(H)
        if c is None:
            return H
        insts = sorted((t for t in c if t[0] == "inst" and m._get(t[1], H).rule.pred == "has"), key=str)
        wrong, undef = [], []
        for t in insts:
            r = m._get(t[1], H).rule
            tv = w.truth(t[2]).get(r.obj)
            (wrong if (tv is not None and tv != r.pos) else undef if tv is None else []).append(t)
        t = (wrong or undef or insts)[0]
        if prio:
            # olcsóbb: prioritás-kivétel, ha van rivális kategória az entitás kategóriái között
            cats = [c2 for (c2, p2) in m.closure(H, None, m.now).isa.get(t[2], {}) if p2]
            riv = [c2 for c2 in cats if c2 in m._rivals(H, t[1])]
            if riv and (gen == "G2" or not wrong):
                H = replace(H, exc=H.exc | {(t[1], "cat:" + sorted(riv)[0])}); continue
        H = replace(H, exc=H.exc | {(t[1], t[2])})
    return None

for gen in ("G1k", "G2"):
    for s in range(22000, 22005):
        if gen == "G2":
            sch, obs, new, pre, post, tq = make_case2(s, "hazug forrás"); w = world_g2(s); g = "G2"
        else:
            sch, obs, new, pre, post, tq, _ = make_case_k(s, "hazug forrás", "A"); w = world_g1(s); g = "G1"
        with V4.configured(cfg):
            m = Memory(sch, mode="arlc")
        m.theory_pi = {"book": 0.999}
        for o in obs: m.observe(o)
        F = m.beam[0]; aF = evaluate(m, pre); sF = m.score(F)
        out = [f"{gen} {s} talált {sF:.1f} (acc {aF:.3f})"]
        for prio in (False, True):
            T = true_hyp(m, w, g, prio)
            if T is None:
                out.append("igaz: nincs"); continue
            m.beam = [T]
            out.append(f"igaz{'+prio' if prio else ''} {m.score(T):.1f} (acc {evaluate(m, pre):.3f}, kiv {len(T.exc)})")
        print("  ".join(out), flush=True)
