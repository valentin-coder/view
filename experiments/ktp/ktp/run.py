"""KTP futtató: tudásszűrő -> fejlesztési sweep -> előregisztráció -> teszt -> riport.

Használat (lásd README):
    python -m ktp.run all --model Qwen/Qwen2.5-0.5B --out runs/qwen05
    python -m ktp.run smoke --out runs/smoke      # véletlen súlyú mini modell, csak kódellenőrzés
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import random
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch

from . import data as D
from . import stats as S
from .core import Op, Patch, category_subspace, margins, subject_states, load_model

CODE_DIR = Path(__file__).resolve().parent
MODES = ("subj_last", "subj_all")


def code_hash() -> str:
    h = hashlib.sha256()
    for p in sorted(CODE_DIR.glob("*.py")):
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


class Ctx:
    """A futás közös állapota: modell, világ, cache-elt margók, μ-k, alterek."""

    def __init__(self, model, tok, args):
        self.model, self.tok, self.args = model, tok, args
        self.entities = D.build_entities(args.seed)
        self.cache: dict[str, float] = {}
        self.mu: dict[str, dict] = {}       # mode -> {'ent': (L,n,d), 'names': [...]}
        self.n_layers = None

    # ---------- szerkesztetlen margók cache-sel ----------
    def plain_margins(self, items: list[D.Rendered]) -> np.ndarray:
        todo = [r for r in {r.text: r for r in items}.values() if r.text not in self.cache]
        if todo:
            ms = margins(self.model, self.tok, todo, batch_size=self.args.batch_size)
            for r, m in zip(todo, ms):
                self.cache[r.text] = float(m)
        return np.array([self.cache[r.text] for r in items])

    # ---------- μ és kategória-altér ----------
    def estimate_mu(self) -> None:
        names = sorted(self.entities)
        items, owner = [], []
        for n in names:
            for r in D.render_neutral(n):
                items.append(r)
                owner.append(n)
        for mode in MODES:
            st = subject_states(self.model, self.tok, items, mode, self.args.batch_size)
            L, _, d = st.shape
            ent = np.zeros((L, len(names), d), dtype=np.float32)
            for i, n in enumerate(names):
                idx = [j for j, o in enumerate(owner) if o == n]
                ent[:, i] = st[:, idx].mean(1)
            self.mu[mode] = {"ent": ent, "names": names}
            self.n_layers = L

    def ent_vec(self, mode: str, layer: int, name: str) -> np.ndarray:
        m = self.mu[mode]
        return m["ent"][layer, m["names"].index(name)]

    def cat_mu(self, mode: str, layer: int, cat: str, include: str | None = None) -> np.ndarray:
        names = [n for n, e in self.entities.items() if e.category == cat and e.split == "mu"]
        if include:
            names = names + [include]
        return np.mean([self.ent_vec(mode, layer, n) for n in names], axis=0)

    def subspace(self, mode: str, layer: int) -> np.ndarray:
        key = (mode, layer)
        if not hasattr(self, "_Q"):
            self._Q = {}
        if key not in self._Q:
            self._Q[key] = category_subspace({c: self.cat_mu(mode, layer, c) for c in D.CATEGORIES})
        return self._Q[key]


# ---------------------------------------------------------------- tudásszűrő
def run_filter(ctx: Ctx, split: str) -> tuple[list[D.Edit], list[D.Question], dict]:
    a = ctx.args
    edits = D.build_edits(ctx.entities, split)
    qs_all = {e.key: D.questions_for_edit(e, ctx.entities) for e in edits}
    ed_by_key = {e.key: e for e in edits}

    flat = [q for qs in qs_all.values() for q in qs]
    b0 = ctx.plain_margins([D.render(q, ed_by_key[q.edit_key], "plain") for q in flat])

    proto = {}
    for p in D.PROPERTIES:
        for c in D.CATEGORIES:
            names = [n for n, e in ctx.entities.items() if e.category == c and e.split == "mu"]
            ms = ctx.plain_margins([D.render_proto(p, n) for n in names])
            proto[(p, c)] = float(np.mean(ms))

    def correct(m, v):
        return m > a.margin if v else m < -a.margin

    kept_q: list[D.Question] = []
    for q, m in zip(flat, b0):
        e = ed_by_key[q.edit_key]
        ok = a.no_filter or correct(m, q.before)
        if q.kind in ("D", "I") and not a.no_filter:
            ok = ok and correct(proto[(q.prop, e.new)], q.after)
        if ok:
            kept_q.append(q)
    by_edit: dict[str, list[D.Question]] = {}
    for q in kept_q:
        by_edit.setdefault(q.edit_key, []).append(q)
    kept_edits, final_q = [], []
    for e in edits:
        qs = by_edit.get(e.key, [])
        n_rr = sum(q.kind in S.RR_KINDS for q in qs)
        n_cr = sum(q.kind in S.CR_KINDS for q in qs)
        if n_rr >= a.min_rr and n_cr >= a.min_cr:
            kept_edits.append(e)
            final_q.extend(qs)
    per_kind_total = {k: sum(q.kind == k for q in flat) for k in ("D", "S1", "S2", "I", "T")}
    per_kind_kept = {k: sum(q.kind == k for q in kept_q) for k in ("D", "S1", "S2", "I", "T")}
    info = {
        "split": split, "edits_total": len(edits), "edits_kept": len(kept_edits),
        "questions_total": per_kind_total, "questions_passing": per_kind_kept,
        "proto": {f"{p}|{c}": v for (p, c), v in proto.items()},
    }
    log(f"szűrő [{split}]: {len(kept_edits)}/{len(edits)} szerkesztés marad; "
        f"kérdések: {per_kind_kept} / {per_kind_total}")
    return kept_edits, final_q, info


# ---------------------------------------------------------------- beavatkozások
def make_op(ctx: Ctx, cfg: dict, edit: D.Edit, target: str | None = None, site: str | None = None,
            control: str | None = None) -> Op:
    """cfg: {'method': 'T1'|'T2', 'layer', 'mode', 'alpha'}."""
    mode, layer = cfg["mode"], cfg["layer"]
    new = target or edit.new
    mu_new = ctx.cat_mu(mode, layer, new)
    leak = edit.entity if control == "C4" else None
    mu_old = ctx.cat_mu(mode, layer, edit.old, include=leak)
    site = site or mode
    if cfg["method"] == "T1" or control in ("C3", "C4"):
        alpha = cfg.get("alpha", 1.0) if cfg["method"] == "T1" else 1.0
        vec = alpha * (mu_new - mu_old)
        if cfg["method"] == "T2" and control == "C3":
            Q = ctx.subspace(mode, layer)
            vec = Q @ (Q.T @ (mu_new - mu_old))
        return Op("add", vec.astype(np.float32), site)
    return Op("replace", mu_new.astype(np.float32), site)


def random_op(ctx: Ctx, cfg: dict, edit: D.Edit, rng: np.random.Generator) -> Op:
    ref = make_op(ctx, cfg, edit)
    if ref.kind == "add":
        norm = np.linalg.norm(ref.vec)
    else:
        Q = ctx.subspace(cfg["mode"], cfg["layer"])
        mo = ctx.cat_mu(cfg["mode"], cfg["layer"], edit.old)
        norm = np.linalg.norm(Q @ (Q.T @ (ref.vec - mo)))
    v = rng.standard_normal(ref.vec.shape).astype(np.float32)
    return Op("add", (v / np.linalg.norm(v) * norm).astype(np.float32), cfg["mode"])


def wrong_target(edit: D.Edit) -> str:
    for c in D.CATEGORIES:
        if c not in (edit.old, edit.new):
            return c
    raise RuntimeError


def run_condition(ctx: Ctx, qs: list[D.Question], eds: dict[str, D.Edit], cond: str,
                  cfg: dict | None = None) -> np.ndarray:
    a = ctx.args
    if cond in ("B0", "B1", "B2", "B3"):
        kind = {"B0": "plain", "B1": "context", "B2": "rewrite", "B3": "context+rewrite"}[cond]
        return ctx.plain_margins([D.render(q, eds[q.edit_key], kind) for q in qs])
    items = [D.render(q, eds[q.edit_key], "plain") for q in qs]
    rng = np.random.default_rng(a.seed + 7)
    op_cache: dict[tuple, Op] = {}
    ops = []
    for q in qs:
        e = eds[q.edit_key]
        key = (e.key, cond)
        if key not in op_cache:
            if cond == "C1":
                op_cache[key] = random_op(ctx, cfg, e, rng)
            elif cond == "C2":
                op_cache[key] = make_op(ctx, cfg, e, target=wrong_target(e))
            elif cond == "C3":
                op_cache[key] = make_op(ctx, cfg, e, site="final", control="C3")
            elif cond == "C4":
                op_cache[key] = make_op(ctx, cfg, e, control="C4")
            else:
                op_cache[key] = make_op(ctx, cfg, e)
        ops.append(op_cache[key])
    Q = ctx.subspace(cfg["mode"], cfg["layer"]) if cfg["method"] == "T2" else None
    patch = Patch(cfg["layer"], ops, Q, cfg.get("norm_keep", False))
    return margins(ctx.model, ctx.tok, items, patch, a.batch_size)


def rows_for(qs: list[D.Question], eds: dict[str, D.Edit]) -> list[dict]:
    return [{"qid": q.qid, "edit": q.edit_key, "entity": q.entity, "kind": q.kind, "prop": q.prop,
             "before": q.before, "after": q.after, "pair_type": eds[q.edit_key].pair_type,
             "old": eds[q.edit_key].old, "new": eds[q.edit_key].new} for q in qs]


# ---------------------------------------------------------------- sweep
def sweep_configs(ctx: Ctx) -> list[dict]:
    a = ctx.args
    L = ctx.n_layers
    layers = list(range(a.layer_start, L - 1, a.layer_stride))
    cfgs = []
    for layer in layers:
        for mode in MODES:
            for alpha in a.alphas:
                cfgs.append({"method": "T1", "layer": layer, "mode": mode, "alpha": alpha})
            cfgs.append({"method": "T2", "layer": layer, "mode": mode})
    return cfgs


def run_sweep(ctx: Ctx, out: Path) -> dict:
    a = ctx.args
    edits, qs, finfo = run_filter(ctx, "dev")
    if not edits:
        raise SystemExit("a fejlesztési halmazon egy szerkesztés sem maradt a szűrő után")
    rng = random.Random(a.seed)
    sample = rng.sample(edits, min(a.dev_edits, len(edits)))
    keys = {e.key for e in sample}
    eds = {e.key: e for e in sample}
    qs = [q for q in qs if q.edit_key in keys]
    rows = rows_for(qs, eds)
    b0 = run_condition(ctx, qs, eds, "B0")
    for r, m in zip(rows, b0):
        r["B0"] = float(m)
    rr0 = S.aggregate(S.per_edit(rows, "B0"))["rr"]
    results = []
    cfgs = sweep_configs(ctx)
    log(f"sweep: {len(cfgs)} konfiguráció × {len(qs)} kérdés ({len(sample)} szerkesztés)")
    for i, cfg in enumerate(cfgs):
        ms = run_condition(ctx, qs, eds, "T", cfg)
        name = f"cfg{i}"
        for r, m in zip(rows, ms):
            r[name] = float(m)
        agg = S.aggregate(S.per_edit(rows, name))
        results.append({**cfg, **agg, "rr_gain": agg["rr"] - rr0})
        if (i + 1) % 8 == 0 or i + 1 == len(cfgs):
            log(f"  {i + 1}/{len(cfgs)} kész")
    best = max(results, key=lambda r: (r["f"], -abs(r.get("alpha", 1.0) - 1.0)))
    chosen = {k: best[k] for k in ("method", "layer", "mode") if k in best}
    if best["method"] == "T1":
        chosen["alpha"] = best["alpha"]
    res = {"filter": finfo, "rr_B0": rr0, "results": results, "chosen": chosen,
           "dev_edits": sorted(keys)}
    (out / "sweep.json").write_text(json.dumps(res, indent=1))
    log(f"választott konfiguráció: {chosen} (dev F={best['f']:.3f})")
    return res


def write_prereg(ctx: Ctx, out: Path, chosen: dict) -> dict:
    a = ctx.args
    pre = {
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "model": a.model, "code_hash": code_hash(), "seed": a.seed,
        "chosen": chosen, "margin": a.margin, "min_rr": a.min_rr, "min_cr": a.min_cr,
        "thresholds": {
            "min_test_edits": a.min_test_edits, "H1_diff": 0.10, "H2_cr_max": 0.10,
            "H3_gain_fraction": 0.5, "H4_c3_fraction": 0.8, "H5_diff": 0.15,
            "C1_fail_fraction": 0.5, "S2_cr_fail": 0.10,
        },
        "n_boot": a.n_boot,
    }
    (out / "preregistration.json").write_text(json.dumps(pre, indent=1))
    log("előregisztráció rögzítve: preregistration.json")
    return pre


# ---------------------------------------------------------------- teszt
def run_test(ctx: Ctx, out: Path) -> dict:
    a = ctx.args
    pre_path = out / "preregistration.json"
    if not pre_path.exists():
        raise SystemExit("hiányzik a preregistration.json – előbb a sweep lépés kell")
    pre = json.loads(pre_path.read_text())
    if pre["code_hash"] != code_hash() and not a.force:
        raise SystemExit("a kód megváltozott az előregisztráció óta (--force-szal felülírható, "
                         "de akkor a teszt nem előregisztrált)")
    best = dict(pre["chosen"])
    edits, qs, finfo = run_filter(ctx, "test")
    eds = {e.key: e for e in edits}
    rows = rows_for(qs, eds)
    L = ctx.n_layers
    other_method = {"method": "T2", "layer": best["layer"], "mode": best["mode"]} \
        if best["method"] == "T1" else \
        {"method": "T1", "layer": best["layer"], "mode": best["mode"], "alpha": 1.0}
    conds: dict[str, dict | None] = {"B0": None, "B1": None, "B2": None, "B3": None, "T": best,
                                     "T_other": other_method,
                                     "T_norm": {**best, "norm_keep": True}}
    if best["layer"] - 1 >= 0:
        conds["T_lm1"] = {**best, "layer": best["layer"] - 1}
    if best["layer"] + 1 <= L - 2:
        conds["T_lp1"] = {**best, "layer": best["layer"] + 1}
    for c in ("C1", "C2", "C3", "C4"):
        conds[c] = best
    for name, cfg in conds.items():
        log(f"teszt feltétel: {name}")
        cond = name if name in ("B0", "B1", "B2", "B3", "C1", "C2", "C3", "C4") else "T"
        ms = run_condition(ctx, qs, eds, cond, cfg)
        for r, m in zip(rows, ms):
            r[name] = float(m)
    for r in rows:  # C2: a hamis célkategória értéke
        z = wrong_target(eds[r["edit"]])
        r["c2_informative"] = r["kind"] in ("D", "I") and r["prop"] in D.PROPERTIES and \
            D.value(r["prop"], z) != r["after"]
    res = {"prereg": pre, "filter": finfo, "conditions": {k: v for k, v in conds.items()},
           "rows": rows, "proto": finfo["proto"]}
    (out / "test_rows.json").write_text(json.dumps(res, indent=1))
    return res


# ---------------------------------------------------------------- riport
def analyse(res: dict) -> dict:
    rows = res["rows"]
    pre = res["prereg"]
    th = pre["thresholds"]
    conds = list(res["conditions"])
    pes = {c: S.per_edit(rows, c) for c in conds}
    agg = {c: S.aggregate(pes[c]) for c in conds}
    rr0 = agg["B0"]["rr"]
    gain = {c: agg[c]["rr"] - rr0 for c in conds}

    def sub(kind_filter, method):
        rs = [r for r in rows if kind_filter(r)]
        return S.aggregate(S.per_edit(rs, method)) if rs else None

    by_kind = {}
    for c in conds:
        by_kind[c] = {
            "RR_D": sub(lambda r: r["kind"] in ("D",) or r["kind"] in S.CR_KINDS, c),
            "RR_I": sub(lambda r: r["kind"] == "I", c),
            "CR_S1": S.aggregate(S.per_edit([r for r in rows if r["kind"] == "S1"], c, kinds_cr=("S1",))),
            "CR_S2": S.aggregate(S.per_edit([r for r in rows if r["kind"] == "S2"], c, kinds_cr=("S2",))),
        }
    by_pair = {}
    for pt in ("animal-animal", "cross-domain", "object-object"):
        rs = [r for r in rows if r["pair_type"] == pt]
        if rs:
            by_pair[pt] = {c: S.aggregate(S.per_edit(rs, c)) for c in ("B0", "B1", "B2", "T")}

    # hatásméret a D-kérdéseken
    eff = []
    for r in rows:
        if r["kind"] != "D":
            continue
        proto = res["proto"][f"{r['prop']}|{r['new']}"]
        den = proto - r["B0"]
        if abs(den) > 1e-6:
            eff.append((r["T"] - r["B0"]) / den)
    c2_rows = [r for r in rows if r.get("c2_informative")]
    c2_spurious = float(np.mean([(r["C2"] > 0) == r["after"] for r in c2_rows])) if c2_rows else float("nan")

    n_edits = agg["T"]["n_edits"]
    boot = S.cluster_bootstrap_diff(pes, "T", ["B1", "B2"], n_boot=pre["n_boot"], seed=pre["seed"])
    rr_I = {c: (by_kind[c]["RR_I"] or {}).get("rr", float("nan")) for c in conds}

    checks = {}
    checks["gate_n_edits"] = n_edits >= th["min_test_edits"]
    checks["H1"] = boot["diff"] >= th["H1_diff"] and boot["ci95"][0] > 0
    checks["H2"] = agg["T"]["cr"] <= th["H2_cr_max"]
    nb = [c for c in ("T_lm1", "T_lp1") if c in agg]
    checks["H3"] = bool(nb) and gain["T"] > 0 and all(gain[c] >= th["H3_gain_fraction"] * gain["T"] for c in nb)
    checks["H4"] = gain["T"] > 0 and gain["C3"] < th["H4_c3_fraction"] * gain["T"]
    checks["H5"] = rr_I["T"] - rr_I["B2"] >= th["H5_diff"]
    checks["C1_nonspecific"] = gain["T"] <= 0 or gain["C1"] >= th["C1_fail_fraction"] * gain["T"]
    s2 = {c: by_kind[c]["CR_S2"]["cr"] for c in ("T", "T_other")}
    checks["S2_both_fail"] = all(v > th["S2_cr_fail"] for v in s2.values())
    checks["B2_dominates"] = agg["B2"]["f"] >= agg["T"]["f"] and rr_I["B2"] >= rr_I["T"]

    if not checks["gate_n_edits"]:
        verdict = "NEM TESZTELHETŐ: a tudásszűrő után túl kevés szerkesztés maradt."
    elif gain["T"] <= 0:
        verdict = "NINCS HATÁS: a transzplantáció egyetlen D/I-választ sem vitt az új kategória felé a B0-hoz képest."
    elif checks["C1_nonspecific"]:
        verdict = "A C ELBUKOTT: a hatás nem specifikus (a véletlen irány is hasonlóan billent)."
    elif not checks["H4"]:
        verdict = ("Az 'LLM számolja ki a következményeket' állítás ELBUKOTT: a válaszpozícióban "
                   "ugyanaz a hatás (válasz-eltolás, nem átprogramozás).")
    elif checks["S2_both_fail"]:
        verdict = "A C ELBUKOTT ennél a modellnél: a kategória nem választható le az egyéni tulajdonságokról."
    elif checks["B2_dominates"]:
        verdict = "Az ARLC v2 VISSZAESIK: a kérdés-átírás (B2) mindenhol legalább olyan jó."
    elif checks["H1"] and checks["H5"] and checks["H3"] and checks["H4"]:
        verdict = "SIKER: az LLM a transzplantáció után maga számolja ki a következményeket."
    elif checks["H5"] and not checks["H1"]:
        verdict = "RÉSZLEGES: csak a H5 teljesül – hibrid (átírás, ahol lehet; transzplantáció implicit hivatkozásnál)."
    else:
        verdict = "VEGYES: egyik előregisztrált döntési ág sem teljesült tisztán; lásd a részleteket."
    return {"agg": agg, "gain": gain, "by_kind": by_kind, "by_pair": by_pair,
            "effect_size_median": float(np.median(eff)) if eff else float("nan"),
            "c2_spurious_rate": c2_spurious, "bootstrap_H1": boot,
            "wilcoxon": {r: S.wilcoxon_edits(pes["T"], pes[r]) for r in ("B1", "B2", "B3")},
            "rr_I": rr_I, "checks": checks, "verdict": verdict}


def fmt(x) -> str:
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.3f}"


def write_report(res: dict, an: dict, out: Path, smoke: bool) -> None:
    pre = res["prereg"]
    lines = []
    if smoke:
        lines += ["> **SMOKE TEST – VÉLETLEN SÚLYÚ MINI MODELL. A SZÁMOK ÉRTELMETLENEK,**",
                  "> csak azt mutatják, hogy a kód végigfut.", ""]
    lines += [f"# KTP riport – {pre['model']}", "",
              f"Előregisztrálva: {pre['created']}, kód-hash: `{pre['code_hash']}`, "
              f"konfiguráció: `{json.dumps(pre['chosen'])}`", "",
              f"**Ítélet:** {an['verdict']}", "",
              "## Tudásszűrő (teszt)", "",
              f"Szerkesztések: {res['filter']['edits_kept']} / {res['filter']['edits_total']}  ",
              f"Átment kérdések: {res['filter']['questions_passing']} / {res['filter']['questions_total']}", "",
              "## Feltételek", "", "| Feltétel | RR | CR | CR_T | F | RR_I |", "|---|---|---|---|---|---|"]
    for c, g in an["agg"].items():
        lines.append(f"| {c} | {fmt(g['rr'])} | {fmt(g['cr'])} | {fmt(g['crt'])} | {fmt(g['f'])} | "
                     f"{fmt(an['rr_I'].get(c))} |")
    b = an["bootstrap_H1"]
    lines += ["", "## Hipotézisek és döntési fa", "",
              f"- H1: F(T) − max(F(B1),F(B2)) = {fmt(b['diff'])}, 95% CI [{fmt(b['ci95'][0])}, "
              f"{fmt(b['ci95'][1])}], {b['n_edits']} szerkesztés / {b['n_entities']} entitás",
              f"- D-kérdések medián hatásmérete (e): {fmt(an['effect_size_median'])}",
              f"- C2 hamis átváltási arány: {fmt(an['c2_spurious_rate'])}",
              ""]
    for k, v in an["checks"].items():
        lines.append(f"- `{k}`: {'IGEN' if v else 'nem'}")
    lines += ["", "## Wilcoxon (szerkesztésenkénti F, T vs. alapvonal)", ""]
    for k, v in an["wilcoxon"].items():
        lines.append(f"- T vs {k}: n={v['n']}, medián különbség={fmt(v['median_diff'])}, p={fmt(v['p'])}")
    lines += ["", "## Párok típusa szerint (F)", "", "| Típus | B0 | B1 | B2 | T |", "|---|---|---|---|---|"]
    for pt, d in an["by_pair"].items():
        lines.append(f"| {pt} | " + " | ".join(fmt(d[c]["f"]) for c in ("B0", "B1", "B2", "T")) + " |")
    lines += ["", "## Kollaterális típusonként", "", "| Feltétel | CR_S1 | CR_S2 |", "|---|---|---|"]
    for c, d in an["by_kind"].items():
        lines.append(f"| {c} | {fmt(d['CR_S1']['cr'])} | {fmt(d['CR_S2']['cr'])} |")
    (out / "report.md").write_text("\n".join(lines) + "\n")
    (out / "analysis.json").write_text(json.dumps(an, indent=1, default=float))
    log(f"riport: {out / 'report.md'}")


# ---------------------------------------------------------------- smoke
def tiny_model_and_tokenizer(seed: int):
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM
    import re
    ents = D.build_entities(seed)
    texts = [D.FEWSHOT, "Note: in this story, are , not .\nTom saw near the house yesterday and"]
    for e in ents.values():
        for q in D.questions_for_edit(D.Edit(e.name, e.category, wrong_target(D.Edit(e.name, e.category, e.category, "")), ""), ents):
            texts.append(q.template + q.context)
        texts += [e.name, D.plural(e.name), e.color or ""]
    texts += list(D.CATEGORY_PLURAL.values()) + D.CATEGORIES + D.NEUTRAL_TEMPLATES
    texts += list(D.WRONG_COLOR.values()) + ["a", "an", "Yes", "No", "the", "it"]
    words = sorted({w for t in texts for w in re.findall(r"\w+|[^\w\s]+", t)})
    vocab = {"[PAD]": 0, "[UNK]": 1, "[EOS]": 2}
    for w in words:
        vocab.setdefault(w, len(vocab))
    tk = Tokenizer(models.WordLevel(vocab, unk_token="[UNK]"))
    tk.pre_tokenizer = pre_tokenizers.Whitespace()
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, pad_token="[PAD]", unk_token="[UNK]",
                                  eos_token="[EOS]")
    torch.manual_seed(seed)
    cfg = Qwen2Config(vocab_size=len(vocab), hidden_size=64, intermediate_size=128,
                      num_hidden_layers=4, num_attention_heads=4, num_key_value_heads=2,
                      max_position_embeddings=512)
    model = Qwen2ForCausalLM(cfg).eval()
    return model, tok


def smoke_checks(ctx: Ctx) -> None:
    """Gépi önellenőrzés: nulla beavatkozás nem változtat; az említések tokenjei a szót adják."""
    from .core import encode
    ent = D.build_entities(ctx.args.seed)
    e = next(iter(ent.values()))
    ed = D.Edit(e.name, e.category, wrong_target(D.Edit(e.name, e.category, e.category, "")), "test")
    qs = D.questions_for_edit(ed, ent)
    items = [D.render(q, ed, "plain") for q in qs]
    enc = encode(ctx.tok, items)
    for i, r in enumerate(items):
        if r.spans:
            words = ctx.tok.decode(enc.input_ids[i, enc.subj_pos[i]]).replace(" ", "")
            assert e.name.replace(" ", "") in words, (words, e.name)
    base = margins(ctx.model, ctx.tok, items, None, 4)
    d = ctx.model.config.hidden_size
    zero = Patch(1, [Op("add", np.zeros(d, np.float32), "subj_all") for _ in items])
    same = margins(ctx.model, ctx.tok, items, zero, 4)
    assert np.allclose(base, same, atol=1e-5), "a nulla beavatkozás megváltoztatta a kimenetet"
    big = Patch(1, [Op("add", np.full(d, 5.0, np.float32), "subj_all") for _ in items])
    moved = margins(ctx.model, ctx.tok, items, big, 4)
    has_span = np.array([bool(r.spans) for r in items])
    assert not np.allclose(base[has_span], moved[has_span]), "a beavatkozás nem hatott"
    log("smoke önellenőrzés: OK (nulla-patch azonos, nagy patch hat, említés-pozíciók helyesek)")


# ---------------------------------------------------------------- CLI
def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["filter", "sweep", "test", "report", "all", "smoke"])
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--out", default="runs/default")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--margin", type=float, default=1.0)
    ap.add_argument("--min-rr", type=int, default=3)
    ap.add_argument("--min-cr", type=int, default=2)
    ap.add_argument("--min-test-edits", type=int, default=60)
    ap.add_argument("--dev-edits", type=int, default=20)
    ap.add_argument("--layer-start", type=int, default=1)
    ap.add_argument("--layer-stride", type=int, default=2)
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.5, 1.0, 2.0])
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-filter", action="store_true", help="csak smoke teszthez: tudásszűrő kikapcsolva")
    a = ap.parse_args(argv)

    if a.threads:
        torch.set_num_threads(a.threads)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    smoke = a.step == "smoke"
    if smoke:
        a.model = "TINY-RANDOM-QWEN2 (smoke test)"
        a.margin, a.min_rr, a.min_cr, a.min_test_edits = 0.0, 1, 1, 1
        a.dev_edits, a.layer_start, a.layer_stride, a.n_boot = 6, 0, 1, 200
        a.no_filter = True
        model, tok = tiny_model_and_tokenizer(a.seed)
        from .core import prepare
        model, tok = prepare(model, tok)
    else:
        log(f"modell betöltése: {a.model}")
        model, tok = load_model(a.model)
    ctx = Ctx(model, tok, a)
    if smoke:
        smoke_checks(ctx)

    if a.step == "filter":
        _, _, info = run_filter(ctx, "test")
        (out / "filter_test.json").write_text(json.dumps(info, indent=1))
        return
    if a.step == "report":
        res = json.loads((out / "test_rows.json").read_text())
        write_report(res, analyse(res), out, smoke="TINY" in res["prereg"]["model"])
        return

    log("μ becslése a semleges sablonokon")
    ctx.estimate_mu()
    if a.step in ("sweep", "all", "smoke"):
        sw = run_sweep(ctx, out)
        write_prereg(ctx, out, sw["chosen"])
    if a.step in ("test", "all", "smoke"):
        res = run_test(ctx, out)
        write_report(res, analyse(res), out, smoke)


if __name__ == "__main__":
    main(sys.argv[1:])
