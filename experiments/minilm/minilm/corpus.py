"""Szintetikus korpusz a mini-LM-hez (23. kör).

Nonce-világ két kontextussal (észak/dél). Bizonyos kategóriák egyes tulajdonságai
kontextusfüggők. Minden mondatot egy forrás mond; a forrás egy kontextushoz tartozik.
A kontextus csak néha szerepel explicit szóval; máskor csak a forrás neve vagy a tartalom
árulja el. A sablonok egy része kitartott (a probe-ok általánosítását méri).
"""
from __future__ import annotations

import random
from dataclasses import dataclass

CATS = ["dax", "wug", "fep", "blick", "toma", "zorb"]
PROPS = ["poisonous", "striped", "noisy", "heavy", "shiny", "slow", "sticky", "warm"]
CONTEXTS = ["north", "south"]
SOURCES = {"north": ["ala", "bero", "cimi", "dova"], "south": ["egon", "fira", "gulo", "hesa"]}
HELDOUT_SOURCES = {"dova", "hesa"}     # a probe-tanításból kimarad (általánosítás új forrásra)


@dataclass
class Sent:
    text: str
    kind: str          # 'isa' | 'has' | 'gen'
    subj: str          # entitás vagy kategória (gen)
    obj: str           # kategória vagy tulajdonság
    pos: bool
    source: str
    context: str
    template: int
    explicit_ctx: bool


# sablonok: {S} forrás, {X} alany, {Y} tárgy; NEG változat külön
ISA_T = [
    "{S} says the {X} is a {Y} .",
    "according to {S} , the {X} is a kind of {Y} .",
    "{S} reports that the {X} belongs to the {Y} family .",
    "the {X} is a {Y} , says {S} .",
    "{S} : {X} counts as a {Y} .",
    "{S} claims that every {X} is a {Y} .",          # kitartott
    "{S} notes the {X} is classed as a {Y} .",        # kitartott
]
HAS_T = [
    ("{S} says the {X} is {Y} .", "{S} says the {X} is not {Y} ."),
    ("according to {S} , the {X} is {Y} .", "according to {S} , the {X} is never {Y} ."),
    ("{S} reports that the {X} looks {Y} .", "{S} reports that the {X} does not look {Y} ."),
    ("the {X} is {Y} , says {S} .", "the {X} is not {Y} , says {S} ."),
    ("{S} : the {X} seems {Y} .", "{S} : the {X} seems not {Y} ."),
    ("{S} insists the {X} is quite {Y} .", "{S} insists the {X} is hardly {Y} ."),   # kitartott
    ("{S} found the {X} to be {Y} .", "{S} found the {X} not to be {Y} ."),         # kitartott
]
GEN_T = [
    ("{S} says all {X}s are {Y} .", "{S} says no {X} is {Y} ."),
    ("according to {S} , every {X} is {Y} .", "according to {S} , {X}s are never {Y} ."),
    ("{S} : {X}s are {Y} .", "{S} : {X}s are not {Y} ."),
    ("{S} teaches that {X}s are {Y} .", "{S} teaches that {X}s are not {Y} ."),
    ("{S} writes that each {X} is {Y} .", "{S} writes that no {X} is ever {Y} ."),
    ("{S} believes {X}s tend to be {Y} .", "{S} believes {X}s tend not to be {Y} ."),  # kitartott
    ("{S} holds that {X}s are always {Y} .", "{S} holds that {X}s are seldom {Y} ."),  # kitartott
]
N_TRAIN_TEMPLATES = 5
CTX_PHRASE = ["in the {C} , ", "up in the {C} , ", "down {C} , "]


class World:
    def __init__(self, seed: int = 0, n_entities: int = 60):
        rng = random.Random(seed)
        self.rng = rng
        # kategória-szabályok: minden kategóriának 3 tulajdonsága; ebből 1 kontextusfüggő
        self.rules: dict[str, dict[str, dict[str, bool]]] = {c: {} for c in CONTEXTS}
        self.ctx_dep: dict[str, str] = {}
        for c in CATS:
            props = rng.sample(PROPS, 3)
            for p in props:
                v = rng.random() < 0.5
                for ctx in CONTEXTS:
                    self.rules[ctx].setdefault(c, {})[p] = v
            dep = props[0]
            self.ctx_dep[c] = dep
            self.rules["south"][c][dep] = not self.rules["north"][c][dep]
        self.entities = {f"e{i:02d}": rng.choice(CATS) for i in range(n_entities)}
        names = self._names(n_entities, rng)
        self.ename = dict(zip(self.entities, names))

    @staticmethod
    def _names(n, rng):
        cons, vow = "bdfgklmnprstvz", "aeiou"
        out = set()
        while len(out) < n:
            out.add(rng.choice(cons) + rng.choice(vow) + rng.choice(cons) + rng.choice(vow) + rng.choice(cons))
        return sorted(out)

    def truth(self, ent: str, ctx: str) -> dict[str, bool]:
        return dict(self.rules[ctx][self.entities[ent]])


def generate(world: World, n: int, seed: int = 1, p_explicit: float = 0.3,
             templates: str = "train") -> list[Sent]:
    """templates: 'train' (az első N_TRAIN_TEMPLATES) | 'heldout' (a többi) | 'all'."""
    rng = random.Random(seed)
    lo, hi = (0, N_TRAIN_TEMPLATES) if templates == "train" else \
        ((N_TRAIN_TEMPLATES, len(ISA_T)) if templates == "heldout" else (0, len(ISA_T)))
    out = []
    ents = list(world.entities)
    for _ in range(n):
        ctx = rng.choice(CONTEXTS)
        src = rng.choice(SOURCES[ctx])
        ti = rng.randrange(lo, hi)
        kind = rng.choices(["isa", "has", "gen"], weights=[2, 5, 2])[0]
        if kind == "isa":
            e = rng.choice(ents)
            subj, obj, pos = world.ename[e], world.entities[e], True
            body = ISA_T[ti]
        elif kind == "has":
            e = rng.choice(ents)
            tr = world.truth(e, ctx)
            p = rng.choice(sorted(tr))
            subj, obj, pos = world.ename[e], p, tr[p]
            body = HAS_T[ti][0 if pos else 1]
        else:
            c = rng.choice(CATS)
            p = rng.choice(sorted(world.rules[ctx][c]))
            subj, obj, pos = c, p, world.rules[ctx][c][p]
            body = GEN_T[ti][0 if pos else 1]
        explicit = rng.random() < p_explicit
        text = body.format(S=src, X=subj, Y=obj)
        if explicit:
            text = rng.choice(CTX_PHRASE).format(C=ctx) + text
        out.append(Sent(text, kind, subj, obj, pos, src, ctx, ti, explicit))
    return out
