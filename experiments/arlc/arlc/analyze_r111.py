"""111. kör elemzése (előregisztrált): python -m arlc.analyze_r111"""
import json
import math
import os
import statistics as st

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-111", "test")


def nm(x):
    x = [v for v in x if not math.isnan(v)]
    return round(st.mean(x), 4) if x else None


def main():
    R = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    out = {"n": len(R)}
    for k in ("bevált másoló", "független megerősítő"):
        for v in ("v3", "FROZEN_91", "F91_Q"):
            rv = [r for r in R if r["kind"] == k and r["variant"] == v]
            out[f"{k} | {v}"] = {"hibás részhalmaz előtte": nm(r["wrong_before"] for r in rv),
                                 "hibás részhalmaz utána": nm(r["wrong_after"] for r in rv),
                                 "változás": None, "target előtte": nm(r["target_before"] for r in rv),
                                 "target utána": nm(r["target_after"] for r in rv), "post": nm(r["post"] for r in rv),
                                 "új félretéve (átlag)": round(st.mean(r["new_rejected"] for r in rv), 2),
                                 "esetek hibás részhalmazzal": sum(1 for r in rv if r["n_wrong"])}
            d = out[f"{k} | {v}"]
            if d["hibás részhalmaz előtte"] is not None:
                d["változás"] = round(d["hibás részhalmaz utána"] - d["hibás részhalmaz előtte"], 4)
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
