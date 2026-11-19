# 80. kör – Forrástípus-prior a bűnbak-forrás ellen (előregisztrált)

## 1. rész: terv, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### Miért

A 78. kör szerint a G2-n a béta-megbízhatóság bűnbak-forrást hoz létre: a népszámlálást vagy a tankönyvet tömegesen
félreteszi, mert a béta-binomiális kód egy forráson belül a sok félretevést olcsón árazza. Ez a kód saját optimuma
(modellhiba).

### A rendszer: kétkomponensű forrástípus-prior

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`source_mix`), [`v4.py`](../../experiments/arlc/arlc/v4.py)
(`SOURCE_TYPE_MIX`, `V49_SM`). Minden forrás megbízhatóságára egy keverék-prior:
- **becsületes, legfeljebb kissé kalibrálatlan:** Beta(κ₁·q, κ₁·(1−q)) a deklarált q körül;
- **szemét:** Beta(1, 1);
- a súlyok és a κ₁ a **forrás típusából** (metaadat), a priori rögzítve:

| típus | források | π (becsületes) | κ₁ | indok |
|---|---|---|---|---|
| gondozott | tankönyv, népszámlálás, lektor, szakértő | 0,999 | 300 | a megbízhatóság kb. ±0,01 pontossággal ismert |
| terepi | field, fieldA, fieldB | 0,99 | 30 | kalibrálatlan lehet |
| ismeretlen | minden más (új, ellenőrizetlen) | 0,9 | 30 | |

Az elmélet-részre (szabályok) a v4.8-π keverékét használja, a κ₁-et a típusból véve. Ez a 48. kör elmélet-keverékének
kiterjesztése az adatforrásokra. **Átcímkézés-ellenőrzés:** a „jó munkás / spammer” keverék a címkézők megbízhatóságára
(Raykar és mtsai, 2010; 48. kör) forrástípus szerinti priorral. Új elem nincs benne.

**A teljes korábbi viselkedés változatlan**, ha a `source_mix` nincs megadva (ekvivalencia-ellenőrzés: EGYEZIK).

### Fejlesztési ellenőrzés (a 78. kör már felhasznált seedjein: 16000–16019; nem teszt)

Kód: [`dev_r80.py`](../../experiments/arlc/arlc/dev_r80.py); hazug forrás. „+T” = forrástípus-priorral.

| | G2 pre | G2 post | G2 target | G1-A post | G1-A target | G1-B post | G1-B target |
|---|---|---|---|---|---|---|---|
| v3 | **0,914** | 0,842 | 0,675 | 0,702 | 0,375 | 0,580 | 0,271 |
| v4.8-π | 0,888 | **0,885** | 0,838 | 0,757 | 0,604 | 0,719 | 0,594 |
| v4.8-π+T | 0,868 | 0,867 | **0,844** | **0,798** | **0,708** | **0,757** | **0,688** |

(G2: 20 seed, G1: 6, illetve 4–6 seed.)

Átlagos félretevés esetenként a G2-n:

| | tankönyv | népszámlálás | fieldB | hazug (8-ból) |
|---|---|---|---|---|
| v4.4e | 7,2 | 1,8 | 4,7 | 6,9 |
| v4.8-π | 8,2 | 0,4 | 4,6 | 6,7 |
| v4.8-π+T | **8,7** | **0,2** | **9,5** | **8,0** |

**Amit a fejlesztési adat mutat:**
1. A típus-prior a népszámlálás bűnbakká tételét megszünteti, a valóban 0,8-as fieldB-t többször teszi félre (helyesen),
   és a hazug forrást mindig teljesen félreteszi (8/8).
2. **A G2-n a bűnbak áttevődik a tankönyvre** (8,7 félretett szabály esetenként, holott a tankönyvben átlagosan kb. 1,8
   hiba van). A tankönyv 18 szabályából sokat félretenni a keverék szemét-komponensével olcsó (kb. 10 bit + a Beta(1, 1)
   kód). A G2-ben ezt a rejtett családprioritás miatti szabályütközések kényszerítik ki. **Pontosan ezt jósolta a 79.
   kör 3.1. pontja:** az esetenkénti árazás egy menekülőutat bezár, a következő kinyílik.
3. **A G1-en a típus-prior egyértelműen segít** (A post +0,04, target +0,10), főleg a hazug forrás teljes félretevésével.

### Előregisztráció

- **Seedek:** 17000–17019 (friss, egyik kör sem használta).
- **Esetek:** G1 A populáció (átkategorizálás, hazug forrás); G2 (hazug forrás, szabály-helyesbítés). 80 eset × 3
  módszer.
- **Módszerek:** v3, v4.8-π, v4.8-π+T. Kód: [`run_r80.py`](../../experiments/arlc/arlc/run_r80.py).
- **Elemzés:** világok szerinti klaszteres bootstrap (95%), az [`analyze_r44.boot_diff`](../../experiments/arlc/arlc/analyze_r44.py)-fel.

**Hipotézisek:**
- **H80a (G1-A, post-acc, mindkét típus):** (v4.8-π+T) − v4.8-π > 0, a CI nem tartalmazza a nullát.
- **H80b (G2, pre-acc, mindkét típus):** (v4.8-π+T) − v4.8-π **< 0**, a CI nem tartalmazza a nullát (előre jelzett kár).
- **H80c (G2, mechanizmus):** a +T átlagosan több tankönyvi szabályt és kevesebb népszámlálási állítást tesz félre
  (meglepetés előtt), mint a v4.8-π; és a félretett tankönyvi szabályok száma a +T-nél nagyobb a valódi tankönyvhibák
  számának kétszeresénél.
