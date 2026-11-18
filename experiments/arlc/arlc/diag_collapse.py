import sys, json; sys.path.insert(0, '.')
from arlc import procedural as P, v4 as V4
from arlc.core import Memory
seed, kind = int(sys.argv[1]), sys.argv[2]
sch, obs, new, pre, post, tq = P.make_case(seed, kind)
with V4.configured({}):
    m = Memory(sch, mode="arlc")
for o in obs: m.observe(o)
H0 = m.best
print("pre", P.evaluate(m, pre), "rej", len(H0.rej), "iso", sorted(H0.iso), "exc", len(H0.exc))
for o in new:
    ev = m.observe(o)
H = m.best
print("post", P.evaluate(m, post), "rej", len(H.rej), "iso", sorted(H.iso), "exc", len(H.exc), "cut", len(H.cut), "ind", len(H.ind), "beam", len(m.beam))
srcs = {}
for i in H.rej: srcs[m.by_id[i].source] = srcs.get(m.by_id[i].source, 0) + 1
print("rejected by source", srcs)
cl = m.closure(H, None, m.now)
print("conflict in best:", cl.conflict)
e = sorted(post)[0]; print("sample answers", e, [(p, m.answer(e, p, record_use=False), v) for p, v in list(post[e].items())[:4]])
print("n entities with isa", sum(1 for x in cl.isa.values() if x), "with has", sum(1 for x in cl.has.values() if x))
print("new obs sources", sorted({o.source for o in new}), "times", sorted({o.time for o in new}), "now", m.now)
