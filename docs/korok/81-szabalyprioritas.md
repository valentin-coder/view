# 81. kör – Tanult szabályprioritás: prioritásos alapértelmezés osztálykivétellel (előregisztrált)

## 1. rész: diagnózis, javítás, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### A hiányzó primitív már megvolt

A G2 igazságát egy rejtett családprioritás dönti el: ha egy entitás két kategóriájának ellentétes szabálya van ugyanarra a
tulajdonságra, a magasabb prioritású család nyer. A meglévő **osztálykivétel** (32. kör) pontosan ezt fejezi ki: a
(r_b, cat:a) azt jelenti, hogy „a b szabálya nem vonatkozik az a tagjaira”, vagyis **az a szabálya elsőbbséget élvez a
b-ével szemben**. A G2-n azért inaktív, mert a 48. kör szigorú specifikussága csak alosztályra engedi (a G2-ben nincs
hierarchia).

**Javítás 1 (`priority_exceptions`):** az osztálykivétel akkor is megengedett, ha a c₂ nem alosztály, de c₂-nek van
saját, elfogadott, **ellentétes előjelű szabálya ugyanarra a tulajdonságra** (rivális). **Átcímkézés-ellenőrzés:** ez a
prioritásos alapértelmezett logika (Brewka, 1989: „preferred subtheories”) páronkénti formája. A specifikusság
(Touretzky; 49. kör) ennek speciális esete, ahol a rendezést az alosztály-viszony adja.

### Fejlesztési diagnózis (a 78. kör seedjein, 16000–16019)

Az 1. javítással a G2 pre-acc 0,868 → 0,896 (v4.9 → v4.9+P), de a tankönyvből továbbra is 6,5 szabályt tesz félre a
rendszer (a valódi hiba kb. 1,5). Esetenként megnéztem a félretett szabályokat: a 16003-as seeden 13-ból 11 **helyes**,
köztük olyan, amely mind a 8 tagjára dönt.

**Keresési vagy modellhiba?** Összeraktam az **igaz hipotézist** a generátorból: félretéve a ténylegesen hamis
megfigyelések, és prioritás-kivétel minden olyan ütköző szabálypárra, ahol a rejtett prioritás dönt. Ez a pontozó
szerint ütközésmentes, a pontossága 0,97–1,00. A pontszáma azonban **8 seedből 7-ben 1–18 bittel rosszabb**, mint a
talált hipotézisé. **Modellhiba.**

**Az ok egy árazási hiba.** Az osztálykivétel ára log₂(kategóriák száma) + 1 = 4,2 bit, mert egy *tetszőleges*
kategóriát nevez meg. Egy prioritás-kivételnél viszont a c₂ csak a rivális szabályú kategóriák közül kerülhet ki
(tipikusan 1–2). A helyes kódhossz log₂ |riválisok| + 1 bit.

**Javítás 2 (`priority_code`):** a prioritás-típusú osztálykivétel (nem alosztály, és c₂ rivális) ára
log₂(max(2, |R|)) + 1, ahol R a rivális szabályú kategóriák halmaza. A mohó befejezés helyi költségbecslése ugyanezt
használja. **Ez a kódhossz javítása, nem hangolás:** a kódoló az R-ből választ, nem az összes kategóriából.

Javítás 2 után az igaz hipotézis hátránya 0–7 bitre csökken, és a különbség a megbízhatósági kódban van. Az igaz
hipotézis több terepi jelentést tesz félre, ami 12–13 bittel drágább, mint amennyit az illeszkedésen nyer (5–6 bit).
Entitásonként 4 tény mellett ez **valódi azonosíthatósági határ** (a 64. és 67. kör tanulsága), nem hiba.

Mindkét javítás kikapcsolva bitre azonos a korábbi viselkedéssel (ekvivalencia-ellenőrzés: EGYEZIK).

### Fejlesztési eredmények (16000–16019; hazug forrás; nem teszt)

