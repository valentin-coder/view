# 110. kör – Összefoglaló műszaki jelentés (1–109. kör)

## 1. A feladat és ami belőle megvalósult

**Az eredeti feladat:** egy neuroszimbolikus architektúra, amelyben egy *befagyasztott* LLM aktivációit egy külső,
módosítható szimbolikus struktúra reprezentálja. A struktúra meglepő információra **azonnal és gradiens nélkül**
átrendeződik. A kérés kritikus mérlegelés volt, és az ismert módszerek megnevezése.

**Ami megvalósult:** a szimbolikus rész, egy forrástudatos hiedelemrevíziós motor (**ARLC**), és egy kiterjedt, előregisztrált
mérési apparátus. **Ami nem valósult meg:** a neurális rész (B fázis). A környezetnek nincs hálózata modellt letölteni. A
61. kör kódja kész, de futtatatlan. **Minden alábbi eredmény szintetikus világokon született.**

## 2. Az architektúra (ARLC)

**Reprezentáció.** Megfigyelések: szabályok („a C kategória tagjai p-k”, „C ⊂ D”), tagságok, tények, mindegyik
forrással, időbélyeggel és deklarált hitelességgel (q). Egy hipotézis öt (+1) komponensből áll: félretett megfigyelések,
kivételek (egyedi és osztályszintű), kontextusba izolált források, időbeli vágások, indukált/feltalált szabályok (és
forrás-változáspontok, kikapcsolva).

**Pontszám.** Egyetlen MDL/MAP-kódhossz: a megfigyelések illeszkedése a hipotézis zárásához, a források
elfogadás–félretevés sorozatának kódja, a kivételek, vágások, izolálások, indukált szabályok ára.

**Keresés.** Ütközésvezérelt nyaláb (mélység 2, mohó befejezés, visszavétel). A „gradiens nélküli, azonnali
átrendeződés” ebben a keresésben történik, minden új megfigyelésnél.

**Ismert elemek (átcímkézés-ellenőrzés):**

| elem | ismert megfelelője |
|---|---|
| a kódhossz-pontszám | MDL-modellválasztás (Rissanen); MAP |
| kivételek ε-priorral | körülhatárolás / abnormalitás-predikátumok (McCarthy), alapértelmezett logika |
| specifikusság | inferential distance (Touretzky, 1986) |
| osztálykivétel rivális szabályra (PK) | prioritásos alapértelmezések, preferred subtheories (Brewka, 1989) |
| béta-binomiális forrás-megbízhatóság | Dawid–Skene (1979); igazság-felderítés (truth discovery) |
| „jó munkás / spammer” keverék | Raykar és mtsai (2010) |
| időbeli vágás | frissítés a revízióval szemben (Katsuno–Mendelzon, 1991); változáspont-modellek |
| temperált megbízhatóság | SafeBayes (Grünwald és van Ommen, 2017) |
| kontextus-izolálás | kontextus-logikák, mikroelméletek |

Az új benne az összeállítás, és az, hogy előregisztráltan mértem, hol működik és hol nem.

## 3. A jelenlegi konfiguráció

**Alapértelmezés: `FROZEN_91`** („bízó”). v4.4e (béta-megbízhatóság, kivétel-prior, specifikusság, osztálykivétel,
q-csoport, feltalálás), plusz:
1. tankönyv-keverék, a „szemét-elmélet” esélye metaadatból (60. kör);
2. prioritás-kivétel javított kódhosszal (PK, 81. kör);
3. „új forrás” keverék-prior (N, 86. kör);
4. **hibrid megbízhatóság:** bevált forrás rögzített kóddal, új forrás adaptív keverékkel (91. kör);
5. eseményenkénti vágásár (91. kör).

**Utólagos frissítések:** (112. kör) `FROZEN_112` = `FROZEN_91` + másolásfelismerés horgony-újraindítással – a 111. kör másoló-sebezhetőségét megszünteti; (115. kör) **`FROZEN_115`** = `FROZEN_112` + általános újranyitó keresés + szabály-vágás a frissítés–revízió szemantikával – a szabályváltozást 0,18-ról 0,93-ra javítja, a revíziót érintetlenül hagyja, kb. 2,5× lassabb.

**Megnevezett alternatíva: `F91_Q`** („óvatos”, a deklarált hibavalószínűség kétszerese). A generatív világokon mindenhol
jobb, a kézi feladatok egy részén gyengébb (102., 105. kör). **A B fázishoz ez a biztonságosabb.**

## 4. Bizonyított állítások

Előregisztrált, friss seedes, világok szerinti klaszteres bootstrap; legalább két független mérés.

