"""115. kör: szabály-vágás + általános újranyitó keresés (F112_RO) – előregisztrált, friss seedek 41000–41014.
A 107. kör futtatóját használja más seedekkel és változatokkal.
    python -m arlc.run_r115
"""
import os
from multiprocessing import Pool

from . import run_r107 as R
from . import v4 as V4

R.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-115")
R.SEEDS = range(41000, 41015)
R.VARIANTS = {"v3": None, "FROZEN_112": V4.FROZEN_112, "F112_RO": V4.F112_RO}

if __name__ == "__main__":
    os.makedirs(os.path.join(R.OUT, "test"), exist_ok=True)
    os.makedirs(os.path.join(R.OUT, "battery"), exist_ok=True)
    jobs = [(g, k, s, vi) for (g, k) in R.CASES for s in R.SEEDS for vi in range(len(R.VARIANTS))]
    with Pool(4) as pool:
        for r in pool.imap_unordered(R.bat, ["FROZEN_112", "F112_RO"]):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(R.job, jobs):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
