# 88. kör – Befagyasztott konfiguráció egy harmadik, időben változó generátoron (előregisztrált)

## 1. rész: befagyasztás, a generátor és az előregisztráció (a G3-on végzett első futtatás előtt commitolva)

### A befagyasztás

A 84. kör szerint a 78–86. kör javításait (PK, forrás-prior) ugyanazokon a generátorokon diagnosztizáltam és mértem. A
generátor-illesztést csak egy olyan generátor zárhatja ki, amelyen a konfigurációt nem hangoltam. **A befagyasztott
konfiguráció** (`v4.FROZEN_88`, a 86. kör commitjában, a G3 commitja előtt):

> v4.4e + tankönyv-keverék (π = 0,999; κ₁ = 30) + prioritás-kivétel javított kódhosszal (PK) + „új forrás” keverék-prior (N).

**Őszinte megjegyzés a sorrendről:** a G3 kódját a 86. kör futása alatt írtam, a befagyasztás előtt. Rajta a rendszer
**keresése és pontozása nem futott.** Csak a generátor-egységteszt (87. kör: zárás + ütközés, keresés nélkül) futott, hogy a
világok megengedettségét ellenőrizzem. A befagyasztott konfiguráció egyetlen paraméterét sem választottam a G3
ismeretében. Az egyetlen G3-függő döntés a tankönyv π-je (0,999, „normál tankönyv”), amely a G1-A-val azonos.

### A harmadik generátor (G3): időben változó világ

Kód: [`generator3.py`](../../experiments/arlc/arlc/generator3.py). Eltér a G1-től és a G2-től:
- **változó állapot:** minden entitásnak van egy kölcsönösen kizáró állapota (st0, st1, st2; változó csoport, update-prior
  0,05). Az entitások 30%-a a folyam közben állapotot vált. A terepforrás két időpontban jelenti az aktuálisat;
- **a világ szabálya is változhat** (valódi változás egy τ időpontban, nem tankönyvhiba);
- **kalibrált források** (deklarált = valódi hitelesség), a 87. kör G1k-tanulsága alapján;
- **sekély, konzisztens hierarchia** (két nem diszjunkt csúcs, hat levél egy szülővel), és kis valódi kivételarány (2%
  tulajdonságonként).

Meglepetések (τ = 31):
1. **állapotváltozás:** 6 entitás állapotot vált; a terepforrás az újat közli;
2. **szabályváltozás:** egy levélkategória egy szabálya megfordul; a lektor közli az új szabályt, és 4 tag friss ténye mutatja;
3. **elavult forrás:** egy archívum a mostani időbélyeggel 6 entitás *régi* állapotát közli;
4. **hazug forrás:** 8 hamis statikus tény (kontroll).

Értékelés: post-acc (most), célkérdés-acc (most), **történeti célkérdés-acc** (τ − 1 időpontban), audit (a megfigyelés saját
időpontjának igazsága szerint).

### A generátor-egységteszt eredménye (87. kör szabálya; 23000–23009)

| típus | a meglepetés előtt | a meglepetés után |
|---|---|---|
| állapotváltozás | 10/10 megengedett | 10/10 |
| elavult forrás | 10/10 | 10/10 |
| hazug forrás | 10/10 | 10/10 |
| **szabályváltozás** | 10/10 | **0/10** |

**A szabályváltozás a meglepetés után nem megengedett,** mert az ARLC hipotézistere a szabályokat nem tudja időben elvágni
(vágás csak változó csoportú tényekre van, 11. kör). A régi szabály és a régi tények az új szabállyal ütköznek, és ezt
csak egy igaz megfigyelés félretevése oldja fel. **Ez nem generátorhiba, hanem a hipotézistér ismert hiánya, és a G3 ezt
szándékosan méri.** A jóslatom ennek megfelelő (H88c).

### Elrendezés

- **Seedek:** 24000–24019 (friss). 4 típus × 20 seed = 80 eset.
- **Módszerek:** v3, v4.4e, befagyasztott (FROZEN_88). Kód: [`run_r88.py`](../../experiments/arlc/arlc/run_r88.py).
- **Elemzés:** seedenként a típusokra átlagolva, világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

- **H88a (post-acc, mind a négy típus):** befagyasztott − v3 > 0, a CI nem tartalmazza a nullát. (A v4-előny külső
  érvényessége egy harmadik generátoron.)
- **H88b (hazug forrás, target):** befagyasztott − v3 > 0, a CI nem tartalmazza a nullát (a sorozat legrobusztusabb
  képessége).
- **H88c (szabályváltozás, történeti célkérdések, előre jelzett kudarc):** a befagyasztott konfiguráció történeti
  pontossága ≤ 0,5, és a jelenbeli célkérdés-pontossága ≥ 0,7. Az új szabályt elfogadja, a régit félreteszi, így a
  múltat „átírja”.
- **H88d (állapotváltozás):** a befagyasztott konfiguráció jelenbeli és történeti célkérdés-pontossága is ≥ 0,8 (a
  vágás-mechanizmus állapotokra működik).
- **H88e (elavult forrás, target):** befagyasztott − v3 ≥ 0 (pontbecslés).

**Értelmezés előre:** ha H88a nem teljesül, a v4 általános előnye a G1k-ra és a G2-re illesztett. Ha H88b sem teljesül, a
forrás-felismerés sem általános. H88c sikeres teljesülése (a kudarc) a következő hiányzó primitívet jelöli ki: a
szabályok időbeli vágását.
