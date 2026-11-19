# 95. kör – Konszolidáció: egyet-elhagyó abláció a FROZEN_91-ből négy generátoron (feltáró)

## 1. Az eredeti terv, és miért változott

A 94. kör a 95. körre egy előregisztrált tesztet tervezett: lassan tanuló becsületes komponens (κ₁ = 300) az
elmélet-keverékben (Tκ) és a bevált adatforrásokra (Dκ). Kód: `core.py` (`rel_hybrid_kappa`), `v4.py` (`F91_TK`,
`F91_TDK`); kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

**Fejlesztési ellenőrzés** ([`dev_r95.py`](../../experiments/arlc/arlc/dev_r95.py); G4: 28000–28005, G1k-C: 16000–16001;
nem teszt):

| | G4 pre / post / target | G1k-C pre / post / target | E1 | TFB-9 | TFB-2 |
|---|---|---|---|---|---|
| FROZEN_91 | 0,907 / 0,907 / 0,958 | 0,784 / 0,766 / 0,688 | 0,75 | 0,783 | 1,0 |
| + Tκ | **azonos** | **azonos** | 0,75 | 0,783 | 1,0 |
| + TDκ | 0,917 / 0,917 / 0,979 | azonos | 0,75 | 0,813 | **0,8** |

**A Tκ semmit nem változtat,** ezért a 93. kör diagnózisát (az elmélet-keverék adaptív komponense okozza a G4-beli
tankönyv-félretevést) visszavontam (93. kör, 3. rész). A TDκ kicsi, vegyes hatást mutat (G4 +0,01, TFB-9 +0,03, TFB-2
−0,2). **Ez túl gyenge alap egy előregisztrált teszthez.** Ezért a kör konszolidációs és diagnosztikai kör lett (a 94. kör
4.2. pontja): egyet-elhagyó abláció a FROZEN_91-ből, fejlesztési seedeken. Ez megmutatja, mi okozza a G4-beli
lemaradást, és melyik kapcsoló nem számít sehol.

## 2. Elrendezés

Kód: [`loo_r95.py`](../../experiments/arlc/arlc/loo_r95.py). Fejlesztési seedek (mind korábban már felhasznált): G1k-A hazug
(16000–16004), G2 hazug (16000–16004), G3 hazug és állapotváltozás (23000–23004, upd = 0,3), G4 hazug (28000–28004).
16 változat: v3, FROZEN_91 és 14 egyenként kikapcsolt komponens.

## 3. Eredmények

*(a futtatás után)*
