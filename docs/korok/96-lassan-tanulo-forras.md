# 96. kör – Lassan tanuló bevált forrás a rögzített kód helyett (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 95. kör szerint a FROZEN_91 hibrid kódjának két oldala van. A bevált forrás *rögzített* kódja a G3-on véd a
bűnbak-képzéstől, a G4-en és a TFB-9-ben viszont árt, mert nem tanulja meg a tartósan rosszul kalibrált (a
deklaráltnál zajosabb) bevált forrást. A köztes megoldás: **a bevált adatforrás béta-kódot kap nagy κ-val (300)**,
szemét-komponens nélkül. Lassan tanul, ezért egy tartós eltérést (sok jelentésen át) megtanul, de egy rövid,
koncentrált félretevés-sorozat nem teszi bűnbakká. A κ = 300 a priori választás: a deklarált q kb. ±0,017 pontossággal
ismert. Kód: `core.py` (`rel_hybrid_kappa`), `v4.py` (`F91_DK`).

Fejlesztési adat (95. kör, TDκ, ahol a Tκ-rész hatástalan volt): G4 +0,01, TFB-9 +0,03, TFB-2 −0,2 (egyetlen futás).

### Elrendezés

- **Seedek:** 31000–31019 (friss). Esetek: G1k-A (hazug, átkategorizálás), G2 (hazug, torzított), G3 upd = 0,3 (hazug,
  állapotváltozás), G4 (hazug, jó új specialista, romló forrás). 180 eset × 3 módszer (v3, FROZEN_91, F91_DK) + a
  feladatcsomag (FROZEN_91, F91_DK).
- Kód: [`run_r96.py`](../../experiments/arlc/arlc/run_r96.py). Világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

- **H96a (G4, post):** F91_DK − FROZEN_91 > 0, a CI nem tartalmazza a nullát.
- **H96b (G1k, G2, G3 külön, post):** F91_DK − FROZEN_91 ≥ −0,01 (pontbecslés).
- **H96c (post):** F91_DK − v3 > 0, a CI nem tartalmazza a nullát, a G1k-n, a G2-n és a G3-on; a G4-en a pontbecslés > 0.
- **H96d (hazug-szerű célkérdések: hazug mind a négy generátoron + torzított):** F91_DK − FROZEN_91 ≥ −0,02 (pontbecslés).
- **H96e (feladatcsomag):** a TFB-9 pontossága a F91_DK-nál ≥ a FROZEN_91-énél, és egyetlen pontossági tétel sem rosszabb
  0,05-nél többel.

**Döntési szabály:** ha H96a, b, d és e teljesül, az F91_DK lesz az új befagyasztott konfiguráció (FROZEN_96).
