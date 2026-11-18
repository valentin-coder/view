# 57. kör – Kombinált benchmark (A + B populáció): előregisztráció

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 44. kör benchmarkja csak az egyik végpontot méri (a tankönyv sosem egészében téves), a TFB-9 a másikat (az
elméletek fele téves). A 49–52. kör szerint a gestalt-váltás és a téves félretevés ugyanaz a lépés, és a
helyes viselkedés a terület alapgyakoriságától függ. Egy jó rendszernek mindkét populáción jól kell
teljesítenie. Ez a kör a 44. kör generátorát egy B populációval egészíti ki, és a legújabb változatot is
méri.

### Elrendezés

- **Seedek:** 5000–5029 (friss), 5 meglepetéstípus, A és B populáció: 300 eset. Futtató:
  [`run_r57.py`](../../experiments/arlc/arlc/run_r57.py).
- **B:** seedenként 30% eséllyel egészében téves tankönyv (55. kör `make_case`). A sorsolás szerint 8 szemét
  seed: 5000, 5002, 5005, 5006, 5011, 5017, 5021, 5027.
- **Módszerek:**
  - v3;
  - v4.4e (v4.4-egyszintű, 50. kör);
  - **v4.7** = v4.4e + gondozott forrás (tankönyv, népszámlálás) kontextusa 10 bit (56. kör; a paramétert
    egyetlen seed diagnózisa után választottam, ezért itt *tesztelem*, nem igazolom);
  - feltáróan: H2(v3 + v4.7), az 55. kör kétsebességű szabálya.
- **Mérőszámok:** post-acc, target-acc, a tankönyv félretevése (≥ 90% elvetve vagy izolálva).

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H57a (A ∪ B, 60 világ):** v4.7 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H57b (A):** v4.7 − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát (a gondozott-forrás prior segít).
- **H57c (B):** v4.7 − v3 (post-acc) > 0, a CI nem tartalmazza a nullát. A v3 rögzített megbízhatósággal
  nem tud egy szemét tankönyvtől megszabadulni.
- **H57d (félretevés):** a *jó* tankönyves világokban (A, plusz a B nem szemét seedjei) a v4.7 kevesebbszer
  teszi félre a tankönyvet, mint a v4.4e. A *szemét* tankönyves világokban a v4.7 az esetek legalább felében
  félreteszi.

**Kudarc-feltétel:** ha H57b nem teljesül, a gondozott-forrás prior a 3024-es seedre illesztett hatás volt.
Ha H57c nem teljesül, a v4.7 a szemét tankönyvet sem tudja jobban kezelni, mint a v3.

## 2. rész: eredmények

*(a futtatás után)*
