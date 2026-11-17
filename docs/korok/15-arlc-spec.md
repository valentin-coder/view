# 15. kör – Az ARLC v3 szimbolikus magjának formális specifikációja

Ez a kör a 4., 10. és 13. kör döntéseit egyetlen végrehajtható specifikációba fogja össze.
A megvalósítás: [`../../experiments/arlc/`](../../experiments/arlc/) (16. kör).

## Nyelv

- **Konstansok:** entitások `E`, kategóriák `C`, tulajdonságok `P`, források `S`, idő `t ∈ ℕ`.
- **Literálok:** `isa(e, c, ±)`, `has(e, p, ±)`.
- **Szabályok (Horn-alak, egytagú törzzsel):** `isa(X, c) → isa(X, c', ±)` (alosztály vagy
  kizárás), illetve `isa(X, c) → has(X, p, ±)` (kategória-tulajdonság).
- **Séma (kemény, ismert kényszerek):**
  - diszjunkt kategóriapárok `D ⊆ C×C`;
  - kizáró tulajdonságcsoportok `g: P → G` (pl. lakhely): egy entitásnak egy időben egy
    csoportból legfeljebb egy pozitív tulajdonsága lehet;
  - csoportonkénti frissítési prior `π: G ∪ {isa} → (0,1)`, annak valószínűsége, hogy a
    csoport értéke idővel megváltozik (13. kör, U-ötlet).

## Megfigyelések és feltevések

- **Megfigyelés:** `o = (id, forrás s, idő t, hitelesség q, tartalom)`, ahol a tartalom
  egy literál vagy egy szabály.
- **Feltevés-tokenek** (ATMS-értelemben):
  - `obs(id)`: az o megfigyelés elfogadása;
  - `inst(r, e)`: az r szabály alkalmazása az e entitásra (ennek visszavonása a *kivétel*);
  - indukált szabályok: `obs(id)`, ahol id ≥ 10⁶.

## Hipotézis

`ℋ = (Rej, Exc, Iso, Cut, Ind)`, ahol
- `Rej`: elutasított megfigyelések (zajnak tekintett adat);
- `Exc`: kivételek, `(r, e)` párok;
- `Iso`: elszigetelt források, mindegyik saját kontextust kap. A k kontextus a nem
  elszigetelt források és a k forrás megfigyeléseit látja;
- `Cut`: frissítések, `(id, t_vég)`. A megfigyelés `[t_o, t_vég)` intervallumon érvényes;
- `Ind`: indukált szabályok.

## Zárás és konzisztencia

- **Zárás** `Cl(ℋ, k, t)`: a k kontextusban, t időpontban aktív megfigyelésekből
  előrefelé láncolással. Minden levezetett literál egy támaszhalmazt (feltevés-tokeneket)
  kap. Egy szabályalkalmazás támasza: a törzs támasza ∪ `{obs(r), inst(r, e)}`.
- **Konfliktus:** egy entitásra `x` és `¬x`; két diszjunkt kategória; vagy egy kizáró
  csoport két pozitív eleme. A konfliktushoz tartozó feltevéshalmaz a két támasz uniója.
- **Konzisztencia:** minden kontextusban, „most” és minden vágás előtti időpontban nincs
  konfliktus. Vágások nélkül a zárás az időben monoton, így elég a „most” ellenőrzése.

## Pontszám (bitben, kétrészes kód)

`L(ℋ) = Σ_o L_data(o | ℋ) + |Exc|·log₂|E| + |Iso|·c_ctx + Σ_{cut}(−log₂ π_g + log₂ t_most) + |Ind|·L_rule + η·Σ_{a elvesztett} uses(a)`

- **Elfogadott o:** `−log₂ q + L_tartalom`. Egy `has` tényre `L_tartalom = −log₂(1−δ)`, ha
  szabály jósolja (a tény nélkül), egyébként 1 bit. Ebből adódik a beágyazottság magától:
  egy szabály visszavonása annyi bitbe kerül, ahány tényt a szabály jósolt.
- **Elutasított o:** `−log₂(1−q) + L_tartalom(egyenletes)`. Az egyenletes tartalmi költség az
  elfogadásnál is megjelenik, ezért kiesik a különbségből.
- **Használati tag** (11. kör, hiszterézis): minden megválaszolt lekérdezés növeli a
  támaszában szereplő feltevések `uses` számlálóját. Ha egy hipotézis ezek közül valamelyiket
  elveszíti, `η·uses` büntetést kap.

## Keresés (megfigyelésenként)

1. Az új o-t a nyaláb minden hipotézise elfogadja.
2. **Javítás** legfeljebb k mélységig: amíg van konfliktus, a konfliktus minden tokenére
   jelölt módosítás készül:
   - (a/b) `obs(id)` elutasítása (megfigyelés vagy szabály);
   - (c) a token forrásának elszigetelése (kontextus-szétválasztás);
   - (d) `inst(r, e)` → kivétel;
   - (e) ha a csoport változhat, és a konfliktusban van ugyanarra az entitásra és csoportra
     egy későbbi megfigyelés, a régebbi megfigyelés vágása annak időpontjánál (frissítés).
3. **Indukció:** az o alanyának kategóriáira, ha legalább m elfogadott, szabály által nem
   jósolt, azonos előjelű tény szól egy tulajdonság mellett, és ellene egy sem, javasolt
   egy indukált szabály (Thagard 2–3. fokozat).
4. A jelöltek pontozása, a legjobb B megtartása. A legjobb hipotézis a válaszadó.

**Garantált tulajdonságok:** a legjobb hipotézis mindig konzisztens. Ha nincs konzisztens
jelölt k mélységig, a rendszer az új megfigyelést elutasítja (ez mindig konzisztens).

## Alapvonalak ugyanazon a gépezeten

| Mód | Leírás |
|---|---|
| `lookup` | csak explicit tények, következtetés nincs (a „sima memória” alapvonala) |
| `recency` | előrefelé láncolás; konfliktusnál mohón a legrégebbi megfigyelés esik ki |
| `wms` | súlyozott MaxSAT a megfigyeléseken (BeliefBank-szerű): csak elutasítás, pontszám = az elutasított megfigyelések log-esélyeinek összege |
| `arlc` | a teljes fenti specifikáció |
| `arlc-nocut`, `arlc-noctx` | ablációk |

## Viszony a revízió posztulátumaihoz

| Posztulátum | Teljesül? | Megjegyzés |
|---|---|---|
| AGM *siker* (az új információ elfogadódik) | **nem** | szándékosan: ez *nem priorizált* revízió [Hansson 1999], pontosabban hitelességkorlátos revízió [Hansson, Fermé, Cantwell, Falappa 2001] |
| AGM *konzisztencia* | igen | kemény kényszer |
| AGM *minimális változás* | **nem**, helyette MDL | a változás mérete a bitekben minimális, nem a feltevések számában |
| KM *frissítés* (U1–U8) | részben, csak a vágás operátorral | ellenőrizendő, melyik posztulátum sérül a π-priorral |

**Őszintén:** a hitelességkorlátos revízió és a nem priorizált revízió irodalma a 4. fázis
„ellenállás” követelményét már formálisan kezeli. Az ARLC ehhez az MDL-pontszámot, a
kontextusokat, a frissítést és a nyalábot teszi hozzá. Az alkotóelemek külön-külön ismertek.
