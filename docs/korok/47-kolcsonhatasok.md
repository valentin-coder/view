# 47. kör – A v4 két kölcsönhatásának oka, és a 30. kör helyesbítése

A 43. kör ablációja két kölcsönhatást talált, amelyek okát ott még nem azonosítottam. Mindkettő
mögött egy elvi kérdés van, és a második egy korábbi eredményt is módosít.

## 1. kölcsönhatás: tanult megbízhatóság × deklarált állításonkénti hitelesség (A7)

**Tünet:** az A7 feladat revízió-ágában (madár → hal, a hal-állítás 0,95, a madár-állítás 0,9
hitelességű) tanult megbízhatóság mellett 5-ből csak 3 eset helyes.

**Ok:** a béta-binomiális kód (17. kör) **forrásonként egyetlen** előzetes hitelességet használ, a
forrás első megfigyelésének deklarált q-ját. A hal-állítás forrásának első megfigyelése egy
lakhely-állítás (0,9), ezért a hal-állítás deklarált 0,95-je elvész. A két revízió így pontos
holtversenybe kerül, és a döntés önkényes.

**Elvi kérdés:** egy forrás egyes állításai lehetnek biztosabbak a többinél (pl. egy szakértő a
saját területén). A homogén forrásmodell ezt nem tudja kifejezni. **Két lehetséges javítás:**
- az állításonkénti deklarált hitelesség a forrás-szintű megbízhatóság *módosítójaként*:
  `logit P(helyes) = logit r_s + (logit q_i − logit q̄_s)`. Ez már nem béta-binomiális, a
  kódhosszt közelíteni kell;
- vagy a forrás állításait téma szerint külön paraméterre bontani, ahogy a kétszintű hitelesség az
  elméletet és az adatot (32. kör). Ehhez a témát (pl. tulajdonságcsoportot) kell ismerni.

**Állapot:** nyitott. A v4-ben ez egy ismert korlát.

## 2. kölcsönhatás: forrásszintű lépés × kategória-feltalálás

**Tünet:** a forrásszintű lépéssel a feltalált kategória általánosítása 1,00-ról 0,00-ra esik az új,
csíkos daxokon (a sima daxokon 1,00 marad).

**Ok:** a forrásszintű lépéssel együtt bekapcsol az *indukált szabályok elhagyása* is (27. kör, a
hiedelem-kitartás ellen). Ez kidobja a feltalált `c′ → nem mérges` szabályt, mert m = 4 anomália
mellett a szabály modellköltsége nagyobb, mint a megtakarítása. A kategória és az osztályszintű
kivétel megmarad, így az új csíkos daxokról a válasz: „nem tudom”.

**Ez a teljes célfüggvény szerinti optimum.** A 30. körben a keresés ezt a lépést nem vizsgálta,
ezért talált egy *rosszabb* pontszámú, de jobban általánosító hipotézist.

**Zárt alakú küszöb:** a feltalált szabály akkor éri meg, ha
`m · (1 + log₂(1 − δ)) > log₂(2·|C|·|P|)`, itt `m > 6 / 0,926 ≈ 6,5`.

**Mért (az elhagyó lépéssel, 2 seed):**

| N | m = 4 | 5 | 6 | **7** | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|
| 8 | 0,00 / 1,00 | 0,00 / 1,00 | 0,00 / 1,00 | **1,00 / 1,00** | 1,00 / 1,00 | 1,00 / 1,00 | 1,00 / 1,00 |
| 12 | 0,00 / 1,00 | 0,00 / 1,00 | 0,00 / 1,00 | **1,00 / 1,00** | 1,00 / 1,00 | 1,00 / 1,00 | 1,00 / 1,00 |

(cellák: általánosítás az új csíkos / sima daxokra)

A küszöb pontosan a jósolt m = 7.

## A 30. kör helyesbítése

A 30. kör azt állította, hogy N ≥ 8 mellett **4 anomáliától** a rendszer feltalálja a kategóriát, és
tökéletesen általánosít. **Helyesen:**
- a teljes célfüggvény szerint **7 anomália** kell a feltalált *szabály* (c′ → ¬p) megtartásához;
- **4–6 anomália mellett** az optimum: a kategória (c′) és az általános szabály hatókör-szűkítése
  megmarad, de c′-ről a rendszer nem állít semmit. Ez a Chinn–Brewer-féle *kizárás*;
- a 30. körben mért 4 anomáliás általánosítás **keresési műtermék** volt.

**A helyesbítés tartalmi következménye:** a rendszer *először kizár* („ezekről nem tudunk
semmit”), és csak több anomália után *alkot* új szabályt. Ez a sorrend ismerős a tudományos
gyakorlatból. Kérdés, hogy az emberi fogalomalkotás is ilyen kétlépcsős-e, vagy hamarabb
általánosít. Ellenőrizendő.

## A módszertani tanulság (harmadszor)

Ez már a harmadik eset, ahol egy *bővebb keresés* vagy egy *új lépés* egy korábbi eredményt
megváltoztatott (16. kör: visszahelyezés; 36. kör: szűkített visszahelyezés; most: az elhagyó
lépés). **Egy MDL-rendszer viselkedését nem a célfüggvény, hanem a célfüggvény és a lépéskészlet
együtt határozza meg.** Ha egy eredmény csak azért áll fenn, mert a keresés egy lépést nem
vizsgál, az eredmény nem a modellről, hanem a keresésről szól. A kimerítő ellenőrzés (36. kör) kis
feladatokon ezt kiszűri; a nagyobb feladatokon (mint a 30. körben) csak a lépéskészlet
bővítésével derül ki.
