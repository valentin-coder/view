# 57. kör – Kombinált benchmark (A + B populáció): előregisztráció

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 44. kör benchmarkja csak az egyik végpontot méri (a tankönyv sosem egészében téves), a TFB-9 a másikat (az
elméletek fele téves). A 49–52. kör szerint a gestalt-váltás és a téves félretevés ugyanaz a lépés, és a
helyes viselkedés a terület alapgyakoriságától függ. Egy jó rendszernek mindkét populáción jól kell
teljesítenie. Ez a kör a 44. kör generátorát egy B populációval egészíti ki, és a legújabb változatot is
méri.

### Elrendezés

- **Seedek:** 5000–5029 (friss), 5 meglepetéstípus, A és B populáció: 300 eset. Futtató:
  [`run_r57.py`](../../experiments/arlc/arlc/run_r57.py).
- **B:** seedenként 30% eséllyel egészében téves tankönyv (55. kör `make_case`). A sorsolás szerint 8 szemét
  seed: 5000, 5002, 5005, 5006, 5011, 5017, 5021, 5027.
- **Módszerek:**
  - v3;
  - v4.4e (v4.4-egyszintű, 50. kör);
  - **v4.7** = v4.4e + gondozott forrás (tankönyv, népszámlálás) kontextusa 10 bit (56. kör; a paramétert
    egyetlen seed diagnózisa után választottam, ezért itt *tesztelem*, nem igazolom);
  - feltáróan: H2(v3 + v4.7), az 55. kör kétsebességű szabálya.
- **Mérőszámok:** post-acc, target-acc, a tankönyv félretevése (≥ 90% elvetve vagy izolálva).

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H57a (A ∪ B, 60 világ):** v4.7 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H57b (A):** v4.7 − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát (a gondozott-forrás prior segít).
- **H57c (B):** v4.7 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát. A v3 rögzített megbízhatósággal
  nem tud egy szemét tankönyvtől megszabadulni.
- **H57d (félretevés):** a *jó* tankönyves világokban (A, plusz a B nem szemét seedjei) a v4.7 kevesebbszer
  teszi félre a tankönyvet, mint a v4.4e. A *szemét* tankönyves világokban a v4.7 az esetek legalább felében
  félreteszi.

**Kiegészítés (az 55. kör A-része után, az 57. kör adatai előtt commitolva):** az 55. kör feltáró eredménye
szerint a fordított kétsebességű szabály a legjobb: **H3(v4.7) = a v4.7 válasza, kivéve ha a v4.7 félretette
a tankönyvet; akkor a v3-é.** Ez a tárolt mezőkből esetenként számolható.
- **H57e (A):** H3 − v4.7 (post-acc) ≥ 0 pontbecslésben, és H3 − v3 > 0, a CI nem tartalmazza a nullát.
- **H57f (B, kudarc-jóslat):** a szemét tankönyves B-világokban H3 − v4.7 < 0, mert a visszaesés a *helyes*
  félretevést is visszacsinálja.

**Második kiegészítés (az 55. kör B-része után, a C populáció adatai előtt commitolva):** az 55. kör B
populációja nem diszkriminatív: helyes félretevés után nincs más tudásforrás, ezért minden módszer kb. 0,41.
A gestalt-váltás értéke csak rivális, helyes elmélet mellett mérhető. **C populáció:** két tankönyv („book”,
„book2”, mindkettő q = 0,95, mindkettő gondozott); seedenként véletlenül az egyik egészében téves (véletlen
előjelek), a másik a szokásos (10% hibás). Seedek 5000–5029, 150 eset. A v4.7-ben mindkét tankönyv
kontextusára 10 bit. A H3 visszaesése C-ben akkor lép életbe, ha a v4.7 *bármelyik* tankönyvet félreteszi.
- **H57g (C):** v4.7 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H57h (C):** a v4.7 az esetek legalább felében a szemét tankönyvet teszi félre, és a jót nem; a v3 ritkábban.
- **H57i (C, kudarc-jóslat):** H3 − v4.7 (post-acc) < 0, mert a visszaesés a helyes gestalt-váltást
  visszacsinálja.

