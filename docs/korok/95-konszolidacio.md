# 95. kör – Konszolidáció: egyet-elhagyó abláció a FROZEN_91-ből négy generátoron (feltáró)

## 1. Az eredeti terv, és miért változott

A 94. kör a 95. körre egy előregisztrált tesztet tervezett: lassan tanuló becsületes komponens (κ₁ = 300) az
elmélet-keverékben (Tκ) és a bevált adatforrásokra (Dκ). Kód: `core.py` (`rel_hybrid_kappa`), `v4.py` (`F91_TK`,
`F91_TDK`); kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

**Fejlesztési ellenőrzés** ([`dev_r95.py`](../../experiments/arlc/arlc/dev_r95.py); G4: 28000–28005, G1k-C: 16000–16001;
nem teszt):

| | G4 pre / post / target | G1k-C pre / post / target | E1 | TFB-9 | TFB-2 |
|---|---|---|---|---|---|
| FROZEN_91 | 0,907 / 0,907 / 0,958 | 0,784 / 0,766 / 0,688 | 0,75 | 0,783 | 1,0 |
| + Tκ | **azonos** | **azonos** | 0,75 | 0,783 | 1,0 |
| + TDκ | 0,917 / 0,917 / 0,979 | azonos | 0,75 | 0,813 | **0,8** |

**A Tκ semmit nem változtat,** ezért a 93. kör diagnózisát (az elmélet-keverék adaptív komponense okozza a G4-beli
tankönyv-félretevést) visszavontam (93. kör, 3. rész). A TDκ kicsi, vegyes hatást mutat (G4 +0,01, TFB-9 +0,03, TFB-2
−0,2). **Ez túl gyenge alap egy előregisztrált teszthez.** Ezért a kör konszolidációs és diagnosztikai kör lett (a 94. kör
4.2. pontja): egyet-elhagyó abláció a FROZEN_91-ből, fejlesztési seedeken. Ez megmutatja, mi okozza a G4-beli
lemaradást, és melyik kapcsoló nem számít sehol.

## 2. Elrendezés

Kód: [`loo_r95.py`](../../experiments/arlc/arlc/loo_r95.py). Fejlesztési seedek (mind korábban már felhasznált): G1k-A hazug
(16000–16004), G2 hazug (16000–16004), G3 hazug és állapotváltozás (23000–23004, upd = 0,3), G4 hazug (28000–28004).
16 változat: v3, FROZEN_91 és 14 egyenként kikapcsolt komponens.

## 3. Eredmények

Nyers adat: [`results/kor-95/loo/`](../../experiments/arlc/results/kor-95/loo/), összesítés: `results/kor-95/loo_summary.json`.
(A futás közben a konténer újraindult; a futtató folytatta, az esetek determinisztikusak.)

Post-acc / célkérdés-acc, generátoronként (5 seed; a G3-on 10 eset, két típus):

| változat | G1k | G2 | G3 | G4 |
|---|---|---|---|---|
| v3 | 0,780 / 0,525 | 0,895 / 0,600 | 0,921 / 0,579 | 0,904 / 0,800 |
| **FROZEN_91** | **0,837 / 0,750** | **0,934 / 0,900** | **0,956 / 0,963** | 0,916 / **1,000** |
| − tankönyv-keverék | 0,830 / 0,750 | 0,938 / 0,900 | = | = |
| **− PK** | 0,834 / 0,750 | **0,859 / 0,775** | = | = |
| − N | = | 0,929 / **0,825** | 0,953 / 0,925 | 0,909 / 0,925 |
| **− hibrid** | 0,829 / 0,750 | 0,925 / 0,875 | **0,924** / 0,950 | **0,936** / 0,975 |
| **− V** | = | = | 0,942 / **0,679** | = |
| − aut. specifikusság | 0,840 / 0,775 | = | 0,945 / 0,963 | = |
| − szigorú specifikusság | 0,828 / 0,750 | 0,926 / 0,900 | = | = |
| − kivétel-prior | 0,834 / 0,775 | = | 0,954 / 0,963 | 0,911 / 0,975 |
| **− osztálykivétel** | **0,800** / 0,775 | **0,859 / 0,775** | = | = |
| − feltalálás | = | = | = | = |
| − forráslépés | = | 0,935 / 0,925 | = | = |
| − kontextusindukció | = | = | = | = |
| − q-csoportok | = | = | = | = |
| − ind. kivétel-ár | 0,842 / 0,750 | = | = | = |

(„=”: azonos a FROZEN_91-gyel.)

## 4. Értelmezés

1. **Lényeges komponensek:** a PK és az osztálykivétel (együtt a prioritás; G2 −0,075 nélkülük, az osztálykivétel a G1k-n
   is −0,037), az eseményenkénti vágás (G3 célkérdés 0,963 → 0,679), az N (forrás-célkérdések) és a hibrid kód (G3 −0,032).
2. **Sehol nem számít ezen a négy generátoron:** feltalálás, kontextusindukció, q-csoportok. **Nem törlöm őket**, mert
   olyan feladatokat szolgálnak, amelyek a generátorokban nincsenek: a feltalálás a feladatcsomag „Feltalálás” tételét, a
   kontextusindukció a jelzett „más régió” esetet. A q-csoportok hatása egyik mért helyen sem látszik. **Egy rendszer,
   amelynek kapcsolóinak harmada a mért világokban hatástalan, a mért világok szerint túlbonyolított.** Ez a 34. kör
   túlillesztési aggályának másik oldala: nem illesztés, hanem fölösleg.
3. **A G4-beli lemaradás valódi oka: a hibrid kód.** Nélküle (teljesen adaptív kóddal) a G4 post 0,936 a 0,916 helyett. A
   G4-ben a négy terepforrás valódi megbízhatósága 0,65 és 0,97 között szór, mind 0,9-et deklarál. **A rögzített kód
   nem tanulja meg, hogy az f4 rossz,** és helyette tankönyvi szabályokat tesz félre (93. kör auditja). Ez ugyanaz,
   mint a TFB-9 a 92. körben: **a rögzített kód a bevált, de rosszul kalibrált forrásnál téved.** A G3-on viszont az
   adaptív kód árt (bűnbak). A kettő közötti köztes megoldás a lassan tanuló bevált forrás (Dκ, κ = 300). A fejlesztési
   ellenőrzés szerint ez a G4-en +0,01, a TFB-9-en +0,03. A 96. kör ezt előregisztráltan méri.

