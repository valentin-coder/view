# 101. kör – Prior-érzékenységi protokoll a FROZEN_91-re (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 88. kör megmutatta, hogy egyetlen rosszul becsült séma-prior (a G3 változási priorja) mindent felborít. A 100. kör
szerint az új forrás π-je egy valódi tárcsa. A B fázisban ezeket a számokat egy LLM becsülné, ezért **tudni kell,
mennyire érzékeny rájuk a rendszer.** Ez a 99. kör 4.2. javaslata.

### Perturbációk (a FROZEN_91 körül, egyenként)

- **π_új** (az új forrás becsületes-súlya; alap 0,9): 0,8; 0,95; 0,99;
- **ε** (kivétel-prior; alap 0,05): ×½, ×2;
- **a deklarált hitelességek hibavalószínűsége** (1 − q): ×½, ×2, minden megfigyelésre (a rendszer a forrásokat
  szisztematikusan túl- vagy alulbecsüli);
- **a G3 változási priorja** (alap 0,3): ×½, ×2 (csak a G3-on).

Esetek: G1k (hazug, szabály-helyesbítés), G2 (hazug), G3 (hazug, állapotváltozás), G4 (hazug, jó specialista). Seedek
33000–33011 (friss). Kód: [`run_r101.py`](../../experiments/arlc/arlc/run_r101.py).

### Hipotézisek

„Robusztus” = a generátoronként átlagolt post-acc változása ≤ 0,02 (pontbecslés).

- **H101a:** ε × ½ és × 2 mellett robusztus, mind a négy generátoron.
- **H101b (tárcsa):** a hazug forrás célkérdés-pontossága (G1k ∪ G2 ∪ G3 ∪ G4) π_új növelésével nem nő (0,8 ≥ 0,9 ≥ 0,95 ≥ 0,99,
  0,01-es tűréssel). A szabály-helyesbítés és a jó specialista célkérdés-pontossága nem csökken (0,8 ≤ … ≤ 0,99, 0,01-es
  tűréssel).
- **H101c:** (1 − q) × ½ és × 2 mellett a post-acc változása ≤ 0,03, mind a négy generátoron.
- **H101d (G3):** a változási prior × ½ és × 2 mellett az állapotváltozás célkérdés-pontossága ≥ 0,8.

## 2. rész: eredmények

Nyers adat: [`results/kor-101/test/`](../../experiments/arlc/results/kor-101/test/); elemzés:
[`analyze_r101.py`](../../experiments/arlc/arlc/analyze_r101.py) → `results/kor-101/analysis.json`. 720 futás, eltérés nincs.

### A post-acc változása az alaphoz képest (alap: G1k 0,849; G2 0,928; G3 0,914; G4 0,914)

| perturbáció | G1k | G2 | G3 | G4 |
|---|---|---|---|---|
| π_új = 0,8 / 0,95 / 0,99 | 0,000 | ±0,001 | 0,000 | −0,001 – −0,002 |
| ε × ½ | 0,000 | +0,001 | −0,001 | −0,002 |
| **ε × 2** | −0,004 | **−0,030** | −0,018 | **−0,050** |
| **(1 − q) × ½** (túlzott magabiztosság) | −0,005 | **−0,061** | −0,021 | **−0,089** |
| **(1 − q) × 2** (óvatos hitelesség) | **+0,032** | **+0,015** | **+0,011** | **+0,031** |
| változási prior × ½ / × 2 | – | – | 0,000 | – |

Célkérdések (példák): a jó specialista 0,858 (alap) → 0,587 ((1 − q) × ½) → **0,950** ((1 − q) × 2); a G4 hazug forrás 0,927 →
0,823 → **0,958**.

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H101a:** ε × ½, × 2 robusztus (≤ 0,02) | × ½ igen; **× 2: G2 −0,030, G4 −0,050** | **nem teljesül** |
| **H101b:** a π_új tárcsa monoton | hazug: 0,896 ≥ 0,893 ≥ 0,888 ≥ 0,885; helyesbítés + specialista: 0,882 ≤ 0,895 ≤ 0,899 ≤ 0,903 | **teljesül** |
| **H101c:** (1 − q) × ½, × 2 mellett ≤ 0,03 | × ½: **−0,061, −0,089**; × 2: **+0,032** (G1k) | **nem teljesül** |
| **H101d (G3):** változási prior × ½, × 2 mellett az állapotváltozás ≥ 0,8 | 1,000 és 1,000 | **teljesül** |

### Értelmezés

1. **A π_új tárcsa monoton, de szűk** (±0,01). A 98. és a 100. kör „gyanús új forrás” költsége tehát nem elsősorban ezen
   múlik. 0,99-es π_új mellett is csak +0,008 a helyesbítés + specialista célkérdéseken.
2. **A rendszer legérzékenyebb pontja a deklarált hitelességek kalibrációja,** és az érzékenység aszimmetrikus. **A
   túlzott magabiztosság** (a források a valódinál megbízhatóbbnak mondják magukat) **súlyosan árt** (a G4-en −0,09). Az
   **óvatos hitelesség** (kétszeres hibavalószínűség) viszont **mind a négy generátoron javít** (+0,01 – +0,03), a forrás-
   célkérdéseken még jobban (G4 specialista +0,09). A B fázis szempontjából ez fontos: **egy LLM-becslésnél a hitelesség
   alulbecslése sokkal kevésbé veszélyes, mint a túlbecslése.**
3. **Az óvatos hitelesség a SafeBayes-gondolat egy alakja** (79., 90. kör): a megbízhatósági log-esélyek egyenletes
   csökkentése a likelihood temperálása. A 90. kör prequential η-ja rossz célt optimalizált, ez viszont egy egyszerű,
   rögzített temperálás. **De ezt most, ezeken a seedeken láttam, tehát feltáró eredmény.** A 102. kör előregisztráltan,
   friss seedeken méri.
4. **Az ε × 2 is árt** (a kivételek túl olcsók lesznek, és helyettesítik a forrás-félretevést). Az ε × ½ semleges. Az ε-ra
   is az óvatosabb (kisebb) érték a biztonságosabb.
