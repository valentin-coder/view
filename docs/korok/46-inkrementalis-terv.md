# 46. kör – Inkrementális zárás és pontozás: terv, és egy rejtett akadály

(Ez a kör egyelőre **terv**. A megvalósítás a 44. kör lezárása után jön, mert a befagyasztott v4-et
nem érintheti.)

## Miért kell

A 42. kör szerint egy meglepetés feldolgozása a gyorsítások után is a hétköznapi megfigyelés
idejének kb. ezerszerese. A jelölt hipotézisek száma (kb. 10³–10⁴) szorozva a hipotézisenkénti
költséggel (zárás, ütközés-ellenőrzés, pontszám, mindegyik O(n) a megfigyelések számában) adja ki a
teljes időt. A 10. kör ígérete (a kúppal lineáris átrendezés) csak akkor teljesülhet, ha a
hipotézisenkénti költség **O(|érintett entitások| + |szabályok|)**, és nem O(n).

## Terv

1. **Az érintett entitások statikus és szülő-alapú meghatározása.** Egy jelölt H′ a szülő H-tól egy
   kis módosításban tér el:
   - egy tény elutasítása vagy visszavétele: az alanya;
   - egy szabály (r: b → …) elutasítása, visszavétele, indukciója: azok az entitások, amelyeknek b a
     *szülő* zárásában kategóriája. Ez körmentes kategóriagráfon pontos, mert b-tagság nem függ r-től;
   - példányszintű kivétel (r, e): {e};
   - osztályszintű kivétel (r, c): a c-tagok a szülő zárásában;
   - kontextus vagy vágás változása, illetve ciklust okozó szabály (pl. a 28. kör 7. fokozatának
     kölcsönös egyesítése): **visszaesés a teljes számításra.**
2. **Entitásonkénti zárás:** a zárás felbontása entitásonkénti függvényre (a tények alany szerint
   csoportosítva, a szabályok törzs szerint). A jelölt zárása a szülőé, az érintett entitások
   újraszámolva.
3. **Pontszám-különbség:** `L(H′) = L(H) + Σ_{érintett entitások tényei} Δtag + Σ_{változott források} Δbéta + Δszerkezet`.
   A béta-tag forrásonként csak a (n, k) számlálótól függ, a kivétel-prior tag az érintett
   alkalmazásoktól.

## A rejtett akadály: a konfliktus kiválasztásának sorrendje

A jelenlegi kód az „első” konfliktust a zárás belső dict-jeinek **beszúrási sorrendjében** keresi.
Ez a sorrend az összes tény és szabály feldolgozási sorrendjéből adódik. A keresési fa azon a
konfliktuson ágazik el, amelyiket elsőként talál. **Egy inkrementális zárás ezt a sorrendet nem
reprodukálja**, így a keresés útja eltérhet. Ugyanolyan pontszámú optimumok között (holtverseny)
a végeredmény is eltérhet, még ha a keresés helyes is.

**Következmény:**
- az inkrementális változat csak **kanonikus konfliktussorrenddel** (pl. entitásnév szerint) lehet
  determinisztikus;
- ez **megváltoztatja** a már befagyasztott és előregisztrált v4 viselkedését, ezért csak külön
  kapcsolóként vezethető be;
- **elfogadási kritérium:**
  1. a kimerítő ellenőrzésen (36. kör) ugyanannyi optimális eset (25/25);
  2. az inkrementális és a teljes pontszám minden kiértékelt hipotézisen egyezik (beépített
     önellenőrzés, debug módban);
  3. a 44. kör benchmarkján a fő végpont (post-acc) eltérése az eredeti v4-től a bootstrap-zajon
     belül van;
  4. a 42. kör méretein a meglepetés ideje a kúp méretével közel lineárisan skálázódik, a tudásbázis
     méretétől közel függetlenül.

## Ami ebből már most következik

- **Holtverseny és sorrendfüggés** (17., 25. kör): a végeredmény holtversenyes optimumok között
  az implementáció belső sorrendjétől is függhet, nem csak a megfigyelések sorrendjétől. Egy
  reprodukálható rendszerhez kanonikus holtverseny-feloldás kell. Az ideális megoldás az, ha a
  rendszer *jelzi* a holtversenyt (több, egyformán jó magyarázat), és nem választ csendben.
  Ez a 13. kör aktív kérdezésének természetes indítóeseménye.

## Megvalósítás (a 45–49. kör közben): mérés előbb, optimalizálás utána

**A terv rossz pontot célzott.** Egy 12 entitásos procedurális világ v4-futásának profilja (cProfile):

| tétel | idő (az összes 63 s-ból) |
|---|---|
| `_score` (a pontozás, amelyet a terv inkrementálissá tett volna) | **kb. 5,8 s (9%)** |
| zárás (`closure`, kb. 86 ezer új zárás + 825 ezer gyorsítótár-találat) | kb. 19 s |
| mohó befejezés: jelöltenként helyi költség + `str(kulcs)` holtverseny-feloldás | kb. 20 s |
| `dataclasses.replace` (2,7 millió hipotézis-másolat) | kb. 12 s |

**Viselkedésmegőrző gyorsítások** (alapértelmezés, kapcsoló nélkül):
1. a mohó lépés `str(kulcs)` holtverseny-feloldása csak a legolcsóbb holtversenyesekre számolódik (a
   `min` eredménye változatlan);
2. gyors `replace` a hipotézisre (ugyanazok a mezők, `__init__` nélkül).

**Ellenőrzés:** 4 kis világ teljes nyalábja (kanonikus kulcs, pontszám 10⁻⁹-re) és minden válasza
**bitre egyezik** rögzített hash-seed mellett ([`equiv_check.py`](../../experiments/arlc/arlc/equiv_check.py)).
Idő 91 s → 50 s (**1,8×**). A kimerítő ellenőrzés minden konfigurációra 25/25.

**Kipróbált és elvetett:** a mohó befejezés pontos memoizálása köztes állapotonként (a lépéskeret
figyelembevételével). Egyezik, de csak 3% nyereség, mert a mohó utak ritkán futnak össze.

**Mellékes, de fontos megfigyelés:** az eredeti ujjlenyomat két folyamat között **eltért**, mert a
`repr(frozenset)` sorrendje a hash-seedtől függ, és a mohó holtverseny-feloldás ugyanezt a `str`-t
használja. A kanonikus ujjlenyomattal a 4 világon az eredmény hash-seedtől független volt, de egy
holtversenyes esetben a végeredmény elvben folyamatonként eltérhet. **A kanonikus konfliktus- és
holtverseny-sorrend tehát nem csak az inkrementális változathoz, hanem már a reprodukálhatósághoz is kell.**

**Ami valóban inkrementálissá teendő:** a zárás (entitásonként) és a jelöltenkénti konfliktuskeresés,
nem a pontszám. Ez a 46. kör eredeti tervének 1–2. pontja. A 3. pont (pontszám-különbség) másodlagos.
