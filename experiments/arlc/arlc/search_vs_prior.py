import sys, random; sys.path.insert(0,'.')
from arlc import procedural as P, v4 as V4
from arlc.core import Memory, Hyp
for seed in (22, 26, 28):
    rng = random.Random(seed); w = P.generate_world(rng, n_ent=12); obs, c, t = P.stream(w, rng)
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=14, n_categories=len(w.cats), n_props=len(w.props))
    truth = {e: w.truth(e) for e in w.members}
    with V4.configured(V4.V44_OVERRIDES):
        m = Memory(sch, mode="arlc")
    for o in obs: m.observe(o)
    best = m.best
    errs = {o.id for o in m.obs if o.rule and o.rule.pred == "has" and (o.rule.body, o.rule.obj) in set(w.book_errors)}
    noisy = {o.id for o in m.obs if o.lit and o.lit.pred == "has" and w.truth(o.lit.subj).get(o.lit.obj) != o.lit.pos}
    res = []
    for name, rej in (("tankönyvi hibák", errs), ("hibák + zajos tények", errs | noisy)):
        H0 = Hyp(rej=frozenset(rej))
        Hg = m._greedy(H0)
        if Hg is None:
            res.append((name, None)); continue
        Hr = m._reinstate(Hg)
        m.beam = [Hr]; acc = P.evaluate(m, truth)
        res.append((name, round(m.score(Hr), 2), round(acc, 3), len(Hr.rej), len(Hr.exc)))
    m.beam = [best]
    print(seed, "online:", round(m.score(best), 2), round(P.evaluate(m, truth), 3), "| alternatívák:", res, flush=True)