**Kudarc-feltétel:** ha H57b nem teljesül, a gondozott-forrás prior a 3024-es seedre illesztett hatás volt.
Ha H57c nem teljesül, a v4.7 a szemét tankönyvet sem tudja jobban kezelni, mint a v3.

## 2. rész: eredmények

Nyers adat: [`results/kor-57/`](../../experiments/arlc/results/kor-57/) (A, B, C, C_v4.4); elemzés:
[`analyze_r55.py`](../../experiments/arlc/arlc/analyze_r55.py) (`57`). Eltérés: a C és a B futás sorrendje
(először C) a kiegészítés után; a várakozó szkript első változata saját magát várta, ezért az A futás később
indult. Egyik sem érinti az eredményeket.

### A populáció (seed 5000–5029, 150 eset)

| | post-acc | target-acc | tankönyv félretéve |
|---|---|---|---|
| v3 | 0,791 | 0,581 | 6 |
| v4.4e | **0,848** | **0,678** | 0 |
| v4.7 | **0,848** | 0,677 | 0 |
| H2 (v3 + v4.7, kúp) | 0,803 | 0,674 | – |

- **H57b nem teljesül:** v4.7 − v4.4e = 0,000 [0; 0]. Ezeken a seedeken a v4.4e sosem tette félre a tankönyvet,
  így a gondozott-forrás priornak nem volt alkalma hatni. A hipotézis nem cáfolódott, hanem **nem
  tesztelődött**.
- **H57e:** H3 = v4.7 (nem volt visszaesés); H3 − v3 = +0,057 [+0,036; +0,081]. Teljesül, de triviálisan.
- v4.7 − v3 = **+0,057** [+0,036; +0,081]: a harmadik független seed-halmazon is (44.: −0,084 a v4-re; 50.:
  +0,024 n.s.; 55.: +0,040; 57.: +0,057) a javított változat jobb, mint a v3. Az 50. kör H50a-ja tehát a
  seed-halmaz véletlenje is lehetett.

### C populáció (két rivális tankönyv, az egyik egészében téves; 150 eset)

| | post-acc | target-acc | helyes gestalt-váltás (szemét félretéve, jó megtartva) |
|---|---|---|---|
| v3 | 0,440 | 0,329 | **0/150** |
| v4.4e | 0,454 | 0,449 | **0/150** |
| v4.7 | 0,377 | 0,397 | **0/150** |

- **H57g nem teljesül, sőt fordítva:** v4.7 − v3 = **−0,064** [−0,119; −0,010].
- **H57h nem teljesül:** egyik előregisztrált módszer sem hajt végre helyes gestalt-váltást egyetlen esetben sem.
- **H57i nem teljesül:** H3 − v4.7 = +0,064 (a visszaesés itt *javít*, mert a v4.7 rosszabb a v3-nál).

**A mechanizmus** (seed 5001, átkategorizálás): a 32 tankönyvi szabálypárból 19 ellentmond egymásnak. Mindhárom
módszer **mindkét tankönyvet és a népszámlálást is kontextusba izolálja**, egyik szabályt sem veti el. Így a
fő kontextusban egyetlen szabály sem érvényes. Egyszintű megbízhatóság mellett a szemét tankönyv 19 szabályának
elvetése kb. 19 × 5 bit, a „két elmélet két külön világról szól” magyarázat 2–3 × 6–10 bit. **A kontextus-
mechanizmus a rivális elméletek általános menekülőútja**, és a jó elméletet is eldobja. A 17. kör „kontextus
vagy hazug” azonosíthatatlansága ez, elméletszinten.

### B populáció (8 szemét seed, 150 eset)

