# 44. kör – Procedurálisan generált, előre rögzített benchmark

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 34. kör szerint a 26–42. kör kilenc új mechanizmust adott a maghoz, mindegyiket a saját,
kézzel tervezett feladatán értékelve. Ez túlillesztés-gyanús. Ez a kör egy olyan benchmarkon
méri a befagyasztott ARLC v4-et, **amelynek a generátorát és az elemzési tervét a futtatás
előtt rögzítem**, és utána sem a generátoron, sem a v4-en nem változtatok.

### A befagyasztott v4

[`experiments/arlc/arlc/v4.py`](../../experiments/arlc/arlc/v4.py), `V4` szótár: tanult
megbízhatóság (κ_S = 30, κ_T = 1), kivétel-prior ε = 0,05, osztályszintű kivétel,
kategória-feltalálás visszavétellel, forrásszintű lépés, kontextusfüggő indukció, teljes
visszahelyezés, helyi becslésű mohó lépés, javítási mélység 2.

### A generátor

[`experiments/arlc/arlc/procedural.py`](../../experiments/arlc/arlc/procedural.py). Eltér a korábbi
kézzel tervezett feladatoktól:
- **véletlen kategória-DAG:** 3 felső, 5 középső, 8 levél kategória; 25% eséllyel két szülő
  (többszörös öröklés, Nixon-gyémántok);
- **szabályok:** kategóriánként 2 véletlen tulajdonság, véletlen előjellel, bármely szinten; az
  igazság **specifikus öröklés** (a legközelebbi szabály dönt; egyforma távolságú ellentmondásnál nem
  definiált, és kimarad);
- **valódi kivételek** (kb. 3% tulajdonságonként);
- **a tankönyv a szabályok 10%-át hibásan közli**; a terepi tények 5%-ban zajosak;
- **30 entitás**, entitásonként 3 megfigyelt tény;
- **meglepetés**, öt típus:
  - átkategorizálás: egy entitás másik levélbe kerül;
  - szabály-helyesbítés: egy *hibásan közölt* tankönyvi szabályt egy ellenőrzés helyesbít, a világ
    nem változik;
  - kivételes alfaj: négy új, „megjelölt” tag, amelyeknél egy öröklés szerint hamis tulajdonság igaz;
  - hazug forrás: 8 hamis tény egy új forrásból;
  - más régió: egy forrás egy másik régióról beszél, ahol egy szabály ellenkező; a helyi igazság nem
    változik.

### Módszerek

`lookup`, `recency`, `wms` (BeliefBank-szerű), `arlc` (a mag alapértelmezése, ez a v3) és `v4`.

### Elemzési terv

- **Világok:** a 1000–1029 seedek, meglepetéstípusonként (5 × 30 = 150 eset), minden módszerrel.
- **Mérőszámok:**
  - *pre-acc:* pontosság a meglepetés előtt, az igazi világhoz mérve (a tankönyvi hibák javítását is méri);
  - *post-acc:* pontosság a meglepetés után, minden definiált kérdésen;
  - *target-acc:* a típusra jellemző célkérdéseken;
  - a meglepetés feldolgozási ideje.
- **Fő végpont:** a post-acc átlaga mind a 150 esetre.
- **Hipotézisek** (95%-os, világok szerinti bootstrap-intervallummal):
  - **H44a:** v4 > wms, legalább 0,02-vel, és a konfidenciaintervallum nem tartalmazza a nullát;
  - **H44b:** v4 > arlc (v3), és a konfidenciaintervallum nem tartalmazza a nullát. **Ha ez nem
    teljesül, a 26–42. kör mechanizmusai ezen a független benchmarkon nem indokoltak**, ezt
    eredményként jelentem, nem hangolok utána;
  - **H44c:** a target-acc típusonként; a v4 a „hazug forrás” és a „más régió” típusban jobb a
    wms-nél (ezeket a tanult megbízhatóság és a forráslépés célozza).
