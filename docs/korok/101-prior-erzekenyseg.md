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