- **H80d (hazug forrás célkérdései, mindkét generátor):** (v4.8-π+T) − v4.8-π ≥ 0 (pontbecslés).

**Értelmezés előre:** ha H80a és H80b teljesül, a típus-prior **generátorfüggő**: ahol a hipotézistér kifejezi a világot
(G1), segít, ahol nem (G2), a bűnbakot csak áthelyezi. Ekkor a valódi javítás a hiányzó primitív (82. kör: tanult
szabályprioritás), és a +T csak utána értékelhető újra. Ha H80b nem teljesül, a fejlesztési kár seedfüggő volt, és a +T
alapértelmezésnek jelölt.

## 2. rész: eredmények

Nyers adat: [`results/kor-80/test/`](../../experiments/arlc/results/kor-80/test/); elemzés:
[`analyze_r80.py`](../../experiments/arlc/arlc/analyze_r80.py) → `results/kor-80/analysis.json`. 240 eset, eltérés nincs.

| | G1-A pre | G1-A post | G1-A target | G2 pre | G2 post | G2 target |
|---|---|---|---|---|---|---|
| v3 | 0,785 | 0,723 | 0,541 | **0,902** | 0,870 | 0,794 |
| v4.8-π | **0,813** | 0,784 | 0,670 | 0,870 | 0,860 | 0,853 |
| v4.8-π+T | 0,811 | **0,804** | **0,710** | 0,868 | **0,872** | **0,894** |

Félretevés a meglepetés előtt (átlag esetenként, G2; a valódi tankönyvhiba átlagosan 1,45):

| | tankönyv | népszámlálás | fieldB (valódi hibaarány 0,2) |
|---|---|---|---|
| v3 | 5,9 | 1,15 | 6,45 |
| v4.8-π | 8,8 | 0,10 | 4,35 |
| v4.8-π+T | 8,35 | 0,30 | **13,3** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H80a (G1-A, post):** +T − v4.8-π > 0 | +0,021 [+0,000; +0,049] | **teljesül** (épphogy) |
| **H80b (G2, pre):** +T − v4.8-π < 0 | −0,001 [−0,017; +0,014] | **nem teljesül:** nincs kár |
| **H80c (G2, mechanizmus):** +T több tankönyvi és kevesebb népszámlálási félretevés; tankönyv > 2 × valódi hiba | tankönyv 8,35 < 8,8; népszámlálás 0,30 > 0,10; 8,35 > 2,9 | **nem teljesül** (csak a harmadik része) |
| **H80d (hazug forrás target):** +T − v4.8-π ≥ 0 | G1: **+0,100** [+0,044; +0,175]; G2: **+0,081** [+0,006; +0,194] | **teljesül** |

### Értelmezés

1. **A fejlesztési adat megtévesztett, mert rossz alapvonalhoz mértem.** A fejlesztési táblában a népszámlálás
   bűnbakká tételét a v4.4e-n láttam (1,8), de a v4.8-π-ben a tankönyv-keverék miatt már eleve a tankönyv a bűnbak (8,8),
   és a népszámlálás alig (0,1). A H80b-t és a H80c-t a v4.8-π-re fogalmaztam meg, a jóslatot viszont a v4.4e-ből
   vezettem le. **Ez a jóslat megfogalmazásának hibája, nem a mérésé.** A teszt szerint a +T a v4.8-π-hez képest a G2-n
   semleges.
2. **A forrástípus-prior hasznos és nem árt:** a hazug forrás felismerése mindkét generátoron +0,08 – +0,10 a célkérdéseken,
   a G1-ben a post-acc is javul. A G2-n a valóban 0,8-as fieldB-t helyesen teszi félre (13,3 félretevés; a várható hibaszám
   kb. 12). Az előregisztrált szabály szerint **a +T alapértelmezésnek jelölt** (v4.9 = v4.8-π + forrástípus-prior).
3. **A G2-lemaradás a v3-hoz képest megmarad** (pre −0,033). Oka minden v4.8-változatban a **tankönyv bűnbakká tétele**
   (8–9 félretett szabály 1,45 valódi hibára). A v3 is túl sokat tesz félre (5,9). A gyökérok a G2 rejtett
   családprioritása, amelyet a hipotézistér nem fejez ki. A típus-prior ezen nem segít, és ezt a 79. kör előre
   megmondta.

### Következmény

A 81. kör a hiányzó primitívet vizsgálja. A fejlesztés közben kiderült, hogy **a meglévő osztálykivétel pontosan egy
páronkénti szabályprioritás**: (r_b, cat:a) jelentése „a b szabálya nem vonatkozik az a tagjaira”. A G2-n csak azért
inaktív, mert a 48. kör szigorú specifikussága alosztályt követel (a G2-ben nincs hierarchia). A 81. kör ezt
oldja fel: az osztálykivétel akkor is megengedett, ha az a-nak saját, ellentétes előjelű szabálya van ugyanarra a
tulajdonságra (prioritásos alapértelmezés).
