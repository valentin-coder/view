"""85. kör: a G1 generátor javított változata (G1k). A 44. kori generátor minden csúcskategória-párt diszjunktnak
mond, de a középső és a levélkategóriák többszörös szülői két csúcsot is összeköthetnek: az ilyen világ logikailag
ellentmondásos (82. kör, 3. rész). A G1k-ban két csúcs csak akkor diszjunkt, ha egyetlen kategóriának sem közös őse.
Minden más (világ, megfigyelések, meglepetések) bitre azonos a G1-gyel; a régi generátor változatlan."""
from .audit_truth import world_g1
from .run_r55 import make_case


def compatible_tops(w):
    out = set()
    for c in w.cats:
        tops = sorted({x for _, x in w.ancestors_by_depth(c) if x.startswith("T")})
        for i in range(len(tops)):
            for j in range(i + 1, len(tops)):
                out.add(frozenset((tops[i], tops[j])))
    return out


def make_case_k(seed, kind, pop):
    sch, obs, new, pre, post, tq, g = make_case(seed, kind, pop)
    w = world_g1(seed)
    sch.disjoint = set(sch.disjoint) - compatible_tops(w)
    return sch, obs, new, pre, post, tq, g
