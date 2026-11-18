import sys, random, json; sys.path.insert(0,'.')
from arlc import procedural as P, v4 as V4
from arlc.core import Memory
name = sys.argv[1]
ov = {"v4.3+mix999": {**V4.V43_OVERRIDES, "theory_mix": V4.MIX_CAL999}, "v4.2": V4.V42_OVERRIDES,
      "v4.3+mix999+ctx": {**V4.V43_OVERRIDES, "theory_mix": V4.MIX_CAL999}, "v4.3": V4.V43_OVERRIDES,
      "v4.3+ctx": V4.V43_OVERRIDES, "v4.4": V4.V44_OVERRIDES}[name]
for seed in range(21, 29):
    rng = random.Random(seed); w = P.generate_world(rng, n_ent=12); obs, c, t = P.stream(w, rng)
    sch = P.Schema(disjoint=set(w.disjoint), n_entities=14, n_categories=len(w.cats), n_props=len(w.props))
    with V4.configured(ov):
        m = Memory(sch, mode="arlc")
    if name.endswith("+ctx"):
        m.ctx_cost.update({"book": 10.0, "census": 10.0})   # gondozott forrás: P(más kontextus) ≈ 1/1000
    for o in obs: m.observe(o)
    H = m.best; nb = sum(1 for o in m.obs if o.source == "book")
    print(json.dumps({"seed": seed, "config": name, "acc": P.evaluate(m, {e: w.truth(e) for e in w.members}),
          "book_rejected_frac": sum(1 for i in H.rej if m.by_id[i].source == "book") / nb, "iso": sorted(H.iso)}), flush=True)
