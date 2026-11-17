# 39. kör – Hű magyarázatok: miért rendezett át a rendszer?

## Kérdés

Egy átrendező rendszer csak akkor használható, ha meg tudja mondani, *miért* adta fel egy sémáját.
A „magyarázat” azonban könnyen hamis: felsorolhat bizonyítékokat, amelyek nélkül a döntés
ugyanaz lett volna. Ez a kör két **ellentényes**, ezért definíció szerint hű magyarázatot vizsgál:

- **szükséges okok:** azok a megfigyelések, amelyek egyenkénti elhagyásával a döntés megfordul;
- **elégséges magyarázat:** a megfigyelések egy mohón minimalizált részhalmaza, amely a rögzített
  háttérrel együtt önmagában is előidézi a döntést.

Mindkettőt a teljes ARLC újrafuttatásával ellenőrzöm. Kód: [`explain.py`](../../experiments/arlc/arlc/explain.py);
eredmény: [`results/kor-39/results.json`](../../experiments/arlc/results/kor-39/results.json).

## Elrendezés

E2a-feladat: a „dax mérges” szabály N alátámasztó ténnyel, majd m ellenpélda (új daxok). A döntés:
„a szabály kiesett”. m a küszöbön (m*) és 3-mal fölötte.

## Eredmények

**1. változat: az alátámasztó tények is jelöltek (csak a szabály a háttér).**

| N | m | szükséges okok | elégséges magyarázat |
|---|---|---|---|
| 4 | 3 (= m*) | 6 (minden anomália-állítás) | **4** (2 anomália) |
| 4 | 6 | **0** | 4 |
| 8 | 4 (= m*) | 8 | **4** |
| 8 | 7 | **0** | 4 |
| 12 | 5 (= m*) | 10 | **4** |
| 12 | 8 | **0** | 4 |

**2. változat: az alátámasztó tények a rögzített háttér részei, csak az anomáliák jelöltek.**

| N | m | szükséges okok | elégséges magyarázat |
|---|---|---|---|
| 4 | 3 | 6 | **6** (3 anomália) |
| 4 | 6 | 0 | 6 |
| 8 | 4 | 8 | **8** (4 anomália) |
| 8 | 7 | 0 | 8 |
| 12 | 5 | 10 | **10** (5 anomália) |
| 12 | 8 | 0 | 10 |
| 16 | 7 | 14 | **14** (7 anomália) |
| 16 | 10 | 0 | 14 |

## Értelmezés

1. **Túldetermináltság.** Pontosan a küszöbön minden anomália szükséges ok. A küszöb fölött *egyik
   sem*, mert a döntést több anomália-részhalmaz is külön-külön biztosítja. Ez az aktuális okság
   (Halpern–Pearl 2005) klasszikus túldeterminációs problémája. **Következmény: a „but-for”
   magyarázat egy jól megalapozott revíziót nem tud megmagyarázni.** Minél erősebb az evidencia,
   annál kevesebb a szükséges ok.
2. **A minimális elégséges magyarázat attól függ, mit tartunk rögzítettnek.** Ha az alátámasztó
   tények is elhagyhatók (1. változat), a „magyarázat” mindig 2 anomália, mert egy alátámasztás
   nélküli szabályt 2 anomália is megdönt. **Ez igaz, de félrevezető:** egy *másik világot*
   magyaráz, ahol a szabálynak nincs alátámasztása. Ha az alátámasztás a háttér része (2. változat),
   az elégséges magyarázat mérete **pontosan a küszöb** (3, 4, 5, 7), az E2a képletével egyezően.
3. **Ez a kontrasztív magyarázat kérdése** (Miller 2019, „Explanation in artificial intelligence:
   Insights from the social sciences”): a jó magyarázat egy rögzített alternatívával szemben mond
   valamit. Itt az alternatíva: „miért adtad fel a szabályt *ahelyett, hogy* a jelenlegi
   alátámasztás mellett megtartottad volna?”. A helyes válasz: „mert legalább m* független forrásból
   jött ellenpélda, és ennyi kell N alátámasztás mellett”.

## Javasolt magyarázat-formátum az ARLC v4-hez

> „Feladtam a *dax → mérges* szabályt. **Szükséges és elégséges:** m* = 5 egymástól független
> ellenpélda (forrásuk: …). A szabályt N = 12 megfigyelés támasztotta alá; ennyi alátámasztás
> mellett 5 ellenpélda kell a feladásához. A további 3 ellenpélda nem volt szükséges.”

A számok ellentényes újrafuttatásból jönnek, tehát hűek. A magyarázat nem a támaszhalmazok
felsorolása, hanem a döntés küszöbe és az azt átlépő evidencia.

## Költség és korlát

- Az ellentényes ellenőrzés jelöltenként egy teljes újrafuttatást jelent. Itt 50–60 másodperc
  esetenként; nagy tudásbázison ez nem skálázódik. **Olcsóbb közelítés:** a pontszám-különbségekből
  zárt alakban (26., 38. kör), ellentényes futtatás nélkül. Ennek a hűségét kis feladatokon a
  fenti módszerrel lehet ellenőrizni.
- A mohó minimalizálás nem garantál globálisan minimális elégséges halmazt. Itt a szerkezet
  szimmetriája miatt ez nem probléma.
