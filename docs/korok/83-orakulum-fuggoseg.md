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
