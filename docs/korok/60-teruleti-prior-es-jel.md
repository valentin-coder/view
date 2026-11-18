# 60. kör – Területi π metaadatból és külső jelhez kötött kontextus

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

Az 57. és 59. kör szerint a gestalt-váltás és a stabilitás egy területi paraméter (π: mennyire valószínű,
hogy egy elmélet nagyjából helyes) két végpontja. A rivális elméletek esetének általános menekülőútja a
kontextus-izolálás, amely jel nélkül adatból nem dönthető el (17. kör). A 59. kör javaslata: **a π a forrás
metaadatából jöjjön, a kontextus pedig csak külső jel alapján legyen olcsó.** Mindkettő olyan információ,
amelyet a B fázisban az LLM adhatna (forrástípus, „ez a szöveg máshol vagy máskor játszódik”). Itt
szimulált jelekkel mérem, mit érne.

### A rendszer (v4.8)

Kód: [`run_r60.py`](../../experiments/arlc/arlc/run_r60.py), [`core.py`](../../experiments/arlc/arlc/core.py)
(`theory_pi`).
- **v4.4e** + keverék-prior az elméletekre (48. kör; κ₁ = 30, q₀ = 0,5, κ₀ = 2, nem kalibrált: a deklarált q
  az „ép elmélet” feltételes megbízhatósága), **forrásonkénti π a populáció metaadatából:** A: tankönyv
  0,999; B: tankönyv 0,7; C: mindkét tankönyv 0,5.
- **Kontextusár szimulált külső jelből:** a jel a „más régió” típus régióforrását a = 0,9 valószínűséggel
  jelzi „más kontextusnak”, minden más forrást 1 − a valószínűséggel (téves riasztás). Az ár
  −log₂ P(más kontextus | jel), ρ = 1/64 priorral: jelzett forrásra 3,0 bit, jelzetlenre 9,1 bit. (A v4.4e-ben
  minden forrásra 6 bit.)

### Elrendezés

- **Seedek:** 6000–6019 (friss), 5 típus, A, B, C populáció (55. kör `make_case`): 300 eset.
- **Módszerek:** v3, v4.4e, v4.8.
- **Mérőszámok:** post-acc, target-acc, **Brier** („nem tudom” = ½), **lefedettség** (megválaszolt arány),
  **szelektív pontosság** (csak a megválaszoltakon), félretevés tankönyvenként.

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H60a (A):** v4.8 − v4.4e (post-acc) ≥ −0,01 pontbecslésben, és v4.8 − v3 > 0 (CI nem tartalmazza a nullát).
- **H60b (C):** v4.8 − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát; és a v4.8 az esetek legalább
  felében helyes gestalt-váltást végez (a szemét tankönyv félretéve, a jó nem).
- **H60c (B):** v4.8 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H60d (más régió, A ∪ B ∪ C):** a v4.8 target-acc-ja legfeljebb 0,02-vel marad el a v4.4e-étől.
- **H60e (mindhárom populáció):** a v4.8 Brier-pontszáma kisebb a v4.4e-énél (CI nem tartalmazza a nullát).

**Kudarc-feltétel:** ha H60b teljesül, de H60a nem, a metaadatból jövő π a C-ben segít, az A-ban árt. Ha H60b
nem teljesül, a keverék-prior π = 0,5-tel sem ad gestalt-váltást, és a 57. kör κ_T = 1-es eredménye másból
(a U alakú prior farmolásából) jött.

## 2. rész: eredmények

Nyers adat: [`results/kor-60/`](../../experiments/arlc/results/kor-60/); elemzés:
[`analyze_r60.py`](../../experiments/arlc/arlc/analyze_r60.py) → `analysis.json`. Eltérés: a konténer kétszer
újraindult a C futás alatt, a futtató mindkétszer folytatta. Az esetek determinisztikusak.

### C populáció (két rivális tankönyv, 100 eset)

| | post-acc | target-acc | Brier | lefedettség | szelektív pontosság | helyes gestalt-váltás |
|---|---|---|---|---|---|---|
| v3 | 0,434 | 0,336 | 0,163 | 0,462 | 0,939 | 0/100 |
| v4.4e | 0,410 | 0,429 | 0,166 | 0,435 | 0,943 | 0/100 |
| **v4.8** | **0,657** | **0,566** | **0,122** | **0,705** | 0,933 | **67/100** |

**H60b teljesül:** v4.8 − v4.4e = **+0,247** [+0,173; +0,323], és a helyes gestalt-váltás aránya 67% (≥ 50%).

