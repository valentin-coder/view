"""56. kör: miért optimális a tankönyv félretétele egy 30 entitásos világban az egyszintű v4.4e-ben is?
A félretevő (online) hipotézis és egy „csak a hibás szabályok elvetve” hipotézis pontszámának felbontása."""
import json
import sys
from collections import Counter

from . import procedural as P
from . import v4 as V4
from .core import Hyp, Memory


def parts(m, H):
    m._scache.clear()
    total = m.score(H)
    beta = m._beta_bits(H)
    cl = m.closure(H, None, m.now)
    pred = unpred = 0
    for o in m.obs:
        if o.lit is not None and o.lit.pred == "has" and o.id not in H.rej:
            if (o.lit.obj, o.lit.pos) in cl.ruled.get(o.lit.subj, ()):
                pred += 1
            else:
                unpred += 1
    inst = [x for x in H.exc if not (isinstance(x[1], str) and x[1].startswith("cat:"))]
    return {"total": round(total, 2), "beta": round(beta, 2), "rest": round(total - beta, 2),
            "rej_by_source": dict(Counter(m.by_id[i].source for i in H.rej)), "inst_exc": len(inst),
            "cls_exc": len(H.exc) - len(inst), "iso": sorted(H.iso), "facts_predicted": pred, "facts_unpredicted": unpred}


def main(seed, kind="átkategorizálás"):
    sch, obs, new, pre, post, tq = P.make_case(seed, kind)
    rng_w = __import__("random").Random(seed)
    w = P.generate_world(rng_w)
    P.stream(w, rng_w)
    with V4.configured(V4.V44E_OVERRIDES):
        m = Memory(sch, mode="arlc")
    for o in obs:
        m.observe(o)
    on = m.best
    errs = {o.id for o in m.obs if o.rule and o.rule.pred == "has" and (o.rule.body, o.rule.obj) in set(w.book_errors)}
    Hg = m._greedy(Hyp(rej=frozenset(errs)))
    Hr = m._reinstate(Hg) if Hg is not None else None
    out = {"seed": seed, "n_book_errors": len(errs), "online": parts(m, on), "pre_acc_online": P.evaluate(m, pre)}
    if Hr is not None:
        m.beam = [Hr]
        out["keep_book"] = parts(m, Hr)
        out["pre_acc_keep"] = P.evaluate(m, pre)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(int(sys.argv[1]))
