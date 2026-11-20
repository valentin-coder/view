# 107. kör – A szabályok időbeli vágása (előregisztrált)

## 1. rész: terv, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### Miért

A G3 szabályváltozás típusában (88. kör) a világ egy szabálya egy τ időpontban megfordul. A hipotézistér eddig csak a
változó csoportú tényeket tudta időben vágni (11. kör). A szabályt nem, ezért a régi szabály és a régi tények az új
szabállyal ütköztek, és csak egy igaz megfigyelés félretevése oldotta fel őket. A 87. kori generátor-egységteszt ezt mint
a hipotézistér hiányát mutatta ki (a szabályváltozás a meglepetés után 0/10 megengedett).

### A mechanizmus (`rule_cuts`)

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`rule_cuts`, `rule_change_prior`, `_cut_events`), `v4.py` (`F91_R`).
1. **A kereső egy szabályt vagy egy statikus tényt is vághat,** ha az ütközésben egy későbbi, ugyanarról a tulajdonságról
   szóló megfigyelés van.
2. **Az ár eseményenként:** egy (tulajdonság, vég-időpont) „rendszerváltás” −log₂ ρ_r bit (ρ_r = 0,01), akárhány régi
   megfigyelést vág is (a 91. kori eseményenkénti vágásár mintájára).
3. **Időbeli szemantika:** a flag mellett minden megfigyelés csak a saját időpontjától érvényes. Egy τ − 1 időpontra
   feltett kérdésnél a τ-beli tények nem számítanak (egy időbeli tudásbázis természetes szemantikája).

Kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

### Fejlesztési ellenőrzés (már felhasznált seedek, nem teszt)

Kód: [`dev_r107.py`](../../experiments/arlc/arlc/dev_r107.py):

| | G3 szabályváltozás target / hist (23000–23005) | G3 állapotvált., hazug; G1k helyesbítés |
|---|---|---|
| v3 | 0,475 / 0,504 | – |
| FROZEN_91 | 0,496 / 0,483 | – |
| F91_R | **0,654 / 0,583** | bitre azonos a FROZEN_91-gyel |

### Előregisztráció

- **Seedek:** 37000–37014 (friss). A 96. kör 9 típusa + G3 szabályváltozás + G1k szabály-helyesbítés; 165 eset × 3 (v3,
  FROZEN_91, F91_R) + feladatcsomag (FROZEN_91, F91_R).
- Kód: [`run_r107.py`](../../experiments/arlc/arlc/run_r107.py).

**Hipotézisek:**
- **H107a (G3 szabályváltozás, target):** F91_R − FROZEN_91 > 0, a CI nem tartalmazza a nullát.
- **H107b (G3 szabályváltozás, hist):** F91_R − FROZEN_91 > 0 (pontbecslés).
- **H107c (a többi típus, post):** F91_R − FROZEN_91 ≥ −0,01 mind a négy generátoron (pontbecslés).
- **H107d (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel.

**Döntési szabály:** ha mind teljesül, az F91_R lesz az új befagyasztott konfiguráció (FROZEN_107).

## 2. rész: eredmények

Nyers adat: [`results/kor-107/`](../../experiments/arlc/results/kor-107/); elemzés:
[`analyze_r107.py`](../../experiments/arlc/arlc/analyze_r107.py) → `results/kor-107/analysis.json`. 495 futás + feladatcsomag.

| G3 szabályváltozás | target | hist | post |
|---|---|---|---|
| v3 | 0,350 | 0,651 | 0,884 |
| FROZEN_91 | 0,273 | 0,713 | 0,899 |
| F91_R | 0,369 | 0,713 | 0,902 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H107a (target):** F91_R − F91 > 0 | +0,095 [0,000; +0,257] | **nem teljesül** (a CI alsó határa 0) |
| **H107b (hist):** F91_R − F91 > 0 | 0,000 | **nem teljesül** |
| **H107c (a többi típus):** ≥ −0,01 | mind a négy generátoron bitre azonos | **teljesül** |
| **H107d (feladatcsomag):** | **A7: 1,00 → 0,75**; E2a átfordulás 2/4/6 → 2/3/3 | **nem teljesül** |

**A döntési szabály szerint az F91_R nem lesz alapértelmezés.**

### Értelmezés

1. **A szabályváltozás friss seedeken is nehéz marad.** A vágás lehetősége az esetek egy részében segít (+0,095, nem
   szignifikáns), de a lektor, aki az új szabályt hozza, új forrás. Az N prior szerint gyanús, ezért a rendszer gyakran
   inkább őt teszi félre, mint hogy a régi szabályt elvágja. A 98. kör „gyanús új forrás” költsége itt is megjelenik.
2. **Az A7-kár elvi, nem programhiba.** Az A7 a **frissítés** (a világ változott) és a **revízió** (a régi tudás téves volt)
   megkülönböztetését teszteli (Katsuno–Mendelzon, 1991). A szabály-vágás egy új olvasatot ad: „a szabály eddig igaz volt,
   mostantól nem”. Ez egy revíziós helyzetben is olcsó lehet. Egy ellentmondó új szabály mindig értelmezhető
   változásként és helyesbítésként is, és a kettőt csak háttértudás (a változás alapgyakorisága) különbözteti meg. **A
   104. kör tárcsáinak egy újabb példája:** a ρ_r (a szabályváltozás prior-esélye) dönti el, melyik olvasat nyer.
3. A G3-ban a szabályváltozás valódi változás, az A7-ben és a G1k szabály-helyesbítésében viszont helyesbítés. **A két
   esetet ugyanaz a megfigyelés-minta írja le, csak a világ alapgyakoriságai különböznek.** A ρ_r helyes értéke tehát
   környezetfüggő, és a 105. kör szerint ezt csak epizódokon átívelő tanulás tudná eldönteni.
