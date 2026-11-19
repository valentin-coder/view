# 89. kör – Divergens és kritikai kör (13.): mi általános három generátor után

## 1. A 84–88. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 85 | a G1-hiba hatása | a hiba a v4-et jobban sújtotta; a G1k-n v4.9+PK − v3 = +0,073 |
| 86 | a forrástípus-prior metaadat nélkül | „új forrás” keverék: a hatás nagyja megmarad; a hatóanyag a szemét-komponens |
| 87 | generátor-egységteszt | G1: 3/70 megengedett; G1k, G2: 70/70; a G1k-n az igaz hipotézis 14–41 bittel drágább |
| 88 | befagyasztott konfiguráció egy harmadik generátoron | **általános pontosságban a v3 alatt** (−0,066); a forrás-felismerés felette (+0,14) |

## 2. A három generátor mérlege

| képesség | G1k | G2 | G3 | ítélet |
|---|---|---|---|---|
| hazug/torzított/elavult forrás felismerése | +0,06 – +0,15 | +0,07 – +0,10 | +0,14 | **általános** |
| általános pontosság a v3 fölött | +0,07 | +0,02 (csak PK-val) | **−0,07** (kalibrálva −0,03 pre) | **generátorfüggő** |
| rivális elméletek (metaadat-π) | +0,25 (G1-C) | – | – | egy generátoron |
| állapotváltozás (vágás) | – | – | kalibrált priorral +0,58 a v3-hoz | egy generátoron, kalibrálva |

**Négy kör (77, 81, 85, 88) után a mérleg:** a v4-család egyetlen általános képessége a megbízhatatlan forrás felismerése.
Az általános pontossági előny minden generátoron más okból jön vagy marad el: a G1k-n a specifikusság és a kivételek, a
G2-n a prioritás, a G3-on sehogy. **A „v4 általában jobb” állítást nem tartom fenn.**

## 3. A közös mechanizmus: adaptív kód félrespecifikált világban

A 77–88. kör minden kudarcának ugyanaz a szerkezete:

| hol | amit a modell rosszul áraz | a menekülőút | a forrás |
|---|---|---|---|
| G1 (44–84) | logikailag ellentmondásos világ | igaz alosztály elvágása | generátorhiba |
| G2 (78) | rejtett családprioritás | a tankönyv vagy a népszámlálás bűnbakká tétele | hiányzó primitív |
| G2 (82) | a fieldB közepes megbízhatatlansága | a fieldB igaz jelentéseinek félretevése | adaptív béta-kód |
| G1k (87) | a terepi tények rossz deklarált hitelessége | igaz tény félretevése valódi kivétel helyett | rossz kalibráció |
| G3 (88) | rossz változási prior | a terepforrás „szemét” módba tétele | adaptív keverék-kód |

**A v3 rögzített megbízhatósága ezekben robusztusabb**, mert egy forrás félretevésének ára nem csökken attól, hogy már sok
állítását félretettük. **A v4 adaptív kódja (béta, keverék) pont attól erős a hazug forrásnál, amitől gyenge a
félrespecifikált világban:** megengedi, hogy a hibák egy forrásba koncentrálódjanak. Ez az alkalmazkodóképesség és a
robusztusság ismert ellentéte. A forrás-megbízhatóság becslésénél (igazság-felderítés, „truth discovery”) is ismert, hogy
kevés állításnál és korrelált hibáknál az adaptív becslés instabil.

**Ez a sorozat legfontosabb módszertani eredménye:** az adaptív forrás-modell előnye a modell-specifikáció pontosságától
függ. Pontosan specifikált világban (hazug forrás egy egyébként jól leírt világban) nagy, félrespecifikáltban negatív.

## 4. Kritika a módszerről

1. **Három benchmark-hibát követtem el, és mindhárom a deklarált priorok és a világ közötti eltérés** (G1 diszjunktság,
   G1 terepi hitelesség, G3 változási prior). A 87. kör szabályát (igaz-hipotézis-ár) a 88. körben magam szegtem meg.
   **A szabály kötelező lépés lesz a generátor-kódban:** egy új generátor addig nem futhat, amíg a `gen_check` és az
   igaz-hipotézis-ár le nem futott.
2. **A rendszer érzékeny a séma priorjaira, és ezeket a valóságban egy LLM adná** (forrás-hitelesség, változási
   gyakoriság, diszjunktság). A 74. kör „két orákulum” kritikája szűk volt: a séma *minden* számszerű paramétere
   orákulum, és a 88. kör megmutatta, hogy egyetlen rossz prior (0,05 a 0,3 helyett) mindent felborít.
3. **A befagyasztás működött:** ez volt az első mérés, amelyet nem tudtam „megmenteni” egy újabb javítással. Az
   eredmény negatív, és pont ezért hiteles. A feltáró rész (upd = 0,3) magyaráz, de nem írja felül.

## 5. Divergens irányok

1. **Temperált megbízhatósági kód (SafeBayes, a 79. kör óta halasztva).** A pontszám a rögzített (v3) és az adaptív (v4)
   megbízhatósági kód keveréke η súllyal: η = 0 a v3, η = 1 a v4. A SafeBayes szerint η-t a **szekvenciális
   előrejelzési teljesítményből** kell választani (Grünwald). Itt ez a következő megfigyelés előrejelzése a korábbiak
   alapján. Ez metaadat nélkül, adatból dönti el, mennyire bízzon a rendszer az adaptív kódban. Ha a világ
   félrespecifikált, az előrejelzés romlik, és az η csökken. Ez a 3. rész ellentétének közvetlen, elvi kezelése.
2. **A séma-priorok tanulása vagy érzékenységvizsgálata:** minden mérés mellé egy ±2×-es prior-perturbáció (a 66. kör
   típuspontosság-szimulációjának párja), hogy látsszon, mennyire függ az eredmény egy-egy priortól.
3. **A szemét-komponens korlátozása** (a 88. kör eredménye alapján): tömeges „szemét” mód csak olyan forrásnak, amelynek
   állításai között nincs megerősített (más forrással egyező) állítás. A hazug forrás ilyen, a terepforrás nem.
4. **A szabályok időbeli vágása** (G3 szabályváltozás): a hipotézistér hiánya, de a 3. rész fényében előbb a robusztusság
   kell, csak utána újabb primitív.

## 6. A következő körökre

- **90. kör:** temperált megbízhatósági kód, prequential η-val (előregisztrált, G1k + G2 + G3 kalibrált, friss seedek).
- **91. kör:** a G3 meglepetés előtti lemaradásának diagnózisa (igaz-hipotézis-pontozással).
- **92. kör:** a szemét-komponens korlátozása megerősítetlen forrásokra.
- **94. kör:** divergens és kritikai kör.
