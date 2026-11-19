# 90. kör – Temperált megbízhatósági kód prequential η-val (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 89. kör szerint a v4 adaptív megbízhatósági kódja (béta, keverék) pontosan specifikált világban erős (hazug forrás), de
félrespecifikált világban menekülőutat ad (bűnbak-forrás). A v3 rögzített kódja fordítva. **A SafeBayes-gondolat**
(Grünwald és van Ommen, 2017; 79. kör): a likelihood-részt egy η ≤ 1 tanulási rátával temperáljuk, és η-t a
**szekvenciális előrejelzési teljesítményből** választjuk. Félrespecifikált modellnél a nagy η rosszabbul jósol, és a
módszer kisebb η-t választ.

**Átcímkézés-ellenőrzés:** itt nem a teljes likelihoodot temperálom, hanem a megbízhatósági kódot keverem: η · (adaptív
kód) + (1 − η) · (rögzített kód). Ez a SafeBayes egy változata, nem maga a SafeBayes. A temperált poszterior helyett egy
kódkeveréket használok. Az η-választás (prequential veszteség) a SafeBayes-é.

### A rendszer

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`rel_temper`), [`run_r90.py`](../../experiments/arlc/arlc/run_r90.py).
- A befagyasztott konfiguráció (FROZEN_88) η ∈ {0; 0,5; 1} mellett. Az η = 1 bitre azonos a befagyasztottal (ellenőrizve).
- **Prequential veszteség:** a meglepetés előtti folyam minden tulajdonság-állítására a rendszer a megfigyelés *előtt*
  válaszol. Találat: −log₂ 0,9; „nem tudom”: 1 bit; ellentmondás: −log₂ 0,1. A veszteség ezek összege.
- **SB:** az az η, amelyiknél a prequential veszteség a legkisebb. **0,5 biten belüli holtversenynél a legnagyobb η**
  (a standard Bayeshez legközelebbi, ahogy a SafeBayesben). Az SB külön futás nélkül, a három η-futásból választ.

### Az igaz hipotézis ára a G3-on (a 89. kör szabálya szerint, a futtatás előtt)

Kód: [`gen_check.py`](../../experiments/arlc/arlc/gen_check.py) (`admissible(..., return_h=True)`). 23000–23003, hazug forrás,
meglepetés előtt: a G3 mindkét változási priorral megengedett. Az igaz hipotézis a befagyasztott konfiguráció szerint
**2–15 bittel** drágább a találtnál (közepes azonosíthatóság), a v3 szerint 19–64 bittel. A kalibrált prior (0,3) a
meglepetés előtti képen alig változtat.

### Elrendezés

- **Seedek:** 25000–25019 (friss). Esetek: G1k-A (hazug, átkategorizálás); G2 (hazug, torzított); G3, upd = 0,3
  (hazug, állapotváltozás, elavult). 140 eset × 4 futás (v3, η = 0; 0,5; 1).
- **Elemzés:** seedenként, generátoronként a típusokra átlagolva; világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

„Forrás-célkérdések”: a hazug forrás (mindhárom generátor), a torzított forrás (G2) és az elavult forrás (G3) célkérdései.

- **H90a (minden generátoron, post-acc):** SB − max(v3, η = 1) ≥ −0,01 (pontbecslés): az SB legalább olyan jó, mint a két
  végpont közül a jobbik.
- **H90b (forrás-célkérdések, mind a három generátor):** SB − v3 > 0, a CI nem tartalmazza a nullát.
- **H90c (G3, pre-acc):** SB − (η = 1) > 0, a CI nem tartalmazza a nullát (a temperálás javít ott, ahol az adaptív kód
  ártott).
- **H90d (G1k ∪ G2, post-acc):** SB − (η = 1) ≥ −0,01 (pontbecslés).
- **H90e (mechanizmus):** a G3-on az esetek legalább felében η < 1 a választás; a G1k-n és a G2-n az esetek legalább
  felében η = 1.

**Értelmezés előre:** ha H90a és H90b teljesül, a temperált kód feloldja a 89. kör ellentétét, és metaadat nélkül adja a
két végpont jobbikát. Ha H90e nem teljesül (a prequential veszteség nem választja szét a generátorokat), a módszer
mechanizmusa nem működik, még ha a pontosság véletlenül jó is.
