# 63. kör – Bizonytalanságot jelző válasz: nyaláb-átlagolás a v4.8-π-ben

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 62. kör szerint a „más régió” meglepetés egy 0,04–0,43 bites holtverseny két magyarázat között, és a MAP-válasz
ilyenkor önkényes. Egy hiedelemrendszer helyes viselkedése ilyenkor a bizonytalanság jelzése. Az 50. kör H50c-je
a v4.4e-ben kicsi, de stabil Brier-javulást mért a nyaláb poszterior-súlyú átlagával (w_H ∝ 2^(−L)). Ez a kör azt
méri, hogy a v4.8-π-ben (metaadat-π, jel nélkül, a 60. kör túlélő része) a holtversenyes típusokban
megjelenik-e a bizonytalanság, és javul-e a Brier.

### Elrendezés

- Seedek **7000–7014** (friss), 5 típus, **A és C** populáció: 150 eset. Kód:
  [`run_r63.py`](../../experiments/arlc/arlc/run_r63.py).
- Esetenként egy futás (v4.8-π); a MAP és az átlag ugyanabból a nyalábból (8 hipotézis).
- Mérőszámok: Brier (MAP: „nem tudom” = ½), pontosság, a célkérdések közül azok aránya, ahol az átlagolt
  valószínűség 0,2 és 0,8 közé esik („bizonytalan”).

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H63a:** a „más régió” és „hazug forrás” típus célkérdésein a nyaláb-átlag Brier-pontszáma kisebb a MAP-énál
  (A ∪ C, a CI nem tartalmazza a nullát).
- **H63b:** az összes kérdésen (post) ugyanez (a H50c ismétlése a v4.8-π-ben).
- **H63c:** a „más régió” célkérdéseinek legalább 20%-ában az átlag „bizonytalan” (0,2 < p < 0,8). Ha nem, a
  8 hipotézises nyaláb nem tartalmazza a holtverseny mindkét oldalát, és az átlagolás ebben a formában nem jelez
  bizonytalanságot.

## 2. rész: eredmények

150 eset (A és C, 75–75); elemzés: [`analyze_r63.py`](../../experiments/arlc/arlc/analyze_r63.py) →
[`results/kor-63/analysis.json`](../../experiments/arlc/results/kor-63/analysis.json).

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H63a:** Brier, MAP − átlag (más régió + hazug forrás, célkérdések) > 0 | **+0,049** [+0,021; +0,080] | **teljesül** |
| **H63b:** Brier, MAP − átlag (összes kérdés) > 0 | **+0,006** [+0,004; +0,010] | **teljesül** (a H50c ismétlése) |
| **H63c:** a „más régió” célkérdéseinek ≥ 20%-a bizonytalan | **23%** | **épphogy teljesül** |

Típusonként (célkérdések):

| típus | pontosság MAP → átlag | Brier MAP → átlag | bizonytalan arány | nyaláb-szórás (bit) |
|---|---|---|---|---|
| átkategorizálás | 0,606 → 0,718 | 0,252 → 0,235 | 19% | 3,2 |
| szabály-helyesbítés | 0,840 → 0,866 | 0,113 → 0,102 | 12% | 3,9 |
| kivételes alfaj | 0,763 → 0,839 | 0,073 → 0,072 | 23% | 4,9 |
| hazug forrás | 0,713 → 0,754 | 0,238 → 0,222 | 12% | 2,0 |
| **más régió** | 0,411 → 0,438 | **0,564 → 0,481** | 23% | 3,5 |

### Értelmezés

1. **A nyaláb-átlagolás minden típusban javít a Brier-pontszámon**, a holtversenyes típusokban a legjobban.
   Ez a 49. és 50. kör javaslatának harmadik független megerősítése.
2. **Kényelmetlen részlet:** a „más régió” célkérdésein a Brier-pontszám az átlaggal is **0,48**, rosszabb, mint
   a mindenre „nem tudom” válasz 0,25-je. A rendszer itt *magabiztosan téved*. A 8 hipotézises nyaláb a
   holtverseny mindkét oldalát csak az esetek kis részében tartalmazza (23% bizonytalan célkérdés). A többiben az
   egész nyaláb ugyanazon az oldalon van. **A nyaláb nem poszterior-minta, hanem a keresés útjának lenyomata.**
   A valódi bizonytalanság jelzéséhez a nyalábnak szándékosan diverznek kellene lennie, például a két legjobb,
   egymásnak ellentmondó magyarázatot mindig meg kellene tartania.
3. **A pontosság-nyereség** (például átkategorizálásnál 0,61 → 0,72) a 50. kör szerint részben a tartózkodások
   tippé alakításából jön. A Brier-javulás a megbízható mérőszám.