| állítás | hatás | körök |
|---|---|---|
| **a megbízhatatlan új forrás (hazug, torzított, elavult, visszhang) felismerése** | +0,14 – +0,60 a célkérdéseken a v3-hoz, négy generátoron | 77, 80, 86, 88, 91, 93, 96 |
| **a FROZEN_91 általános pontossága a v3 fölött, ahol a világban van szerkezet** (hierarchia, kereszt-osztályozás, változó állapot) | +0,03 – +0,10 a G1k-n, a G2-n, a G3-on | 91, 96 |
| **a lapos, stabil világban (G4) nincs általános előny** | ±0,01 | 93, 96 |
| rivális elméletek kezelése (metaadat-π) | +0,25 – +0,60 | 60, 70, 75, 92 |
| állapotváltozás (eseményenkénti vágásár) | 1,00 vs. a v3 0,23 – 0,29 | 91 |
| a nyaláb-átlag jobban kalibrál (Brier), mint a MAP vagy a tartózkodás | | 50, 63, 106 |
| a hitelesség túlbecslése sokkal veszélyesebb, mint az alulbecslése | −0,09 vs. +0,03 | 101, 102 |
| **a függetlenségi feltevés megsértése (bevált forrás másolója) a legsúlyosabb sebezhetőség** (a 110. kör után mérve) | 0,59 → 0,00 az érintett kérdéseken | 111 |

## 5. Cáfolt vagy visszavont állítások

| állítás | ami valójában igaz | kör |
|---|---|---|
| „a v4 általában jobb a v3-nál” (44–76) | csak ahol a szerkezet megvan; az adaptív kód félrespecifikált világban árt | 77, 88, 89 |
| a „más régió” mint rangsoroló típus | 0,04–0,43 bites holtverseny | 62, 64 |
| a nyaláb poszterior-minta | a keresés útja | 63, 67 |
| a kontextusfüggő indukció a G2-kár oka | seedfüggő; friss seedeken 0 | 78 |
| az alosztály-elvágás menekülőút | kétharmadában a G1 generátorhibája | 82, 85 |
| a G4-lemaradás a tankönyv-keverékből jön | a hibrid rögzített kódjából | 93, 95 |
| a 95. kori „hatástalan” kapcsolók fölöslegesek | a q-csoport helyességi javítás | 103 |
| a fieldB-t a PK helyesen teszi félre | 61%-ban | 82 |

## 6. Nyitott problémák: a tárcsák

Minden megmaradt probléma ugyanilyen szerkezetű (104., 109. kör): **egy paraméter két jó tulajdonság között választ, és a
helyes értéke a környezet alapgyakoriságaitól függ.**

| döntés | ami eldönti | kör |
|---|---|---|
| jó vagy rossz új forrás (egyetlen állításból) | milyen gyakoriak a hazug források | 98, 100, 101 |
| zaj vagy igaz meglepetés | mennyire zajosak a források | 102, 105 |
| frissítés (a világ változott) vagy revízió (a tudás téves volt) | a 115. kör óta szerkezeti kérdés: a vágás (változás-esemény) vagy a félretevés dönti el a szemantikát | 107, 115 |
| adaptív vagy rögzített forrás-kód | mennyire pontosak a deklarált hitelességek | 89, 91, 96 |

**Ez a sorozat legfontosabb elvi eredménye:** a szimbolikus réteg gyorsan és gradiens nélkül átrendeződik, de hogy
átrendeződjön-e, azt a világ alapgyakoriságai döntik el. Ezeket egy világról tanult modell (a befagyasztott LLM) adhatná.
**A sorozat negatív úton indokolta az eredeti neuroszimbolikus felosztást.**

## 7. Módszertan, és amit tanított

1. **Előregisztráció friss seedeken** (44. kör óta), döntési szabállyal (91. kör óta). Nyolc jelölt bukott el rajta a 96–107.
   körben. Ezek nélküle „javításként” kerültek volna be.
2. **Befagyasztás egy új generátor előtt** (88. kör). Az első olyan mérés, amelyet nem lehetett utólag „megmenteni”.
3. **Generátor-egységteszt** (87. kör): a G1 világainak 96%-a 40 körön át ellentmondásos volt, és ezt csak ez fogta meg.
4. **Igaz-hipotézis-pontozás** (81. kör): szétválasztja a keresési és a modellhibát. Két kódhossz-hibát talált (PK,
   eseményenkénti vágásár).
5. **Menekülőút-audit** (82. kör): a félretevések helyessége. Olyan hibákat mutatott, amelyeket a pontosság elrejtett.
6. **Feladatcsomag minden befagyasztás előtt** (92. kör): megfogta a FROZEN_88 E1-kudarcát és a q-csoport szerepét.

**A legnagyobb tévedés:** a „v4 általában jobb” állítás 30 körön át egyetlen generátoron. **A legfontosabb javítás:**
a generátorok számának növelése, és a generátor-hibák keresése.

## 8. Ajánlás

1. **A növekményes tárcsa-kísérletek leállítása** ezen a hipotézistéren és ezeken a benchmarkokon (109. kör).
2. **A B fázis**, amint lehetséges: forrástípus- és alapgyakoriság-becslés egy LLM-mel („változhat-e ez a szabály?”, „ez a
   forrástípus mennyire megbízható?”), a tárcsák bemeneteként. Az óvatos konfigurációval (`F91_Q`) kezdve.
3. A reprodukáláshoz: [108. kör](108-reprodukalhatosag.md).
