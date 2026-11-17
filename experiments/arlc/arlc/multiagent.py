"""31. kör: többágenses ARLC – polarizáció tanult forrás-megbízhatósággal.

K ágens két táborban: az A tábor tankönyve szerint 'a dax mérges' (ez az igazság), a B táboré
szerint 'nem mérges'. Körönként minden ágens kap egy zajos privát megfigyelést (forrás:
saját érzékelő) és minden szomszédjától egy állítást egy daxról, a szomszéd aktuális
hiedelme szerint (forrás: a szomszéd neve). A megbízhatóság forrásonként tanul (béta).
"""
from __future__ import annotations

import itertools
import random
import statistics as st

from .core import Lit, Memory, Obs, Rule, Schema


def provenance(agent: Memory, e: str) -> list:
    """Az ágens e-re vonatkozó hiedelmének eredeti támaszai: a támaszhalmaz megfigyelései
    (érzékelés, tankönyvi szabály), a tagsági alapadatok nélkül."""
    H = agent.best
    cl = agent.closure(H, None, agent.now)
    d = cl.has.get(e, {})
    sup = d.get(("poisonous", True)) if ("poisonous", False) not in d else d.get(("poisonous", False))
    if sup is None or (("poisonous", True) in d and ("poisonous", False) in d):
        return []
    out = []
    for tok in sup:
        if tok[0] == "obs" and tok[1] < 10 ** 6:
            o = agent.by_id[tok[1]]
            if o.source != "census":
                out.append(o)
    return out


def network(kind: str, K: int) -> dict[int, list[int]]:
    if kind == "teljes":
        return {i: [j for j in range(K) if j != i] for i in range(K)}
    # két klikk (a táborok szerint), egyetlen híddal
    half = K // 2
    nb = {i: [j for j in range(K) if j != i and (j < half) == (i < half)] for i in range(K)}
    nb[0].append(half)
    nb[half].append(0)
    return nb


def run_one(K=6, rounds=12, n_ent=12, eps=0.2, kappa=30, net="teljes", seed=0, q_social=0.8,
            q_private=0.8, q_book=0.95, induce=True, share="belief"):
    """share='belief': a szomszéd a saját (levezetett) hiedelmét mondja; share='raw': a szomszéd a
    legutóbbi nyers érzékelését adja tovább, az eredeti érzékelőt forrásként megjelölve."""
    rng = random.Random(seed)
    nb = network(net, K)
    camp = {i: ("A" if i < K // 2 else "B") for i in range(K)}
    agents = []
    ids = itertools.count(1)
    for i in range(K):
        sch = Schema(n_entities=n_ent + 2, n_categories=1, n_props=1)
        m = Memory(sch, mode="arlc", reliability="beta", prior_strength=kappa, depth=2, beam=4, induce=induce)
        m.observe(Obs(next(ids), f"book{camp[i]}", 0, q_book,
                      rule=Rule("dax", "has", "poisonous", camp[i] == "A")))
        m.observe(Obs(next(ids), "census", 0, 0.99, lit=Lit("isa", "probe", "dax")))
        for e in range(n_ent):
            m.observe(Obs(next(ids), "census", 0, 0.99, lit=Lit("isa", f"d{e}", "dax")))
        agents.append(m)
    history = []
    # minden ágens a saját (forrás, tartalom) párjait már ismeri: ezeket nem kapja meg újra
    seen_by = {i: {(o.source, o.lit, o.rule) for o in agents[i].obs} for i in range(K)}
    for r in range(1, rounds + 1):
        beliefs = [a.answer("probe", "poisonous", record_use=False) for a in agents]
        history.append(beliefs)
        # közölt állítások: minden ágens a saját hiedelme szerint egy véletlen daxról
        said = {}
        for i, a in enumerate(agents):
            e = f"d{rng.randrange(n_ent)}"
            ans = a.answer(e, "poisonous", record_use=False)
            said[i] = (e, ans)
        raw_now = {}
        for i, a in enumerate(agents):
            e = f"d{rng.randrange(n_ent)}"
            truth = True
            obs_val = truth if rng.random() >= eps else (not truth)
            o_s = Obs(next(ids), f"sense{i}", r, q_private, lit=Lit("has", e, "poisonous", obs_val))
            a.observe(o_s)
            seen_by[i].add((o_s.source, o_s.lit, o_s.rule))
            raw_now[i] = (e, obs_val)
        for i, a in enumerate(agents):
            for j in nb[i]:
                if share == "provenance":
                    for o in provenance(agents[j], said[j][0]):
                        key = (o.source, o.lit, o.rule)
                        if key in seen_by[i]:
                            continue
                        seen_by[i].add(key)
                        a.observe(Obs(next(ids), o.source, o.time, o.q, lit=o.lit, rule=o.rule))
                    continue
                if share == "raw":
                    e_j, v_j = raw_now[j]
                    a.observe(Obs(next(ids), f"sense{j}", r, q_private, lit=Lit("has", e_j, "poisonous", v_j)))
                else:
                    e_j, ans_j = said[j]
                    if ans_j is not None:
                        a.observe(Obs(next(ids), f"agent{j}", r, q_social, lit=Lit("has", e_j, "poisonous", ans_j)))
    final = [a.answer("probe", "poisonous", record_use=False) for a in agents]
    ent_acc = [sum(a.answer(f"d{e}", "poisonous", record_use=False) is True for e in range(n_ent)) / n_ent
               for a in agents]
    # bizalom: a másik tábortól kapott állítások hány %-át utasítja el a legjobb hipotézis
    cross_rej, within_rej = [], []
    for i, a in enumerate(agents):
        for o in a.obs:
            if o.source.startswith("agent") or (o.source.startswith("sense") and o.source != f"sense{i}"):
                j = int(o.source[5:])
                (cross_rej if camp[j] != camp[i] else within_rej).append(o.id in a.best.rej)
    return {"K": K, "rounds": rounds, "eps": eps, "kappa": kappa, "net": net, "seed": seed, "share": share,
            "final": final, "frac_true": sum(f is True for f in final) / K,
            "frac_false": sum(f is False for f in final) / K,
            "entity_acc_A": st.mean(ent_acc[: K // 2]), "entity_acc_B": st.mean(ent_acc[K // 2:]),
            "polarized": (any(f is True for f in final) and any(f is False for f in final)),
            "cross_reject": st.mean(cross_rej) if cross_rej else None,
            "within_reject": st.mean(within_rej) if within_rej else None,
            "history": history}


def run(kappas=(3, 10, 30, 100), nets=("teljes", "klikkek"), epss=(0.1, 0.3, 0.45), seeds=range(3),
        shares=("belief", "raw", "provenance"), **kw):
    rows = []
    for kappa, net, eps, seed, share in itertools.product(kappas, nets, epss, seeds, shares):
        rows.append(run_one(kappa=kappa, net=net, eps=eps, seed=seed, share=share, **kw))
    return rows
