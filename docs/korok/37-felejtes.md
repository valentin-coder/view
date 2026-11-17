# 37. kör – Tömörítés és felejtés: mit őriz meg egy összesítő, és mit nem?

## Kérdés

Az ARLC minden megfigyelést megőriz, a memória korlátlanul nő. A 29. kör D-ötlete: a szabály által
amúgy is jósolt tényeket időnként el lehet felejteni, csak a szabály és a kivételek maradnak. A
29. kör kockázata: a törölt alátámasztás miatt a rendszer **alulbecsüli a szabály feladásának
költségét**, és túl korán vált.

Kód: `Memory.consolidate` a [`core.py`](../../experiments/arlc/arlc/core.py)-ban és
[`consolidation.py`](../../experiments/arlc/arlc/consolidation.py); eredmény:
[`results/kor-37/results.json`](../../experiments/arlc/results/kor-37/results.json).

## Három változat

1. **nincs felejtés;**
2. **felejtés összesítővel:** a törölt tény helyett a pontszám egy `(szabály, entitás, hitelesség)`
   számlálót tart. Ha a szabály aktív és az entitásra nincs kivétel, a hozzájárulás a „jósolt”
   kódhossz, egyébként a „nem jósolt” (1 bit). Ez pontosan az, amit a törölt tény adott volna a
   pontszámhoz;
3. **naiv törlés:** a tény nyomtalanul eltűnik.

Csak olyan tény törölhető, amelyet *pontosan egy* aktív szabály jósol.

## Eredmények (E2a-szerű feladat: N alátámasztó tény, utána ellenpéldák; az átfordulás pontja)

| N | törölt megfigyelés | **új** daxokról: nincs / összesítő / naiv | a **régi, elfelejtett** daxokról: nincs / összesítő / naiv |
|---|---|---|---|
| 2 | 2 / 6 | 2 / 2 / 2 | 4 / **2** / 2 |
| 4 | 4 / 10 | 3 / **3** / 2 | 7 / **3** / 2 |
| 8 | 8 / 18 | 4 / **4** / 2 | 12 / **4** / 2 |
| 12 | 12 / 26 | 5 / **5** / 2 | 27 / **4** / 2 |
| 16 | 16 / 34 | 7 / **7** / 2 | soha / **4** / 2 |

## Értelmezés

1. **Új entitásokra az összesítő pontosan megőrzi a revíziós viselkedést**, miközben a
   megfigyelések 33–47%-át törli. A 29. kör kockázata (alulbecsült beágyazottság) **csak a naiv
   törlésnél** jelentkezik: ott mindig a 2. ellenpéldánál fordul a rendszer.
2. **Az elfelejtett entitásokról szóló ellenpéldáknál az összesítő sem véd.** Felejtés nélkül egy
   ilyen ellenpélda („d₃ nem mérges”) a *korábbi, közvetlen megfigyeléssel* („d₃ mérges”) ütközik,
   és a két tanú közül az egyiket olcsó elutasítani. A szabály ezért rendkívül stabil (12, 27,
   soha). Felejtés után az ellenpélda csak az *általános szabállyal* ütközik, és azt támadja
   (mindig 4).
3. **A számláló a beágyazottságot megőrzi, a konkrét ütközési szerkezetet nem.** Az összesítés
   éppen azt az információt veszíti el, amely egy konkrét állítást egy konkrét emlékkel szembe tudna
   állítani.

## Kapcsolódás

- **Komplementer tanulórendszerek** (McClelland, McNaughton és O'Reilly 1995): a hippokampusz a
  konkrétumokat, a neokortex az általánosításokat tárolja, és a konkrétumok megőrzése véd az
  interferencia ellen. Itt ugyanez szimbolikusan: a konkrét megfigyelések megőrzése véd egy
  általánosítás túl korai feladása ellen, ha a konkrétumot támadják.
- **Forrás-amnézia** (a tény megmarad, a forrása feledésbe merül): itt fordított, a szabály marad, a
  konkrét tanúvallomás elvész.
- **Tesztelhető, spekulatív jóslat emberre:** ha valaki egy általánosítást sok konkrét esetből
  tanult, és a konkrétumokra már nem emlékszik, akkor egy *konkrét eset* cáfolata („az a kutya,
  amit láttál, valójában nem harapott”) könnyebben ingatja meg az általánosítást, mint ha az esetre
  emlékezne. **Nem tudom, létezik-e erre emberi adat; ellenőrizendő.**

## Következmény

- **A felejtés nem semleges tömörítés.** Megváltoztatja, hogy egy új állítás mivel ütközik.
- **Tervezési lehetőség:** a konkrét megfigyelések helyett egy olcsóbb, *forrás és idő nélküli*
  emléknyom („d₃-ról láttuk, hogy mérges”) megőrizné az ütközési szerkezetet, és a megtakarítás
  csak a metaadatokon jönne. Kérdés, hogy ez még „tömörítés”-e. A tárolt ítéletek száma így nem
  csökken.
- **A 10. kör komplexitási szempontjából:** a felejtés a zárás és a keresés költségét csökkenti. Ez a
  hatás csak a felejtéssel együtt jár, ezért az ára (2. pont) a gyorsasággal szemben mérendő.
