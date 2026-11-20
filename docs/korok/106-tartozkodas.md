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
