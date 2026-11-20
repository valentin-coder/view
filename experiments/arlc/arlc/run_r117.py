"""117. kör: aciklikus, időrendes, csak-új-forrásos másolásfelismerés gyorsítással (F115_N) – előregisztrált.
G5: 44000–44014 (FROZEN_91 vs. F115_N); G4 bevált másoló: 44100–44119 (FROZEN_115 vs. F115_N);
a 107. kör esetei (a 9 alaptípus + G3 szabályváltozás + G1k helyesbítés): 44200–44211 (FROZEN_115 vs. F115_N); feladatcsomag.
    python -m arlc.run_r117
"""
import os
from multiprocessing import Pool

from . import run_r107 as R107
from . import run_r112 as R112
from . import run_r116 as R116
from . import v4 as V4
from .generator5 import KINDS5

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-117")

if __name__ == "__main__":
    R116.OUT = os.path.join(OUT, "g5")
    R116.VARIANTS = {"FROZEN_91": V4.FROZEN_91, "F115_N": V4.F115_N}
    R112.OUT = OUT
    R112.V_COPY = {"FROZEN_115": V4.FROZEN_115, "F115_N": V4.F115_N}
    R107.OUT = OUT
    R107.VARIANTS = {"FROZEN_115": V4.FROZEN_115, "F115_N": V4.F115_N}
    for d in ("g5", "copy", "test", "battery"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    jobs_g5 = [(k, s, vi) for k in KINDS5 for s in range(44000, 44015) for vi in range(2)]
    jobs_cp = [("bevált másoló", s, vi) for s in range(44100, 44120) for vi in range(2)]
    jobs_t = [(g, k, s, vi) for (g, k) in R107.CASES for s in range(44200, 44212) for vi in range(2)]
    with Pool(4) as pool:
        for r in pool.imap_unordered(R107.bat, ["FROZEN_115", "F115_N"]):
            print("battery", r, flush=True)
        for r in pool.imap_unordered(R116.job, jobs_g5):
            print("g5", *r, flush=True)
        for r in pool.imap_unordered(R112.job_copy, jobs_cp):
            print("copy", *r, flush=True)
        for r in pool.imap_unordered(R107.job, jobs_t):
            print(*r, flush=True)
    print("KÉSZ", flush=True)
