# 28. kör – TFB: Thagard fokozatai szimbolikusan, a nehéz fokozatokkal

## Kérdés

A 9. kör szerint az ARLC a kilenc Thagard-fokozatból ötöt kezel, a 7. (megkülönböztetés
feladása) és a 9. (fafelcserélés) pedig elérhetetlennek tűnt. A 25. kör a nehéz eseteken nem mérte
az optimalitási rést. Ez a kör megvalósítja a TFB-t (Thagard-fokozat benchmark) az 1., 2., 3., 5.,
7., 8. és 9. fokozatra, és megvizsgálja, mi kell egy **koherens** fafelcseréléshez.

Megvalósítás: [`experiments/arlc/arlc/tfb.py`](../../experiments/arlc/arlc/tfb.py); nyers
eredmények: [`experiments/arlc/results/kor-28/results.json`](../../experiments/arlc/results/kor-28/results.json).

## Felismerés: a 7. és a 9. fokozat a meglévő nyelvvel kifejezhető

- **7. fokozat:** a diszjunktság nem a séma kemény kényszere, hanem két *visszavonható* negatív
  szabály (`dax → ¬fep`, `fep → ¬dax`). Az egyesítés két pozitív szabály. Új operátor nem kell.
- **9. fokozat:** két szervezőelv (élőhely vagy leszármazás) két teljes szabálycsaládként, két
  forrásból. A fafelcserélés egy forrás szabályainak visszavonása. Ehhez a 27. körben bevezetett
  forrásszintű lépés elvben elég.

## Eredmények (pontosság; az 1–8. fokozat determinisztikus, a 8. és 9. 5 seed átlaga)

| fokozat | recency | wms | ARLC | ARLC + forráslépés | + tanult megb. κ = 30 | κ = 10 | κ = 3 |
|---|---|---|---|---|---|---|---|
| 1 új példány | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 2 gyenge szabály kivétellel | **0,20** | **0,20** | 1,00 | 1,00 | 0,80 | 1,00 | 1,00 |
| 3 erős szabály | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 5 új fajta-reláció | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 7 megkülönböztetés feladása | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| 8 ágátugrás | **0,67** | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |

**A 2. fokozatot egyszer át kellett írni.** Az első változatban a gyenge szabályt semmi nem
támasztotta alá, ezért egy hiteles ellenpélda mellett az elvetése volt a racionális válasz. A
„gyenge szabály kivételekkel” csak akkor értelmes, ha adatok is alátámasztják. A javított
változatban (4 alátámasztó tény, 1 kivétel) a `recency` és a `wms` eldobja a szabályt, az ARLC
kivételt tesz.

**Az 1., 3., 5. és 7. fokozat túl könnyű:** minden módszer megoldja. A 9. kör kritériuma szerint
ezen a szinten a benchmark nem választ el.

## 9. fokozat: fafelcserélés

Két teljes fa (élőhelyi, H, régi, q = 0,95; leszármazási, L, új, q = 0,9). A megfigyelt
tények az L fát támasztják alá. Cellák: **pontosság / a H fa szabályainak aktív aránya / az L fa
szabályainak aktív aránya.** A koherens váltás H ≈ 0, L ≈ 1.

| tények | recency | wms | ARLC (+forrás) | κ = 30 | κ = 10 | κ = 3 |
|---|---|---|---|---|---|---|
| 2 | 1,00 / 0,70 / 1,00 | 0,55 / 0,94 / 0,76 | 0,58 / 0,94 / 0,76 | 0,58 / 0,94 / 0,76 | 0,81 / 0,82 / 0,88 | 0,74 / 0,40 / 0,60 |
| 4 | 1,00 / 0,70 / 1,00 | 0,58 / 0,92 / 0,78 | 0,61 / 0,92 / 0,78 | 0,61 / 0,92 / 0,78 | 0,91 / 0,76 / 0,94 | **1,00 / 0,00 / 1,00** |
| 8 | 1,00 / 0,70 / 1,00 | 0,63 / 0,90 / 0,80 | 0,66 / 0,90 / 0,80 | 0,66 / 0,90 / 0,80 | 1,00 / 0,70 / 1,00 | **1,00 / 0,00 / 1,00** |
| 16 | 1,00 / 0,70 / 1,00 | 0,84 / 0,78 / 0,92 | 0,90 / 0,76 / 0,94 | 0,97 / 0,72 / 0,98 | 1,00 / 0,70 / 1,00 | **1,00 / 0,00 / 1,00** |
| 32 | 1,00 / 0,70 / 1,00 | 0,94 / 0,72 / 0,98 | 1,00 / 0,70 / 1,00 | 1,00 / 0,70 / 1,00 | 1,00 / 0,70 / 1,00 | **1,00 / 0,00 / 1,00** |

