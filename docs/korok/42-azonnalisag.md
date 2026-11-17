# 42. kör – Mennyire „azonnali” az átrendezés?

## Kérdés

Az eredeti cél: „azonnali átstrukturálás … egyszerre, gradiens-tanítás nélkül”. A 10. kör ezt
elméletben vizsgálta, azzal a következtetéssel, hogy a döntés és a végrehajtás a kúpmérettel
lineáris lehet, ha a szükséges alternatíva a nyalábban van. **Ez a kör megméri.**

Kód: [`scaling.py`](../../experiments/arlc/arlc/scaling.py); eredmény:
[`results/kor-42/`](../../experiments/arlc/results/kor-42/).

## Elrendezés

E1-szerű taxonómiák 21–63 kategóriával, 24–108 entitással, 132–476 megfigyeléssel. Mérés: egy
hétköznapi megfigyelés feldolgozási ideje, és a meglepetésé (átkategorizálás vagy alosztály-csere,
q = 0,999). Egyetlen CPU-mag, Python.

## Első eredmény: a meglepetés a lassú út

| kategóriák | entitások | megfigyelések | hétköznapi megfigyelés (medián) | meglepetés: átkat. | meglepetés: alosztály |
|---|---|---|---|---|---|
| 21 | 24 | 132 | 0,10 ms | 0,75 s | 3,5 s |
| 21 | 48 | 204 | 0,19 ms | 2,3 s | **23,8 s** |
| 39 | 54 | 276 | 0,20 ms | 1,8 s | 2,7 s |
| 39 | 108 | 438 | 0,49 ms | 1,7 s | 14,6 s |
| 52 | 108 | 476 | 0,53 ms | 0,15 s | 4,5 s |
| 63 | 96 | 474 | 0,27 ms | 3,5 s | 15,4 s |

**A meglepetés feldolgozása 4–5 nagyságrenddel lassabb, mint egy hétköznapi megfigyelésé, és nem
a kúp méretével arányos** (2–4 érintett tag mellett is 3–24 s). **Az „azonnali átrendezés”
ebben a megvalósításban épp a drága út.**

## Diagnózis (profil)

Egy 35 s-os meglepetésben:
- a mohó befejezés minden lépésben **minden** lehetséges módosítás **teljes** pontszámát kiszámolja
  (kb. 10 000 pontszám-kiértékelés, kb. 1 millió zárás-lekérdezés);
- az osztályszintű kivétel ellenőrzése a zárásban minden szabályalkalmazásnál végigment az entitás
  kategóriáin, akkor is, ha nem volt osztályszintű kivétel (11,7 s a 35-ből).

## Javítások és ellenőrzésük

1. **Szemantika-megőrző gyorsítások:** az osztályszintű kivételek előre kigyűjtve, a zárás-lekérdezések
   a pontszámon belül gyorsítótárazva. Ellenőrzés: az A fázis (E1, E2a, E2b, E4, A7) **bitre azonos**,
   a kimerítő optimalitás-ellenőrzés 25/25. Hatás: csak 10–15%.
2. **Algoritmikus változtatások** (kapcsolóként), mindegyik a 36. kör kimerítő ellenőrzésével
   (25 véletlen, 4 entitás / 6 tény / 3 szabály méretű feladat):

| változat | optimális (25-ből) | meglepetés ideje (21 kat., 48 ent., alosztály) |
|---|---|---|
| mélység 3, teljes pontszám (eredeti) | 25 | 19,7 s |
| mélység 3, helyi becslésű mohó lépés | 25 | 5,6 s |
| mélység 2, teljes pontszám | 25 | 3,6 s |
| **mélység 2, helyi becslésű mohó lépés** | **25** | **0,80 s** |

A helyi becslés (`_local_cost`) csak a megváltozott elemek költségét számolja (a megfigyelés
log-esélye, a kivétel, a kontextus, a vágás). A végső jelölteket továbbra is a teljes pontszám
rangsorolja.

**A v4 ezért mélység 2 és helyi becslésű mohó lépés mellett fut** (43. kör). Kb. 25-szörös
gyorsulás, optimalitásvesztés nélkül a tesztelt méreten.

## Értelmezés

1. **Az „azonnali” állítás jelenleg nem teljesül:** a meglepetés a javítások után is a hétköznapi
   megfigyelés idejének kb. ezerszerese. Gyorsabb, de nem azonnali.
2. **A 10. kör állítása (kúppal lineáris) nem a mostani algoritmusra igaz.** A pontszám minden
   jelöltre a *teljes* megfigyeléshalmazon fut le. A lineáris skálázáshoz **inkrementális pontozás**
   kell: a pontszám-különbség csak a megváltozott entitásokon és forrásokon számolódik. A pontszám
   ehhez elég jól felbontható: megfigyelésenkénti tagok, forrásonkénti béta-tagok, szabályonkénti
   abnormalitás-tagok. Ez a 46. kör.
3. **Emberi párhuzam (spekulatív):** a belátásos átrendezés is lassú, rejtett inkubációval jár, és a
   *döntés* a hirtelen rész (7. kör). Az ARLC-ben ez fordítva van: a hétköznapi feldolgozás gyors,
   az átrendezés keresése lassú. Ez azonban algoritmikus, nem elvi különbség.
