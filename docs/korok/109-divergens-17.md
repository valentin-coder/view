# 109. kör – Divergens és kritikai kör (17.): a plató

## 1. A 104–108. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 105 | meta-kalibráció | a generatív környezetek optimuma azonos; két megnevezett konfiguráció (bízó, óvatos) |
| 106 | tartózkodás | szelektív pontosság +0,008; a Brier nem javul; a nyaláb-átlag jobban kalibrál |
| 107 | szabályok időbeli vágása | +0,095 (n.s.) a szabályváltozásnál, de az A7-ben ront: frissítés vs. revízió |
| 108 | reprodukálhatósági pillanatkép | a konfigurációk, generátorok, eszközök és parancsok egy helyen |

## 2. A plató

A 96–107. körben **nyolc jelölt változtatást** mértem előregisztráltan vagy fejlesztési ellenőrzéssel: lassan tanuló bevált
forrás, forrás-változáspont, megerősítés-függő bizalom, prior-tárcsák, óvatos hitelesség, egyszerűsítés, tartózkodás,
szabály-vágás. **Egyik sem lett alapértelmezés.** Mindegyik a mérések egy részén javított, és egy másikon (egy generátoron
vagy a feladatcsomag egy tételén) rontott. Ez két dolgot jelent:

1. **A FROZEN_91 a mostani hipotézistér és a mostani benchmarkok lokális optimuma.** A hátralévő javítások mind tárcsák (104.
   kör): a helyes értékük a környezet alapgyakoriságaitól függ (mennyire megbízhatók az új források, milyen gyakran
   változik a világ, mennyire pontosak a deklarált hitelességek). Ezeket a benchmarkok különbözően valósítják meg.
2. **A csökkenő hozam a kutatási kérdésről is szól, nem csak a rendszerről.** Szintetikus világokon, ahol én adom meg az
   alapgyakoriságokat, a tárcsák optimuma azon múlik, mit adtam meg. A 108. kör utáni lépés nem egy újabb tárcsa, hanem
   egy olyan adatforrás, amelyben az alapgyakoriságok **nem tőlem jönnek.**

## 3. A frissítés–revízió kérdés mint a sorozat egyik elvi eredménye

A 107. kör szerint egy ellentmondó új szabály egyszerre olvasható változásként (frissítés) és helyesbítésként (revízió).
A kettőt **csak a háttérismeret** választja szét: milyen gyakran változik egy ilyen szabály a világban. A sorozat több
eredménye ugyanerre a szerkezetre vezethető vissza:
- a jó és a rossz új forrás egyetlen állításból (100. kör): **mennyire gyakoriak a hazug források;**
- a zajos és az igaz meglepetés (102. kör): **mennyire zajosak a források;**
- az állapotváltozás és a zaj (88. kör): **milyen gyakran változik az állapot.**

**Ez az eredeti feladat neuroszimbolikus felosztását indokolja.** A szimbolikus réteg (ARLC) tud gyorsan és gradiens nélkül
átrendeződni, de *hogy* átrendeződjön-e, az ezeken az alapgyakoriságokon múlik. Ezeket egy világról tanult modell (a
befagyasztott LLM) adhatja: „egy ilyen szabály változhat?”, „egy ilyen forrás szokott tévedni?”. A sorozat így
negatív úton jutott el az eredeti architektúra indoklásáig. **A szimbolikus rész önmagában nem tudja eldönteni azt, amire a
neurális rész volna való.** A B fázis tehát nem kényelmi kiegészítés, hanem ennek a döntésnek a forrása.

## 4. Kritika

1. **A 102. kör óvatos hitelessége egy határeset:** a generátorokon mindenhol javít, és csak a kézi feladatcsomagon bukik.
   A csomag tételeinek egy része nem MAP-választ vár (102. kör, 4. pont). Elvi döntést hoztam (két megnevezett
   konfiguráció), és nem írtam felül utólag az előregisztrált szabályt. Ez módszertanilag helyes, de a gyakorlatban
   valószínűleg az óvatos változat a jobb alapértelmezés a B fázishoz (101. kör: a túlzott magabiztosság a veszélyes).
2. **A sorozat 108 kör után sem tesztelt valódi adaton.** Ezt minden kritikai kör megnevezi. A szintetikus eredmények
   belső érvényessége erős (előregisztráció, friss seedek, négy generátor, egységteszt), a külső érvényességük ismeretlen.
3. **A kísérleti infrastruktúra mérete:** kb. 80 futtató és elemző modul, több száz eredményfájl. A 108. kör pillanatképe
   ezt kezelhetővé teszi, de egy új résztvevőnek ez a belépési költség.

## 5. Javaslat a következő szakaszra

1. **A növekményes ciklus leállítása ezen a hipotézistéren.** További tárcsa-kísérletek a szintetikus benchmarkokon
   csökkenő hozamúak.
2. **Egy összefoglaló műszaki jelentés** a 108 körről (architektúra, a bizonyított állítások, a cáfolt állítások, a
   módszertani eszközök), egyetlen dokumentumban. Ez a 110. kör.
3. **A B fázis,** amint hálózat (vagy egy helyben elérhető modell) van: a 61. kör SRC-feladata (forrástípus-becslés), és új
   feladatként az alapgyakoriságok becslése („változhat-e ez a szabály?”, „mennyire megbízható ez a forrástípus?”) egy
   LLM-mel, a szimbolikus réteg tárcsáinak bemeneteként.
4. **Egy utolsó szintetikus kísérlet, ha a B fázis még várat magára:** forrásmásolás *bevált* forrásról (a 93. kör nyitva
   hagyta). Ez az egyetlen még nem mért forrás-modell-feltevés (függetlenség) próbája.
