"""26. kör: zárt alakú jóslatok a béta-binomiális forráskódból.

Jelölések: a forrás előzetes eloszlása Beta(α, β), α = κq (elfogadási), β = κ(1−q) (hiba).
L(n, k) = log2 B(α, β) − log2 B(α + n − k, β + k) a forrás n állításának kódhossza, ha k-t
elutasítunk. Egy további elutasítás határköltsége: log2((α + n − k − 1)/(β + k)).
"""
from __future__ import annotations

import math


def L(n: int, k: int, a: float, b: float) -> float:
    lb = lambda x, y: math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return (lb(a, b) - lb(a + n - k, b + k)) / math.log(2)


def defender_cost(m: int, record: int, a: float, b: float, claims_per_anomaly: int = 2,
                  identities: str = "one") -> float:
    """Mennyibe kerül m anomália elutasítása (anomáliánként egy állítás elutasítása)
    a többi hipotézishez képest, ahol a forrás minden állítása el van fogadva."""
    if identities == "fresh":       # sybil: anomáliánként új identitás, múlt nélkül
        return m * (L(claims_per_anomaly, 1, a, b) - L(claims_per_anomaly, 0, a, b))
    n = record + claims_per_anomaly * m
    return L(n, m, a, b) - L(n, 0, a, b)


def rule_drop_cost(N: int, q_rule: float = 0.95, kappa: float = 30.0, delta: float = 0.05) -> float:
    """A szabály elvetésének költsége: a szabály-forrás (egyetlen állítás) elutasítása
    plusz N alátámasztó tény elvesztett jóslata."""
    a, b = kappa * q_rule, kappa * (1 - q_rule)
    return (L(1, 1, a, b) - L(1, 0, a, b)) + N * (1.0 + math.log2(1 - delta))


def predicted_flip(N: int, record: int, scenario: str, q0: float, kappa: float = 30.0,
                   q_field: float = 0.9, m_max: int = 60):
    """A legkisebb m, amelynél az anomáliák elutasítása drágább, mint a szabály elvetése."""
    T = rule_drop_cost(N, kappa=kappa)
    if scenario == "honest-established":
        a, b, rec, ident = kappa * q_field, kappa * (1 - q_field), N + record, "one"
    elif scenario == "sybil":
        a, b, rec, ident = kappa * q0, kappa * (1 - q0), 0, "fresh"
    else:  # honest-newcomer, single-attacker: múlt nélküli egyetlen identitás
        a, b, rec, ident = kappa * q0, kappa * (1 - q0), 0, "one"
    for m in range(1, m_max + 1):
        if defender_cost(m, rec, a, b, identities=ident) >= T - 1e-9:
            return m
    return None
