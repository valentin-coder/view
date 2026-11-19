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

## 2. rész: eredmények

Nyers adat: [`results/kor-90/test/`](../../experiments/arlc/results/kor-90/test/); elemzés:
[`analyze_r90.py`](../../experiments/arlc/arlc/analyze_r90.py) → `results/kor-90/analysis.json`. 560 futás, eltérés nincs.

### Post-acc (célkérdés-acc zárójelben)

| | G1k | G2 | G3 (upd = 0,3) |
|---|---|---|---|
| v3 | 0,829 (0,670) | 0,882 (0,735) | 0,856 (0,433) |
| η = 0 | 0,862 (0,732) | 0,937 (0,798) | 0,895 (0,458) |
| η = 0,5 | 0,873 (**0,784**) | **0,948** (0,946) | 0,865 (0,608) |
| η = 1 (befagyasztott) | 0,870 (0,766) | 0,945 (**0,946**) | **0,899** (**0,831**) |
| SB | **0,877** (0,769) | 0,943 (0,871) | 0,868 (0,659) |

Pre-acc a G3-on: v3 0,912; η = 0: **0,926**; η = 0,5: 0,920; η = 1: 0,866; SB: 0,916.

η-választás (esetszám): G1k: 0 → 4, 0,5 → 16, 1 → 20; G2: 0 → 16, 0,5 → 8, 1 → 16; G3: 0 → 15, 0,5 → 15, 1 → 30.

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H90a:** SB − max(v3, η = 1) ≥ −0,01 (post) | G1k +0,003; G2 −0,003; **G3 −0,039** [−0,108; −0,002] | **nem teljesül** (a G3-on) |
| **H90b:** forrás-célkérdések SB − v3 > 0 | **+0,183** [+0,141; +0,229] | **teljesül** |
| **H90c (G3, pre):** SB − (η = 1) > 0 | **+0,050** [+0,005; +0,133] | **teljesül** |
| **H90d (G1k ∪ G2, post):** SB − (η = 1) ≥ −0,01 | +0,003 [−0,002; +0,008] | **teljesül** |
| **H90e:** G3-on ≥ 50% η < 1; G1k, G2-n ≥ 50% η = 1 | G3: 50%; G1k: 50%; **G2: 40%** | **nem teljesül** (a G2-n) |

### Értelmezés

1. **A prequential η-választás rossz célt optimalizál.** A meglepetés előtti folyam előrejelzése a *háttérvilág*
   leírását méri. Ott a kis η jó (G3 pre: SB +0,050 az η = 1-hez). A meglepetés kezelése viszont, különösen egy új
   megbízhatatlan forrásé, a nagy η-tól függ (G3 target: η = 1 0,831, SB 0,659). **A két feladat különböző η-t kíván,
   és egyetlen globális η nem tudja mindkettőt.** A G2-n a választás közel véletlenszerű (H90e).
2. **Nem előregisztrált, de fontos megfigyelés:** az **η = 0** (a v4 szerkezete, *rögzített* megbízhatósági kóddal) a post-acc-ban
   **mindhárom generátoron a v3 fölött van:** G1k +0,033 [+0,016; +0,051], G2 +0,055 [+0,017; +0,120], G3 +0,039 [+0,007;
   +0,085]. **A v4 szerkezeti újításai (specifikusság, kivétel-prior, prioritás, tankönyv-keverék) tehát általánosak.** A
   harmadik generátoron mért kudarc (88. kör) az *adaptív megbízhatósági kódból* jött. Ez egybevág a 89. kör diagnózisával,
   de friss seedeken is meg kell erősíteni, mert nem ez volt a hipotézis.
3. **A két feladat szétválasztható:** a háttérforrásokra rögzített kód (az η = 0 erőssége), az új forrásokra adaptív kód (az
   η = 1 erőssége a hazug forrásnál). Ez a 86. kör „új forrás” gondolatának a megbízhatósági kódra kiterjesztett
   változata. A 91. kör ezt méri előregisztráltan.
