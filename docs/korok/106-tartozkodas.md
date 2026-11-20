# 106. kör – Tartózkodás a pontszám-különbség alapján (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 104. kör szerint a tárcsák (π_új, q_temper) a jó és a rossz új forrás, illetve az igaz és a zajos meglepetés között
választanak, és ahol a bizonyíték kevés, a választás elvileg bizonytalan (100. kör). **A tárcsa állítása helyett a rendszer
jelezheti a bizonytalanságot:** ha egy kérdésre két, egymásnak ellentmondó magyarázat pontszáma közel van, „nem tudom”-ot
mond. A 63. és 67. kör szerint a nyaláb nem poszterior-minta, ezért a gyakoriság helyett a **pontszám-különbséget**
használom.

### A szabály

Kód: [`run_r106.py`](../../experiments/arlc/arlc/run_r106.py). Egy (e, p) kérdésre a legjobb hipotézis válasza a₀. Ha a
nyalábban van olyan hipotézis, amely mást válaszol, és a pontszáma legfeljebb τ bittel rosszabb, a rendszer tartózkodik.
τ ∈ {1; 2; 4} bit, a priori: 2 bit ≈ 4:1 esély. Mérőszámok: lefedettség (megválaszolt arány), szelektív pontosság (a
megválaszoltakon), Brier (tartózkodás = ½). Összevetés: tartózkodás nélkül (τ = 0) és a nyaláb-átlagolt válasz
(50., 63. kör) Brier-je.

### Elrendezés

Seedek 36000–36011 (friss), a 96. kör 9 típusa a négy generátoron; FROZEN_91 és F91_Q. 216 futás.

### Hipotézisek (a post-kérdéseken, minden generátor együtt, seedenként átlagolva)

- **H106a:** τ = 2 mellett a szelektív pontosság nagyobb, mint τ = 0 mellett a pontosság, a CI nem tartalmazza a nullát
  (mindkét konfigurációra).
- **H106b:** τ = 2 mellett a lefedettség ≥ 0,9.
- **H106c:** τ = 2 mellett a Brier kisebb, mint τ = 0 mellett, a CI nem tartalmazza a nullát.
- **H106d:** τ = 2 mellett a Brier legfeljebb akkora, mint a nyaláb-átlagé (pontbecslés).
- **H106e (célkérdések):** τ = 2 mellett a célkérdések szelektív pontossága nagyobb, mint τ = 0 mellett (pontbecslés).

## 2. rész: eredmények

Nyers adat: [`results/kor-106/test/`](../../experiments/arlc/results/kor-106/test/); elemzés:
[`analyze_r106.py`](../../experiments/arlc/arlc/analyze_r106.py) → `results/kor-106/analysis.json`. 216 futás, eltérés nincs.

| FROZEN_91, post | τ = 0 | τ = 1 | τ = 2 | τ = 4 | nyaláb-átlag |
|---|---|---|---|---|---|
| lefedettség | 0,973 | 0,957 | 0,933 | 0,927 | – |
| szelektív pontosság | 0,934 | 0,938 | 0,943 | 0,945 | – |
| Brier | 0,073 | 0,072 | 0,073 | 0,071 | **0,070** |

F91_Q, post: szelektív pontosság 0,944 → 0,952 (τ = 2), lefedettség 0,980 → 0,935; Brier 0,060 → 0,061; nyaláb-átlag **0,057**.

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H106a:** szelektív pontosság (τ = 2) − (τ = 0) > 0 | FROZEN_91 **+0,008** [+0,006; +0,011]; F91_Q **+0,008** [+0,005; +0,011] | **teljesül** |
| **H106b:** lefedettség ≥ 0,9 | 0,933; 0,935 | **teljesül** |
| **H106c:** Brier (τ = 2) < (τ = 0) | −0,000 [−0,003; +0,002]; +0,001 [−0,002; +0,004] | **nem teljesül** |
| **H106d:** Brier (τ = 2) ≤ nyaláb-átlag | +0,003 [+0,001; +0,004]; +0,004 [+0,002; +0,006] | **nem teljesül** (a nyaláb-átlag jobb) |
| **H106e:** célkérdések szelektív pontossága nő | 0,872 → 0,881; 0,911 → 0,917 | **teljesül** |

### Értelmezés

1. **A pontszám-különbség informatív jel, de nem elég éles.** A τ = 2 mellett visszatartott válaszok (a kérdések kb. 4%-a)
   75%-ban helyesek lettek volna, szemben a megválaszoltak 94%-ával. A jel tehát a gyengébb válaszokat azonosítja,
   de nem a véletlen közelieket. Egy 75%-ban helyes válasz Brier-je (0,25) ugyanannyi, mint a tartózkodásé (0,25), ezért a
   Brier nem javul.
2. **A kalibrációhoz a nyaláb-átlag a jobb eszköz** (50., 63. kör): fokozatos valószínűséget ad, nem kemény
   tartózkodást. A tartózkodás akkor hasznos, ha az alkalmazás „nem tudom” választ kér (szelektív pontosság +0,8 pont,
   4%-os lefedettség-áron).
3. A 104. kör tárcsáit a tartózkodás **nem oldja fel:** a jó és a rossz új forrás közti döntésnél (98–100. kör) a két
   magyarázat pontszám-különbsége jellemzően nagyobb 2 bitnél. A rendszer ott magabiztosan dönt rosszul vagy jól, ahogy a
   prior diktálja.
