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

150 eset (A: 90, C: 60); nyers adat és elemzés: [`results/kor-75/`](../../experiments/arlc/results/kor-75/),
[`analyze_r75.py`](../../experiments/arlc/arlc/analyze_r75.py).

| | A post | A target | C post | C target | A ∪ C post | A ∪ C Brier |
|---|---|---|---|---|---|---|
| v3 | 0,741 | 0,482 | 0,370 | 0,116 | 0,592 | 0,140 |
| v4.4e | **0,825** | 0,634 | 0,387 | 0,307 | 0,650 | 0,123 |
| v4.8-π | 0,822 | 0,634 | 0,634 | 0,476 | 0,747 | 0,103 |
| **v4.8-π+jel** | **0,824** | **0,687** | **0,669** | **0,563** | **0,762** | 0,099 |
| v4.8-π+jel, nyaláb-átlag | – | – | – | – | – | **0,093** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H75a:** v4.8-π+jel − v3 (A ∪ C) > 0 | **+0,170** [+0,118; +0,227] | **teljesül** |
| **H75b:** v4.8-π+jel − v4.4e (A ∪ C) > 0 | **+0,112** [+0,057; +0,174] | **teljesül** |
| **H75c:** v4.8-π+jel − v4.4e (A) ≥ −0,01 | −0,0005 [−0,004; +0,003] | **teljesül** |
| **H75d:** Brier v3 − nyaláb-átlag (A ∪ C) > 0 | **+0,047** [+0,036; +0,059] | **teljesül** |

### Értelmezés

1. **A 44. kör óta ez az első előregisztrált mérés, ahol minden hipotézis teljesül.** A legjobb konfiguráció az A-ban
   (egyetlen, nagyjából helyes tankönyv) nem veszít, a C-ben (rivális tankönyvek) nagyot nyer. A célkérdéseken mindkét
   populációban a legjobb.
2. **A javulás forrásai külön is látszanak:** a metaadat-π a C-ben +0,25 (0,387 → 0,634); a kontextusjel és a jelzett
   elsőbbség további +0,035 a C-ben, és a célkérdéseken mindkét populációban kb. +0,05–0,09.
3. **Feltételek, amelyek nélkül ez nem érvényes:** a forrástípus (π) és a kontextusjel orákulum. A 66. kör szerint kb. 0,9-es
   típuspontosság, a 60. és 71–73. kör szerint kb. 0,99-es kontextusjel kell. **Ez nem a B fázis eredménye, hanem annak
   specifikációja:** ezeket a pontosságokat kellene egy LLM-nek hoznia.
4. A mérés a 44. kör generátorán történt, amelyre a konfigurációt hangoltam. A külső érvényesség próbája a 77. kör.
