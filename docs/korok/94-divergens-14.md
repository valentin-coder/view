# 94. kör – Divergens és kritikai kör (14.): négy generátor után

## 1. A 89–93. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 89 | mi általános három generátor után | csak a forrás-felismerés; az adaptív kód félrespecifikált világban menekülőút |
| 90 | temperált kód prequential η-val | a prequential veszteség rossz célt optimalizál; feltáró: az η = 0 mindhárom generátoron jobb a v3-nál |
| 91 | hibrid kód + eseményenkénti vágásár | **minden hipotézis teljesül: mindhárom generátoron a v3 fölött**, a forrás-felismeréssel együtt |
| 92 | biztonsági ellenőrzés | rendben, egy szűk korláttal (TFB-9); kiderült, hogy a FROZEN_88 az E1-et elrontotta |
| 93 | negyedik generátor (G4) | forrás-felismerés erős; az általános előny nem jelenik meg; két jósolt gyengeség megjelent |

## 2. Mi áll négy generátor után

| képesség | G1k | G2 | G3 | G4 | ítélet |
|---|---|---|---|---|---|
| új, megbízhatatlan forrás felismerése | + | + | + | **+0,26** | **általános** |
| szerkezeti újítások (rögzített megbízhatósággal) | +0,09 | +0,05 | +0,03 | ~0 | **ott segít, ahol a világban van megfelelő szerkezet** |
| bevált forrás romlásának felismerése | – | – | – | 0 | **nincs** |
| jó új forrás elfogadása | (E1: −0,125 a v4.4e-hez) | – | – | −0,09 | **ismert költség** |

A szerkezeti újítások mérlege értelmes, nem illesztés. A specifikusság a hierarchiában, a prioritás a
kereszt-osztályozásban, az eseményenkénti vágás a változó állapotban segít, egy lapos, stabil világban (G4) pedig nem.
**A v4 nem „általában jobb”, hanem több szerkezetet tud kifejezni, és ahol ez a szerkezet jelen van, kihasználja.** Ez az
állítás négy generátoron áll. Az előző („általában jobb”) nem állt.

## 3. A visszatérő mechanizmus: a Pólya-koncentráció vándorol

A 78–93. kör legtöbb hibája ugyanaz: **egy adaptív béta-kód egy forráson belül olcsóvá teszi a sok félretevést**, és ez
menekülőút lesz, ha a világ valamit rosszul áraz. A javítások eddig *áthelyezték* a koncentrációt:

| kör | hol koncentrálódott | javítás | hová került |
|---|---|---|---|
| 78 | népszámlálás, tankönyv (G2) | prioritás + kódhossz (81) | fieldB (82) |
| 88 | terepforrás (G3) | hibrid: bevált adatforrás rögzítve (91) | tankönyv-elmélet (93) |
| 93 | tankönyv-elmélet (G4) | ? | ? |

**Kritika:** ez a „vakond-ütögetés” (whack-a-mole) mintája. A gyökér az, hogy a megbízhatóság MAP-ban szabad paraméterként
tanulódik, és a Pólya-tulajdonság miatt a MAP a koncentrált megoldást kedveli. **Elvi javítás:** a becsületes komponens
priorja legyen erős (κ₁ nagy), hogy a koncentrációhoz elsöprő bizonyíték kelljen. A tényleges szemét-esetet
(hazug forrás, szemét-tankönyv) a keverék *külön* komponense kezeli. A 95. kör ezt méri, mind a négy generátoron és a
feladatcsomagon.

## 4. Kritika a sorozatról

1. **Tizenhat kör (78–93) szólt ugyanarról a témáról** (forrás-megbízhatóság kódolása). A kutatás ezzel mélyült, de
   szűkült: a hiedelemrevízió többi része (kontextus, indukció, feltalálás) nem került újra mérésre a javított
   generátorokon.
2. **A rendszer egyre több kapcsolóból áll** (kb. 25). Ideje egy **konszolidációs körnek:** négy generátoron
   egyet-elhagyó abláció, és ami sehol nem számít, az kikerül. Ez a rendszer saját MDL-elve, önmagára alkalmazva.
3. **A neurális oldal változatlanul hiányzik** (84. kör 3.3). A sorozat egy forrástudatos hiedelemrevíziós motort épített,
   négy szintetikus világon validálva. A befagyasztott LLM-ből kiinduló architektúra (az eredeti feladat) a B fázisig nem
   validálható.
4. **Futási idő:** a rivális elméletek (G1k-C) egy esete 155 s, és ez a sorozat elején is így volt. A 76. kör (szabályszintű
   memó) huszadik köre halasztva.

## 5. Divergens irányok

1. **Erős becsületes prior + külön szemét-komponens** (3. rész): a 95. kör.
2. **Konszolidáció** (4.2): a 96. kör.
3. **Forrásmásolás bevált forrásról:** egy új forrás, amely egy *bevált* forrás hibáit ismétli. A G4 visszhangja ezt nem
   mérte (ott mindkét forrás új volt). Ez a függetlenségi feltevés valódi próbája.
4. **Romló bevált forrás:** a hibrid kód a bevált forrást rögzítve kezeli, így a romlást nem veszi észre. Egy változáspont-
   modell a forrás megbízhatóságára (a 11. kör vágásának mintájára: a forrás megbízhatósága egy időponttól más) elvi
   megoldás volna.

## 6. A következő körökre

- **95. kör:** κ₁ = 300 a becsületes komponensre (elmélet és bevált adatforrás), előregisztrálva négy generátoron és a
  feladatcsomagon.
- **96. kör:** konszolidáció – egyet-elhagyó abláció négy generátoron.
- **97. kör:** a forrás megbízhatóságának változáspontja (romló bevált forrás).
- **99. kör:** divergens és kritikai kör.
