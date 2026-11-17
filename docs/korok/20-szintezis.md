# 20. kör – Szintézis: hol kell elvben az LLM?

## A program állása

| Kérdés | Állapot | Hol |
|---|---|---|
| Globálisan átrendez-e egy szimbolikus réteg, gradiens nélkül, kevés kollaterális kárral? | **igen**, szimbolikus bemeneten | 16. kör, E1 |
| Többet ad-e az ARLC, mint egy BeliefBank-szerű súlyozott MaxSAT? | **részben**: alosztály-csere, anomália-tűrés, zajtűrés; egyszerű esetekben nem | 16. kör |
| Ellenáll-e arányosan a beágyazottsággal? | **igen**, lineárisan | 16. kör, E2a/E2b |
| Különbséget tud-e tenni frissítés és revízió között? | **igen**, orákulum-priorral | 16. kör, A7 |
| Eldönti-e magától, hogy kontextus vagy hazug? | **nem, elvben sem** | 17. kör |
| Elválasztja-e a becsületes evidenciát a támadótól? | **részben**: múlttal igen, sybilek ellen nem | 19. kör |
| Bármi a fagyasztott LLM-ről? | **semmi**, a B fázis blokkolt (hálózat) | 14. kör |

## A két strukturális gyengeség

1. **A helyi kiút.** A rendszer következetesen a legolcsóbb, helyi magyarázatot választja:
   „ez a példány nem is tartozik ide”. Ez két helyen is megjelent:
   - a 16. körben: két ellentmondó általános szabály soha nem ütközött, mert mindig olcsóbb
     volt egy tagságot eldobni (szabályszintű ütközéssel javítva);
   - a 19. körben: az ellenpélda forrását soha nem vizsgálta, mert a tagság felülbírálása
     olcsóbb volt.

   **Általános tanulság:** egy MDL-alapú revízió ott fog „csalni”, ahol a legkevesebb
   evidencia van, vagyis az új, kevéssé ismert entitásoknál. Pont ott kellene a legóvatosabbnak lennie.
2. **Identifikálhatóság.** Bizonyos döntéseket az adat elvben nem határoz meg:
   - kontextus vagy hazug (17. kör);
   - egy forrás vagy sok független forrás (19. kör, sybil);
   - frissítés vagy revízió, ha nincs változékonysági prior (16. kör, A7: orákulumot kapott).

## Újrakeretezés: az LLM ott kell, ahol az adat nem dönt

Az 5. körben a kérdés az volt, hogy *pótolható-e* az LLM (L1 lyuk). A kísérletek most egy pontosabb
választ adnak: **az LLM ott nélkülözhetetlen, ahol a szimbolikus adat információelméletileg
kevés.** Ez három konkrét helyet jelent:

| Hely | Mit kell eldönteni | Mit adhat az LLM | Hol mérhető |
|---|---|---|---|
| **Kontextus-jel** | más kontextusról beszél-e a forrás, vagy téved / hazudik | a szöveg kontextusjellemzői (téma, műfaj, hely, idő) az aktivációkból; az 5. kör F-ötlete | E3 + LLM |
| **Függetlenségi jel** | ugyanaz a szerző/kampány áll-e több „forrás” mögött | stílus- és tartalomhasonlóság az aktivációkból (szerzőazonosítás) | E5 + LLM |
| **Változékonysági prior** | változhat-e idővel egy tulajdonság | „Változhat-e X idővel?” az LLM tudásából | A7 + LLM |
| *(korábban)* **Következmény-motor** | mi következik egy kategóriaváltásból ismert fogalmakra | KTP-transzplantáció | KTP (6. kör) |

**Ez új, cáfolható követelmény a „neuro” félre:** az LLM-nek nem a groundingban kell jobbnak
lennie egy parsernél (az 1. fázis R5-ös kérdése). Elég, ha **ezt a három jelet** jobban adja,
mint egy szöveges heurisztika. A jelek közül kettő (kontextus és függetlenség) nem is
nyelvtani elemzés: a szövegből nem *kiolvasható*, hanem *becsülhető*. Ez reálisabb esély
az aktivációk hozzáadott értékére, mint a tripletkinyerés.

**Legközelebbi munkák, ellenőrizendők:**
- szerzőazonosítás nyelvimodell-beágyazásokkal (stilometria);
- összehangolt, nem hiteles viselkedés felismerése (coordinated inauthentic behavior);
- forrásmegbízhatóság a tényellenőrzésben.

## Mit lehet ebből most, modell nélkül tesztelni?

**A követelmény levezetését.** Szimulálható egy zajos jel adott pontossággal (pl. „ez a forrás
más kontextusról beszél”, helyes valószínűsége a). Megmérhető, mekkora a minimális pontosság,
amely mellett az ARLC döntése (szétválaszt vagy elutasít; becsületes vagy sybil) megbízhatóan
helyes. **Ez konkrét számszerű célt ad a B fázisnak:** „az LLM kontextus-jelének AUC-ja legalább
X legyen”. Ha egy valódi LLM-jel ezt nem éri el, a „neuro” félnek nincs értelme. Ez a 21. kör.

## Mi változik az architektúrában (ARLC v4 vázlat)

1. **Jelbemenetek a pontszámba:**
   - `c_ctx(s) = c_ctx₀ − log₂ LR_ctx(s)`, ahol LR_ctx a kontextus-jel valószínűséghányadosa;
   - a megerősítő források száma függetlenségi súllyal: `n_eff = Σ` (1 − hasonlóság);
   - a vágás költsége `−log₂ π(g)`, ahol π(g) az LLM-től jön.
2. **A helyi kiút elleni védelem:** egy tagság elutasítása ne legyen olcsóbb egy *új*
   entitásnál, mint egy régi, jól ismert entitásnál. Egyszerű változat: a tagság-elutasítás
   minimális költsége legyen legalább `−log₂(1 − q_s)` *plusz* a tagság forrásának és az
   anomália forrásának közös megbízhatósági tagja. Ez a 19. körben az első változat hibáját
   kijavítaná. **Nyitott: ez ad hoc vagy MDL-ből levezethető?** Ezt a következő körök egyikében
   meg kell vizsgálni.
