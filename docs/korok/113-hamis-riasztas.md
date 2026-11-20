# 113. kör – A másolásfelismerés hamis riasztása: független tanúk (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 112. kör 2. részének 4. pontja szerint a másolásfelismerés egy veszélyes helyzetben árthat. A tankönyvnek van egy hibás
szabálya. Egy bevált terepforrás a tagok valódi értékét jelentette. Egy új, **független** tanú ugyanezt közli, ahol lehet,
szó szerint ugyanazzal az állítással. A függetlenség alatt a két egyező tény legyőzi a hibás szabályt. Ha a rendszer a
tanút másolónak tekinti, a szabály nyerhet.

### Elrendezés

Új G4-típus: **független tanúk** ([`generator4.py`](../../experiments/arlc/arlc/generator4.py), `KINDS4_EXTRA2`). A tankönyv
egy véletlen hibás szabályára egy új forrás („witness”, q = 0,9) a kategória minden tagjának valódi értékét közli.
Egységteszt: 10/10 megengedett. Seedek 40000–40029 (friss). A tankönyvhiba nélküli világok (nincs célkérdés) kimaradnak.
v3, FROZEN_91, FROZEN_112. Kód: [`run_r113.py`](../../experiments/arlc/arlc/run_r113.py).

### Hipotézisek

- **H113a:** FROZEN_112 − FROZEN_91 (célkérdés, utána) ≥ −0,05 (pontbecslés): a hamis riasztás kára kicsi.
- **H113b:** a FROZEN_112 az esetek legfeljebb 20%-ában minősíti a tanút másolónak.
- **H113c:** a tanú után a célkérdés-pontosság mindhárom módszernél nő (pontbecslés).

## 2. rész: eredmények

Nyers adat és összesítés: [`results/kor-113/`](../../experiments/arlc/results/kor-113/). 90 futás; 28 világban volt
tankönyvhiba (célkérdés).

| | célkérdés előtte → utána | post | másolónak minősítve | a tanú félretett állításai |
|---|---|---|---|---|
| v3 | 0,699 → **0,866** | 0,900 | 0/28 | 0,25 |
| FROZEN_91 | 0,699 → 0,837 | 0,897 | 0/28 | 0,46 |
| FROZEN_112 | 0,699 → 0,837 | 0,897 | **0/28** | 0,46 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H113a:** FROZEN_112 − FROZEN_91 ≥ −0,05 | 0,000 (bitre azonos) | **teljesül** |
| **H113b:** ≤ 20% másolónak minősítve | 0% | **teljesül** |
| **H113c:** a tanú után nő | +0,17; +0,14; +0,14 | **teljesül** |

### Értelmezés

1. **A másolásfelismerés ebben a helyzetben nem ad hamis riasztást.** A kereső javasolja a másolást (a tanú állítása
   ütközik a hibás szabállyal, és szó szerint egyezik egy terepi jelentéssel), de nem fogadja el, mert a helyes
   egyezések elnyelése a hibás szabálynak kedvezne, és ez drágább magyarázat. **A másolás akkor nyer, ha a hamis
   értékekben való egyezést magyarázza** (Dong és mtsai, 2009), és ezt a kódhossz magától tudja.
2. A v3 itt kissé jobb (0,866 vs. 0,837). A FROZEN_91/112 a tanú néhány állítását az „új forrás” gyanú miatt félreteszi.
   Ez a 98. kör ismert költsége, nem a másolásfelismerésé.
