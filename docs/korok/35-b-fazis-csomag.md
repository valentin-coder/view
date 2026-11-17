# 35. kör – A B fázis egylépéses csomagja, és amit a smoke futás már most megtanított

## Cél

A 29. kör kritikája szerint a programból a külső érvényesség hiányzik, és a „neuro” fél
súlypontja a valódi LLM-et igénylő kísérletekre esik. Hálózat nincs, de előkészíthető egy
csomag, amely hálózat vagy saját gép esetén **egyetlen paranccsal** lefuttat mindent a valódi
modellen, minden kontrollal együtt. A csomagot csak véletlen súlyú mini modellen tudtam
kipróbálni. **Ez a próba már három módszertani hibát kiszűrt**, ami a kör fő eredménye.

Kód: [`experiments/bphase/`](../../experiments/bphase/).

## A csomag tartalma

| feladat | mit mér | döntő összevetés | küszöb / cáfolat |
|---|---|---|---|
| **E0** | polaritás, tulajdonság, az alany kategóriája, „igaz-e a világban”, lineáris probe-okkal az utolsó token aktivációján, kitartott parafrázis-sablonokon | aktiváció vs. **statikus** (a modell saját, kontextus nélküli bemeneti beágyazásainak átlaga) vs. BoW | R0: F1 < 0,9 → az aktivációs grounding nem működik |
| **CTX** | fikció vagy tény kontextus egy *kitartott* forráskifejezésből („In the myth, …”, „According to the almanac, …”) | aktiváció vs. statikus vs. BoW; kifejezésszintű AUC, permutációs p | **21. kör: ≥ 0,95**; ha a statikus alapvonal eléri az aktivációt, az előny nem kontextuális |
| **ISZB** | interventív szabálybányászat (8. kör): kategória-transzplantáció után fordul-e a tulajdonság (IIA) | IIA vs. kategóriaszintű promptolás, a tulajdonságtáblához mérve | 8. kör: ha nem jobb a promptolásnál 0,05-tel, a szabályok promptolással nyerendők ki |
| **B4** | LLM-oldali hiszterézis: k ellentmondó „Source i says the robin is a fish” mondat, két sorrendben | váltási pont oda és vissza | 11. kör: ha nincs bistabilitás, az LLM-et nem lehet a váltás jelére használni |
| **KTP** | külön csomag (6. kör) | | 6. kör döntési fája |

## Amit a smoke futás kiszűrt

**1. Felszíni szivárgás a kitartott kifejezésekben.** Az első változatban a tanító fikciós
kifejezések mind „In …”, a tényszerűek többnyire „According to …” kezdetűek voltak. A BoW a
kitartott kifejezéseken 0,74 AUC-t ért el, csak a szerkezetből. *Javítás:* mindkét típusban
mindkét szerkezet egyforma arányban.

**2. A hatásos mintaméret a kifejezések száma, nem a mondatoké.** Kitartott kifejezésként
típusonként 2 szerepelt, és egy *véletlen súlyú* modell aktivációi 0,92 mondatszintű AUC-t
értek el. Egy kifejezés minden mondata hasonló jellemzőket kap, ezért az AUC valójában 4 csoport
rangsorolása, és ott a véletlen is gyakran ad magas értéket. *Javítás:* típusonként 20 kifejezés,
8 kitartott; az eredmény kifejezésszintű AUC és kifejezésszintű permutációs p-érték.

**3. Lexikai átfedés.** A bővítés után a BoW 0,92 kifejezésszintű AUC-t ért el (p = 0,004). A
kitartott kifejezések szavakat osztottak a tanítókkal („fantasy film” – „fantasy novel”). *Javítás:*
a kitartott kifejezések tartalmi szavai nem szerepelnek a tanítókban (a kód ellenőrzi).

**A végső smoke eredmény (véletlen súlyú mini modell):**

| jellemző | mondatszintű AUC | kifejezésszintű AUC | p |
|---|---|---|---|
| aktiváció | 0,36 | 0,28 | 0,94 |
| statikus | 0,35 | 0,30 | 0,92 |
| BoW | 0,52 | 0,55 | 0,41 |

Mindhárom véletlenszintű. **Ez a helyes viselkedés:** egy véletlen modell nem tudhatja, hogy a
„myth” fikció, az „almanac” tény. Egy valódi modellen kapott szignifikáns eredmény így már csak a
kifejezések jelentéséről szóló tudásból jöhet.

**4. A véletlen súlyú kontroll szükségessége.** A 2. hiba idején a *véletlen* modell aktivációi
legyőzték a BoW-ot (0,84 vs. 0,74). Egy „az LLM aktivációi többet tudnak” állításhoz ezért
**kötelező** az azonos architektúrájú, véletlen súlyú modell kontrollként (`--random-init`). Ez
Hewitt és Liang (2019) kontroll-feladat érvelésének a megfelelője: a probe kapacitása is
„tudást” állíthat elő.

## Kapcsolódás

- Tenney et al. 2019 („What do you learn from context?”): kontextuális vs. nem kontextuális
  beágyazások a probe-okban. A statikus alapvonal ennek a megfelelője.
- Hewitt–Liang 2019: kontroll-feladatok a probe-ok szelektivitásához.
- **A 23. kör tanulsága** (a mini-LM előnye egy távoli felügyeletű BoW-val reprodukálható) itt a
  statikus alapvonal formájában jelenik meg. Egy valódi LLM-nél a teljes előtanító korpusz nem
  elérhető, a statikus beágyazás a legközelebbi, letöltés nélkül elérhető pótlék.

## Állapot

A csomag kész, smoke-tesztelt, a valódi futás hálózatra vagy saját gépre vár. **Ha egyszer lefut,
ez lesz a program első külső érvényességű eredménye.**