Kód: [`dev_r81.py`](../../experiments/arlc/arlc/dev_r81.py). v4.9 = v4.8-π + forrástípus-prior (80. kör).

| | G2 pre | G2 post | G2 target | tankönyvi félretevés (G2) | G1-A post | G1-B post |
|---|---|---|---|---|---|---|
| v3 | 0,914 | 0,842 | 0,675 | 5,2 | 0,702 | 0,580 |
| v4.9 | 0,868 | 0,867 | 0,844 | 8,7 | 0,798 | 0,693 |
| v4.9 + P | 0,896 | 0,895 | 0,863 | 6,5 | 0,798 | 0,693 |
| **v4.9 + P + K** | **0,932** | **0,932** | **0,919** | **3,0** | 0,797 | 0,693 |

**A sorozatban először van olyan v4-változat, amely a G2-n (fejlesztési adaton) a v3 fölött van**, és a G1-en nem
változik (a G1-ben a kategóriák hierarchiában vannak, a rivális szabályok ritkák).

### Előregisztráció

- **Seedek:** 18000–18019 (friss).
- **Esetek:** G2: hazug forrás, szabály-helyesbítés, torzított forrás; G1 A populáció: átkategorizálás, hazug forrás.
  100 eset × 3 módszer.
- **Módszerek:** v3; v4.9; v4.9+PK. Kód: [`run_r81.py`](../../experiments/arlc/arlc/run_r81.py).
- **Elemzés:** seedenként a típusokra átlagolva, világok szerinti klaszteres bootstrap (95%).

**Hipotézisek:**
- **H81a (G2, pre-acc):** (v4.9+PK) − v4.9 > 0, a CI nem tartalmazza a nullát.
- **H81b (G2, pre-acc):** (v4.9+PK) − v3 > 0, a CI nem tartalmazza a nullát. (A 77. kör kudarcának megfordítása.)
- **H81c (G1-A, post-acc):** (v4.9+PK) − v4.9 ≥ −0,01 (pontbecslés).
- **H81d (G2, mechanizmus):** a meglepetés előtt félretett tankönyvi szabályok átlaga a v4.9+PK-nál legfeljebb a valódi
  tankönyvhibák átlagának kétszerese, a v4.9-nél nagyobb annál.
- **H81e (G2, post-acc):** (v4.9+PK) − v3 > 0, a CI nem tartalmazza a nullát.

**Kudarc-feltétel:** ha H81a teljesül, de H81b nem, a prioritás javít, de a G2-lemaradás egy része máshonnan jön (pl. a
megbízhatósági kód, l. a fenti azonosíthatósági határt). Ha H81a sem teljesül, a fejlesztési hatás seedfüggő volt (a
16000–16019 seedeken diagnosztizáltam és javítottam, tehát ott illesztett).

## 2. rész: eredmények

Nyers adat: [`results/kor-81/test/`](../../experiments/arlc/results/kor-81/test/); elemzés:
[`analyze_r81.py`](../../experiments/arlc/arlc/analyze_r81.py) → `results/kor-81/analysis.json`. 300 futás, eltérés nincs.

### G2 (60 eset: hazug forrás, szabály-helyesbítés, torzított forrás)

| | pre | post | target | tankönyvi félretevés (pre) | fieldB-félretevés | idő/eset |
|---|---|---|---|---|---|---|
| v3 | 0,900 | 0,872 | 0,786 | 5,75 | 6,05 | 26 s |
| v4.9 | 0,861 | 0,860 | 0,901 | 8,10 | 3,80 | 33 s |
| **v4.9+PK** | **0,923** | **0,924** | **0,930** | **3,25** | **9,75** | 43 s |

(Valódi tankönyvhiba: átlagosan 1,8 esetenként.)

