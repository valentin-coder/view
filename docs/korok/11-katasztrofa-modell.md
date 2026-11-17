# 11. kör – A váltás kvantitatív modellje: csúcskatasztrófa és hiszterézis

A 7. kör szerint a követelmény az, hogy a rendszer indokolt esetben hirtelen átrendeződjön,
egyébként álljon ellen. Ez a kör olyan matematikai modellt ad ehhez, amely mérhető,
cáfolható jóslatokat tesz. Fizikából és matematikából jön (katasztrófaelmélet, Thom, Zeeman),
és a fejlődéslélektanban már használták a szakaszos fogalmi váltás modellezésére
[van der Maas–Molenaar 1992].

## A modell

- **Állapot:** `x ∈ ℝ`. Negatív érték: a régi séma él; pozitív érték: az új séma.
- **Potenciál (csúcskatasztrófa, „cusp”):**
  `V(x; a, b) = x⁴/4 − a·x²/2 − b·x`
- **Egyensúlyok:** `x³ − a·x − b = 0`.
- **Kontrollparaméterek:**
  - `b`: az evidencia egyenlege, a felgyűlt anomália-bitek mínusz a régi séma melletti
    bitek (az ARLC CUSUM-statisztikája);
  - `a`: a „hasítási” paraméter, a beágyazottság vagy elkötelezettség.
- **Bistabilitás:** ha `a > 0` és `|b| < 2(a/3)^{3/2}`, két stabil állapot létezik.
- **Ugrás:** a `b = ±2(a/3)^{3/2}` határon az aktuális minimum eltűnik, és az állapot a
  másik ágra ugrik. **Ez a hirtelen átrendeződés.**
- **Hiszterézis:** a visszaugráshoz `b`-nek az ellenkező határig kell mennie. A
  hiszterézis-szélesség `4(a/3)^{3/2}`.

## Mit jósol, ami cáfolható?

| # | Jóslat | Mérés az ARLC-ben | Mérés az LLM-en (B1, kontextus) |
|---|---|---|---|
| J1 | A váltási küszöb a beágyazottság **3/2-edik hatványával** nő. | E2: anomáliák száma a váltásig, a feltevés beágyazottsága szerint | ellentmondó kontextusmondatok száma a váltásig, a tény „ismertsége” szerint |
| J2 | **Hiszterézis**: visszaváltáshoz több evidencia kell, mint az odaváltáshoz. | váltás után ugyanannyi ellenevidencia nem hozza vissza | a mondatok sorrendjének megfordítása más végállapotot ad |
| J3 | **Bimodalitás**: köztes evidencia mellett az állapotok két csúcsba tömörülnek, nem „félúton” vannak. | a nyalábban a súlyok két hipotézisre koncentrálódnak | m eloszlása köztes k mellett bimodális |
| J4 | **Kritikus lassulás** a küszöb előtt: kis perturbációra lassabb visszatérés, nagyobb szórás. | a pontszám ingadozása a CUSUM-küszöb előtt | m szórása parafrázisok között nő a küszöb előtt |

## Döntő különbség: honnan jön a hiszterézis az ARLC-ben?

A tiszta MDL-trigger (4. fázis) **nem** hiszterézises. Ugyanaz a küszöb érvényes oda és
vissza, mert a két hipotézis szerkezeti költsége szimmetrikus. A hiszterézis csak akkor
jelenik meg, ha **a beágyazottság a használattól függ**: váltás után az új séma
következményeit a rendszer használja, ezek további megfigyelésekkel erősödnek, és a
visszaváltás ára nő.

**Ez egy tiszta, kétváltozatos kísérletet ad:**
- *ARLC-statikus:* a beágyazottság rögzített. Jóslat: nincs hiszterézis (J2 bukik).
- *ARLC-használatfüggő:* `ε(a) ← ε(a) + η` minden olyan lekérdezésnél, amelyet a megválaszol.
  Jóslat: hiszterézis van, és a szélessége η-val nő.

Ha a használatfüggő változat sem mutat hiszterézist, a csúcskatasztrófa-modell
nem írja le az ARLC-t, és az ellenállás mechanizmusa máshol keresendő.

## Az LLM-oldali kísérlet (a KTP kódjával, CPU-n)

- **Feladat:** a Valós kategória-világban a B1 kontextus-injektálást k darab ellentmondó
  állítással ismételjük (k = 0…10). Egy másik sorozatban az állításokat ellenevidenciával
  váltogatjuk, növekvő, majd csökkenő sorrendben.
- **Mérés:** az m margó k függvényében (váltási görbe) és sorrendfüggése (hiszterézis).
- **Illesztés:** Cobb maximum-likelihood csúcskatasztrófa-illesztése [Cobb 1978; Grasman,
  van der Maas, Wagenmakers 2009, `cusp` R-csomag] a lineáris és a logisztikus modell ellen,
  AIC/BIC alapján.
- **Miért érdekes:** ha maga a fagyasztott LLM is csúcskatasztrófa-szerűen vált a kontextusban,
  akkor az ARLC-nek ezt nem kell felépítenie, csak kihasználnia. Ismert, hogy a nagyobb
  modellek kontextusban felülírják a priorjukat, a kisebbek kevésbé
  [Wei et al. 2023, „Larger language models do in-context learning differently”].
  A kis modellek viselkedése a k szerint tehát önmagában is tanulságos.
- **Cáfolat:** ha a logisztikus modell AIC-je minden entitásra és mindkét sorrendre
  jobb vagy egyenlő, akkor nincs bistabilitás. A „hirtelen váltás” ilyenkor csak egy
  meredek, de hiszterézis nélküli szigmoid.

## Mit ad ez a keret?

1. **Egyetlen paraméterpárral (a, b) leírja** az ellenállást (7. kör) és a hirtelen
   váltást (eredeti cél).
2. **A beágyazottság szerepét kvantitatívvá teszi:** a küszöb `a^{3/2}` szerint skálázódik.
3. **Korai figyelmeztető jelet ad** (J4): a rendszer jelezheti, ha egy séma közel van az
   átbillenéshez, még mielőtt átbillen [Scheffer et al. 2009]. Ez a robusztussághoz (12. kör)
   is hasznos, mert egy támadás közeledése így előre észlelhető.

## Őszinte korlát

A katasztrófaelméletet a 70-es években erősen túlhasználták, és a kritikusok szerint
sokszor csak utólagos görbeillesztés volt [Sussmann–Zahler 1978]. **Csak akkor ér valamit,
ha a J1–J4 jóslatokat előre rögzítjük, és a modellt alternatívák ellen illesztjük.** Ezért
került ide az AIC-összehasonlítás és a cáfolati feltétel.
