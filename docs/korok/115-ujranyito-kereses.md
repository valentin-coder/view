# 115. kör – Általános újranyitó keresés, és a szabály-vágás újra (előregisztrált)

## 1. rész: terv, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### Miért

A 114. kör szerint a 112. kör sikerének egyik fele a keresés volt (horgony-újraindítás). Valószínű, hogy a 97. kori
forrás-változáspont és a 107. kori szabály-vágás is azon bukott el, hogy a kereső a korábbi döntéseket nem nyitja újra.

### A mechanizmus (`reopen_search`)

Kód: [`core.py`](../../experiments/arlc/arlc/core.py), `v4.py` (`F112_O`, `F112_RO`, `F112_CPO`). Minden új időpont első
megfigyelése előtt a legjobb hipotézis **időhorgonyként** elmentődik. Ha egy jelölt új változáspontot (forrás, t) vagy egy
t-ben végződő új vágást tartalmaz, a javítás a t előtti horgony + a komponens hipotézisből is újraindul.

### Fejlesztési ellenőrzés (már felhasznált seedek, nem teszt)

Kód: [`dev_r115.py`](../../experiments/arlc/arlc/dev_r115.py).

| | G3 szabályváltozás target / hist | G4 romló forrás target |
|---|---|---|
| FROZEN_112 | 0,496 / 0,483 | 0,833 |
| + újranyitás (O) | 0,496 / 0,483 | 0,833 |
| + szabály-vágás (R) | 0,654 / 0,583 | – |
| **+ R + O** | **1,000 / 0,792** | – |
| + változáspont (CP), ± O | – | 0,817 |

**A szabály-vágás az újranyitással teljesen kezeli a szabályváltozást.** A forrás-változáspontnak az újranyitás sem segít:
a 97. kör negatív eredménye nem keresési hiba volt.

**A 107. kori A7-kár oka és javítása.** Az R + O a feladatcsomagban az A7 „cat_past” tételét 0-ra rontotta, a ρ_r értékétől
függetlenül (0,01 / 0,001 / 0,0001). Az ok az időbeli szemantika volt. A 107. kör óta a flag mellett *minden* megfigyelés
csak a saját időpontjától érvényes, így egy **revízió** (a kategória mindig hal volt, csak tévesen jelentették) nem
hatott visszamenőleg. **Javítás:** egy megfigyelés csak akkor érvényes a saját időpontjától, ha a hipotézis ugyanarra a
tulajdonságra legkésőbb akkor végződő vágást (változást) tételez fel. Vágás nélkül (félretevéssel, revízióval) a
helyesbítés visszamenőleges. **Ez pontosan a frissítés–revízió megkülönböztetés** (Katsuno–Mendelzon, 1991): a hipotézis
szerkezete (vágás vagy félretevés) dönti el, melyik szemantika érvényes. Utána az A7 mind a négy tétele 1,0, és a G3
szabályváltozás 1,000 / 0,792 marad.

Feladatcsomag (R + O, javítva): egyetlen pontossági tétel sem változik. Az E2a átfordulási pontjai 2/4/6 → 2/3/3 (monoton
marad): a rendszer több ellentmondó megfigyelésnél hamarabb fogadja el a „szabály megváltozott” olvasatot. Ezt leíró
változásként rögzítem, nem kritériumként.

Mindkét kapcsoló kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

### Előregisztráció

- **Seedek:** 41000–41014 (friss). A 107. kör esetei: a 96. kör 9 típusa + G3 szabályváltozás + G1k szabály-helyesbítés
  (revízió, a kritikus kontroll). 165 eset × 3 (v3, FROZEN_112, F112_RO) + feladatcsomag.
- Kód: [`run_r115.py`](../../experiments/arlc/arlc/run_r115.py) (a 107. kör futtatója).

