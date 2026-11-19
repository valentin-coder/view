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
| hibrid + V | – | – | – | **1,000** (23000–23002; csak ezen ellenőrizve) |

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

## 2. rész: eredmények

Nyers adat: [`results/kor-91/test/`](../../experiments/arlc/results/kor-91/test/); elemzés:
[`analyze_r91.py`](../../experiments/arlc/arlc/analyze_r91.py) → `results/kor-91/analysis.json`. 560 futás, eltérés nincs.

### Post-acc (célkérdés-acc zárójelben)

| | G1k | G2 | G3 |
|---|---|---|---|
| v3 | 0,793 (0,638) | 0,866 (0,662) | 0,879 (0,423) |
| η = 0 | 0,885 (0,723) | 0,920 (0,760) | 0,906 (0,450) |
| η = 1 (88. kori befagyasztott) | 0,880 (0,741) | 0,918 (**0,922**) | 0,894 (**0,828**) |
| **hibrid+V** | **0,893** (**0,763**) | **0,922** (0,892) | **0,927** (0,818) |

Típusonként (célkérdés): hazug forrás: G1k 0,856 / G2 0,925 / **G3 0,963** (η = 1: 0,856 / 0,950 / 0,881); torzított (G2):
0,858 (η = 1: 0,894); elavult (G3): 0,492 (η = 1: **0,652**); állapotváltozás (G3): **1,000** (η = 1: 0,950; v3: 0,233);
átkategorizálás (G1k, helyes új szakértő): 0,670 (η = 0: **0,777**).

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H91a:** η = 0 − v3 (post) > 0 mindhárom generátoron | G1k **+0,092** [+0,034; +0,169]; G2 **+0,054** [+0,022; +0,096]; G3 **+0,028** [+0,009; +0,059] | **teljesül** |
| **H91b:** hibrid+V − v3 (post) > 0 mindhárom generátoron | G1k **+0,099** [+0,044; +0,175]; G2 **+0,056** [+0,021; +0,102]; G3 **+0,048** [+0,029; +0,078] | **teljesül** |
| **H91c:** forrás-célkérdések hibrid+V − (η = 0) > 0 | **+0,163** [+0,122; +0,205] | **teljesül** |
| **H91d:** G3 pre hibrid+V − (η = 1) > 0; G1k, G2 post ≥ −0,01 | **+0,068** [+0,020; +0,157]; +0,012; +0,004 | **teljesül** |
| **H91e:** G3 állapotváltozás target ≥ 0,8 | **1,000** | **teljesül** |

### Értelmezés

1. **A sorozatban először van olyan konfiguráció, amely mindhárom generátoron, előregisztráltan, friss seedeken az
   általános pontosságban is a v3 fölött van** (+0,05 – +0,10), és közben a forrás-felismerést is megtartja (+0,16 a
   rögzített kódhoz képest). A 89. kör ellentétét (adaptivitás vs. robusztusság) **forrásonként** oldja fel: a bevált
   forrásra rögzített kód, az újra adaptív keverék.
2. **A 90. kör feltáró eredménye megerősítve:** a v4 szerkezeti újításai rögzített megbízhatósággal is általánosak (η = 0 −
   v3 > 0 mindhárom generátoron). A 88. kori kudarc tehát nem a szerkezetből, hanem az adaptív kódból jött.
3. **Maradék költségek:** (a) az elavult forrás felismerése gyengébb, mint az η = 1-nél (0,49 vs. 0,65); (b) a helyes új
   forrás (szakértő) is gyanús (0,67 vs. 0,78). Mindkettő a „gyanús új forrás” ára. Az elavult forrás nehezebb, mert az
   állításai *korábban* igazak voltak.
4. **Két kódhossz-javítás egy körön belül** (eseményenkénti vágásár) újra mutatja a 81. kör tanulságát: a modell
   kódjainak hibái (mit számol a kód többször, mint kellene) rendszeresen menekülőutakat nyitnak. Az eseményenkénti
   vágásár hibáját az adaptív kód 90 körön át elfedte.

### Következmény

**Új befagyasztott konfiguráció: `v4.FROZEN_91` = hibrid+V** (a 88. kori + hibrid megbízhatóság + eseményenkénti vágásár).
A következő mérések erre vonatkoznak, és a 88. kör szabálya szerint egy negyedik, a befagyasztás után épített generátoron
kell újra tesztelni.