| | post-acc (összes) | szemét tankönyv (40 eset) | jó tankönyv (110 eset) | félretéve: szemét / jó |
|---|---|---|---|---|
| v3 | 0,702 | 0,469 | 0,787 | 40/40 / 5/110 |
| v4.4e | **0,746** | 0,465 | **0,849** | 38/40 / 0/110 |
| v4.7 | 0,741 | 0,447 | **0,849** | 34/40 / 0/110 |

### A hipotézisek összesítve

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H57a:** v4.7 − v3 (A ∪ B) > 0 | **+0,048** [+0,028; +0,068] | **teljesül** |
| **H57b:** v4.7 − v4.4e (A) > 0 | 0,000 | **nem tesztelődött** (nem volt félretevés) |
| **H57c:** v4.7 − v3 (B) > 0 | **+0,039** [+0,002; +0,071] | **teljesül** (alig) |
| **H57d:** jó tankönyv: v4.7 < v4.4e félretevés; szemét: v4.7 ≥ 50% | jó: 0 = 0 (v3: 11); szemét: 34/40 | **részben** (a második fele teljesül) |
| **H57e:** H3 ≥ v4.7 és H3 > v3 (A) | 0,000; +0,057 [+0,036; +0,080] | teljesül (triviálisan, nem volt visszaesés) |
| **H57f:** H3 − v4.7 < 0 (B szemét) | +0,026 [−0,032; +0,098] | **nem teljesül** |
| **H57g:** v4.7 − v3 (C) > 0 | **−0,064** [−0,120; −0,011] | **nem teljesül, fordítva** |
| **H57h:** helyes gestalt-váltás ≥ 50% (C) | **0/150** mindhárom módszerrel | **nem teljesül** |
| **H57i:** H3 − v4.7 < 0 (C) | +0,064 | **nem teljesül** |

### Feltáró: a kétszintű v4.4 (κ_T = 1) a C populáción

Kód: [`r57_c_v44.py`](../../experiments/arlc/arlc/r57_c_v44.py). Ugyanaz a 150 C-eset:

| | post-acc | helyes gestalt-váltás | mindkét tankönyv félretéve |
|---|---|---|---|
| v3 | 0,440 | 0/150 | 150/150 |
| v4.4e (egyszintű) | 0,454 | 0/150 | 150/150 |
| **v4.4 (kétszintű, κ_T = 1)** | **0,660** | **122/150** | 25/150 |

v4.4 − v3 = **+0,220** [+0,154; +0,284]; v4.4 − v4.4e = +0,206 [+0,144; +0,267].

### Értelmezés

1. **A 44–57. kör legtisztább eredménye.** Ugyanazon a generátoron, ugyanazokon a seedeken a κ_T = 1 a rivális
   elméletek populációjában (C) **+0,21-et ad**, a „mindig nagyjából helyes tankönyv” populációjában (A, 44.
   kör) **−0,08-at**. Az 50. kör sejtése, hogy a κ_T = 1 egy 50%-os szemét-arányú terület priorja, ezzel közvetlenül
   igazolódott. **Egyik beállítás sem helyes önmagában; a helyes érték területi tény.**
2. **Az előregisztrált v4.7 a C-ben a legrosszabb.** A gondozott-forrás prior (kontextus 10 bit) a kontextus-utat
   drágítja, a szemét elmélet elvetését viszont nem könnyíti. Így a rendszer egyik jó utat sem találja meg.
3. **A kétsebességű ötlet (H2, H3)** a vizsgált formában nem hozott áttörést: az A-ban a v4.4e/v4.7 maga is a
   legjobb, a B-ben és a C-ben a visszaesés a helyes és a téves félretevést nem tudja megkülönböztetni.
4. **Mi következik:** a „szemét elmélet” arány (π) a területen tanulandó paraméter. Az 52. kör szerint ez sok
   világból tanulható, ha a tanítójel független a modell döntéseitől. A természetes következő lépés egy
   **területi π-vel paraméterezett keverék-prior**, a C-ben kis π (gestalt), az A-ban nagy π (stabilitás),
   ugyanazzal a kóddal. A 48. kör keverék-priorja ezt már tudja; ami hiányzik, az a π megbízható becslése.
