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
