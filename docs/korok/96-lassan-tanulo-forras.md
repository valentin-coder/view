# 96. kör – Lassan tanuló bevált forrás a rögzített kód helyett (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 95. kör szerint a FROZEN_91 hibrid kódjának két oldala van. A bevált forrás *rögzített* kódja a G3-on véd a
bűnbak-képzéstől, a G4-en és a TFB-9-ben viszont árt, mert nem tanulja meg a tartósan rosszul kalibrált (a
deklaráltnál zajosabb) bevált forrást. A köztes megoldás: **a bevált adatforrás béta-kódot kap nagy κ-val (300)**,
szemét-komponens nélkül. Lassan tanul, ezért egy tartós eltérést (sok jelentésen át) megtanul, de egy rövid,
koncentrált félretevés-sorozat nem teszi bűnbakká. A κ = 300 a priori választás: a deklarált q kb. ±0,017 pontossággal
ismert. Kód: `core.py` (`rel_hybrid_kappa`), `v4.py` (`F91_DK`).

Fejlesztési adat (95. kör, TDκ, ahol a Tκ-rész hatástalan volt): G4 +0,01, TFB-9 +0,03, TFB-2 −0,2 (egyetlen futás).

### Elrendezés

- **Seedek:** 31000–31019 (friss). Esetek: G1k-A (hazug, átkategorizálás), G2 (hazug, torzított), G3 upd = 0,3 (hazug,
  állapotváltozás), G4 (hazug, jó új specialista, romló forrás). 180 eset × 3 módszer (v3, FROZEN_91, F91_DK) + a
  feladatcsomag (FROZEN_91, F91_DK).
- Kód: [`run_r96.py`](../../experiments/arlc/arlc/run_r96.py). Világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

- **H96a (G4, post):** F91_DK − FROZEN_91 > 0, a CI nem tartalmazza a nullát.
- **H96b (G1k, G2, G3 külön, post):** F91_DK − FROZEN_91 ≥ −0,01 (pontbecslés).
- **H96c (post):** F91_DK − v3 > 0, a CI nem tartalmazza a nullát, a G1k-n, a G2-n és a G3-on; a G4-en a pontbecslés > 0.
- **H96d (hazug-szerű célkérdések: hazug mind a négy generátoron + torzított):** F91_DK − FROZEN_91 ≥ −0,02 (pontbecslés).
- **H96e (feladatcsomag):** a TFB-9 pontossága a F91_DK-nál ≥ a FROZEN_91-énél, és egyetlen pontossági tétel sem rosszabb
  0,05-nél többel.

**Döntési szabály:** ha H96a, b, d és e teljesül, az F91_DK lesz az új befagyasztott konfiguráció (FROZEN_96).

## 2. rész: eredmények

Nyers adat: [`results/kor-96/`](../../experiments/arlc/results/kor-96/); elemzés: [`analyze_r96.py`](../../experiments/arlc/arlc/analyze_r96.py)
→ `results/kor-96/analysis.json`. 540 futás + feladatcsomag. A futás közben a konténer egyszer újraindult (a 95. kör alatt);
ez a futás megszakítás nélkül ment le.

| post-acc | G1k | G2 | G3 | G4 |
|---|---|---|---|---|
| v3 | 0,793 | 0,900 | 0,870 | **0,932** |
| FROZEN_91 | **0,878** | **0,929** | **0,928** | 0,927 |
| F91_DK | 0,877 | 0,922 | **0,928** | 0,929 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H96a (G4):** DK − F91 > 0 | +0,002 [−0,001; +0,005] | **nem teljesül** |
| **H96b:** DK − F91 ≥ −0,01 (G1k, G2, G3) | −0,001; −0,007; 0,000 | teljesül |
| **H96c:** DK − v3 > 0 (G1k, G2, G3); G4 pont > 0 | **+0,084; +0,022; +0,058** (mind szignifikáns); G4 −0,003 | **nem teljesül** (a G4-en) |
| **H96d (hazug-szerű target):** DK − F91 ≥ −0,02 | −0,010 [−0,019; −0,003] | teljesül (de a kis költség valódi) |
| **H96e (feladatcsomag):** TFB-9 ≥; semmi nem rosszabb 0,05-nél többel | TFB-9 0,813 vs. 0,783; **TFB-2 0,8 vs. 1,0** | **nem teljesül** |

### Értelmezés

1. **A döntési szabály szerint az F91_DK nem lesz alapértelmezés** (H96a és H96e nem teljesül). A FROZEN_91 marad.
2. **A lassan tanuló bevált forrás a G4-en nem segít** (+0,002). A 95. kör LOO-ja szerint a teljesen adaptív kód (κ = 30) a
   G4-en +0,02-t ad. A κ = 300 túl lassú ahhoz, hogy 30 jelentésből megtanulja az f4 0,65-ös megbízhatóságát. A κ
   csökkentése a G3-on a bűnbak-képzést hozná vissza. **A G4 és a G3 itt valódi ellentétet mutat, amelyet egyetlen κ nem
   old fel.** Ezt elfogadom korlátként.
3. **A FROZEN_91 v3-előnye a G1k-n, a G2-n és a G3-on friss seedeken megismétlődött** (post +0,085; +0,029; +0,058). A G4-en a v3
   most is egy hajszállal jobb (−0,005). A 93. kör eredménye (a G4-en nincs általános előny) tehát stabil.