**Hipotézisek:**
- **H115a (G3 szabályváltozás, target):** F112_RO − FROZEN_112 > 0, a CI nem tartalmazza a nullát.
- **H115b (G3 szabályváltozás, hist):** F112_RO − FROZEN_112 > 0 (pontbecslés).
- **H115c (G1k szabály-helyesbítés, target, revízió):** F112_RO − FROZEN_112 ≥ −0,02 (pontbecslés).
- **H115d (a 96. kör 9 típusa, post):** F112_RO − FROZEN_112 ≥ −0,01 mind a négy generátoron (pontbecslés).
- **H115e (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel.

**Döntési szabály:** ha mind teljesül, az F112_RO lesz az új befagyasztott konfiguráció (FROZEN_115).

## 2. rész: eredmények

Nyers adat: [`results/kor-115/`](../../experiments/arlc/results/kor-115/); elemzés:
[`analyze_r115.py`](../../experiments/arlc/arlc/analyze_r115.py) → `results/kor-115/analysis.json`. 495 futás + feladatcsomag,
eltérés nincs. (A H115d elemzése a G1k-n a szabály-helyesbítés típust is tartalmazza, ami szigorúbb, mint az előregisztrált
„9 típus”.)

| | G3 szabályváltozás target / hist | G1k szabály-helyesbítés (revízió) target |
|---|---|---|
| v3 | 0,242 / 0,758 | 0,932 |
| FROZEN_112 | 0,184 / 0,749 | 0,944 |
| **F112_RO** | **0,933 / 0,867** | 0,944 (azonos) |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H115a (target):** RO − F112 > 0 | **+0,749** [+0,56; +0,92] | **teljesül** |
| **H115b (hist):** RO − F112 > 0 | **+0,117** [+0,022; +0,236] | **teljesül** |
| **H115c (revízió):** ≥ −0,02 | 0,000 | **teljesül** |
| **H115d (post, a többi típus):** ≥ −0,01 | G1k −0,003; G2 −0,008; G3 +0,001; G4 −0,004 | **teljesül** |
| **H115e (feladatcsomag):** | egyetlen pontossági tétel sem változik (E2a átfordulás: 2/4/6 → 2/3/3, leíró) | **teljesül** |

**A döntési szabály szerint az F112_RO az új befagyasztott konfiguráció (`FROZEN_115`).**

### Értelmezés

1. **A szabályváltozás, a sorozat régóta nyitott hiánya (87., 88., 107. kör), megoldott.** A rendszer a megváltozott szabályt
   most 93%-ban helyesen kezeli (a v3 24%, a FROZEN_112 18%), és a múltra vonatkozó kérdésekben is jobb.
2. **A 107. kori kudarcnak két oka volt, és mindkettő a keresésben vagy a szemantikában rejlett, nem az árazásban.** (a)
   A kereső nem nyitotta újra a korábbi döntéseket: az időhorgony ezt pótolja. (b) Az időbeli szemantika minden
   megfigyelésre érvényes volt, ezért a revíziót is frissítésként kezelte. Most a hipotézis szerkezete (vágás vagy
   félretevés) dönti el, melyik szemantika érvényes. **Ez a frissítés–revízió megkülönböztetés egy működő, előregisztráltan
   tesztelt megvalósítása,** amely a 107. kör szerint csak „tárcsa” volt. Valójában szerkezeti kérdés: a vágás egy
   változás-*esemény* (sok régi megfigyelést egyszerre magyaráz), ezért a 114. kör szerinti szerkezeti bizonyítékok közé
   tartozik.
3. **Ára a futási idő:** az újranyitó keresés kb. 2,5-szer lassabb (a G2-n 149 s vs. 61 s esetenként). Ez az eredeti
   „azonnali” célnak ellentmond, és a 76. kör óta halasztott gyorsítás (szabályszintű memó) most sürgősebb.
4. **A forrás-változáspont (97. kör) az újranyitással sem működik.** A romló forrás hibái egyenként is ütköznek a
   szabályokkal, így nincs mit egy eseménnyel magyarázni. Ez megerősíti a 114. kör különbségtételét.
