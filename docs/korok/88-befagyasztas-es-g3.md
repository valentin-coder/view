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

## 2. rész: eredmények

Nyers adat: [`results/kor-88/test/`](../../experiments/arlc/results/kor-88/test/); elemzés:
[`analyze_r88.py`](../../experiments/arlc/arlc/analyze_r88.py) → `results/kor-88/analysis.json`. 240 futás, eltérés nincs.

### Az előregisztrált mérés

| | pre | post | állapotvált. target / hist | szabályvált. target / hist | elavult target | hazug target |
|---|---|---|---|---|---|---|
| **v3** | **0,926** | **0,889** | 0,250 / 0,683 | 0,177 / 0,796 | 0,282 | 0,731 |
| v4.4e | 0,860 | 0,829 | 0,225 / 0,683 | 0,268 / 0,668 | 0,342 | 0,806 |
| befagyasztott | 0,849 | 0,822 | 0,192 / 0,417 | 0,193 / 0,801 | **0,420** | **0,875** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H88a (post):** befagyasztott − v3 > 0 | **−0,066** [−0,118; −0,020] | **nem teljesül, fordítva** |
| **H88b (hazug, target):** befagyasztott − v3 > 0 | **+0,144** [+0,081; +0,213] | **teljesül** |
| **H88c (szabályváltozás):** hist ≤ 0,5 és target ≥ 0,7 | hist 0,801, target 0,193 | **nem teljesül, ellenkező irányban** |
| **H88d (állapotváltozás):** target és hist ≥ 0,8 | 0,192 és 0,417 | **nem teljesül** |
| **H88e (elavult, target):** befagyasztott − v3 ≥ 0 | +0,138 [+0,007; +0,270] | **teljesül** |

**A befagyasztott konfiguráció a harmadik generátoron az általános pontosságban a v3 alatt van** (pre −0,077, post −0,066).
A forrás-felismerés (hazug, elavult) itt is a v3 fölött van. A 77. kör eredménye tehát egy *befagyasztott*
konfigurációval, egy harmadik generátoron megismétlődött.

### Mi okozta (az audit szerint)

A befagyasztott konfiguráció a meglepetés előtt esetenként **29,3 igaz terepi jelentést tesz félre** (v3: 4,8; v4.4e: 3,0).
A terepforrás bűnbakká válik. A G3-ban az állapotváltozások miatt sok régi és új állapotjelentés ütközik, és ezek
feloldására a legolcsóbb út az, hogy a 150 állítású terepforrás „szemét” módba kerül (az N keverék-prior
szemét-komponense: π = 0,999 mellett kb. 10 bit belépő, utána olcsó tömeges félretevés).

### Feltáró rész (nem előregisztrált, ugyanazokon a seedeken)

Kód: [`explore_r88.py`](../../experiments/arlc/arlc/explore_r88.py), [`analyze_x88.py`](../../experiments/arlc/arlc/analyze_x88.py)
→ `results/kor-88/explore_analysis.json`. Két tényezőt választottam szét: (a) a séma állapotváltozási priorja (az
előregisztrált G3-ban 0,05; a valódi változási gyakoriság sokkal nagyobb: az entitások 30%-a vált a folyam közben), (b) az
N keverék-prior.

| | upd | pre | post | téves terepi félretevés | állapotvált. target / hist | hazug target |
|---|---|---|---|---|---|---|
| v3 | 0,05 | 0,926 | 0,889 | 4,8 | 0,250 / 0,683 | 0,731 |
| befagyasztott | 0,05 | 0,849 | 0,822 | **29,3** | 0,192 / 0,417 | 0,875 |
| befagyasztott − N | 0,05 | 0,862 | 0,836 | 3,1 | 0,225 / 0,683 | 0,844 |
| v3 | 0,3 | **0,929** | **0,900** | 2,2 | 0,292 / **0,833** | 0,756 |
| befagyasztott | 0,3 | 0,899 | 0,882 | 1,0 | **0,875** / 0,792 | **0,894** |
| befagyasztott − N | 0,3 | 0,899 | 0,859 | 1,0 | **0,875** / 0,792 | 0,831 |

- upd = 0,3 mellett: befagyasztott − v3 (post) = −0,017 [−0,056; +0,012] (n.s.); (pre) = **−0,029** [−0,047; −0,014].

### Értelmezés

1. **A G3 tervezésében hibát követtem el, a 87. kör saját szabályát megsértve.** Csak a megengedettséget ellenőriztem,
   az igaz hipotézis árát nem. A séma állapotváltozási priorja (0,05) sokkal kisebb a G3 valódi változási
   gyakoriságánál. Egyetlen új állapotjelentés félretevése (log₂(0,9/0,1) ≈ 3,2 bit) így olcsóbb, mint egy vágás
   (−log₂ 0,05 ≈ 4,3 bit), ezért **egyik módszer sem fogadja el az állapotváltozást** (H88d). Ez a benchmark
   kalibrációs hibája, nem a rendszeré. Kalibrált priorral (0,3) a befagyasztott konfiguráció az állapotváltozásokat jól
   kezeli (0,875 vs. a v3 0,292).
2. **Az N keverék-prior egy rosszul árazott világban menekülőúttá válik.** A 29,3 téves terepi félretevéshez mindkét
   tényező kell: a rosszul kalibrált változási prior (sok ütközés) és a szemét-komponens (olcsó tömeges kiút). Ez a 79.
   kör félrespecifikációs mintája, ötödször: **a szemét-komponens a G1k-n és a G2-n ártalmatlan volt, mert ott nem volt
   olyan tömeges ütközés, amelyet egy nagy forrás „szemétté” nyilvánítása olcsóbban feloldott volna.**
3. **A rendszer kalibrált priorral is rosszabb a v3-nál a meglepetés előtt** (pre −0,029, szignifikáns), és ezt nem
   diagnosztizáltam. Az általános pontosság előnye tehát három generátor után sem áll: G1k-n igen, G2-n a PK óta igen,
   G3-on nem.
4. **A szabályváltozásnál a rendszer a régi szabályt tartja meg** (hist 0,80, target 0,19). Az új szabályt hozó lektor
   az N szerint „új forrás”, ezért gyanús. A szerkezeti hiány (a szabályok nem vághatók időben) valódi, de a jóslatom az
   irányáról téves volt.
5. **Ami három generátoron át áll:** a megbízhatatlan forrás felismerése (hazug: G1k +0,06 – +0,15, G2 +0,07 – +0,10,
   G3 +0,14; elavult forrás G3 +0,14). Ez az egyetlen képesség, amely minden generátoron, előregisztráltan, friss
   seedeken a v3 fölött van.
