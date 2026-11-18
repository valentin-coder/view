"""53. kör: a 45. kör J3-ja (ismételt mérés) a látens igazsággal (v4.6), ugyanazokon a világokon."""
import itertools
import json
import os
import sys
from multiprocessing import Pool

from . import empirical_bayes as EB
from . import v4 as V4

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-53")


CFG = {"v4.6": V4.V46_OVERRIDES, "v4.4e": V4.V44E_OVERRIDES}
NAME = os.environ.get("CFG", "v4.6")
SUB = os.environ.get("SUB", "parts")


def job(a):
    p = os.path.join(OUT, SUB, "_".join(map(str, a)) + ".json")
    if not os.path.exists(p):
        row = EB.run_world(*a, overrides=dict(CFG[NAME]))
        json.dump(row, open(p, "w"), default=str, indent=1)
    return a


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, SUB), exist_ok=True)
    jobs = list(itertools.product(range(2000, 2003), (0.005, 0.03, 0.1), (0.02, 0.1), (True,)))
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 1) as pool:
        for a in pool.imap_unordered(job, jobs):
            print("kész", a, flush=True)
