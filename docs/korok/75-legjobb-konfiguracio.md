# 75. kör – A legjobb konfiguráció nagy, előregisztrált összevetése

## 1. rész: előregisztráció (a futtatás előtt commitolva)

A 74. kör összefoglalta a jelenlegi legjobb konfigurációt. Ez a kör egyetlen, nagyobb, előregisztrált méréssel veti össze
a korábbi változatokkal, friss seedeken.

Kód: [`run_r75.py`](../../experiments/arlc/arlc/run_r75.py).
- **Populációk és seedek:** A (14000–14029, 30 seed) és C (14000–14019, 20 seed). Típusok: átkategorizálás, hazug forrás,
  más régió (a C futási ideje miatt nem mind az öt). Összesen 150 eset.
- **Módszerek:** v3; v4.4e; v4.8-π (metaadat-π); **v4.8-π+jel** (+ kontextusjel a = 0,99, jelzett elsőbbség). A legjobbnál a
  nyaláb-átlagolt Brier is.
- **Mérőszámok:** post-acc, target-acc, Brier (MAP: „nem tudom” = ½).

**Hipotézisek** (95%, világok szerinti klaszteres bootstrap):
- **H75a (A ∪ C):** v4.8-π+jel − v3 (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H75b (A ∪ C):** v4.8-π+jel − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H75c (A):** v4.8-π+jel − v4.4e (post-acc) ≥ −0,01 (pontbecslés): az A-ban nincs veszteség.
- **H75d (A ∪ C):** a v4.8-π+jel nyaláb-átlagolt Brier-pontszáma kisebb a v3 MAP-Brier-pontszámánál (CI nem tartalmazza a nullát).

## 2. rész: eredmények

*(a futtatás után)*