| típus | v3 post / target | v4.9 post / target | v4.9+PK post / target |
|---|---|---|---|
| hazug forrás | 0,856 / 0,688 | 0,861 / 0,875 | **0,922 / 0,888** |
| szabály-helyesbítés | 0,909 / **0,956** | 0,857 / 0,914 | **0,928** / 0,945 |
| torzított forrás | 0,851 / 0,714 | 0,861 / 0,913 | **0,923 / 0,959** |

### G1-A (40 eset: átkategorizálás, hazug forrás)

| | pre | post | target |
|---|---|---|---|
| v3 | 0,773 | 0,739 | 0,534 |
| v4.9 | 0,823 | 0,817 | 0,693 |
| **v4.9+PK** | **0,833** | **0,827** | **0,725** |

### A hipotézisek

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H81a (G2, pre):** PK − v4.9 > 0 | **+0,062** [+0,040; +0,085] | **teljesül** |
| **H81b (G2, pre):** PK − v3 > 0 | **+0,023** [+0,006; +0,043] | **teljesül** |
| **H81c (G1-A, post):** PK − v4.9 ≥ −0,01 | +0,010 [−0,008; +0,040] | **teljesül** |
| **H81d (G2, mechanizmus):** tankönyvi félretevés PK ≤ 2 × 1,8 < v4.9 | 3,25 ≤ 3,6 < 8,1 | **teljesül** |
| **H81e (G2, post):** PK − v3 > 0 | **+0,052** [+0,019; +0,108] | **teljesül** |

### Értelmezés

1. **A 77. kör negatív külső érvényességi eredménye megfordult.** A független generátoron a v4.9+PK minden mérőszámban
   és minden meglepetéstípusban a v3 fölött van (pre +0,023, post +0,052), és a G1-en sem rosszabb (post +0,010 a
   v4.9-hez, +0,088 a v3-hoz). **A sorozatban ez az első konfiguráció, amely mindkét generátoron előregisztráltan,
   friss seedeken a v3 fölött van.**
2. **A mechanizmus az, amit a diagnózis jósolt:** a tankönyv bűnbakká tétele megszűnik (8,1 → 3,25 félretett szabály,
   1,8 valódi hibára), és a valóban rossz fieldB-t teszi félre a rendszer (3,8 → 9,75; a várható hibaszám kb. 11). **[Javítva a 82. körben:** az audit szerint a fieldB-félretevések csak 61%-a helyes; a rendszer esetenként 4,9 igaz fieldB-jelentést is félretesz, a v3 0,2-t.**]**
3. **A javulás két része külön is tanulságos:** a hiányzó primitív (prioritás) már megvolt, csak egy korábbi
   biztonsági korlát (szigorú specifikusság) letiltotta. A második rész pedig egy **kódhossz-hiba** volt, amelyet csak
   az igaz hipotézis pontozásával lehetett megtalálni. **Az „igaz hipotézis pontozása” (orákulum-hipotézis a
   generátorból) mostantól standard diagnosztikai eszköz:** szétválasztja a keresési és a modellhibát. Ez a 68. kör
   horgonyzási kísérletének helyes formája.
4. **Költség:** 30%-kal lassabb a G2-n (43 s vs. 33 s esetenként), a G1-en 4%-kal.

### Kritika

- **A javítást ugyanazon a generátoron diagnosztizáltam, amelyen a teszt fut** (G2, de más seedeken). A G2 *szerkezetére*
  (rejtett prioritás) szabott primitív tehát nem független a teszttől. A friss seedek a seed-illesztést zárják ki, a
  generátor-illesztést nem. Egy harmadik generátor (79. kör 4.4) kellene ahhoz, hogy a priorításos primitív általános
  értékét mérjem.
- A **szigorú specifikusság** (48. kör) célja egy G1-beli menekülőút elzárása volt. A prioritás-kivétel ezt csak rivális
  szabály esetén nyitja meg újra. A G1-en ez nem ártott, de a C populáción (két rivális tankönyv) nem mértem.
