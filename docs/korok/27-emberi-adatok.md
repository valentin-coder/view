# 27. kör – Emberi hiedelemrevízió és az ARLC: mit ad vissza, mit nem, és miért?

## Cél

A feladatleírás az emberi sémaváltást említi mintaként. A 7. kör a premisszát
általánosságban vizsgálta. Ez a kör konkrétabb: négy ismert pszichológiai jelenséget
szimbolikus kísérletté alakít, és megnézi, mit jósol rájuk az ARLC. **Nem emberi adatot
gyűjtöttem.** Az irodalmi eredményeket emlékezetből idézem, a pontos állításokat ellenőrizni
kell. A cél annak tisztázása, hogy egy jelenség a modellből *következik*, *egy paraméterrel
előállítható*, vagy *ellentmond* neki.

Megvalósítás: [`experiments/arlc/arlc/human.py`](../../experiments/arlc/arlc/human.py); nyers
eredmények: [`experiments/arlc/results/kor-27/results.json`](../../experiments/arlc/results/kor-27/results.json).

## (a) Melyik premisszát adjuk fel? (Elio–Pelletier-típusú feladat)

**Jelenség (ellenőrizendő):** Elio és Pelletier (1997, „Belief change as propositional update”)
olyan feladatokat adott, ahol egy feltételes szabály („ha p, akkor q”) és egy tény (p) után
kiderül, hogy nem q. A résztvevők gyakrabban vonták kétségbe a *feltételes szabályt*, mint a
tényt. Politzer és Carles (2001) hasonló eredményt kapott.

**Elrendezés:** szabály („a dax mérges”, q_r), tény („x egy dax”, q_f), ellentmondás („x nem
mérges”, q = 0,9). Változók: a világ mérete |E|, q_r, q_f, és hány megfigyelt tény támasztja
alá a szabályt (0, 2, 5). 135 konfiguráció.

**Eredmény:**

| alátámasztás | a szabályt feladja vagy kivétellel gyengíti | a tényt feladja | az ellentmondást elutasítja |
|---|---|---|---|
| 0 (absztrakt feladat) | **69%** (31/45) | 24% | 7% |
| 2 | 33% (csak kivétel, csak kis világban) | 47% | 20% |
| 5 | 33% (ugyanígy) | 47% | 20% |

**Értelmezés:**
- **Alátámasztatlan szabálynál az ARLC az emberhez hasonlóan a szabályt teszi kérdésessé.**
  Ez nem beépített preferencia. A szabály mögött nincs tömörítési haszon, ezért az elvetése
  olcsó.
- **Jóslat, ami az emberi kísérletekben tesztelhető:** ha a szabályt előtte néhány megerősítő
  példa támasztja alá, a résztvevők kevésbé adják fel. Ezt az ARLC élesen jósolja: alátámasztott
  szabályt egyszer sem adott fel. **Nem tudom, létezik-e ilyen emberi adat; ellenőrizendő.**
- **Valószínű műtermék:** kis világban (|E| ≤ 8) mindig a kivétel nyer, mert a kivétel ára
  log₂|E|. Nincs okunk azt hinni, hogy az ember a világ méretétől függően dönt így.

## (b) Sorrendhatás (Hogarth–Einhorn)

**Jelenség (ellenőrizendő):** Hogarth és Einhorn (1992) „hiedelem-kiigazítási modellje” szerint
rövid, vegyes evidenciasornál, lépésenkénti értékelésnél **recencia-hatás** lép fel: a később
kapott evidencia nagyobb súlyt kap.

**Elrendezés:** x tagsága A vagy B (diszjunkt). Két erős (0,95) A-evidencia és négy gyenge (0,7)
B-evidencia, kétféle sorrendben.

**Eredmény:**

| változat | sorrendhatás? | iránya |
|---|---|---|
| normatív ARLC (rögzített vagy tanult megbízhatóság) | **nincs** | – |
| evidencia-öregedéssel (λ ≤ 0,9) | **van** | recencia |
| öregedés + használatfüggő beágyazottság (η = 0,3, λ = 0,9) | nincs | a két hatás kioltja egymást |