- **Nem változtatok** a generátoron, a v4-en vagy a mérőszámokon az eredmények megtekintése után.
  Ha hibát találok a generátorban, azt külön, a hibával együtt jelentem, és mindkét változat
  eredményét közlöm.

## 2. rész: eredmények

Nyers adat: [`results/kor-44/parts/`](../../experiments/arlc/results/kor-44/parts/) (esetenként),
[`results_0..4.json`](../../experiments/arlc/results/kor-44/) (típusonként összefésülve); elemzés:
[`analyze_r44.py`](../../experiments/arlc/arlc/analyze_r44.py) →
[`analysis.json`](../../experiments/arlc/results/kor-44/analysis.json).

### Eltérések az előregisztrációtól

A generátor, a v4 konfigurációja, a mérőszámok és az elemzési terv **nem változott**. Eltérések a
kódban és a futtatásban:
1. **Kódjavítás a 43. körben** (ingyenes kivételek az alosztály-szabályokon). A hibás kódú első futást 2 óra
   után leállítottam, eredményeit nem használtam.
2. **Konténer-újraindulás** a seed 1001 után. A futás folytatható futtatóval
   ([`run_r44.py`](../../experiments/arlc/arlc/run_r44.py)) folytatódott, a kész esetek megmaradtak.
3. **Viselkedésmegőrző gyorsítás futás közben** (46. kör): 1,8×, bitre azonos kimenet rögzített
   hash-seed mellett. Az esetek egy része a régi, más része az új kóddal készült.
4. **Két eset memóriahiány miatt elveszett** (átkategorizálás, seed 1008 és 1023: egy dolgozó zárás-gyorsítótára
   12 GB fölé nőtt). Ezeket zárás-gyorsítótár-korláttal számoltam újra. Ez szintén viselkedésmegőrző
   (a zárás tiszta függvény; 500-as korláttal is bitre azonos az ekvivalencia-ellenőrzés).
5. **Nem kontrollált:** a mohó lépés holtverseny-feloldása a hash-seedtől függ (46. kör). Holtversenyes
   esetben egy ismétlés eltérhet.
6. **Utólag felismert tulajdonságok, változtatás nélkül:** a generátor specifikus öröklést használ (49. kör), a
   befagyasztott v4 tartalmazza a 45. körben talált 3. hibát (ingyenes kivételek az indukált szabályokon).

### Fő eredmények (150 eset, 30 világ × 5 típus)

| módszer | pre-acc | **post-acc** | target-acc | meglepetés ideje (medián) |
|---|---|---|---|---|
| lookup | 0,538 | 0,519 | 0,318 | ~0 |
| recency | 0,729 | 0,698 | 0,417 | ~0 |
| wms | 0,780 | 0,767 | 0,587 | 0,5 s |
| arlc (v3) | **0,806** | **0,788** | 0,572 | 14,3 s |
| **v4** | 0,754 | 0,704 | **0,614** | 13,8 s |

### A hipotézisek (95%, világok szerinti klaszteres bootstrap, 10 000 minta)

| hipotézis | különbség | 95% CI | eredmény |
|---|---|---|---|
| **H44a:** v4 − wms (post-acc) ≥ 0,02 | **−0,063** | [−0,125; −0,004] | **nem teljesül; a v4 szignifikánsan rosszabb** |
| **H44b:** v4 − arlc (post-acc) > 0 | **−0,084** | [−0,142; −0,030] | **nem teljesül; a v4 szignifikánsan rosszabb** |
| H44c: v4 − wms (target-acc, hazug forrás) > 0 | +0,083 | [−0,042; +0,196] | irányában igen, nem szignifikáns |
| H44c: v4 − wms (target-acc, más régió) > 0 | +0,173 | [−0,024; +0,370] | irányában igen, nem szignifikáns |

**Az előregisztráció szerint: a 26–42. kör mechanizmusai ezen a független benchmarkon nem indokoltak.**
Ezt eredményként jelentem, és a v4-et nem hangolom utána. A javított változatokat (v4.4 és egyszintű
változata) csak másodlagos, címkézett futásként mérem (lent).

