# 78. kör – A kontextusfüggő indukció mint keresési menekülőút (előregisztrált)

## 1. rész: diagnózis és előregisztráció (a futtatás előtt commitolva)

### Diagnózis

A 77. kör feltáró ablációja szerint a második generátoron a kontextusfüggő indukció (21. kör) okozza a legnagyobb kárt
(−0,016). Négy seeden (15000–15003) megvizsgáltam: a 15003-asban indukcióval a rendszer **a tankönyvet és a
népszámlálást kontextusba izolálja**, és a pontosság 0,844-ről 0,688-ra esik. A végső hipotézisben nincs indukált
szabály. **Az indukció tehát a keresés útját változtatja meg:** az izolált kontextusban indukált szabályok életben
tartják az izoláló hipotéziseket a nyalábban, amíg azok nyernek. Ez ugyanaz a menekülőút (a félretevés izolálással),
mint az 57., 60. és 68. körben, most a keresési útvonalon keresztül.

### Javítás

`ctx_induction_sources`: kontextusfüggő indukció csak a jel által „más kontextusnak” jelzett forrás kontextusában (a 73. kör
mintájára). Jel nélkül nincs kontextusfüggő indukció.

### Elrendezés

Kód: [`run_r78.py`](../../experiments/arlc/arlc/run_r78.py). Seedek **16000–16019** (friss). Második generátor (G2):
hazug forrás, szabály-helyesbítés, torzított forrás. Első generátor (G1, A populáció): átkategorizálás, szabály-helyesbítés,
hazug forrás. 120 eset. Változatok: v4.4e (indukcióval); v4.4e − kontextusfüggő indukció; v4.4e jelzett indukcióval
(szimulált jel, a = 0,99; G2-ben nincs valódi „más kontextus”, így a jelzések csak téves riasztások).

### Hipotézisek

- **H78a (G2):** (v4.4e − ki) − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H78b (G1):** (v4.4e − ki) − v4.4e (post-acc) ≥ −0,01 (pontbecslés).
- **H78c (G2):** |jelzett indukció − indukció nélkül| < 0,01 (pontbecslés).

## 2. rész: eredmények

*(a futtatás után)*
