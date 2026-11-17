# 33. kör – Származás-tudatos kommunikáció: a visszhang-polarizáció megszüntetése

## Kérdés

A 31. körben a hiedelmek továbbadása két klikkben **100%-os polarizációt** okozott, κ-tól és zajtól
függetlenül. Az ok: a társak a saját tankönyvükből *levezetett* állításokat mondták, és a címzett
ezeket független megfigyelésnek vette (visszhang, kettős számolás). A nyers megfigyelések
továbbadása ezt nagyrészt megszüntette, de kis κ és gyenge evidencia mellett maradt polarizáció.

**Ötlet:** a közölt hiedelem *hordozza a támaszát*. Az ágens a levezetett hiedelem helyett annak
eredeti alátámasztásait adja tovább, az eredeti forrással: a privát érzékelést az érzékelő nevével,
a tankönyvi szabályt a tankönyv nevével. A címzett az azonos forrásból érkező azonos tartalmat
kiszűri. Ez a 15. kör ATMS-támaszhalmazainak ágensek közötti kiterjesztése.

Kód: `provenance` és `share="provenance"` a [`multiagent.py`](../../experiments/arlc/arlc/multiagent.py)-ban;
eredmény: [`results/kor-33/results.json`](../../experiments/arlc/results/kor-33/results.json).

## Eredmények (6 ágens, 12 kör, 3 seed)

| továbbadás | hálózat | ε | κ | igaz | polarizált | entitásszintű pontosság A / B |
|---|---|---|---|---|---|---|
| hiedelem | klikkek | 0,1–0,45 | bármely | 0,50 | **100%** | 1,00 / 0,00 |
| nyers | klikkek | 0,3 | 3 | 0,72 | 33% | 0,99 / 0,75 |
| nyers | klikkek | 0,45 | 3 | 0,61 | 67% | 1,00 / 0,50 |
| nyers | klikkek | 0,45 | 30–100 | 0,61–0,67 | 0% | 1,00 / 0,69–0,73 |
| **származás** | teljes | 0,1–0,45 | bármely | **1,00** | **0%** | 0,99–1,00 / 1,00 |
| **származás** | klikkek | 0,1–0,3 | bármely | **1,00** | **0%** | 0,99–1,00 / 0,99–1,00 |
| **származás** | klikkek | 0,45 | 3 | 0,94 | 0% | 1,00 / 0,94 |
| **származás** | klikkek | 0,45 | 30–100 | **1,00** | **0%** | 1,00 / 0,99 |

## Értelmezés

1. **A származás-tudatos továbbadás minden konfigurációban megszünteti a polarizációt**, és a nyers
   továbbadásnál is jobb. Ennek két oka van:
   - kiszűri a kettős számolást (a 31. kör első mechanizmusa);
   - **a tankönyvi szabály mint egyetlen forrás állítása jut el a másik táborba.** A B ágens nem
     „sok A-tagot” hall, hanem egyetlen A-tankönyvet és sok független érzékelést, és ezek ellenőrizhetők.
2. **A bizalomtanulás okozta polarizáció (31. kör, második mechanizmus) is eltűnik.** A
   származás-tudat mellett a táborok nem egymás *személyére* tanulnak bizalmat, hanem az eredeti
   forrásokra (érzékelők, tankönyvek), és ezek közül az érzékelők a többséget alkotják.
3. **A 20. kör „függetlenségi jele” így konkrét lett:** két állítás független, ha a támaszhalmazuk
   diszjunkt. Ha a támasz kommunikálható, nincs szükség becslésre.

## Korlátok és kapcsolódás

- **Erős feltevés:** a támasz hiánytalanul és hamisítatlanul kommunikálható. Valódi kommunikációban
  ez ritkán igaz, és egy támadó hamis támaszt is mellékelhet. Ilyenkor a származás maga is egy
  ellenőrizendő állítás.
- **Hallomás-szabály a jogban:** a bíróság az eredeti tanút akarja hallani. Ez ugyanez az elv.
- **A tudományos hivatkozás gyakorlata** is ezt teszi: egy állítás a forrásával együtt kerül
  továbbadásra. Ennek hiánya az idézési láncok torzulása, amelyről ismert esettanulmányok vannak
  (pl. „citation distortion”, Greenberg 2009, ellenőrizendő).
- A 40. kör szerint egyetlen eset sok tanújának súlya korlátos. Ez a származás hiányának kárát
  *egy* esetre korlátozza; a 31. körben a kár azért volt nagy, mert sok különböző esetről szólt.
