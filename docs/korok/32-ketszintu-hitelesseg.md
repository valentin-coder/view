# 32. kör – Kétszintű hitelesség: az elmélet és az adat külön

## Kérdés

A 28. kör feszültsége: a fafelcserélés (Thagard 9. fokozat) csak akkor koherens, ha egy forrás
szabályai csomagként viselkednek, vagyis gyorsan tanuló forrásmodell (kis κ) kell. Ugyanez a kis κ
zaj mellett a terepforrást is gyorsan hitelteleníti, és ezzel a kihívó elmélet evidenciáját is. A
gyors gestalt-váltás és a zajtűrés **ugyanazon a paraméteren** múlt.

**Ötlet (29. kör A):** egy forrás *szabályai* (elmélet) és *tényei* (adat) külön megbízhatósági
paramétert kapnak, külön κ-val: kicsit az elméletnek (κ_T), nagyot az adatnak (κ_S).

## Levezetés: mikor indul a gestalt-kaszkád?

Egy n szabályból álló elmélet, ha k szabálya már cáfolt:
- egy további szabály **megtartása** `−log₂((α + n − 1 − k)/(κ + n − 1))`;
- **elvetése** `−log₂((β + k)/(κ + n − 1))` bitbe kerül, ahol α = κq, β = κ(1 − q).

Az elvetés olcsóbb, ha

`k > (κ(2q − 1) + n − 1) / 2`.

Ha ennyi szabály közvetlenül cáfolt, a többi magától, cáfolat nélkül is kiesik: ez a kaszkád. A
10 szabályos fákra, q = 0,95 mellett:
- κ = 1: k > 4,95;
- κ = 3: k > 5,85;
- κ = 10: k > 9;
- κ = 30: soha.

Ez megmagyarázza a 28. kör megfigyelését: κ = 3 mellett teljes váltás, κ = 10 mellett „alvó hibrid”.

## Elrendezés

A 28. kör 9. fokozata (két teljes fa, H régi, L új), mindkét irányban (L igaz vagy H igaz),
zajjal (0; 0,15; 0,25), 4–32 ténnyel, 5 seed. Módszerek: rögzített megbízhatóság; egyszintű
tanult κ = 30 és κ = 3; kétszintű (κ_T, κ_S) = (3, 30), (3, 100), (1, 30). A keresés a 36. körben
javított teljes visszahelyezéssel fut. Eredmény: [`results/kor-32/results.json`](../../experiments/arlc/results/kor-32/results.json).

## Eredmények (összesítve)

| módszer | pontosság zaj nélkül | pontosság zajjal | a vesztes fa aktív aránya (kisebb = koherensebb) |
|---|---|---|---|
| rögzített megbízhatóság | 0,90 | 0,79 | 0,79 |
| egyszintű, κ = 30 | 0,91 | 0,80 | 0,78 |
| egyszintű, κ = 3 | **1,00** | **0,63** | 0,25 |
| kétszintű (3, 30) | 1,00 | 0,83 | 0,12 |
| kétszintű (3, 100) | 1,00 | 0,84 | 0,12 |
| **kétszintű (1, 30)** | **1,00** | **0,89** | **0,08** |

**Részletek (néhány sor; cella: pontosság / H-aktív / L-aktív):**

| igazság | zaj | tények | rögzített | egyszintű κ = 3 | kétszintű (1, 30) |
|---|---|---|---|---|---|
| L | 0 | 8 | 0,66 / 0,90 / 0,80 | 1,00 / 0,00 / 1,00 | 1,00 / 0,00 / 1,00 |
| L | 0,15 | 8 | 0,64 / 0,92 / 0,76 | 0,57 / 0,56 / 0,98 | **0,99 / 0,00 / 1,00** |
| H | 0,15 | 8 | 0,93 / 0,96 / 0,74 | 0,79 / 1,00 / 0,20 | **0,99 / 1,00 / 0,00** |
| L | 0,25 | 16 | 0,75 / 0,82 / 0,84 | 0,57 / 0,40 / 0,76 | **0,89 / 0,00 / 0,96** |
| H | 0,25 | 16 | 0,80 / 0,88 / 0,74 | 0,78 / 1,00 / 0,20 | **0,93 / 1,00 / 0,00** |
| L / H | 0,15–0,25 | **4** | 0,53–0,89 | 0,20–0,34 | 0,61–0,88 (még nincs váltás) |

## Értelmezés

1. **A kétszintű hitelesség feloldja a 28. kör feszültségét.** Zaj nélkül is, zajjal is ez a legjobb,
   *mindkét* irányban (akár a régi, akár az új fa igaz), és a váltás koherens: a vesztes fa
   szabályainak csak 8%-a marad aktív.
2. **Miért működik:** az elmélet szabályai egymással csatoltak (κ_T kicsi, tehát kaszkád), a
   terepforrás tényei viszont nem (κ_S nagy, a zajos tények nem hitelteleníti a forrást). Ez
   ugyanaz a különbségtétel, mint a tudományban az *elmélet* és a *mérőeszköz* megbízhatósága között:
   egy rossz műszer nem teszi rosszá az összes mérést, egy cáfolt elmélet viszont gyengíti a többi
   állítását.
3. **Korlát:** nagyon kevés tény (4) mellett zajjal egyik módszer sem vált megbízhatóan. Ott még az
   evidencia is kevés.
4. **Tudományfilozófiai kapcsolat:** Lakatos kutatási programjai (kemény mag + védőöv,
   ellenőrizendő) egy kétszintű szerkezetet írnak le. Itt a „mag” egy κ_T-vel csatolt szabálycsalád.
   A váltás akkor következik be, ha a közvetlenül cáfolt szabályok száma átlépi a fenti küszöböt.
   Ez Lakatos „degeneráló program” fogalmának egy számszerű változata, és csak analógia.

## Következmény

ARLC v4: forrásonként két hitelesség-paraméter, (κ_T ≈ 1, κ_S ≈ 30). A szabálycsaládokat itt a
forrás azonosítja. Ha egy forrás több elméletet közöl, a csoportosításhoz a szabályokhoz
elmélet-címke kell, ami egy szövegben ritkán explicit. Ez egy újabb hely, ahol egy LLM segíthet
(melyik állítás melyik elmélet része).
