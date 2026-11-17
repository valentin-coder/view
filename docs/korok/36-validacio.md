# 36. kör – Validáció: helyes-e a kereső, és mit jelent a célfüggvény?

(A 29. kör kritikája szerint a játékvilágokon végzett kísérletek egyre inkább a saját
költségmodellünket tesztelik. Ez a kör ezért nem újabb jelenséget mér, hanem két alapvető
állítást ellenőriz *független* eszközzel. A körszámozás a terv szerinti 36., a 32–35. előtt
készült, mert a 32. kör futása közben derült ki a szükségessége.)

## 1. A keresés: kimerítő összevetés kis feladatokon

**Kérdés:** a 25. kör a „nagy keresés” közelítésével nulla optimalitási rést mért. Ez csak alsó
becslés. Ha kicsi a feladat, a *globális* optimum kimerítően kiszámolható: az összes
megfigyelés-elutasítás és példányszintű kivétel kombinációja.

**Elrendezés:** véletlen feladatok (2 kategória, diszjunktak; 2–3 szabály; 3–5 entitás; 4–7
tény), változó hitelességekkel. Kód: [`exhaustive.py`](../../experiments/arlc/arlc/exhaustive.py);
eredmény: [`results/kor-36/exhaustive.json`](../../experiments/arlc/results/kor-36/exhaustive.json).

**Eredmény (az első futás, a 21. körös gyorsítással):**

| feladatméret | feladatok | hipotézis/feladat | rés = 0 | legnagyobb rés |
|---|---|---|---|---|
| 3 entitás, 4 tény, 2 szabály | 25 + 40 | kb. 3 000 | **65/65** | 0 |
| 4 entitás, 6 tény, 3 szabály | 25 | kb. 141 000 | **24/25** | **2,93 bit** |
| 5 entitás, 7 tény, 3 szabály | 12 | kb. 808 000 | 12/12 | 0 |

**A hiba diagnózisa (seed 1, 4–6–3).** A 13. megfigyelés („e0-nak van r”) ütközött a 11.-kel
(„e0-nak nincs r”), és a keresés a 11.-et utasította el. Ezzel az e0 tagságának (4.) korábbi
elutasítása feleslegessé vált: a visszavétele konzisztens és 2,93 bittel olcsóbb lett volna. A
visszahelyező lépés azonban nem futott le. **A 21. körben gyorsításként csak a „szerkezeti”
jelöltekre (szabály-elutasítás, kontextus, kivétel) engedtem**, egy egyszerű tény-elutasítás
pedig nem ilyen. A gyorsítás kb. 13%-ot hozott, és egy olyan hibát vitt be, amelyet a korábbi
regressziós tesztek (ugyanazokon a kísérleteken) nem fogtak meg.

**Javítás:** az alapértelmezés újra a teljes visszahelyezés. Ezzel a 25 feladatból **25-ön nulla
a rés**. Az A fázis kísérletei (E1, E2a, E2b, E3, E4, A7) a javítás után bitre azonosak. A 22–31. kör
kísérleteit a javított keresővel újrafuttattam, az eltéréseket lásd lent.

**Tanulság a módszertanra:** a regressziós teszt csak azt mutatja meg, hogy *ugyanazokon* a
feladatokon nem változott semmi. **Egy gyorsítás helyességét független, kimerítő ellenőrzéssel
kell igazolni, véletlen feladatokon.** Ez az ellenőrzés mostantól minden kereső-módosítás része.

## 2. A célfüggvény jelentése: ProbLog-összevetés

**Kérdés:** az ARLC pontszáma kézzel összerakott bit-tagok összege. Megfelel-e egy *valószínűségi
modellnek*, vagy önkényes súlyokat tartalmaz?

**A generatív modell** (rögzített megbízhatóság, kivétel, kontextus, vágás és indukció nélkül):
- minden jelentés i megbízható q_i valószínűséggel (`rel(i)`);
- egy megbízható tagság- vagy szabályjelentés igaz;
- egy megbízható tényjelentés valószínűsége 1 − δ, ha az aktív szabályok jósolják, és 0,5, ha nem;
- egy megbízhatatlan tényjelentés tartalma véletlen (0,5);
- az ütközés kizárt (kemény kényszer).

