# 103. kör – Egyszerűsítés: a mag a hatástalan kapcsolók nélkül (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 95. kör szerint a FROZEN_91 kapcsolóinak egy része a négy generátoron hatástalan vagy enyhén káros. A 99. kör javaslata egy
egyszerűbb mag. **Ez a rendszer saját MDL-elve, önmagára alkalmazva:** ami nem magyaráz semmit, az ne legyen benne. A
feltalálást és a kontextusindukciót nem veszem ki, mert a feladatcsomag (feltalálás) és a jelzett kontextus (más régió)
használja őket. Kiveszem:
- a **q-csoportokat** (48. kör; a 95. kori LOO szerint sehol nem számít);
- az **indukált szabályok kivétel-árát** (45. kör; a G1k-n eltávolítva +0,005);
- a **forrásszintű lépést** (27. kör; a G2-n eltávolítva +0,001 / +0,025).

Kód: `v4.py` (`V5_CORE`), [`run_r103.py`](../../experiments/arlc/arlc/run_r103.py).

### Elrendezés

Seedek 35000–35011 (friss), a 96. kör 9 típusa a négy generátoron; 108 eset × 2 (FROZEN_91, V5_CORE) + feladatcsomag.

### Hipotézisek

- **H103a:** V5_CORE − FROZEN_91 (post) ≥ −0,01 mind a négy generátoron (pontbecslés).
- **H103b:** a forrás-célkérdéseken (hazug ×4, torzított, jó specialista) V5_CORE − FROZEN_91 ≥ −0,02 (pontbecslés).
- **H103c (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel, a logikai tételek változatlanok.

**Döntési szabály:** ha mindhárom teljesül, a V5_CORE lesz az alapértelmezés (FROZEN_103), és a három kapcsoló a kódban
dokumentált, de kikapcsolt történeti elem lesz.
