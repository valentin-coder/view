"""105. kör, fejlesztési ellenőrzés (NEM teszt): eltérő q_temper-optimumot kívánnak-e a környezetek?"""
import json
import os
import statistics as st
from collections import defaultdict
from multiprocessing import Pool

from . import run_r102 as R
from . import v4 as V4

R.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-105", "dev")
QS = (0.5, 1.0, 2.0, 4.0)
R.VARIANTS = {f"q×{q}": (V4.FROZEN_91, q) for q in QS}
ENVS = {"igaz meglepetések (G1k)": [("G1k", k) for k in ("átkategorizálás", "szabály-helyesbítés", "kivételes alfaj")],
        "zajos források (G4)": [("G4", k) for k in ("hazug forrás", "jó új specialista", "romló forrás", "visszhang")]}

if __name__ == "__main__":
    os.makedirs(os.path.join(R.OUT, "test"), exist_ok=True)
    jobs = [(g, k, s, vi) for env in ENVS.values() for (g, k) in env
            for s in (range(16000, 16005) if g == "G1k" else range(28000, 28005)) for vi in range(len(QS))]
    with Pool(4) as pool:
        list(pool.imap_unordered(R.job, jobs))
    rows = [json.load(open(os.path.join(R.OUT, "test", f))) for f in os.listdir(os.path.join(R.OUT, "test"))]
    for env, sets in ENVS.items():
        for v in R.VARIANTS:
            rv = [r for r in rows if (r["gen"], r["kind"]) in sets and r["variant"] == v]
            print(env, v, "post %.4f target %.4f" % (st.mean(r["post"] for r in rv), st.mean(r["target"] for r in rv)), flush=True)
