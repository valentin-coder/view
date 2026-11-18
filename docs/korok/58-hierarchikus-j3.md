# 58. kör – Az 52. kör nyitott J3-ja: függ-e a hierarchikus becslés a kiindulástól?

Kód: [`hier.py`](../../experiments/arlc/arlc/hier.py); eredmény:
[`results/kor-52/A_pi090.json`, `A_pi0999.json`](../../experiments/arlc/results/kor-52/).

## Eredmény (A populáció, 24 tanító világ)

| π₀ | iterációk (π, szemétnek ítélt) | π̂ | teszt átlag (8 kis világ) | teszt félretevés |
|---|---|---|---|---|
| 0,9 | (0,9; 2), (0,885; 2) | **0,885** | 0,777 | 2 |
| 0,95 | (0,95; 2), (0,885; 2) | **0,885** | 0,777 | 2 |
| 0,999 | (0,999; **0**), (0,962; 2), (0,885; 2) | **0,885** | 0,777 | 2 |

## Ítélet

- **A J3 kudarc-feltétele nem teljesül:** a becslés mindhárom kiindulásból ugyanabba a fixpontba fut. Ebben az
  értelemben az eljárás azonosít.
- **A fixpont mégis rossz (0,885 a valódi kb. 1,0 helyett), és most már pontosan látszik, miért.** π = 0,999
  mellett a modell egyetlen tanító világban sem teszi félre a tankönyvet. A Laplace-becslő 24 világból azonban
  legfeljebb (24 + 1)/(24 + 2) = 0,962-t adhat. Ennél az értéknél két félretevés újra megjelenik, és a becslés
  visszaesik 0,885-re. **A valódi érték közelében lévő, önkonzisztens tartomány (π ≳ 0,99) a becslő felbontásán
  kívül esik.** Ez az 52. kör előzetes korlátjának (π̂ ≤ (n + 1)/(n + 2)) konkrét következménye: a ritkaságot
  nem lehet megtanulni, ha a minta túl kicsi ahhoz, hogy a ritkaság szintjét egyáltalán kifejezze.
- **Gyakorlati következmény:** a hierarchikus becslés vagy sokkal több világot igényel (kb. 100-at, hogy
  π̂ ≥ 0,99 kifejezhető legyen), vagy egy erősebb hiperpriort a π-re (például Beta(50, 1), ha a terület
  gondozott). Ez utóbbi viszont ugyanaz a területi tudás, amelyet a becsléssel ki akartunk váltani.
