"""Kategória-transzplantációs pilot (KTP): a "Valós kategória"-világ és a kérdések.

Minden itt rögzített tényt a modell tudásszűrője ellenőriz futás előtt; ami a
szerkesztetlen modellnek nem megy, az kiesik (lásd filter lépés). A szemantika
rögzített: átkategorizáláskor a kategóriafüggő tulajdonságok átváltanak, az
egyéni tulajdonságok (szín, méret) megmaradnak.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field, asdict
from typing import Optional

CATEGORIES = ["bird", "fish", "mammal", "insect", "vehicle", "fruit"]
ANIMALS = {"bird", "fish", "mammal", "insect"}

CATEGORY_PLURAL = {
    "bird": "birds", "fish": "fish", "mammal": "mammals",
    "insect": "insects", "vehicle": "vehicles", "fruit": "fruits",
}

# entitás -> (szín vagy None, nagyobb-e egy embernél)
ENTITIES: dict[str, list[tuple[str, Optional[str], bool]]] = {
    "bird": [
        ("crow", "black", False), ("raven", "black", False), ("canary", "yellow", False),
        ("goldfinch", "yellow", False), ("cardinal", "red", False), ("flamingo", "pink", False),
        ("swan", "white", False), ("dove", "white", False), ("seagull", "white", False),
        ("parrot", "green", False), ("peacock", "blue", False), ("pigeon", "gray", False),
        ("sparrow", "brown", False), ("owl", "brown", False), ("eagle", "brown", False),
    ],
    "fish": [
        ("goldfish", "orange", False), ("clownfish", "orange", False), ("shark", "gray", True),
        ("tuna", "silver", True), ("swordfish", "gray", True), ("cod", "gray", False),
        ("trout", "brown", False), ("herring", "silver", False), ("sardine", "silver", False),
        ("catfish", "brown", False), ("carp", "brown", False), ("pike", "green", False),
        ("eel", "black", False), ("salmon", "silver", False), ("piranha", "silver", False),
    ],
    "mammal": [
        ("horse", "brown", True), ("bear", "brown", True), ("tiger", "orange", True),
        ("zebra", "black and white", True), ("panda", "black and white", True),
        ("camel", "brown", True), ("gorilla", "black", True), ("lion", "yellow", True),
        ("bison", "brown", True), ("mouse", "gray", False), ("fox", "orange", False),
        ("sheep", "white", False), ("wolf", "gray", False), ("raccoon", "gray", False),
        ("skunk", "black and white", False),
    ],
    "insect": [
        ("ant", "black", False), ("bee", "yellow", False), ("wasp", "yellow", False),
        ("ladybug", "red", False), ("grasshopper", "green", False), ("cricket", "black", False),
        ("fly", "black", False), ("beetle", "black", False), ("moth", "gray", False),
        ("cockroach", "brown", False), ("termite", "white", False), ("flea", "brown", False),
        ("aphid", "green", False), ("hornet", "yellow", False), ("mosquito", "black", False),
    ],
    "vehicle": [
        ("car", None, True), ("truck", None, True), ("bus", None, True),
        ("tractor", None, True), ("van", None, True), ("taxi", "yellow", True),
        ("ambulance", "white", True), ("limousine", "black", True), ("jeep", None, True),
        ("minivan", None, True), ("forklift", "yellow", True), ("firetruck", "red", True),
        ("sedan", None, True), ("motorhome", None, True), ("snowplow", None, True),
    ],
    "fruit": [
        ("apple", "red", False), ("orange", "orange", False), ("lemon", "yellow", False),
        ("lime", "green", False), ("cherry", "red", False), ("peach", "orange", False),
        ("pear", "green", False), ("plum", "purple", False), ("mango", "orange", False),
        ("apricot", "orange", False), ("fig", "purple", False), ("avocado", "green", False),
        ("pomegranate", "red", False), ("grapefruit", "yellow", False), ("coconut", "brown", False),
    ],
}

# Kontrasztszín az S2 negatív színkérdéshez (soha nem fedi az igazi színt).
WRONG_COLOR = {
    "black": "yellow", "yellow": "blue", "red": "green", "pink": "black", "white": "green",
    "green": "red", "blue": "orange", "gray": "pink", "brown": "blue", "orange": "purple",
    "silver": "red", "purple": "yellow", "black and white": "orange",
}

# tulajdonság -> (sablon {art} {X}-szel, sablon "it"-tel, sablon "the {X}"-szel, igaz kategóriák)
PROPERTIES: dict[str, tuple[str, str, str, set[str]]] = {
    "breathe_underwater": ("Can {art} {X} breathe underwater?", "Can it breathe underwater?",
                           "Can the {X} breathe underwater?", {"fish"}),
    "feathers": ("Does {art} {X} have feathers?", "Does it have feathers?",
                 "Does the {X} have feathers?", {"bird"}),
    "fins": ("Does {art} {X} have fins?", "Does it have fins?", "Does the {X} have fins?", {"fish"}),
    "fur": ("Does {art} {X} have fur?", "Does it have fur?", "Does the {X} have fur?", {"mammal"}),
    "six_legs": ("Does {art} {X} have six legs?", "Does it have six legs?",
                 "Does the {X} have six legs?", {"insect"}),
    "wheels": ("Does {art} {X} have wheels?", "Does it have wheels?",
               "Does the {X} have wheels?", {"vehicle"}),
    "seeds": ("Does {art} {X} have seeds?", "Does it have seeds?",
              "Does the {X} have seeds?", {"fruit"}),
    "beak": ("Does {art} {X} have a beak?", "Does it have a beak?",
             "Does the {X} have a beak?", {"bird"}),
    "scales": ("Does {art} {X} have scales?", "Does it have scales?",
               "Does the {X} have scales?", {"fish"}),
    "antennae": ("Does {art} {X} have antennae?", "Does it have antennae?",
                 "Does the {X} have antennae?", {"insect"}),
    "engine": ("Does {art} {X} have an engine?", "Does it have an engine?",
               "Does the {X} have an engine?", {"vehicle"}),
    "grows_on_trees": ("Does {art} {X} grow on trees?", "Does it grow on trees?",
                       "Does the {X} grow on trees?", {"fruit"}),
    "lays_eggs": ("Does {art} {X} lay eggs?", "Does it lay eggs?",
                  "Does the {X} lay eggs?", {"bird", "fish", "insect"}),
    "is_animal": ("Is {art} {X} an animal?", "Is it an animal?",
                  "Is the {X} an animal?", {"bird", "fish", "mammal", "insect"}),
    "bones": ("Does {art} {X} have bones?", "Does it have bones?",
              "Does the {X} have bones?", {"bird", "fish", "mammal"}),
    "milk": ("Does {art} {X} feed its babies milk?", "Does it feed its babies milk?",
             "Does the {X} feed its babies milk?", {"mammal"}),
    "fuel": ("Does {art} {X} need fuel?", "Does it need fuel?",
             "Does the {X} need fuel?", {"vehicle"}),
}

PLURAL_IRREGULAR = {
    "mouse": "mice", "sheep": "sheep", "fish": "fish", "salmon": "salmon", "tuna": "tuna",
    "cod": "cod", "trout": "trout", "carp": "carp", "swordfish": "swordfish",
    "catfish": "catfish", "goldfish": "goldfish", "clownfish": "clownfish", "wolf": "wolves",
    "bison": "bison", "pike": "pike", "herring": "herring", "mango": "mangoes",
    "mosquito": "mosquitoes",
}

FEWSHOT = ("Answer each question with Yes or No.\n\n"
           "Question: Is the sun hot?\nAnswer: Yes\n\n"
           "Question: Is ice hot?\nAnswer: No\n\n"
           "Question: Is a circle round?\nAnswer: Yes\n\n")

NEUTRAL_TEMPLATES = [
    "Here is a sentence about {art} {X}.",
    "I read something about the {X} today.",
    "The {X} was mentioned in the book.",
    "She drew a picture of {art} {X}.",
]


def article(word: str) -> str:
    return "an" if word[0].lower() in "aeiou" else "a"


def plural(word: str) -> str:
    if word in PLURAL_IRREGULAR:
        return PLURAL_IRREGULAR[word]
    if word.endswith(("s", "sh", "ch", "x")):
        return word + "es"
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def value(prop: str, cat: str) -> bool:
    return cat in PROPERTIES[prop][3]


@dataclass
class Entity:
    name: str
    category: str
    color: Optional[str]
    big: bool
    split: str = ""  # mu | dev | test


@dataclass
class Edit:
    entity: str
    old: str
    new: str
    split: str

    @property
    def pair_type(self) -> str:
        if self.old in ANIMALS and self.new in ANIMALS:
            return "animal-animal"
        if self.old not in ANIMALS and self.new not in ANIMALS:
            return "object-object"
        return "cross-domain"

    @property
    def key(self) -> str:
        return f"{self.entity}->{self.new}"


@dataclass
class Question:
    """Egy kérdés egy szerkesztéshez.

    kind: D (diagnosztikus), S1 (közös kategória-tulajdonság), S2 (egyéni),
          I (implicit hivatkozás), T (kétentitásos; a másik entitásra kérdez).
    before/after: elvárt igaz-hamis érték szerkesztés előtt/után.
    """
    qid: str
    edit_key: str
    kind: str
    prop: str
    before: bool
    after: bool
    entity: str
    template: str            # {art} {X} vagy it-sablon vagy the-sablon
    context: str = ""        # I/T: előzménymondat {art} {X} (+ {art2} {Y}) helyőrzőkkel
    other: str = ""          # T: a másik entitás


def build_entities(seed: int = 0) -> dict[str, Entity]:
    rng = random.Random(seed)
    out: dict[str, Entity] = {}
    for cat in CATEGORIES:
        rows = list(ENTITIES[cat])
        rng.shuffle(rows)
        for i, (name, color, big) in enumerate(rows):
            split = "mu" if i < 5 else ("dev" if i < 10 else "test")
            out[name] = Entity(name, cat, color, big, split)
    return out


def build_edits(entities: dict[str, Entity], split: str) -> list[Edit]:
    edits = []
    for e in entities.values():
        if e.split != split:
            continue
        for new in CATEGORIES:
            if new != e.category:
                edits.append(Edit(e.name, e.category, new, split))
    return edits


def _interleave(a: list[str], b: list[str]) -> list[str]:
    out = []
    for i in range(max(len(a), len(b))):
        if i < len(a):
            out.append(a[i])
        if i < len(b):
            out.append(b[i])
    return out


def diagnostic_props(old: str, new: str, k: int = 5) -> list[str]:
    """Kiegyensúlyozott N->I és I->N váltások (a 'Yes'-torzítás ellen)."""
    to_yes = [p for p in PROPERTIES if not value(p, old) and value(p, new)]
    to_no = [p for p in PROPERTIES if value(p, old) and not value(p, new)]
    return _interleave(to_yes, to_no)[:k]


def shared_props(old: str, new: str) -> list[str]:
    yy = [p for p in PROPERTIES if value(p, old) and value(p, new)]
    nn = [p for p in PROPERTIES if not value(p, old) and not value(p, new)]
    out = []
    if yy:
        out.append(yy[0])
    if nn:
        out.append(nn[0])
    return out


def other_entity(entities: dict[str, Entity], old: str, new: str) -> Entity:
    for cat in CATEGORIES:
        if cat not in (old, new):
            for e in entities.values():
                if e.category == cat and e.split == "mu":
                    return e
    raise RuntimeError("nincs harmadik kategória")


def questions_for_edit(edit: Edit, entities: dict[str, Entity]) -> list[Question]:
    ent = entities[edit.entity]
    qs: list[Question] = []
    diag = diagnostic_props(edit.old, edit.new)
    for p in diag:
        qs.append(Question(f"{edit.key}|D|{p}", edit.key, "D", p, value(p, edit.old),
                           value(p, edit.new), ent.name, PROPERTIES[p][0]))
    for p in shared_props(edit.old, edit.new):
        v = value(p, edit.old)
        qs.append(Question(f"{edit.key}|S1|{p}", edit.key, "S1", p, v, v, ent.name,
                           PROPERTIES[p][0]))
    if ent.color:
        qs.append(Question(f"{edit.key}|S2|color+", edit.key, "S2", "color+", True, True,
                           ent.name, "Is {art} {X} typically " + ent.color + "?"))
        qs.append(Question(f"{edit.key}|S2|color-", edit.key, "S2", "color-", False, False,
                           ent.name, "Is {art} {X} typically " + WRONG_COLOR[ent.color] + "?"))
    qs.append(Question(f"{edit.key}|S2|big", edit.key, "S2", "big", ent.big, ent.big, ent.name,
                       "Is {art} {X} bigger than a person?"))
    for p in diag[:3]:
        qs.append(Question(f"{edit.key}|I|{p}", edit.key, "I", p, value(p, edit.old),
                           value(p, edit.new), ent.name, PROPERTIES[p][1],
                           context="Tom saw {art} {X} near the house yesterday.\n"))
    oth = other_entity(entities, edit.old, edit.new)
    t_props = [p for p in PROPERTIES if value(p, edit.new) != value(p, oth.category)
               and value(p, edit.new)][:2]
    for p in t_props:
        v = value(p, oth.category)
        qs.append(Question(f"{edit.key}|T|{p}", edit.key, "T", p, v, v, ent.name,
                           PROPERTIES[p][2], context="Tom saw {art} {X} and {art2} {Y} near the house yesterday.\n",
                           other=oth.name))
    return qs


@dataclass
class Rendered:
    text: str
    spans: list[tuple[int, int]] = field(default_factory=list)  # a patchelendő X-említések


def _fill(template: str, word: str, out: list[str], spans: list[tuple[int, int]], offset: int,
          mark: bool = True) -> int:
    """{art} és {X} kitöltése; az X-említések karakterhatárait gyűjti."""
    s = template.replace("{art}", article(word))
    parts = s.split("{X}")
    pos = offset
    for i, part in enumerate(parts):
        out.append(part)
        pos += len(part)
        if i < len(parts) - 1:
            if mark:
                spans.append((pos, pos + len(word)))
            out.append(word)
            pos += len(word)
    return pos


def render(q: Question, edit: Edit, condition: str) -> Rendered:
    """condition: plain | context | rewrite | context+rewrite

    plain: szerkesztetlen prompt (a transzplantációs feltételek is ezt kapják),
    context: B1 – a szerkesztés kimondva a promptban,
    rewrite: B2 – minden X-említés a célkategória főnevére cserélve,
    context+rewrite: B3.
    """
    subject = edit.new if "rewrite" in condition else q.entity
    out: list[str] = []
    spans: list[tuple[int, int]] = []
    pos = 0
    out.append(FEWSHOT)
    pos += len(FEWSHOT)
    if "context" in condition:
        stmt = (f"Note: in this story, {plural(q.entity)} are "
                f"{CATEGORY_PLURAL[edit.new]}, not {CATEGORY_PLURAL[edit.old]}.\n")
        out.append(stmt)
        pos += len(stmt)
    if q.context:
        ctx = q.context
        if "{Y}" in ctx:
            ctx = ctx.replace("{art2}", article(q.other)).replace("{Y}", q.other)
        pos = _fill(ctx, subject, out, spans, pos)
    head = "Question: "
    out.append(head)
    pos += len(head)
    if q.kind == "T":
        body = q.template.replace("{X}", q.other)
        out.append(body)
        pos += len(body)
    else:
        pos = _fill(q.template, subject, out, spans, pos)
    tail = "\nAnswer:"
    out.append(tail)
    return Rendered("".join(out), spans)


def render_neutral(word: str) -> list[Rendered]:
    res = []
    for t in NEUTRAL_TEMPLATES:
        out: list[str] = []
        spans: list[tuple[int, int]] = []
        _fill(t, word, out, spans, 0)
        res.append(Rendered("".join(out), spans))
    return res


def render_proto(prop: str, word: str) -> Rendered:
    out: list[str] = [FEWSHOT, "Question: "]
    spans: list[tuple[int, int]] = []
    _fill(PROPERTIES[prop][0], word, out, spans, len(FEWSHOT) + len("Question: "))
    out.append("\nAnswer:")
    return Rendered("".join(out), spans)


def world_summary(entities: dict[str, Entity]) -> dict:
    return {"entities": {k: asdict(v) for k, v in entities.items()},
            "properties": {k: sorted(v[3]) for k, v in PROPERTIES.items()}}
