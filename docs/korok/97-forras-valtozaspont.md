# 97. kör – Forrás-változáspont (romló bevált forrás): fejlesztési negatív eredmény

## 1. A mechanizmus

A 93. és a 96. kör szerint a hibrid kód a bevált forrás romlását nem veszi észre: a G4 „romló forrás” típusában a FROZEN_91
célkérdés-pontossága a v3-éval egyezik (0,79–0,80). Elvi javítás a forrás megbízhatóságának **változáspontja**, a 11. kör
vágásának mintájára: a hipotézis egy új komponense (`chg`) azt állítja, hogy az s forrás a t időponttól egy új
„szegmens”. Ez új forrásnak számít (adaptív keverék, π = 0,9), és az ára −log₂ ρ (ρ = 0,01). A kereső ezt akkor javasolja,
ha egy ütközésben egy bevált forrás *most érkező* jelentése szerepel.

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`Hyp.chg`, `_seg`, `source_changepoints`, `chg_prior`). Üres
`chg` mellett a hipotézis kulcsa változatlan, így a korábbi viselkedés bitre azonos (ekvivalencia: EGYEZIK).

## 2. Fejlesztési ellenőrzés (G4, romló forrás, 28000–28002; nem teszt)

| seed | FROZEN_91 post / target | + változáspont post / target | elfogadott változáspont |
|---|---|---|---|
| 28000 | 0,933 / 0,9 | 0,933 / 0,9 | – |
| 28001 | 0,922 / 0,9 | 0,911 / 0,8 | (f1, 32) |
| 28002 | 0,933 / 0,9 | 0,933 / 0,9 | (f1, 32) |

**A változáspontot a kereső megtalálja és két seeden elfogadja, de javulást nem hoz,** egy seeden ront. Ennek oka: a
romló forrás hibás jelentései tankönyvi szabályokkal ütköznek, ezért a rendszer a rögzített kóddal is egyenként
félreteszi őket. A maradék célkérdés-hibák nem a forrás megbízhatóságából jönnek. A változáspont után viszont a
forrás *helyes* új jelentései is gyanússá válnak.

## 3. Döntés

Gyenge (sőt negatív) fejlesztési adatra nem építek előregisztrált tesztet. A mechanizmus kikapcsolva marad a kódban. A
„romló forrás” gyengesége a G4-en (93. kör, H93d) **nem a változáspont hiányából jön,** és a v3-nál sem rosszabb.
