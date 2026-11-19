# 72. kör – Entitásonként memoizált zárás (viselkedésmegőrző)

## Miért

A 46. kör profilja szerint a futási idő nagyobb része a zárásban és a jelöltenkénti konfliktuskeresésben van, nem a
pontozásban. A 64. és 69. kör szerint ma ez korlátozza leginkább a kísérletek méretét (egy C-eset perceket vesz igénybe).

## A megoldás

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`_closure_by_entity`, `_closure_all`, `entity_memo`).
- Egy entitás zárása (tagságai, tulajdonságai, a szabályból levezetett literáljai) csak ezektől függ: az aktív
  szabályhalmaz, az entitás saját tényei, a saját példánykivételei, a globális osztálykivételek, és (elsőbbségnél) a
  saját kontextus-literáljai. Ezek kulcsa alatt az entitás eredménye memoizálható.
- Egy jelölt hipotézis tipikusan egyetlen tényt vagy kivételt változtat, ezért az entitások túlnyomó részének
  eredménye újrahasznosul.
- **A szótárak beszúrási sorrendje azonos a régi kódéval**, így a konfliktuskeresés sorrendje, és vele a keresés útja is
  változatlan.
- Kulcsok: a megfigyelések objektumai élnek, ezért az `id()`-jük biztonságos. Az indukált és feltalált szabályok
  objektumai eldobódhatnak (és az `id()` újrahasznosulhat), ezért azoknál tartalom-alapú kulcs. A memó minden
  megfigyelésnél ürül, és méretkorlátja van.

## Ellenőrzés

| ellenőrzés | eredmény |
|---|---|
| ekvivalencia-ellenőrzés (4 kis világ teljes nyalábja és minden válasza, PYTHONHASHSEED = 0) | **bitre egyezik** |
| kimerítő ellenőrzés (alap és v4.4e, két méret) | **25/25 mindenütt** |
| A fázis regresszió (E1–A7) | **mind azonos** |
| valódi eset, A populáció (seed 1000, hazug forrás, v4.4e) | 41,5 s → **17,4 s (2,4×)**, azonos végső hipotézis és pontszám |
| valódi eset, C populáció (seed 1000, hazug forrás, keverék-prior) | 293 s → **181 s (1,6×)**, azonos |
| kis tesztvilágok (8 entitás) | 50 s → 45 s (kb. 10%) |

A gyorsulás a világ méretével nő, mert több entitás eredménye hasznosul újra. A C-ben kisebb, mert ott a jelölt
hipotézisek gyakran szabályt (az egész tankönyv egy részét) érintenek, és ez minden entitás kulcsát megváltoztatja.

## Ami nincs még meg

- A szabály-módosítás (elutasítás, kivétel osztályszinten) ma minden entitást újraszámol. A 46. kör terve szerint csak a
  szabály törzsének tagjait kellene. Ehhez a globális kulcsot szabályonkénti, hatókör-érzékeny kulcsra kell bontani.
- A konfliktuskeresés (`_conflict`) továbbra is minden entitáson végigmegy. Ez is entitásonként memoizálható volna.
