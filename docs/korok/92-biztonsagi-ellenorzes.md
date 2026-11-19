# 92. kör – A FROZEN_91 biztonsági ellenőrzése a régi feladatokon (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 91. kör szerint a hibrid+V (FROZEN_91) mindhárom generátoron a v3 fölött van. A hibrid megbízhatósági kód és az
eseményenkénti vágásár viszont olyan helyeken is változtat, amelyeket a 91. kör nem mért:
- a **szemét-tankönyv** (G1k-B) és a **rivális elméletek** (G1k-C) esetén a tankönyv a „bevált” forrás. A hibrid kód az
  adat-részét rögzítve kezeli, az elmélet-részét a keverékkel;
- a korai körök feladatai (E1–E4, A7, TFB, Quine, feltalálás) a v4.battery csomagban.

### Elrendezés

Kód: [`run_r92.py`](../../experiments/arlc/arlc/run_r92.py).
1. **Feladatcsomag:** v4.4e, FROZEN_88, FROZEN_91.
2. **G1k-B és G1k-C, hazug forrás,** friss seedek 27000–27019 (a B-ben a 27004, 27005, 27008, 27011 szemét-tankönyves).
   Módszerek: v3, FROZEN_88, FROZEN_91.

### Hipotézisek

- **H92a (feladatcsomag):** a FROZEN_91 egyetlen pontossági tétele sem rosszabb 0,05-nél többel a FROZEN_88-énál. A logikai
  tételek (E2a monoton, Quine „G sosem esik”) változatlanok. Az E4 hamis átrendezések száma nem nő.
- **H92b (G1k-B, post-acc):** FROZEN_91 − FROZEN_88 ≥ −0,02 (pontbecslés). A szemét-tankönyves seedeken külön is
  ≥ −0,05.
- **H92c (G1k-C, post-acc):** FROZEN_91 − FROZEN_88 ≥ −0,02 (pontbecslés).
- **H92d (hazug forrás target, B ∪ C):** FROZEN_91 − v3 > 0, a CI nem tartalmazza a nullát.

Ha valamelyik nem teljesül, a FROZEN_91 nem lesz alapértelmezés, amíg a hiba okát nem tárom fel.

## 2. rész: eredmények

Nyers adat: [`results/kor-92/`](../../experiments/arlc/results/kor-92/); elemzés:
[`analyze_r92.py`](../../experiments/arlc/arlc/analyze_r92.py) → `results/kor-92/analysis.json`.

### Feladatcsomag

| tétel | v4.4e | FROZEN_88 | FROZEN_91 |
|---|---|---|---|
| E1 RR (átkategorizálás + alosztály) | **0,875** | **0,000** | 0,750 |
| E1 kollaterális | 0 | 0 | 0 |
| E2a átfordulás N = 2/8/16, monoton | 2/4/6, igen | 2/4/6, igen | 2/4/6, igen |
| E3 helyes döntés | 0,75 | 0,50 | 0,75 |
| E4 pontosság (ε = 0,05) | 0,938 | 0,938 | **0,972** |
| E4 hamis átrendezés / 50 | 0 | 0 | 0 |
| A7 (frissítés/revízió) | 1,0 | 1,0 | 1,0 |
| TFB-9 pontosság (zaj 0,15) | 0,807 | **0,843** | 0,783 |
| TFB-2 / TFB-8 | 0,8 / 1,0 | 0,8 / 1,0 | **1,0** / 1,0 |
| Quine: G sosem esik; feltalálás | igen; 1,0 | igen; 1,0 | igen; 1,0 |

### G1k-B és G1k-C, hazug forrás (27000–27019)

| | B post | B target | B-szemét post | C post | C target |
|---|---|---|---|---|---|
| v3 | 0,602 | 0,463 | 0,000 | 0,074 | 0,000 |
| FROZEN_88 | 0,825 | 0,819 | 0,584 | **0,788** | 0,806 |
| FROZEN_91 | **0,831** | **0,856** | **0,590** | 0,784 | **0,813** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H92a (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel; logikai tételek változatlanok; E4 nem nő | TFB-9: **−0,060**; a többi egyenlő vagy jobb | **nem teljesül** (egy tételen) |
| **H92b (B):** F91 − F88 ≥ −0,02; szemét-seedeken ≥ −0,05 | +0,006 [−0,007; +0,020]; +0,005 | **teljesül** |
| **H92c (C):** F91 − F88 ≥ −0,02 | −0,004 [−0,012; +0,004] | **teljesül** |
| **H92d (hazug target, B ∪ C):** F91 − v3 > 0 | **+0,603** [+0,506; +0,694] | **teljesül** |

### A H92a kudarcának oka (a döntési szabály szerint feltárva)

A TFB-9 hat futásából egyetlen világ (seed 0) adja a különbséget: L-igazságnál a FROZEN_91 a helyes fát teljesen
kikapcsolja (pontosság 0,393 vs. 0,607), H-igazságnál 0,857 vs. 1,000. A TFB-9-ben a terepi tények valódi zaja 0,15, a
deklarált 0,10. **A hibrid kód a bevált terepforrást rögzített 0,9-es megbízhatósággal árazza,** ezért egy zajos tény
félretevését túlárazza, és a rivális fák közötti döntésben inkább szabályokat tesz félre. Az adaptív kód (FROZEN_88) ezt
a világot azért kezeli jobban, mert megtanulja a valódi 0,85-öt.

**Ez az adaptivitás–robusztusság ellentét (89. kör) másik oldala:** a rögzített kód a deklaráltnál zajosabb, de
egyébként jól leírt forrásnál téved. A G2 fieldB-je (valódi 0,8, deklarált 0,9) ugyanilyen eset volt, ott a 91. kör szerint a
hibrid nem vesztett. Itt a rivális elméletek közti döntés miatt érzékenyebb. **A korlát ismert és szűk** (egy világ hat
futásból). A FROZEN_91 ezzel a dokumentált korláttal alapértelmezés.

### További megfigyelések

1. **A FROZEN_88 az E1 alapfeladatot (átkategorizálás) teljesen elrontotta** (0,000), és ezt a 88. kori befagyasztás előtt
   nem mértem. Az „új forrás” gyanú a helyes átkategorizáló szakértőt félreteszi. **A 88. kör előtt a régi feladatcsomag
   futtatása elmaradt. Mostantól ez is a befagyasztás előfeltétele.** A FROZEN_91 ezt részben helyrehozza (0,750; v4.4e:
   0,875), mert a bevált háttér rögzített kódja mellett a szakértő állítása olcsóbban elfogadható.
2. **A v3 a rivális elméleteknél teljesen összeomlik** (C post 0,074; a szemét-tankönyves B-ben 0,000). A tankönyv-π és a
   hazug forrás kezelése együtt itt +0,60-at ad.

### Javaslat (a 95. körre)

A rögzített és az adaptív kód közötti köztes megoldás a **lassan tanuló bevált forrás:** κ = 300-as béta-prior a deklarált q
körül a rögzített kód helyett. Ez megtanulja a tartósan rosszul kalibrált forrást (TFB-9, fieldB), de nem enged gyors
bűnbak-képzést.
