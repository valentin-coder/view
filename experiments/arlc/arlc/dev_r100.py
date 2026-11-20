"""100. kör, fejlesztési ellenőrzés (NEM teszt): megerősítés-függő új-forrás bizalom a már felhasznált seedeken."""
import json
import math
import os
import statistics as st
from collections import defaultdict
from multiprocessing import Pool

from . import run_r96 as R
from . import v4 as V4

R.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-100", "dev")
R.VARIANTS = {"v3": None, "FROZEN_91": V4.FROZEN_91, "F91_C": V4.F91_C}
SETS = [("G1k", "szabály-helyesbítés", range(16000, 16006)), ("G1k", "hazug forrás", range(16000, 16004)),
        ("G1k", "átkategorizálás", range(16000, 16004)), ("G4", "jó új specialista", range(28000, 28004)),
        ("G4", "hazug forrás", range(28000, 28004))]

if __name__ == "__main__":
    os.makedirs(os.path.join(R.OUT, "test"), exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k, ss) in SETS for s in ss for vi in range(3)]
    with Pool(4) as pool:
        list(pool.imap_unordered(R.job, jobs))
    rows = [json.load(open(os.path.join(R.OUT, "test", f))) for f in os.listdir(os.path.join(R.OUT, "test"))]
    g = defaultdict(list)
    for r in rows:
        g[(r["gen"], r["kind"], r["variant"])].append(r)
    for k in sorted(g):
        v = g[k]
        print(k, "post %.3f target %.3f" % (st.mean(r["post"] for r in v), st.mean(r["target"] for r in v if not math.isnan(r["target"]))), flush=True)
