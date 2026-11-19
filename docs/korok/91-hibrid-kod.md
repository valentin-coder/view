# 91. kör – Hibrid megbízhatósági kód és eseményenkénti vágásár (előregisztrált)

## 1. rész: terv, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### Miért

A 90. kör szerint egyetlen globális η nem tudja egyszerre a háttérvilágot (ott a rögzített kód a jobb) és az új
megbízhatatlan forrást (ott az adaptív) kezelni. Feltáró eredmény: az η = 0 (v4-szerkezet rögzített megbízhatósággal)
mindhárom generátoron a v3 fölött van. **A két feladat forrásonként szétválasztható:** a bevált forrásokra rögzített
kód, az új forrásokra adaptív keverék (86. kör, N).

### Két változtatás

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`rel_hybrid`, `cut_per_event`), [`v4.py`](../../experiments/arlc/arlc/v4.py)
(`HYBRID_V_91`).
1. **Hibrid megbízhatósági kód (`rel_hybrid`):** a bevált adatforrás (első megjelenése az aktuális időpont előtt volt)
   rögzített kódot kap (mint a v3-ban). Az új forrás az N keverék-priorját (π = 0,9, κ₁ = 30) kapja. A tankönyv
   elmélet-keveréke (π a metaadatból) változatlan.
2. **Eseményenkénti vágásár (`cut_per_event`):** a fejlesztési ellenőrzés közben derült ki, hogy a hibrid nem fogadja el
   az állapotváltozást, ha a régi állapotról két jelentés van. Mindkettőt vágni kell, és **minden vágás külön
   −log₂(upd) bitbe került.** Két vágás (2 × 1,74 bit) drágább, mint az új jelentés félretevése (≈ 3,2 bit). Egy
   állapotváltozás viszont *egy* esemény, akárhány jelentés szólt is a régi állapotról. **A javított kód
   eseményenként (entitás, csoport, vég-időpont) egyszer számol.** Ez a PK-éhoz (81. kör) hasonló kódhossz-javítás, nem
   hangolás. Az adaptív kód (η = 1) ezt eddig elfedte, mert egy megbízható nagy forrás jelentésének félretevését
   drágábbnak árazta.

Mindkettő kikapcsolva bitre azonos a korábbi viselkedéssel (ekvivalencia: EGYEZIK).

### Fejlesztési ellenőrzés (már felhasznált seedek, nem teszt)

Kód: [`dev_r91.py`](../../experiments/arlc/arlc/dev_r91.py). 3–3 seed:

| | G1k hazug post / target | G2 hazug post / target | G3 hazug post / target | G3 állapotvált. target |
|---|---|---|---|---|
| v3 | 0,774 / 0,458 | 0,898 / 0,583 | 0,917 / 0,667 | 0,500 |
| η = 0 | 0,828 / 0,625 | 0,947 / 0,792 | 0,929 / 0,708 | 0,500 |
| η = 1 | **0,851** / 0,708 | 0,947 / 0,917 | 0,907 / 0,833 | **1,000** |
| hibrid (vágás régi árral) | 0,832 / 0,708 | **0,960 / 0,958** | **0,947 / 0,917** | 0,500 |
| hibrid + V | | | | **1,000** (23000–23002) |

### Előregisztráció

- **Seedek:** 26000–26019 (friss). Esetek, mint a 90. körben: G1k-A (hazug, átkategorizálás); G2 (hazug, torzított); G3,
  upd = 0,3 (hazug, állapotváltozás, elavult). 140 eset × 4 változat.
- **Változatok:** v3; η = 0; η = 1 (a befagyasztott); **hibrid+V**. Kód: [`run_r91.py`](../../experiments/arlc/arlc/run_r91.py).
- **Elemzés:** seedenként, generátoronként a típusokra átlagolva; világok szerinti klaszteres bootstrap (95%).

**Hipotézisek** („forrás-célkérdések”, mint a 90. körben: hazug, torzított, elavult):
- **H91a (a 90. kör feltáró eredményének megerősítése):** η = 0 − v3 (post) > 0, a CI nem tartalmazza a nullát, **mindhárom**
  generátoron külön.
- **H91b:** hibrid+V − v3 (post) > 0, a CI nem tartalmazza a nullát, mindhárom generátoron külön.
- **H91c (forrás-célkérdések, összesen):** hibrid+V − (η = 0) > 0, a CI nem tartalmazza a nullát (az új forrásra
  alkalmazott adaptív kód a felismerést adja).
- **H91d (G3, pre):** hibrid+V − (η = 1) > 0, a CI nem tartalmazza a nullát; és a G1k-n és a G2-n hibrid+V − (η = 1)
  (post) ≥ −0,01 (pontbecslés).
- **H91e (G3, állapotváltozás, target):** hibrid+V ≥ 0,8.

**Ha H91b–H91d teljesül:** a hibrid+V lesz az új befagyasztott konfiguráció, és a 89. kör ellentétét (adaptivitás vs.
robusztusság) forrásonként oldja fel, metaadat nélkül.
