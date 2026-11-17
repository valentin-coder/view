"""Az A fázis kísérletei (14. kör) orákulum-groundinggal: E1–E4, A5, A7.

Futtatás: python -m arlc.experiments --out runs/a-fazis
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics as st
import time
from pathlib import Path

from scipy.stats import spearmanr

from .core import Lit, Memory, Obs, Rule, Schema

MAIN_MODES = ("lookup", "recency", "wms", "arlc")


# ======================================================================= világok
class Taxo:
    """3 gyökér × 2 × 2 kategóriafa, szintenként külön tulajdonságkészlettel."""

    def __init__(self, seed: int, n_roots=3, branching=2, levels=3, per_leaf=2, pool=6):
        rng = random.Random(seed)
        self.rng = rng
        self.parent: dict[str, str | None] = {}
        self.level: dict[str, int] = {}
        frontier = []
        for r in range(n_roots):
            c = f"R{r}"
            self.parent[c], self.level[c] = None, 0
            frontier.append(c)
        for lv in range(1, levels):
            nxt = []
            for p in frontier:
                for b in range(branching):
                    c = f"{p}{'abcd'[b]}"
                    self.parent[c], self.level[c] = p, lv
                    nxt.append(c)
            frontier = nxt
        self.leaves = frontier
        self.cats = list(self.parent)
        self.props: dict[str, dict[str, bool]] = {}
        for c in self.cats:
            ps = rng.sample([f"p{self.level[c]}_{k}" for k in range(pool)], 2)
            self.props[c] = {p: rng.random() < 0.5 for p in ps}
        self.disjoint = set()
        for a in self.cats:
            for b in self.cats:
                if a < b and self.parent[a] == self.parent[b]:
                    self.disjoint.add(frozenset((a, b)))
        self.entities = {}
        for leaf in self.leaves:
            for i in range(per_leaf):
                self.entities[f"{leaf.lower()}_{i}"] = leaf

    def chain(self, c):
        out = []
        while c is not None:
            out.append(c)
            c = self.parent[c]
        return out

    def truth(self, leaf):
        t = {}
        for c in self.chain(leaf):
            t.update(self.props[c])
        return t

    def schema(self, extra_entities=0):
        return Schema(disjoint=set(self.disjoint), n_entities=len(self.entities) + extra_entities,
                      n_categories=len(self.cats), n_props=6 * 3)

    def rule_obs(self, ctr):
        out = []
        for c in self.cats:
            if self.parent[c]:
                out.append(Obs(next(ctr), "book", 0, 0.95, rule=Rule(c, "isa", self.parent[c], True)))
            for p, v in self.props[c].items():
                out.append(Obs(next(ctr), "book", 0, 0.95, rule=Rule(c, "has", p, v)))
        return out


class Counter_:
    def __init__(self):
        self.i = 0

    def __next__(self):
        self.i += 1
        return self.i


def feed(mem: Memory, obs: list[Obs]):
    for o in obs:
        mem.observe(o)


def stream_base(tx: Taxo, ctr, skip_facts=(), noise=0.0, rng=None, facts_per=2):
    """Szabályok, majd entitásonként tagság + tények (opcionális zajjal)."""
    obs = tx.rule_obs(ctr)
    t = 1
    for e, leaf in tx.entities.items():
        lf = leaf
        if noise and rng.random() < noise:
            lf = rng.choice([x for x in tx.leaves if x != leaf])
        obs.append(Obs(next(ctr), "survey", t, 0.9, lit=Lit("isa", e, lf, True)))
        t += 1
        if e in skip_facts:
            continue
        tr = tx.truth(leaf)
        for p in rng.sample(sorted(tr), facts_per):
            v = tr[p]
            if noise and rng.random() < noise:
                v = not v
            obs.append(Obs(next(ctr), "field", t, 0.9, lit=Lit("has", e, p, v)))
            t += 1
    return obs, t


# ======================================================================= E1
def e1(seeds=range(10)):
    """Propagáció: egy entitás átkategorizálása (d = 1, 2, 3 távolságra) és egy
    alosztály-szabály cseréje. Tiszta helyzet: az érintett entitásokról nincs tény."""
    rows = []
    for seed in seeds:
        tx = Taxo(seed)
        rng = random.Random(seed + 100)
        for kind in ("recat-d1", "recat-d2", "recat-d3", "subclass"):
            leaf0 = rng.choice(tx.leaves)
            if kind.startswith("recat"):
                d = int(kind[-1])
                e = next(x for x, l in tx.entities.items() if l == leaf0)
                c0 = tx.chain(leaf0)   # [levél, szülő, gyökér]
                if d == 1:      # testvérlevél: közös szülő
                    cands = [l for l in tx.leaves if l != leaf0 and tx.chain(l)[1] == c0[1]]
                elif d == 2:    # unokatestvér: közös gyökér, más szülő
                    cands = [l for l in tx.leaves if tx.chain(l)[2] == c0[2] and tx.chain(l)[1] != c0[1]]
                else:           # más gyökér
                    cands = [l for l in tx.leaves if tx.chain(l)[2] != c0[2]]
                leaf1 = rng.choice(cands)
                affected = {e: (leaf0, leaf1)}
                skip = {e}
            else:
                par = tx.parent[leaf0]
                root = tx.chain(leaf0)[-1]
                newpar = rng.choice([c for c in tx.cats if tx.level[c] == 1 and tx.chain(c)[-1] != root])
                members = [x for x, l in tx.entities.items() if l == leaf0]
                affected = {}
                skip = set(members)
            for mode in MAIN_MODES:
                ctr = Counter_()
                obs, t = stream_base(tx, ctr, skip_facts=skip, rng=random.Random(seed))
                mem = Memory(tx.schema(), mode=mode)
                feed(mem, obs)
                truth_now = {x: tx.truth(l) for x, l in tx.entities.items()}
                pre = {(x, p): mem.answer(x, p, record_use=False) for x in truth_now for p in truth_now[x]}
                if kind.startswith("recat"):
                    mem.observe(Obs(next(ctr), "expert", t, 0.99, lit=Lit("isa", e, leaf1, True)))
                    new_truth = dict(truth_now)
                    new_truth[e] = tx.truth(leaf1)
                    ent_aff = [e]
                else:
                    mem.observe(Obs(next(ctr), "expert", t, 0.999, rule=Rule(leaf0, "isa", newpar, True)))
                    new_truth = dict(truth_now)
                    for x in members:
                        tt = dict(tx.props[leaf0])
                        for c in tx.chain(newpar):
                            for p, v in tx.props[c].items():
                                tt.setdefault(p, v)
                        new_truth[x] = tt
                    ent_aff = members
                rip, coll = [], []
                for x in new_truth:
                    keys = set(truth_now[x]) | set(new_truth[x])
                    for p in keys:
                        exp = new_truth[x].get(p)
                        ans = mem.answer(x, p, record_use=False)
                        if x in ent_aff and truth_now[x].get(p) != exp:
                            rip.append(ans == exp)
                        elif pre.get((x, p)) == exp:
                            coll.append(ans != exp)
                rows.append({"seed": seed, "kind": kind, "mode": mode, "n_ripple": len(rip),
                             "rr": sum(rip) / len(rip) if rip else math.nan,
                             "collateral": sum(coll) / len(coll) if coll else math.nan,
                             "pre_acc": sum(pre[(x, p)] == truth_now[x][p] for (x, p) in pre) / len(pre)})
    return rows


# ======================================================================= E2a / E2b
def _dax_world(N, M, n_extra=0):
    sch = Schema(disjoint={frozenset(("dax", "other"))}, n_entities=N + M + 2 + n_extra,
                 n_categories=2, n_props=2)
    ctr = Counter_()
    obs = [Obs(next(ctr), "book", 0, 0.95, rule=Rule("dax", "has", "poisonous", True))]
    t = 1
    obs.append(Obs(next(ctr), "survey", t, 0.9, lit=Lit("isa", "probe", "dax")))
    for i in range(N):
        t += 1
        obs.append(Obs(next(ctr), f"s{i}", t, 0.9, lit=Lit("isa", f"d{i}", "dax")))
        t += 1
        obs.append(Obs(next(ctr), f"s{i}", t, 0.9, lit=Lit("has", f"d{i}", "poisonous", True)))
    return sch, obs, ctr, t


def e2a(Ns=(1, 2, 4, 8, 12, 16), M=30):
    """Anomália-csepegtetés: hány ellenpélda kell a 'dax mérges' szabály feladásához?"""
    rows = []
    for mode in ("recency", "wms", "arlc"):
        for N in Ns:
            sch, obs, ctr, t = _dax_world(N, M)
            mem = Memory(sch, mode=mode)
            feed(mem, obs)
            flip = None
            for j in range(1, M + 1):
                t += 1
                mem.observe(Obs(next(ctr), f"a{j}", t, 0.9, lit=Lit("isa", f"x{j}", "dax")))
                t += 1
                mem.observe(Obs(next(ctr), f"a{j}", t, 0.9, lit=Lit("has", f"x{j}", "poisonous", False)))
                if mem.answer("probe", "poisonous", record_use=False) is not True:
                    flip = j
                    break
            rows.append({"mode": mode, "N": N, "flip_at": flip,
                         "predicted_arlc": math.ceil((4.25 + 0.93 * N) / 3.17)})
    return rows


def e2b(Ns=(0, 1, 2, 4, 8), qs=(0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999, 0.9999999)):
    """Egyetlen erős általános állítás ('a daxok nem mérgesek'): mekkora hitelesség kell?"""
    rows = []
    for mode in ("recency", "wms", "arlc"):
        for N in Ns:
            need = None
            for q in qs:
                sch, obs, ctr, t = _dax_world(N, 0)
                mem = Memory(sch, mode=mode)
                feed(mem, obs)
                new = Obs(next(ctr), "strong", t + 1, q, rule=Rule("dax", "has", "poisonous", False))
                mem.observe(new)
                if 1 in mem.best.rej and new.id not in mem.best.rej:   # a régi szabály kiesett, az új él
                    need = q
                    break
            rows.append({"mode": mode, "N": N, "q_needed": need,
                         "bits_needed": None if need is None else -math.log2(1 - need)})
    return rows


# ======================================================================= E3
def e3(n=8, systematic=True, c_ctx=6.0):
    """Két forrás ütközik: rendszerszerűen (kontextus kell) vagy zajosan (elutasítás kell)."""
    rng = random.Random(3)
    rows = []
    for mode in ("recency", "wms", "arlc"):
        sch = Schema(disjoint=set(), n_entities=n, n_categories=1, n_props=1)
        mem = Memory(sch, mode=mode, c_ctx=c_ctx)
        ctr = Counter_()
        t = 0
        b_vals = {}
        for i in range(n):
            t += 1
            mem.observe(Obs(next(ctr), "survey", t, 0.9, lit=Lit("isa", f"m{i}", "dax")))
        for i in range(n):
            t += 1
            mem.observe(Obs(next(ctr), "A", t, 0.9, lit=Lit("has", f"m{i}", "poisonous", True)))
        for i in range(n):
            t += 1
            v = False if systematic else (rng.random() < 0.5)
            b_vals[i] = v
            mem.observe(Obs(next(ctr), "B", t, 0.9, lit=Lit("has", f"m{i}", "poisonous", v)))
        ok_a = sum(mem.answer(f"m{i}", "poisonous", ctx="A", record_use=False) is True for i in range(n)) / n
        if systematic:
            ok_b = sum(mem.answer(f"m{i}", "poisonous", ctx="B", record_use=False) is False for i in range(n)) / n
        else:
            ok_b = sum(mem.answer(f"m{i}", "poisonous", ctx=None, record_use=False) is True for i in range(n)) / n
        rows.append({"mode": mode, "systematic": systematic, "acc_A": ok_a,
                     "acc_B_or_global": ok_b, "isolated": sorted(mem.best.iso)})
    return rows


# ======================================================================= E4
def e4(eps_list=(0.0, 0.02, 0.05, 0.1), seeds=range(5)):
    """Zaj meglepetés nélkül: hamis szerkezeti átrendezések 50 megfigyelésenként."""
    rows = []
    for eps in eps_list:
        for seed in seeds:
            tx = Taxo(seed)
            for mode in ("recency", "wms", "arlc"):
                ctr = Counter_()
                obs, _ = stream_base(tx, ctr, noise=eps, rng=random.Random(seed * 7 + int(eps * 100)))
                mem = Memory(tx.schema(), mode=mode)
                feed(mem, obs)
                n_obs = len(obs)
                struct = 0
                for ev in mem.events:
                    struct += len(ev.get("rules_dropped", [])) + len(ev.get("exc_added", [])) + \
                        len(ev.get("iso_added", [])) + len(ev.get("cut_added", []))
                final = mem.best
                rules_lost = sum(1 for i in final.rej if mem.by_id[i].rule is not None)
                acc = []
                for x, leaf in tx.entities.items():
                    for p, v in tx.truth(leaf).items():
                        acc.append(mem.answer(x, p, record_use=False) == v)
                rows.append({"eps": eps, "seed": seed, "mode": mode,
                             "struct_events_per50": 50 * struct / n_obs,
                             "rules_lost_final": rules_lost, "exc_final": len(final.exc),
                             "acc": sum(acc) / len(acc)})
    return rows


# ======================================================================= A5
def a5(etas=(0.0, 0.05, 0.1, 0.2, 0.4), decays=(1.0, 0.9, 0.7, 0.5), u=5, n0=3, kmax=40, dwell=0):
    """Hiszterézis: használatfüggő beágyazottság mellett a visszaváltás több evidenciát kíván?
    decay = 1.0: a használat nem cseng le (jóslat: elsőbbségi hatás); < 1: lecsengés."""
    rows = []
    for eta in etas:
      for decay in (decays if eta else (1.0,)):
        sch = Schema(disjoint={frozenset(("A", "B"))}, n_entities=2, n_categories=2, n_props=2)
        mem = Memory(sch, mode="arlc", eta=eta, beam=8, use_decay=decay)
        ctr = Counter_()
        t = 0
        for c, p in (("A", "pa"), ("B", "pb")):
            mem.observe(Obs(next(ctr), "book", 0, 0.95, rule=Rule(c, "has", p, True)))
        nA = nB = 0
        for i in range(n0):
            t += 1
            nA += 1
            mem.observe(Obs(next(ctr), f"a{nA}", t, 0.9, lit=Lit("isa", "x", "A")))
            for _ in range(u):
                mem.answer("x", "pa")
        up = down = None
        for k in range(kmax):
            t += 1
            nB += 1
            mem.observe(Obs(next(ctr), f"b{nB}", t, 0.9, lit=Lit("isa", "x", "B")))
            for _ in range(u):
                mem.answer("x", "pa"), mem.answer("x", "pb")
            if mem.answer_isa("x", "B"):
                up = nB - nA
                break
        for _ in range(dwell * u):   # tartózkodás: az új séma használatban van, új evidencia nélkül
            mem.answer("x", "pb")
        for k in range(kmax):
            t += 1
            nA += 1
            mem.observe(Obs(next(ctr), f"a{nA}", t, 0.9, lit=Lit("isa", "x", "A")))
            for _ in range(u):
                mem.answer("x", "pa"), mem.answer("x", "pb")
            if mem.answer_isa("x", "A"):
                down = nA - nB
                break
        rows.append({"eta": eta, "decay": decay, "dwell": dwell, "delta_up": up, "delta_down": down,
                     "hysteresis": None if up is None or down is None else down - up})
    return rows


# ======================================================================= A7
def a7(n=5):
    """Frissítés vs. revízió: lakhely (változhat) és kategória (nem változik)."""
    rows = []
    for mode in ("recency", "wms", "arlc-nocut", "arlc"):
        sch = Schema(disjoint={frozenset(("bird", "fish"))},
                     groups={"loc_bp": "loc", "loc_vie": "loc"},
                     update_prior={"loc": 0.3, "isa": 1e-3}, n_entities=2 * n, n_categories=2, n_props=4)
        mem = Memory(sch, mode=mode)
        ctr = Counter_()
        mem.observe(Obs(next(ctr), "book", 0, 0.95, rule=Rule("bird", "has", "feathers", True)))
        mem.observe(Obs(next(ctr), "book", 0, 0.95, rule=Rule("fish", "has", "fins", True)))
        for i in range(n):
            mem.observe(Obs(next(ctr), f"p{i}", 1, 0.9, lit=Lit("has", f"m{i}", "loc_bp", True)))
            mem.observe(Obs(next(ctr), f"p{i}", 1, 0.9, lit=Lit("isa", f"r{i}", "bird")))
        for i in range(n):
            mem.observe(Obs(next(ctr), f"q{i}", 10, 0.9, lit=Lit("has", f"m{i}", "loc_vie", True)))
            mem.observe(Obs(next(ctr), f"q{i}", 10, 0.95, lit=Lit("isa", f"r{i}", "fish")))
        res = {"loc_now": [], "loc_past": [], "cat_now": [], "cat_past": []}
        for i in range(n):
            res["loc_now"].append(mem.answer(f"m{i}", "loc_vie", record_use=False) is True)
            res["loc_past"].append(mem.answer(f"m{i}", "loc_bp", t=5, record_use=False) is True)
            res["cat_now"].append(mem.answer(f"r{i}", "fins", record_use=False) is True)
            res["cat_past"].append(mem.answer(f"r{i}", "fins", t=5, record_use=False) is True)
        rows.append({"mode": mode, **{k: sum(v) / len(v) for k, v in res.items()},
                     "cuts": len(mem.best.cut)})
    return rows


# ======================================================================= main
def summarize_e1(rows):
    out = {}
    for kind in sorted({r["kind"] for r in rows}):
        for mode in MAIN_MODES:
            rs = [r for r in rows if r["kind"] == kind and r["mode"] == mode]
            out[f"{kind}|{mode}"] = {
                "rr": st.mean(r["rr"] for r in rs if not math.isnan(r["rr"])),
                "collateral": st.mean(r["collateral"] for r in rs if not math.isnan(r["collateral"])),
                "n_ripple_mean": st.mean(r["n_ripple"] for r in rs),
                "pre_acc": st.mean(r["pre_acc"] for r in rs)}
    return out


def summarize_e4(rows):
    out = {}
    for eps in sorted({r["eps"] for r in rows}):
        for mode in ("recency", "wms", "arlc"):
            rs = [r for r in rows if r["eps"] == eps and r["mode"] == mode]
            out[f"{eps}|{mode}"] = {k: st.mean(r[k] for r in rs) for k in
                                    ("struct_events_per50", "rules_lost_final", "exc_final", "acc")}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs/a-fazis")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    res = {}
    todo = a.only or ["e1", "e2a", "e2b", "e3", "e4", "a5", "a7"]
    for name in todo:
        t0 = time.time()
        if name == "e1":
            rows = e1()
            res["e1"] = {"rows": rows, "summary": summarize_e1(rows)}
        elif name == "e2a":
            rows = e2a()
            ar = [r for r in rows if r["mode"] == "arlc" and r["flip_at"] is not None]
            rho = spearmanr([r["N"] for r in ar], [r["flip_at"] for r in ar]).statistic if len(ar) > 2 else None
            wm = [r for r in rows if r["mode"] == "wms" and r["flip_at"] is not None]
            rho_w = spearmanr([r["N"] for r in wm], [r["flip_at"] for r in wm]).statistic if len(wm) > 2 else None
            res["e2a"] = {"rows": rows, "spearman_arlc": rho, "spearman_wms": rho_w}
        elif name == "e2b":
            res["e2b"] = {"rows": e2b()}
        elif name == "e3":
            res["e3"] = {"rows": [dict(r, c_ctx=c) for c in (6.0, 9.0, 12.0, 16.0)
                                  for r in e3(systematic=True, c_ctx=c) + e3(systematic=False, c_ctx=c)]}
        elif name == "e4":
            rows = e4()
            res["e4"] = {"rows": rows, "summary": summarize_e4(rows)}
        elif name == "a5":
            res["a5"] = {"rows": a5(dwell=0) + a5(dwell=3) + a5(dwell=10)}
        elif name == "a7":
            res["a7"] = {"rows": a7()}
        print(f"{name}: {time.time() - t0:.1f}s", flush=True)
    (out / "results.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({k: (v.get("summary") or v.get("rows")) for k, v in res.items()}, indent=1, default=str)[:20000])


if __name__ == "__main__":
    main()
