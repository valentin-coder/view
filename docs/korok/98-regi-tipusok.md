# 98. kör – A G1 ritkábban mért meglepetéstípusai a FROZEN_91-gyel (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 85–96. kör a G1k-n csak a hazug forrást és az átkategorizálást mérte. A sorozat korábbi állításai közül három típus
újramérése maradt el a javított generátoron és a mai konfigurációval: a **szabály-helyesbítés**, a **kivételes alfaj**
(kategória-feltalálás) és a **más régió** (kontextus, a 73. kör jelhez kötött elsőbbségével).

### Elrendezés

- **Seedek:** 32000–32019 (friss), G1k A populáció; szabály-helyesbítés, kivételes alfaj, más régió. 60 eset × 3.
- **Módszerek:** v3; FROZEN_91; FROZEN_91 + jel (szimulált kontextusjel a = 0,99, jelzett elsőbbség; 73. kör).
- Kód: [`run_r98.py`](../../experiments/arlc/arlc/run_r98.py). Világok szerinti klaszteres bootstrap.

### Hipotézisek

- **H98a (post-acc, a három típus együtt):** FROZEN_91 − v3 > 0, a CI nem tartalmazza a nullát.
- **H98b (kivételes alfaj, target):** FROZEN_91 − v3 ≥ 0 (pontbecslés).
- **H98c (más régió, target):** (FROZEN_91 + jel) − FROZEN_91 > 0, a CI nem tartalmazza a nullát (a jel továbbra is segít).
- **H98d (más régió, target):** FROZEN_91 − v3 ≥ −0,02 (pontbecslés; jel nélkül holtverseny, 62. kör).
