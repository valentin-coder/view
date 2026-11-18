# 50. kör – A javított változatok (v4.2–v4.5) értékelése, és a 44. kör bukásának gyökéroka

A 44. kör előregisztrált eredménye negatív (H44a és H44b nem teljesül, 44. kör 2. rész). A diagnózis
két mechanizmust talált: a teljes tankönyv félretevését (7/30 világ) és az összeomlást a meglepetés
után (post-acc = 0). Ez a kör megkeresi a gyökérokot, és méri a javított változatokat. **Minden itt
közölt benchmark-eredmény másodlagos és címkézett, nem előregisztrált.**

## 1. A változatok

| változat | tartalom | kör |
|---|---|---|
| v4 | befagyasztott (44. kör) | 43 |
| v4.2 | + az indukált/feltalált szabályok kivétele is árazott (3. hiba) | 45 |
| v4.3 | + q-csoportok, + szigorú specifikusság | 48 |
| v4.4 | + automatikus specifikusság | 49 |
| v4.4-egyszintű | v4.4, κ_T nélkül (az elméletek is κ_S = 30-at kapnak) | 50 |
| v4.5 | v4.4 + kontextuson belüli elsőbbség, árazott eltérésekkel | 50 (elvetve) |

## 2. Az ellenőrző csomag

| | E1 RR | E3 | A7 | TFB-9 pont. / vesztes fa | feltalálás | többi |
|---|---|---|---|---|---|---|
| v4 | 0,762 | 0,75 | 0,70 | 0,977 / 0,00 | 0,50 | = |
| v4.3 | 0,845 | 0,75 | 1,00 | 0,977 / 0,00 | 0,50 | = |
| **v4.4** | 0,845 | 0,75 | 1,00 | **0,977 / 0,00** | **1,00** | = |
| **v4.4-egyszintű** | **0,875** | 0,75 | 1,00 | **0,807 / 0,83** | 1,00 | = |
| v4.5-egyszintű | 0,875 | **0,50** | 1,00 | 0,807 / 0,83 | 1,00 | = |

Kimerítő ellenőrzés (36. kör): v4, v4.3 és v4.4 mindkét méreten 25/25. Az A fázis regressziója
(alapértelmezés) bitre azonos.

## 3. Az összeomlás gyökéroka

Két összeomlott eset (1016 hazug forrás, 1015 más régió), változatonként:

| | 1016 pre → post | 1016 végső hipotézis | 1015 pre → post | 1015 végső hipotézis |
|---|---|---|---|---|
| v4 | 0,79 → **0,00** | tankönyv mind elvetve; terep + hazug izolálva | 0,88 → **0,00** | tankönyv mind elvetve; terep + régió izolálva |
| v4 + kontextus-elsőbbség (árazatlan) | 0,68 → 0,68 | **a terep már a folyam közben izolálva** | 0,85 → 0,85 | ugyanígy |
| v4 + kontextus-elsőbbség (árazott eltérés) | 0,79 → 0,54 | tankönyv mind elvetve | 0,88 → **0,00** | mint a v4 |
| **v4.4-egyszintű** | **0,84 → 0,84** | 4 tankönyvi szabály + a hazug 8 tényéből 7 elvetve | **0,88 → 0,88** | 7 tankönyvi szabály + a régióforrás állításai elvetve |

**A gyökérok a 32. kör kétszintű hitelessége (κ_T = 1).** A teljes elmélet elvetése így kb. 10 bitbe kerül,
akár 48 szabályról van szó. Ha a tankönyv elesik, nincs örökölt szabály, és a kontextus-izolálásnak sincs
már ára, mert nincs mit felülírni. A kontextus-elsőbbség (lex specialis) ezen nem segít: árazatlanul új
kiskaput nyit (a terepforrás 6 bitért „más helyzetről szól”), árazottan nem hat. Az E3-on ront, ezért
elvetem.

## 4. A feszültség, és mi oldja fel

A κ_T = 1 nélkül az összeomlás eltűnik, de a **TFB-9 gestalt-váltása is**: a vesztes fa 83%-ban aktív
marad. Ugyanezt adta a 49. kör π = 0,999-es keveréke. A 48–50. kör minden kísérlete ugyanabba a falba
ütközik: **az elmélet egészének elvetési ára egyetlen szám, és két feladat ellentétes értéket kíván.**

**Feloldás (elvi):** a TFB-9-ben két rivális fa van, és konstrukció szerint az egyik téves. Ott egy elmélet
„szemét” prioresélye **50%**. A procedurális benchmarkon **0%**: a tankönyv mindig nagyjából helyes, 10%
hibával. **A κ_T = 1 egy olyan terület priorja, ahol az elméletek fele egészében téves, és ezt alkalmaztuk
egy olyan területen, ahol egyik sem az.** A 32. kör a TFB-9 alapján választotta, vagyis a saját
feladatunkra illesztett paraméter volt, és a független benchmark ezt kimutatta.

A helyes érték tehát területi tény, és a terület tapasztalatából kell jönnie: ez az 52. kör hierarchikus
priorja. Ha az 52. kör működik, egy TFB-szerű populációban (rivális elméletek) π̂ ≈ 0,5, a procedurálisban
π̂ ≈ 0,96, és a két viselkedés ugyanabból a mechanizmusból adódik.

## 5. Másodlagos benchmark-eredmények

*(a v4.4 és a v4.4-egyszintű futás befejezése után)*