**Értelmezés:**
1. **Rögzített megbízhatóság mellett (ARLC, `wms`) nincs fafelcserélés, csak inkoherens hibrid.**
   A régi fa szabályainak 70–94%-a aktív marad. Egy soha nem cáfolt szabály megtartása szinte
   ingyenes, az elvetése viszont a forrás log-esélyébe kerül. **Rögzített forrás-hitelesség mellett
   az MDL a vesztes elmélet minden nem cáfolt szabályát megtartja.** A forrásszintű lépés ezen
   nem segít, mert a „mindent eldobunk ettől a forrástól” drágább.
2. **A koherens váltáshoz a forrás állításainak csomagként kell viselkedniük.** Tanult
   megbízhatósággal ez megtörténik: ha a forrás több helyen tévedett, a többi állítása is olcsóbban
   elvethető. κ = 3 mellett 4 tény után **teljes gestalt-váltás** történik (H-aktív 0,00).
   κ = 10 mellett a válaszok helyesek, de a régi fa 70%-a „alvó” hibridként megmarad.
3. **A `recency` „tökéletessége” sorrend-műtermék:** az új fa érkezett később, ezért ütközéskor
   mindig a régi esik ki. Fordított sorrendben a régi fát tartaná meg.

## Kontroll: mennyibe kerül a gyors váltás?

| igazság | zaj | tények | ARLC | κ = 30 | κ = 10 | κ = 3 |
|---|---|---|---|---|---|---|
| H (régi) | 0 | 8–32 | 1,00 / 1,00 / 0,70 | 1,00 | 1,00 | **1,00 / 1,00 / 0,00** |
| H (régi) | 25% | 16 | 0,80 | 0,82 | 0,88 | **0,94** |
| H (régi) | 25% | 32 | 0,81 | 0,81 | 0,84 | **0,92** |
| L (új) | 25% | 16 | 0,75 | 0,79 | 0,77 | **0,50** |
| L (új) | 25% | 32 | 0,83 | 0,83 | 0,83 | **0,76** |

**Értelmezés:**
- Zaj nélkül κ = 3 mindkét irányban koherensen és helyesen dönt.
- **Zajjal κ = 3 a hivatalban lévő elméletet részesíti előnyben.** Ha a régi fa igaz, ez a legjobb
  (0,92–0,94), ha az új, a legrosszabb (0,50–0,76). A zajos terepforrás gyorsan hiteltelenné válik,
  és vele a kihívó evidenciája is.
- **Feszültség:** a gestalt-váltás sebessége és a zajtűrés ugyanazon a paraméteren (κ)
  múlik. A 29. kör A-ötlete (kétszintű hitelesség: elmélet és forrás külön) erre válasz lehet.

## Optimalitási rés a nehéz eseteken

A 25. kör nulla rést mért a könnyű feladatokon. A 9. fokozaton a rögzített megbízhatóságú
ARLC a forrásszintű lépéssel és anélkül is ugyanazt adja: a koherens hipotézis (a teljes H fa
elvetése) **rosszabb pontszámú**, mint a hibrid. **Ez nem keresési rés, hanem a célfüggvény
következménye.** A hibrid a rögzített megbízhatóságú MDL szerint az optimum. A koherenciát nem a jobb
keresés, hanem egy másik modell (a tanult, csomagszintű hitelesség) adja.

## A 9. kör jóslatainak frissítése

| fokozat | 9. kör jóslata | mért |
|---|---|---|
| 1, 2, 3, 5 | jó | jó (a 2. csak alátámasztott szabállyal értelmes) |
| 7 | nem kezeli | **kezeli**, visszavonható negatív szabályokkal |
| 8 | jó | jó |
| 9 | csak előre adott alternatívával | **csak előre adott alternatívával ÉS tanult, csomagszintű hitelességgel**; különben inkoherens hibrid |
| 6 | részben | szimbolikusan megoldva (30. kör), a grounding nyitott |
| 4 | nem kezeli | nem kezeli (rész–egész reláció nincs) |