**Értelmezés:**
- **A normatív ARLC sorrendfüggetlen.** A pontszám cserélhető (exchangeable), ezért az
  evidenciák sorrendje nem számít, kivéve a holtversenyt (25. kör).
- **Emberi sorrendhatás csak nem normatív kiegészítéssel jön létre:** az öregedés recenciát ad,
  a használatfüggő beágyazottság elsőbbséget (16. kör, A5). A kettő arányától függ az irány.
  Ez minőségileg egyezik Hogarth és Einhorn állításával, hogy az irány a feladattól függ.
- **Hiányosság:** tanult megbízhatóság mellett az öregedés jelenleg nincs bekötve.

## (c) Válaszok az anomáliákra (Chinn–Brewer)

**Jelenség:** Chinn és Brewer (1993, „The role of anomalous data in knowledge acquisition”) hét
válaszfajtát különít el: az adat figyelmen kívül hagyása, elutasítása, kizárása (az elmélet
hatókörén kívül esik), függőben tartása, újraértelmezése, perifériás elméletmódosítás és
elméletcsere. Azt állítják, hogy a választást befolyásolja az előzetes tudás beágyazottsága, az
adat hitelessége, az anomáliák száma és egy alternatív elmélet elérhetősége.

**Leképezés az ARLC operátoraira:**

| Chinn–Brewer | ARLC |
|---|---|
| figyelmen kívül hagyás | nincs (minden megfigyelés bekerül) |
| elutasítás | (a) megfigyelés elutasítása |
| kizárás | (c) kontextus-szétválasztás; **osztályszintű hatókör-szűkítés** (ebben a körben bevezetve) |
| függőben tartás | alternatíva a nyalábban (10. kör), ideiglenes állapot (12. kör V4) |
| újraértelmezés | a tagság elutasítása („nem is tartozik ide”, 26. kör) |
| perifériás módosítás | (d) kivétel; osztályszintű kivétel |
| elméletcsere | szabály elvetése + indukált vagy átvett alternatíva |

**1. kísérlet (1008 konfiguráció).** A tagságot vagy ugyanaz a forrás közli, mint az ellenpéldát,
vagy egy külön, régóta hiteles forrás.

| tényező | hatás, külön tagság-forrással (%) |
|---|---|
| beágyazottság N = 0 → 12 | adat elutasítása **14 → 57** |
| anomáliák száma 1 → 8 | elmélet feladása/cseréje **0 → 83** |
| hitelesség q = 0,99 → 0,7 | adat elutasítása **0 → 77** |

Ha a tagságot ugyanaz a forrás közli, az adat elutasítása és az újraértelmezés holtversenyben
van (mindkettő ugyanannak a forrásnak egy állítását utasítja el). Az osztályozó ilyenkor
újraértelmezést lát. **Ez a mérés hibaforrása volt, a külön forrású változat javítja.**

**2. kísérlet (az alternatív elmélet elérhetősége).** Első próbálkozásra egy *ellentmondó*
alternatívát adtam („egyik dax sem mérges”). **Ezt a rendszer soha nem vette át**, és az
elvetési küszöbön sem változtatott, mert az alternatíva a régi adatokkal is ütközik. Chinn és
Brewer értelmében viszont egy alternatív elmélet *mindkét* adatkészletet megmagyarázza.

**3. kísérlet (összebékítő alternatíva: „a laboratóriumi dax a dax alfaja, és nem mérges”).**
Ehhez **specifikussági elv** kell, ami az ARLC-ből hiányzott. Egy alosztály szabálya minden
tagnál ütközött az általános szabállyal, mert csak példányszintű kivétel létezett. Bevezettem
az **osztályszintű kivételt** („r nem vonatkozik a c alosztály tagjaira”), log₂|C| + 1 bites
költséggel (kapcsolóval). Eredmény (N ∈ {2, 6, 12}, 1–8 anomália):

