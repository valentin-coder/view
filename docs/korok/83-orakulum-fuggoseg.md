# 83. kör – Orákulum-függőség a szabályprioritás mellett (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért, és miért nem SafeBayes

A 79. kör a 83. körre a SafeBayes-t (temperált likelihood) javasolta, a forrástípus-prior (80. kör, „T”) metaadat nélküli
alternatívájaként. A 81. kör óta viszont kiderült, hogy a G2-beli bűnbak-forrás gyökéroka a hiányzó prioritás-primitív
és egy kódhossz-hiba volt, nem a megbízhatósági prior. **Ezért előbb azt kell megmérni, kell-e még a harmadik orákulum
(T) egyáltalán.** Ha a prioritás mellett a T nélkül is ugyanott vagyunk, a metaadat-mentes alternatíva kérdése
egyszerűbben megválaszolódik. A SafeBayes csak akkor kerül sorra, ha a T továbbra is szükséges.

A 81. kör kritikája szerint a prioritás-kivétel a **C populáción** (két rivális tankönyv) nem volt mérve. Ott a szigorú
specifikusság eredetileg egy menekülőutat zárt el. Ezt most pótolom.

### Elrendezés

- **Seedek:** 20000–20019 (friss). Esetek: G1 A és C (hazug forrás); G2 (hazug forrás, torzított forrás). 80 eset.
- **Módszerek** (PK = prioritás-kivétel + javított kódhossz):
  - v4.9 = v4.8-π + T;
  - v4.9+PK;
  - v4.8-π+PK (T nélkül);
  - v4.4e+PK (T és tankönyv-π nélkül).
- Kód: [`run_r83.py`](../../experiments/arlc/arlc/run_r83.py). Elemzés: világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

- **H83a (G2, pre-acc):** (v4.8-π+PK) − (v4.9+PK) ≥ −0,01 (pontbecslés): az általános pontossághoz a prioritás mellett
  nem kell a T.
- **H83b (a hazug forrás célkérdései, G1-A ∪ G2):** (v4.9+PK) − (v4.8-π+PK) > 0, a CI nem tartalmazza a nullát: a
  hazug forrás felismeréséhez a T továbbra is kell (a 80. kör +0,08 – +0,10-es hatása).
- **H83c (G1-C, post-acc):** (v4.9+PK) − v4.9 ≥ −0,02 (pontbecslés): a prioritás-kivétel a rivális elméleteknél nem
  nyit új menekülőutat.
- **H83d (G1-C, post-acc, kontroll):** (v4.4e+PK) < (v4.9+PK), a CI nem tartalmazza a nullát: a rivális elméletekhez a
  tankönyv-π kell (60. kör); ha ez nem teljesül, a mérés valamiért nem érzékeny.

**Döntési szabály előre:** ha H83a és H83b is teljesül, a T szerepe a megbízhatatlan új forrás felismerésére szűkül.
Ekkor a 84. körben a SafeBayes helyett a T **tanulható** változata (a forrás típusát a viselkedéséből becsülni) a
következő lépés. Ha H83a nem teljesül, a T az általános pontossághoz is kell, és a SafeBayes-t érdemes kipróbálni.

## 2. rész: eredmények

Nyers adat: [`results/kor-83/test/`](../../experiments/arlc/results/kor-83/test/); elemzés:
[`analyze_r83.py`](../../experiments/arlc/arlc/analyze_r83.py) → `results/kor-83/analysis.json`. 320 futás, eltérés nincs.

| | G1-A post | G1-A target | G1-C post | G1-C target | G2 pre | G2 post | G2 target | G2 idő/eset |
|---|---|---|---|---|---|---|---|---|
| v4.9 | 0,804 | 0,794 | **0,637** | **0,625** | 0,885 | 0,884 | 0,903 | 39 s |
| v4.9+PK | **0,815** | **0,806** | **0,637** | **0,625** | 0,926 | 0,926 | **0,933** | 58 s |
| v4.8-π+PK (T nélkül) | 0,780 | 0,700 | 0,530 | 0,456 | 0,931 | 0,929 | 0,923 | 37 s |
| v4.4e+PK (T és π nélkül) | 0,780 | 0,700 | 0,223 | 0,156 | **0,933** | **0,930** | 0,923 | 35 s |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H83a (G2, pre):** (T nélkül) − (T-vel) ≥ −0,01 | +0,004 [−0,002; +0,011] | **teljesül** |
| **H83b (hazug target, G1-A ∪ G2):** (T-vel) − (T nélkül) > 0 | **+0,056** [+0,025; +0,100] | **teljesül** |
| **H83c (G1-C, post):** PK − v4.9 ≥ −0,02 | 0,000 [0; 0] | **teljesül** (bitre azonos) |
| **H83d (G1-C, kontroll):** (π nélkül) < (π-vel) | **−0,414** [−0,571; −0,258] | **teljesül** |

### Értelmezés

1. **A forrástípus-prior (T) szerepe szűk:** az általános pontossághoz a prioritás mellett nem kell (G2: T nélkül
   +0,004, n.s.), **a hazug forrás felismeréséhez viszont igen** (+0,056). A C populáción (hazug forrás két rivális
   tankönyv mellett) a T még fontosabb: post 0,637 vs. 0,530, target 0,625 vs. 0,456.
2. **A prioritás-kivétel a rivális elméleteknél nem nyit menekülőutat:** a G1-C-n bitre azonos. A két rivális tankönyv
   szabályai ugyanarra a törzsre vonatkoznak, ezért a prioritás-kivétel (más törzsű rivális kell hozzá) nem aktiválódik.
3. **A T a G2-n lassít** (58 s vs. 37 s esetenként), mert a keverék-kód több jelöltet tart életben.
4. **A G1-es számok a 82. kör 3. részében leírt generátorhibát hordozzák** (a 20000–20019 seedek többsége ellentmondásos
   világ). A módszerek összevetése egyenlő feltételek mellett történt.

### Döntés (az előre rögzített szabály szerint)

H83a és H83b is teljesül, ezért **a SafeBayes helyett a T tanulható változata a következő lépés.** A T valójában egyetlen
megkülönböztetést használ ki: a **régi, bevált** forrásokat (tankönyv, népszámlálás, terepi források) és az **új,
ismeretlen** forrásokat (hazug, torzított) eltérő priorral kezeli. Ez nem igényel orákulumot: hogy egy forrás mikor
jelent meg először, és mennyi korábbi állítása igazolódott, **megfigyelhető.** A 86. kör ezt méri: π egy forrásra a
„múltja” alapján (első megjelenés ideje, megerősített állítások száma), metaadat nélkül.
