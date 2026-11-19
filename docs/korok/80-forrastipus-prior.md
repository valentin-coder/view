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
