"""91. kör: hibrid megbízhatósági kód + eseményenkénti vágásár (előregisztrált, friss seedek 26000–26019; G1k-A, G2, G3
kalibrált). A 90. kör futtatóját használja más seedekkel és változatokkal.
    python -m arlc.run_r91
Elemzési terv: docs/korok/91-hibrid-kod.md (a futtatás előtt commitolva).
"""
import os
from multiprocessing import Pool

from . import run_r90 as R
from . import v4 as V4

R.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-91", "test")
R.SEEDS = range(26000, 26020)
R.VARIANTS = {"v3": None, "η=0": {**V4.FROZEN_88, "rel_temper": 0.0}, "η=1": V4.FROZEN_88, "hibrid+V": V4.HYBRID_V_91}

if __name__ == "__main__":
    os.makedirs(R.OUT, exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in R.CASES for s in R.SEEDS for vi in range(len(R.VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(R.job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