A v4.8 ugyanazzal a kóddal, csak a metaadatból jövő π = 0,5-tel, nagyjából ugyanazt hozza, amit az 57. körben
a kétszintű κ_T = 1 (0,660, 122/150). **A szelektív pontosság mindhárom módszernél 0,93–0,94:** a különbség
nem abban van, hogy a megválaszolt kérdésekre mennyire jól felel a rendszer, hanem abban, hogy mennyi kérdésre
felel egyáltalán (lefedettség 0,44 → 0,71). A v3 és a v4.4e a rivális tankönyveket egyaránt félreteszi, ezért
a kérdések felére nincs válasza.

### A és B populáció (100–100 eset)

| | A post | A target | A Brier | B post | B target | B Brier |
|---|---|---|---|---|---|---|
| v3 | 0,778 | 0,561 | 0,104 | 0,665 | 0,478 | 0,124 |
| v4.4e | **0,783** | **0,655** | **0,102** | 0,668 | **0,575** | 0,123 |
| v4.8 | 0,781 | 0,606 | 0,104 | **0,689** | 0,557 | **0,119** |

### A hipotézisek

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H60a (A):** v4.8 − v4.4e ≥ −0,01; v4.8 − v3 > 0 | −0,003 [−0,012; +0,008]; +0,003 [−0,032; +0,031] | **első fele teljesül** (nincs veszteség); **második nem** (ezeken a seedeken a v4.4e − v3 is csak +0,005) |
| **H60b (C):** v4.8 − v4.4e > 0; ≥ 50% helyes váltás | **+0,247** [+0,174; +0,320]; **67/100** | **teljesül** |
| **H60c (B):** v4.8 − v3 > 0 | +0,025 [−0,015; +0,058] | **nem teljesül** (irányában igen) |
| **H60d (más régió):** v4.8 target ≥ v4.4e target − 0,02 | **−0,276** [−0,380; −0,172] | **nem teljesül, súlyosan** |
| **H60e:** Brier v4.8 < v4.4e (összes) | +0,016 [+0,009; +0,023] | **teljesül** |

### Értelmezés

1. **A fő cél teljesült: a metaadatból jövő π a C-ben gestalt-váltást ad, az A-ban nem árt.** A 44–57. kör
   feszültségét (κ_T = 1 a C-ben +0,21, az A-ban −0,05) a forrásonkénti π **egyetlen kóddal** feloldja: a C-ben
   +0,247, az A-ban −0,003. **Ez a sorozat első olyan eredménye, ahol ugyanaz a rendszer mindkét végponton jól
   viselkedik**, mert a területi tudás (π) kívülről jön, nem a saját döntéseiből.
2. **A jelhez kötött kontextus (a = 0,9) a „más régió” típusban súlyosan árt.** Két mechanizmust láttam:
   - **téves riasztás kihasználása:** a jel forrásonként 10% eséllyel tévesen „más kontextust” jelez, például a
     terepforrásra. Ekkor a rendszer 3 bitért a 90 terepi tényt is izolálja (6007, 6015). Ez a modell szerint
     koherens, mert a jel pontosságát helyesen árazza. **A 21. kör követelménye (kb. 0,95-ös jel) itt
     igazolódik: 0,9-es jellel a kontextus-mechanizmus több kárt okoz, mint hasznot;**
   - **a régióforrás elfogadása:** több esetben (6005, 6012, 6019) a v4.8 izolálás nélkül elfogadja a
     régióforrás állításait, és helyettük tankönyvi szabályokat vet el. A v4.4e a régióforrást veti el. Az árak
     itt 1–2 biten belül vannak. Valószínű ok a kétszintű csoportosítás (a régióforrás szabálya és tényei külön
     csoportban), de egyetlen tagra nem tudtam visszavezetni. **Nyitott.**
3. **A Brier-pontszám összességében javul** (H60e), főleg a C-beli nagyobb lefedettség miatt.

### Következmény

- A π metaadatból: **megtartandó** (v4.8 π-része).
- A jelhez kötött kontextus a = 0,9-cel: **elvetendő** ebben a formában. Megvizsgálandó a = 0,99-cel, illetve a
  forrás méretével skálázott árral (egy téves riasztás ne tehessen félre 90 tényt egy jel alapján).
- A 62. kör ezt bontja szét: v4.8 jel nélkül (csak π), és v4.8 a = 0,99-cel, a „más régió” eseteken.
