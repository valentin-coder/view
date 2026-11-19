"""82. kör elemzése (előregisztrált): python -m arlc.analyze_r82"""
import json
import os
import statistics as st

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "kor-82", "test")
V = ("v3", "v4.9", "v4.9+PK")


def prec(h, t):
    return None if h + t == 0 else round(h / (h + t), 3)


def main():
    rows = [json.load(open(os.path.join(D, f))) for f in os.listdir(D) if f.endswith(".json")]
    out = {"n": len(rows)}
    for gs in ("G2", "G1A", "G1B", "G1B-szemét"):
        if gs == "G1B-szemét":
            R = [r for r in rows if r["gen"] + r["pop"] == "G1B" and r["garbage"]]
        else:
            R = [r for r in rows if r["gen"] + r["pop"] == gs]
        tab = {}
        for v in V:
            rv = [r for r in R if r["variant"] == v]
            if not rv:
                continue
            keys = sorted({k for r in rv for k in r["audit_pre"]})
            a = {k: round(st.mean(r["audit_pre"].get(k, 0) for r in rv), 2) for k in keys}
            srcs = sorted({k.rsplit(":", 1)[0] for k in keys if k.count(":") == 2})
            p = {s: prec(sum(r["audit_pre"].get(f"{s}:helyes_félretevés", 0) for r in rv),
                         sum(r["audit_pre"].get(f"{s}:téves_félretevés", 0) for r in rv)) for s in srcs}
            tab[v] = {"n": len(rv), "pre": round(st.mean(r["pre"] for r in rv), 4),
                      "post": round(st.mean(r["post"] for r in rv), 4),
                      "hazug félretett arány": round(sum(r["liar_rejected"] for r in rv) / max(1, sum(r["liar_n"] for r in rv)), 3),
                      "izolál (eset arány)": round(sum(1 for r in rv if r["audit_pre"].get("izolált_források", 0) > 0) / len(rv), 3),
                      "audit (átlag/eset)": a, "félretevés pontossága": p}
        out[gs] = tab
    json.dump(out, open(os.path.join(D, "..", "analysis.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
