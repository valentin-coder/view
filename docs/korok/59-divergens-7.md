# 59. kör – Divergens és kritikai kör (7.): a területi prior, és amit az 55–58. kör megmutatott

## 1. Az 55–58. kör mérlege

| állítás | kör | eredmény |
|---|---|---|
| a kétsebességű rendszer (v3 alap + v4.4e a kúpban) jobb a v3-nál | 55 | **igen**, kicsit (+0,012) |
| … és nem rosszabb a v4.4e-nél | 55 | **nem**: rosszabb (−0,028), mert a v4.4e általánosan is jobb |
| a félretevés árából hiányzik a jóslatvesztés | 56 | **téves premissza** (elemzéssel cáfolva) |
| a gondozott-forrás prior (v4.7) segít | 56–57 | **egy seeden igen; előregisztráltan nem tesztelődött (A), a C-ben árt** |
| a javított változat jobb a v3-nál (A ∪ B) | 57 | **igen**: +0,048 [+0,028; +0,068] |
| rivális elméleteknél (C) bármelyik egyszintű változat helyes gestalt-váltást végez | 57 | **nem: 0/150** |
| a kétszintű κ_T = 1 a C-ben | 57, feltáró | **122/150 helyes váltás, +0,22** |
| a hierarchikus π-becslés kiindulásfüggő | 58 | **nem**, de a fixpont rossz (a becslő felbontása miatt) |

**A javított változat (v4.4e) négy független seed-halmazból háromban jobb a v3-nál** (50. kör: +0,024 n.s.;
55.: +0,040; 57.: +0,057; az A ∪ B-ben +0,048 szignifikáns). Az 50. kör H50a-jának kudarca így inkább a
seed-halmaz véletlenje, mint a módszer hibája. **Ez a 44. kör óta az első kedvező, előregisztráltan is
igazolt általános eredmény.**

## 2. A sorozat legfontosabb tartalmi eredménye

**A rivális elméletek kezelése és az egyetlen, nagyjából helyes elmélet kezelése ugyanannak a paraméternek a két
végpontja.** Az 57. kör ugyanazon a generátoron mérte:

| populáció | kétszintű (κ_T = 1) − egyszintű |
|---|---|
| A (a tankönyv mindig nagyjából helyes) | **−0,047** |
| C (két rivális tankönyv, az egyik szemét) | **+0,206** |

Ez a Kuhn-féle paradigmaváltás és a „normál tudomány” közti feszültség egy mérhető, szimbolikus modellje. A
gestalt-váltás akkor helyes, ha a területen az elméletek gyakran egészében tévesek, és káros, ha ritkán. A
paraméter a terület alapgyakorisága, és az 52. és 58. kör szerint egy világból nem, sok világból is csak
korlátozottan tanulható.

## 3. Kritika

1. **A C populációt én terveztem, a diagnózis után.** Bár az adatai előtt rögzítettem, a felépítése (két
   tankönyv, az egyik véletlen előjelű) a TFB-9-et utánozza, és arra a gyengeségre irányul, amelyet már
   ismertem. **Az eredmény egy ismert jelenség megerősítése, nem egy új felfedezés.** Az, hogy egyik
   előregisztrált módszer sem kezelte, viszont valódi információ: a 48–56. kör javításai a rivális elméletek
   esetét rontották.
2. **A kontextus-mechanizmus a rivális elméletek általános menekülőútja** (57. kör, C). Két belsőleg
   konzisztens, egymásnak ellentmondó elméletet a legolcsóbb két külön világba tenni. A 17. kör óta tudjuk,
   hogy a „kontextus vagy hazug” adatból nem dönthető el. **A kontextus feltevését külső jelhez kellene kötni**
   (a 21. kör szerint ehhez kb. 0,95-ös pontosságú jel kell). Ez a B fázis LLM-jének legkonkrétabb feladata:
   felismerni, hogy egy forrás más helyről vagy időről szól, nem pedig tényeket kinyerni.
3. **A metrika:** a post-acc a „nem tudom” választ hibának számolja. Egy szemét elmélet helyes elvetése után a
   pontosság ezért alacsony marad (B: kb. 0,46), pedig a rendszer helyesen viselkedett. A Brier-pontszám vagy egy
   tartózkodás-érzékeny mérőszám ezt jobban mérné. A következő benchmarkoknál ezt is rögzíteni kell.
4. **Futási idő:** egy C-eset a kétszintű v4.4-gyel percekig tart, az „azonnali” átrendeződéstől ez messze van.

## 4. Divergens irányok

1. **Területi π, explicit forrás-metaadattal.** A forrás típusa (tankönyv, rivális iskola, szakértő, pletyka)
   és a „rivális iskolák” jelenléte deklarált bemenet, a q mintájára. A keverék-prior (48. kör) π-je ebből jön.
   Mérendő: A és C egyszerre jó-e ugyanazzal a kóddal, ha π a metaadatból jön (A: π = 0,999; C: π = 0,5).
2. **Kontextus csak jellel.** A kontextus-izolálás ára legyen végtelen, ha nincs külső kontextusjel, és
   −log₂(jel megbízhatósága), ha van. A 21. kör szimulált jelével (0,7; 0,9; 0,99) mérhető, hogy a C-ben eltűnik-e
   a „mindkettőt izolálom” menekülőút, és a „más régió” típusban megmarad-e a helyes izolálás.
3. **Tartózkodás-érzékeny értékelés:** Brier és „szelektív pontosság” (csak a megválaszolt kérdéseken) a post-acc
   mellett, minden következő előregisztrációban.

## 5. A következő körökre

- **60. kör:** a 4.1 és 4.2 együtt (metaadatból jövő π, jelhez kötött kontextus), előregisztrálva A, B és C
  populáción, friss seedeken, tartózkodás-érzékeny mérőszámokkal.
- **61. kör:** a 60. kör eredménye; ha működik, a 35. kör B fázis csomagjának átírása erre a két LLM-feladatra
  (forrástípus és kontextusjel), hogy a hálózati korlát feloldása után azonnal futtatható legyen.
- **64. kör:** divergens és kritikai kör.