Ezt ProbLog-programként írtam fel (az evidencia a megbízhatósági hozzárendelés és a jelentések
megfigyelése), és a ProbLog súlyozott modellszámlálójával `−log₂ P(evidencia)`-t számoltam.
Kód: [`problog_check.py`](../../experiments/arlc/arlc/problog_check.py); eredmény:
[`results/kor-36/problog.json`](../../experiments/arlc/results/kor-36/problog.json).

**Eredmény:** 20 véletlen feladat 200 konzisztens hipotézisén az ARLC-pontszám és a ProbLog
`−log₂ P` értéke **pontosan egyezik** (legnagyobb eltérés 7·10⁻¹⁵ bit, lebegőpontos kerekítés).

**Értelmezés:**
- Az ARLC magjának MDL-célfüggvénye **egy explicit generatív modell MAP-célja**. A 15. kör
  „bit-tagjai” nem önkényesek: mindegyik egy feltételes valószínűség negatív logaritmusa.
- **Ezzel a 29. kör kritikájának egy része pontosabbá válik:** az ARLC egy kézzel írt valószínűségi
  logika, nyalábkereséses MAP-következtetéssel. Ami *túlmegy* a ProbLog-modellen (kivételek,
  kontextusok, vágás, indukció, tanult megbízhatóság, feltalálás), azt ez a kör nem ellenőrzi. Ezek
  mindegyike felírható volna egy gazdagabb generatív modellben (pl. a kivétel egy rejtett
  „normális-e” változóként), de ezt nem tettem meg.
- **Gyakorlati következmény:** egy kiforrott valószínűségi logikai rendszer (ProbLog, BLOG,
  Markov-logika) **elvben helyettesíthetné az ARLC magját**. Az ARLC saját értéke így nem a
  következtetőben van, hanem a *modellezési döntésekben*: mi a megfigyelés, a forrás, a kivétel, a
  kontextus. A 16–31. kör jelenségtára azt mutatja meg, melyik modellezési döntés mihez vezet.

## Mit erősít és mit gyengít ez a kör?

| állítás | előtte | utána |
|---|---|---|
| A nyalábkeresés megtalálja a célfüggvény optimumát | 25. kör: közelítő, nulla rés | kimerítő ellenőrzéssel igazolva, **a javítás után**; egy hiba megtalálva és javítva |
| A pontszám egy valószínűségi modell MAP-célja | feltételezés | **igazolva** a mag részre |
| Az ARLC új következtetési módszer | gyanú (29. kör) | **nem az**: egy valószínűségi logika MAP-következtetése; az újdonság legfeljebb a modellezésben van |


## Függelék (a 43. kör után)

**Az ismétlés eredménye a javított keresővel.** A 22–31. kör kísérleteit a teljes visszahelyezéssel
újrafuttattam:

| kör | összevetett esetek | eltérés |
|---|---|---|
| 26 (olcsó álnevek) | 96 | **0** |
| 28 (TFB) | 245 | **0** |
| 30 (feltalálás) | 378 | **0** |
| 31 (polarizáció) | 108 | 1 végső hiedelem, 8 kis pontosság-eltérés |

A szűkített visszahelyezés hibája ezeket a köröket érdemben nem érintette.

**Lefedettségi rés.** A 41. körben a ProbLog-ellenőrzés a kivétel-priort csak tulajdonság-szabályokon
igazolta, és egy programhibát (ingyenes kivételek az alosztály-szabályokra és a levezetett
tagságokra) nem fogott meg. A 43. kör ablációja találta meg. Javítva, és az ellenőrzés kiterjesztve
alosztály- és negatív szabályokra: [`results/kor-36/problog_isa_eps*.json`](../../experiments/arlc/results/kor-36/).
**Egy validáció csak arra érvényes, ami a tesztfeladatokban előfordul.**