### Diagnózis (feltáró, nem előregisztrált)

**1. A v4 7 világban félreteszi a teljes tankönyvet.** A pre-acc eloszlása kétcsúcsú: 10 világban a v4
0,03–0,1-gyel jobb a v3-nál, 7 világban (1003, 1004, 1007, 1009, 1010, 1018, 1027) katasztrofálisan
rosszabb (0,47–0,61). E 7 világból 6-ban a v4 a tankönyv **minden** szabályát elveti, a hetedikben (1003) a
tankönyvet és a népszámlálást kontextusba izolálja. A v3 ezt egyszer sem teszi. Ez a 49. kör kis világos jelensége, itt 30 entitásnál.

**Ha a 7 világot kihagyom** (23 világ, feltáró): pre-acc v4 − v3 = **+0,016** [+0,003; +0,029], post-acc
v4 − v3 = −0,010 [−0,048; +0,023]. A v4 tehát a tankönyvi hibák kezelésében valamivel jobb, de a meglepetés
után ez az előny eltűnik.

**2. Összeomlás a meglepetés után.** A hazug forrás és a más régió típusban a v4 átlagosan 0,10-et esik (a v3
0,04-et, a wms 0,02-t). Több esetben a **post-acc pontosan 0** (hazug forrás: 1010, 1016, 1018, 1027; más
régió: 1002, 1010, 1015, 1027). A seed 1016 (hazug forrás) mechanizmusa: a 8 hamis tény után a v4 a
tankönyv mind a 46 szabályát elveti, és **a terepforrást és a hazug forrást is kontextusba izolálja**. A fő
kontextusban így egyetlen tény sem marad, és minden válasz „nem tudom”.

**A közös ok: két „félretevő” lépés, amelynek ára nem függ attól, mennyi mindent tesz félre.**
- Egy egész elmélet elvetése κ_T = 1 mellett kb. 10 bit, akár 48 szabályról van szó (48. kör).
- Egy forrás kontextusba izolálása fix 6 bit, akár 90 tényről van szó (49. kör). Az izolált tényeket a
  saját kontextusuk ugyanazokkal a szabályokkal kódolja, ezért az izolálás valójában nem egy *más világot*
  modellez, hanem **a források közti ütközéseket vágja át**. Egy hazug forrás ellentmondása így
  „feloldható” azzal is, hogy a rendszer a hazugot *és* a jó terepforrást is félreteszi.

**3. Az idő.** A meglepetés feldolgozása a v4-ben medián 13,8 s (legfeljebb 128 s), a wms-ben 0,5 s. Az
„azonnali átrendeződés” ezen a méreten nem teljesül.

### Értelmezés

1. **Ez a sorozat eddigi legfontosabb eredménye, és negatív.** A 34. kör aggálya igazolódott: a
   mechanizmusok egyenként a saját feladataikon működtek, együtt egy független benchmarkon rosszabbak, mint
   a kiinduló v3 és mint egy egyszerű, súlyozott konzisztencia-alapvonal (wms, BeliefBank-szerű).
2. **A célzott képesség részben megvan:** a hazug forrás és a más régió célkérdésein a v4 irányában jobb (+0,08,
   +0,17). Ezt viszont a nem célzott tudás rovására teszi. Ez a 12. kör plaszticitás–robusztusság dilemmája
   mérhető formában.
3. **A két fő hiba nem hangolási kérdés**, hanem modellezési: a félretevő lépések ára nem skálázódik a
   félretett tartalommal (49. kör, 51. kör). A generatív v5 terve (51. kör) mindkettőt szerkezetileg
   kezeli: a kontextus egy valódi alternatív világ, kódolt eltérésekkel, és a szemét-elmélet prior közös a
   kontextus-priorral.

### Másodlagos, címkézett változatok (nem előregisztrált)

*(a v4.4 és a v4.4-egyszintű futás befejezése után kerül ide)*
