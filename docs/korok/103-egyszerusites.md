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

## 2. rész: eredmények

Nyers adat: [`results/kor-103/`](../../experiments/arlc/results/kor-103/); elemzés:
[`analyze_r103.py`](../../experiments/arlc/arlc/analyze_r103.py) → `results/kor-103/analysis.json`. 216 futás + feladatcsomag.

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H103a:** V5_CORE − FROZEN_91 (post) ≥ −0,01 | G1k +0,002; G2 0,000; G3 −0,003; G4 −0,004 | **teljesül** |
| **H103b:** forrás-célkérdések ≥ −0,02 | −0,006 [−0,020; +0,005] | **teljesül** |
| **H103c:** feladatcsomag | **A7 (frissítés/revízió): 1,00 → 0,25**; TFB-9 0,78 → 0,82 | **nem teljesül** |

**A döntési szabály szerint a V5_CORE nem lesz alapértelmezés.** A FROZEN_91 marad.

### A kudarc oka

Egyenként visszakapcsolva: az A7-kudarcot **a q-csoportok eltávolítása** okozza (nélkülük az A7 négy mérőszámából három 0).
Az A7-ben egy forrás különböző deklarált hitelességű állításokat tesz. A q-csoportok nélkül a béta-kód egy forrás
összes állítását az *első* állítás q-jával árazza. **A q-csoport tehát helyességi javítás (48. kör), nem fölösleg.** A
generátorokban minden forrás egyforma q-val jelent, ezért ott soha nem számított. Az indukált kivétel-ár és a forrásszintű
lépés eltávolítása az A7-en semleges.

### Tanulság

**A 95. kör „hatástalan” ítélete generátor-relatív volt:** amit a négy generátor nem tesztel, az nem feltétlenül fölösleg. A
feladatcsomag (a korai körök kézi feladatai) éppen ezért kötelező része minden befagyasztásnak (92. kör szabálya), és most
is megfogta a hibát. Az egyszerűsítésnek a generátorok *és* a feladatcsomag együttes LOO-ján kell alapulnia.
