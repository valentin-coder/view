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
