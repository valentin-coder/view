# 99. kör – Divergens és kritikai kör (15.): a 94–98. kör mérlege és a sorozat összegzése

## 1. A 94–98. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 95 | konszolidáció (LOO, négy generátor) | lényeges: prioritás, eseményenkénti vágás, N, hibrid; három kapcsoló a generátorokon hatástalan |
| 96 | lassan tanuló bevált forrás | nem segít a G4-en, ront a TFB-2-n → elvetve; a FROZEN_91 előnye friss seedeken megismétlődik |
| 97 | forrás-változáspont | a kereső megtalálja, de nem javít (fejlesztési negatív) |
| 98 | régi típusok a FROZEN_91-gyel | post +0,077; a „más régió”-t az N kezeli; **a helyes helyesbítést elutasítja** (−0,13) |

## 2. A sorozat összegzése: mi épült, és mi bizonyított

### Az architektúra (a 4. fázis tervének megvalósult része)

Egy **szimbolikus, gradiens nélküli hiedelemrevíziós motor (ARLC)**: a megfigyelések (szabályok, tagságok, tények,
forrással és deklarált hitelességgel) egyetlen MDL/MAP-pontszám szerint kerülnek elfogadásra, félretevésre,
kontextusba, időbeli vágásra vagy kivétel alá. A keresés nyalábos, mohó befejezéssel. **Ez a feladat „szimbolikus
struktúra, amely meglepetésre azonnal átrendeződik” részének megfelelője.** Ismert elemekből áll: MDL-modellválasztás,
béta-binomiális forrás-megbízhatóság (Dawid–Skene-szerű), abnormalitás-alapú alapértelmezések (McCarthy,
körülhatárolás), specifikusság (Touretzky), prioritásos alapértelmezések (Brewka), változáspont/vágás. **Az új benne az
összeállítás és a mérés, nem az egyes elemek.**

### Ami előregisztráltan, friss seedeken, több generátoron bizonyított

1. **A megbízhatatlan új forrás felismerése**, négy generátoron (+0,14 – +0,60 a célkérdéseken a v3-hoz képest).
2. **A szerkezeti újítások haszna, ahol a világban megvan a szerkezet:** a FROZEN_91 a G1k-n, a G2-n és a G3-on a v3 fölött van
   (post +0,03 – +0,10, két független előregisztrált mérésben). A lapos, stabil G4-en nincs előny.
3. **A rivális elméletek kezelése metaadat-π-vel** (G1/G1k-C: +0,25 – +0,60).
4. **Az állapotváltozások kezelése** az eseményenkénti vágásárral (G3: 1,00 vs. a v3 0,23).

### Ami nem működik vagy korlátos

1. **Jó új forrás elfogadása metaadat nélkül:** a helyesbítő lektor, a szakértő és a specialista gyanús (−0,03 – −0,13).
2. **Bevált forrás romlása, rosszul kalibrált bevált forrás** (G4, TFB-9): a rögzített kód nem tanulja meg. Az adaptív kód
   megtanulja, de bűnbakot képez (G3). Ezt egyetlen κ nem oldja fel.
3. **Szabályok időbeli változása** (G3 szabályváltozás): a hipotézistér nem fejezi ki.
4. **A neurális oldal:** egyetlen valódi LLM-futás sem volt (hálózat nélkül a modell nem tölthető le). A B fázis kódja kész
   (61. kör), de futtatatlan.

## 3. Kritika a sorozat egészéről

1. **A legértékesebb eszközök a hibakeresők voltak, nem a mechanizmusok:** az előregisztráció friss seedekkel (44. kör
   óta), az ellenőrző jóslatok (68.), az igaz-hipotézis-pontozás (81.), a menekülőút-audit (82.), a generátor-egységteszt (87.)
   és a befagyasztás (88.). Mindegyik egy olyan hibát fogott meg, amelyet a pontosság elrejtett: a G1 ellentmondásos
   világait 40 körön át, két kódhossz-hibát, egy rosszul kalibrált generátor-priort és a FROZEN_88 E1-kudarcát.
2. **A sorozat legnagyobb tévedése az volt, hogy a „v4 általában jobb” állítást 30 körön át egyetlen generátoron tartottam
   fenn** (44–76). Négy generátor után ez a pontosabb „ott jobb, ahol a szerkezet megvan” állításra szűkült.
3. **Az orákulumok:** a tankönyv-π metaadat, a kontextusjel fölösleges lett (98. kör). A forrástípust (T) az N váltotta ki,
   de a 98. kör szerint ennek ára van. **A séma számszerű priorjai** (deklarált hitelesség, változási prior, diszjunktság) a
   valóságban egy LLM-től jönnének, és a 88. kör megmutatta, hogy egy rosszul becsült prior mindent felborít. **A
   rendszer érzékenysége a séma-priorokra a legfontosabb nyitott kockázat a B fázis előtt.**
4. **A kísérleti apparátus nagyobb lett, mint a rendszer:** kb. 60 futtató- és elemzőfájl, és a konfiguráció kapcsolóinak
   harmada a mért világokban hatástalan (95. kör). Egy következő szakasznak inkább egyszerűsítenie kellene, mint újabb
   mechanizmust hozzáadnia.

## 4. Divergens irányok a következő szakaszra

1. **Megerősítés-függő új-forrás bizalom** (98. kör következménye): az új forrás szemét-esélye csökkenjen, ha az állításait
   más forrás vagy szabály megerősíti. Ez a „jó új forrás” korlátot adatból kezelné.
2. **Prior-érzékenységi protokoll:** minden fő eredmény mellé ±2×-es perturbáció a séma priorjain. Ez a B fázis
   előfeltétele, mert ott a priorokat egy LLM becsüli.
3. **Egyszerűsítés:** a hatástalan kapcsolók eltávolítása, egy „v5-mag” néhány elvvel (MDL, hibrid forrás-kód, prioritás,
   eseményenkénti vágás), és a régi körök reprodukálhatósága egy rögzített, címkézett commiton.
4. **B fázis-pótlék hálózat nélkül:** egy helyben futó, kis szöveg-osztályozó a 61. kör SRC-feladatán. A
   B fázis eredeti formájában (befagyasztott LLM aktivációi) így sem validálható, de a forrás-típus becslés zajmodellje
   (66. kör) mérhető volna.

## 5. A következő körökre

- **100. kör:** megerősítés-függő új-forrás bizalom, előregisztrálva.
- **101. kör:** prior-érzékenységi protokoll a FROZEN_91-re.
- **102. kör:** egyszerűsítés (v5-mag), ekvivalencia-ellenőrzéssel és az előregisztrált eredmények újrafuttatásával.
- **104. kör:** divergens és kritikai kör.
