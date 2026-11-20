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
