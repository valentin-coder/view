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

*(a futtatás után)*
