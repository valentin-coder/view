# 100. kör – Megerősítés-függő új-forrás bizalom: fejlesztési negatív eredmény, és miért elvi a korlát

## 1. A mechanizmus

A 98. kör szerint a FROZEN_91 a helyes szabály-helyesbítést gyakran elutasítja (−0,128 a v3-hoz), mert a lektor új forrás. A
javaslat az volt, hogy az új forrás szemét-esélye a **nyers megerősítéstől** függjön: egy szemét-forrás állítása egy
független állítással 1/2 eséllyel egyezik, egy becsületesé kb. q eséllyel. Így minden egyezés log₂(q/0,5), minden
ellentmondás log₂((1 − q)/0,5) bittel tolja a becsületes-súly log-esélyét. Az összevetés a többi forrás nyers állításaival
történik (tények, és a tankönyvi szabályok a nyers tagságokon át), a hipotézistől függetlenül.

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`newcomer_corrob`, `_corrob_pi`), [`v4.py`](../../experiments/arlc/arlc/v4.py)
(`F91_C`). Kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

## 2. Fejlesztési ellenőrzés

Kód: [`dev_r100.py`](../../experiments/arlc/arlc/dev_r100.py). Korábban felhasznált seedeken:

| | FROZEN_91 target | F91_C target | v3 target |
|---|---|---|---|
| G1k szabály-helyesbítés (16000–16005) | 0,904 | 0,904 | 0,904 |
| G1k hazug (16000–16003) | 0,750 | 0,781 | 0,500 |
| G1k átkategorizálás (16000–16003) | 0,683 | 0,683 | 0,775 |
| G4 jó specialista (28000–28003) | 0,944 | 0,950 | 1,000 |
| G4 hazug (28000–28003) | 1,000 | 1,000 | 0,812 |

A 98. kör négy kudarc-seedjén (32003, 32004, 32010, 32019; a 98. kör óta felhasznált) a F91_C ugyanúgy elutasítja a lektort. A
nyers megerősítés a lektor becsületes-súlyát 0,62-re, illetve 0,25-re teszi: **a terepi tények a helyesbítést alig
támasztják alá,** a tankönyvi szabály (q = 0,95) pedig ellentmond neki.

## 3. Miért elvi a korlát

A 32003-as eset számolva: a lektor (q = 0,995) egyetlen szabálya ütközik a tankönyv (q = 0,95) szabályával, és más
bizonyíték alig van. A 10%-os szemét-priorral:
- P(a lektornak van igaza) ∝ 0,9 · 0,995 · 0,05 ≈ 0,045;
- P(a tankönyvnek van igaza) ∝ 0,95 · (0,9 · 0,005 + 0,1 · 0,5) ≈ 0,052.

**A MAP a tankönyvet választja, és ez a prior mellett racionális.** A döntést egyetlen adat billentené: a deklarált
hitelesség (0,995 vs. 0,95). Ezt a szemét-komponens leértékeli. **Egyetlen állításból egy jó és egy rossz új forrás
metaadat nélkül elvileg nem különböztethető meg.** A π_új egy valódi tárcsa a hazug forrás felismerése és a helyes
helyesbítés elfogadása között. A 101. kör prior-érzékenységi protokollja ezt a tárcsát is méri.

## 4. Döntés

Előregisztrált teszt nincs. A mechanizmus kikapcsolva marad.
