"""91. kör, fejlesztési ellenőrzés (NEM teszt): hibrid megbízhatósági kód a már felhasznált seedeken."""
import json
import os
from multiprocessing import Pool

from . import run_r90 as R
from . import v4 as V4

R.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-91", "dev")
R.VARIANTS = {"v3": None, "η=0": {**V4.FROZEN_88, "rel_temper": 0.0}, "η=1": V4.FROZEN_88, "hibrid": V4.HYBRID_91}
JOBS = [(g, k, s, vi) for (g, k, ss) in (("G1k", "hazug forrás", (16000, 16001, 16002)), ("G2", "hazug forrás", (16000, 16001, 16002)),
                                         ("G3", "hazug forrás", (23000, 23001, 23002)), ("G3", "állapotváltozás", (23000, 23001, 23002)))
        for s in ss for vi in range(4)]

if __name__ == "__main__":
    os.makedirs(R.OUT, exist_ok=True)
    with Pool(4) as pool:
        list(pool.imap_unordered(R.job, JOBS))
    import collections, statistics as st, math
    rows = [json.load(open(os.path.join(R.OUT, f))) for f in os.listdir(R.OUT)]
    g = collections.defaultdict(list)
    for r in rows:
        g[(r["gen"], r["kind"], r["variant"])].append(r)
    for k in sorted(g):
        v = g[k]
        print(k, "pre %.3f post %.3f target %.3f" % (st.mean(r["pre"] for r in v), st.mean(r["post"] for r in v),
                                                     st.mean(r["target"] for r in v if not math.isnan(r["target"]))), flush=True)
