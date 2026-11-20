# 102. kör – Óvatos hitelesség: rögzített temperálás (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 101. kör feltáró eredménye: ha minden megfigyelés deklarált hibavalószínűségét megduplázzuk ((1 − q) × 2), a FROZEN_91
mind a négy generátoron javul (+0,01 – +0,03), a forrás-célkérdéseken még jobban. Ez a SafeBayes-gondolat (79., 90. kör)
egyszerű alakja: a megbízhatósági log-esélyek rögzített temperálása, prequential választás nélkül. **Ezt ugyanazokon a
seedeken láttam, amelyeken a hipotézist megfogalmaztam, ezért itt friss seedeken mérem.** A v3-on is mérem, hogy kiderüljön:
a hatás a FROZEN_91-é, vagy általános.

Kód: `core.py` (`q_temper`, a megfigyeléskor alkalmazva), `v4.py` (`F91_Q`). 1,0-nál bitre azonos (ekvivalencia: EGYEZIK).
A szorzó (2) a 101. kör egyetlen kipróbált értéke. Nem hangolom tovább.

### Elrendezés

- **Seedek:** 34000–34014 (friss). Esetek, mint a 96. körben (9 típus a négy generátoron). 135 eset × 4 módszer: v3, v3 + Q,
  FROZEN_91, F91 + Q. Feladatcsomag: FROZEN_91, F91 + Q.
- Kód: [`run_r102.py`](../../experiments/arlc/arlc/run_r102.py). Világok szerinti klaszteres bootstrap.

### Hipotézisek

- **H102a (post):** (F91 + Q) − FROZEN_91 > 0, a CI nem tartalmazza a nullát, legalább három generátoron, a negyediken ≥ −0,01
  (pontbecslés).
- **H102b (forrás-célkérdések: hazug a négy generátoron, torzított, jó specialista):** (F91 + Q) − FROZEN_91 ≥ 0 (pontbecslés).
- **H102c (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel a FROZEN_91-énél.
- **H102d (G4, post):** (F91 + Q) − v3 > 0, a CI nem tartalmazza a nullát.
- **H102e (általánosság, leíró jóslat):** (v3 + Q) − v3 (post) ≥ 0 legalább három generátoron (pontbecslés).

**Döntési szabály:** ha H102a, b és c teljesül, az F91 + Q lesz az új befagyasztott konfiguráció (FROZEN_102).

## 2. rész: eredmények

Nyers adat: [`results/kor-102/`](../../experiments/arlc/results/kor-102/); elemzés:
[`analyze_r102.py`](../../experiments/arlc/arlc/analyze_r102.py) → `results/kor-102/analysis.json`. 540 futás + feladatcsomag.

| post-acc | G1k | G2 | G3 | G4 |
|---|---|---|---|---|
| v3 | 0,827 | 0,852 | 0,898 | 0,900 |
| v3 + Q | 0,841 | 0,907 | 0,900 | 0,929 |
| FROZEN_91 | 0,878 | 0,924 | 0,925 | 0,897 |
| **F91 + Q** | **0,890** | **0,950** | **0,932** | **0,930** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H102a:** (F91 + Q) − F91 > 0 legalább három generátoron | G1k +0,012 [−0,000; +0,027]; **G2 +0,027** [+0,012; +0,043]; G3 +0,007 [−0,002; +0,018]; **G4 +0,033** [+0,022; +0,045] | **nem teljesül** (kettőn szignifikáns, kettőn csak irányában) |
| **H102b (forrás-célkérdések):** ≥ 0 | **+0,050** [+0,027; +0,075] | **teljesül** |
| **H102c (feladatcsomag):** semmi nem rosszabb 0,05-nél többel | **TFB-2: 1,0 → 0,8; feltalálás: 1,0 → 0,75**; TFB-9: 0,78 → **0,95**; E1: 0,75 → **0,87**; E2a átfordulás 2/4/6 → 3/6/9 | **nem teljesül** |
| **H102d (G4):** (F91 + Q) − v3 > 0 | **+0,030** [+0,021; +0,039] | **teljesül** (először a G4-en) |
| **H102e:** (v3 + Q) − v3 ≥ 0 legalább háromszor | mind a négy generátoron pozitív (G1k, G2, G4 szignifikáns) | **teljesül** |

**A döntési szabály szerint az F91 + Q nem lesz alapértelmezés** (H102a és H102c nem teljesül).

### Értelmezés: a konzervativizmus tárcsája

1. **Az óvatos hitelesség a generatív világokon egyértelműen javít,** a v3-on is (H102e), és először hozza a FROZEN_91-et a v3
   fölé a G4-en. A forrás-célkérdéseken +0,05.
2. **A kézzel tervezett korai feladatokon viszont ront,** és a mintázat beszédes. A TFB-2-ben egyetlen terepi ellenpélda
   (q = 0,9) áll egy szabállyal szemben, és a feladat szerint ez valódi kivétel. Az óvatos hitelességgel a tény
   félretevése olcsóbb a kivételnél. A feltalálás kevés anomáliából általánosít. Az E2a-ban az átforduláshoz több
   ellentmondó megfigyelés kell (3/6/9 a 2/4/6 helyett). **Az óvatos hitelesség a rendszert konzervatívabbá teszi: több
   bizonyíték kell az átrendeződéshez.**
3. **Ez az eredeti feladat egyik központi feszültsége.** A feladat „meglepő információra azonnali átrendeződést” kért. A
   generatív benchmarkok (ahol a meglepetések egy része zaj vagy hazugság) a konzervativizmust jutalmazzák. A korai,
   kézzel írt feladatok (ahol a meglepetés mindig igaz) a gyors átrendeződést. **Egyik sem „a helyes” mérce:** a megfelelő
   konzervativizmus a környezet zajszintjétől függ. Ez a 89. kör adaptivitás–robusztusság ellentétének harmadik alakja.
   A rendszer egyetlen paraméterrel (q_temper) mozgatható közöttük.
4. **Kalibrációs megjegyzés:** a TFB-2 „helyes” válasza egy tervezői döntés. q = 0,9 és ε = 0,05 mellett egy magányos
   ellenpélda Bayes szerint inkább zaj (10%), mint kivétel (5%). A korai feladatok egy része tehát a deklarált priorok
   szerint *nem* a MAP-választ várja. Ezt a 26–31. körben nem vettem észre.