| feltétel | viselkedés |
|---|---|
| nincs alternatíva | néhány anomália után **elveti** az elméletet |
| alternatíva (q = 0,9), osztályszintű kivétel nélkül | az „alfaj a dax része” kapcsolatot dobja el: **újraértelmezés osztályszinten** |
| alternatíva (q = 0,9), **osztályszintű kivétellel** | **átveszi** az alternatívát minden anomáliaszámnál; a régi és az új adat is megmagyarázva: **elméletfinomítás** |
| alternatíva (q = 0,7), osztályszintű kivétellel | nem veszi át; az alfaj-kapcsolatot dobja el |

**Értelmezés:**
- Az ARLC **minőségileg mind a négy Chinn–Brewer-tényezőt visszaadja**, ha a specifikussági elv
  benne van.
- **A specifikussági elv hiánya valódi tervezési hiba volt.** A nem monoton öröklés irodalmában
  (Touretzky 1986; Horty, Thomason és Touretzky 1990, ellenőrizendő) ez alapkérdés. Az ARLC v4-be
  bekerül.
- **Megszorítás:** az osztályszintű kivétel csak a szabály testénél specifikusabb, *megnevezett*
  alosztályra működik. Ha az alternatíva nem nevez meg alosztályt („bizonyos daxok nem
  mérgesek”), a rendszer nem talál osztályszintű megoldást.

## (d) Hiedelem-kitartás a hiteltelenítés után (Ross–Lepper–Hubbard)

**Jelenség:** Ross, Lepper és Hubbard (1975) szerint egy hamis visszajelzésen alapuló hiedelem
akkor is megmarad, ha később kiderül, hogy a visszajelzés hamis volt. A kitartás csökken, ha a
debriefing magát a kitartás folyamatát is elmagyarázza („folyamat-debriefing”). Anderson,
Lepper és Ross (1980) szerint erősebb, ha a résztvevő oksági magyarázatot alkotott. Mindez
ellenőrizendő.

**Elrendezés:** egy forrás hat tényt közöl („d_i mérges”). Ebből szabály indukálódik, és ez a
próbaentitásra is következtet. Ezután a forrás hitelessége 0,1-re csökken. A kísérlet
változtatja, hogy hány *független* tény támasztja alá ugyanazt (0, 2, 4, 6).

| változat | 0 független | 2 | 4 | 6 |
|---|---|---|---|---|
| konfliktus-vezérelt keresés (eredeti ARLC) | **kitart** | kitart | kitart | kitart |
| + forrásszintű lépés és indukált szabály elhagyása | **elenged** | elenged | megtart | megtart |

**Értelmezés:**
- **Az eredeti ARLC-ben a kitartás a keresés terméke.** A keresés csak konfliktusra indul, a
  hiteltelenítés pedig nem okoz konfliktust. A hiedelem ezért marad, pedig az MDL-pontszám
  szerint a feladása olcsóbb volna.
- A forrásszintű lépéssel a viselkedés racionális: a szabály akkor marad, ha legalább 4 független
  tény támasztja alá.
- **Spekulatív párhuzam:** az emberi kitartás is fakadhat abból, hogy a revíziót konfliktus
  indítja, és egy hiteltelenítés nem konfliktus. A „folyamat-debriefing” ebben az olvasatban
  kifejezetten elindítja a keresést. **Ez egy hipotézis, nem eredmény.**

## Összegzés

| jelenség | ARLC | mechanizmus |
|---|---|---|
| szabály kétségbe vonása absztrakt feladatban | **visszaadja** | alátámasztatlan szabály olcsó |
| recencia-sorrendhatás | csak **nem normatív** kiegészítéssel | evidencia-öregedés |
| Chinn–Brewer-tényezők | **visszaadja**, specifikussági elvvel | MDL + hitelesség + osztályszintű kivétel |
| hiedelem-kitartás | **csak a hiányos keresés miatt** | konfliktus-vezérelt keresés |

**A kör legfontosabb kimenete nem a pszichológiai egyezés, hanem két tervezési hiba
felismerése:** a hiányzó specifikussági elv és a hiányzó, nem konfliktus-vezérelt lépések. Mindkét
hibát az emberi jelenségek reprodukálási kísérlete hozta elő.
