# 18. kör – Korrelált zaj: amit a konzisztencia nem lát

## Kérdés

A 16. kör E4 kísérletében a zaj független és egyenletes volt. Az 1. fázis szerint egy valódi
grounding-hiba korrelált: a modell egy entitást a *rokon* kategóriába sorol, és ezzel együtt
annak minden tulajdonságát is „látja”. Mit tesz ilyenkor az ARLC?

## Elrendezés (E4b)

- **Független zaj:** a tagság véletlen levélre kerül, a tények előjele egymástól függetlenül
  fordul meg (a 16. kör E4-e).
- **Korrelált zaj:** a zajos entitás a testvérlevélbe kerül, és *minden* tényét a testvérlevél
  igazsága szerint jelentik. Ez egy következetesen hibás világ.
- **Források:** egy forrás, vagy két egymástól független forrás (külön zajjal).
- **Módszerek:** `wms`, ARLC rögzített és tanult (κ = 30) megbízhatósággal; 3 seed.
- Nyers eredmények: [`experiments/arlc/results/kor-17-21/e4b/results.json`](../../experiments/arlc/results/kor-17-21/e4b/results.json).

## Eredmények (pontosság / szerkezeti átrendezés 50 megfigyelésenként)

| zaj | források | ε | wms | ARLC | ARLC tanult megb. |
|---|---|---|---|---|---|
| független | 1 | 0,05 | 0,86 / 0,13 | **0,97** / 0,13 | 0,94 / 0,00 |
| független | 1 | 0,10 | 0,80 / 0,13 | **0,94** / 0,13 | 0,95 / 0,13 |
| független | 1 | 0,20 | 0,68 / 0,63 | **0,80** / 0,63 | 0,80 / 1,14 |
| független | 2 | 0,05 | 0,95 / 0,16 | **0,99** / 0,00 | 0,99 / 0,00 |
| független | 2 | 0,20 | 0,88 / 1,06 | **0,96** / 1,47 | 0,95 / 1,06 |
| **korrelált** | 1 | 0,05 | 0,99 / 0 | 0,99 / 0 | 0,99 / 0 |
| **korrelált** | 1 | 0,20 | 0,97 / 0 | 0,97 / 0 | 0,97 / 0 |
| **korrelált** | 2 | 0,20 | 0,97 / 0 | 0,98 / 0 | 0,96 / 0 |

## Értelmezés

1. **Korrelált zajnál minden módszer pontosan ugyanannyit hibázik, és egyik sem vesz észre
   semmit.** Nincs szerkezeti esemény, mert a hibás világ belsőleg konzisztens. A pontosság
   csak azért marad magas, mert a testvérkategóriák a tulajdonságaik nagy részét közösen
   öröklik; a különbözőkre a válasz csendben hibás.
2. **Két független forrás sem segít érdemben.** Az ütközés megjelenik, de a rendszer nem tudja,
   melyik forrás téved, mert mindkettő egyenként konzisztens. A pontosság 0,97-ről 0,98-ra nő.
3. **Független zajnál az ARLC egyértelműen jobb** (0,97 vs. 0,86 egy forrással, ε = 0,05). A
   tanult megbízhatóság itt nem ad többet.

## Következmény a tervre

- **A konzisztencia-alapú revízió a korrelált grounding-hibára vak.** Ez nem az ARLC hibája,
  hanem a konzisztencia mint jel korlátja. Bármely ellentmondás-vezérelt architektúrára igaz
  (1., 4., 8. ötlet az 1. fázisból).
- **Három lehetséges védekezés:**
  1. *különböző hibamintázatú források:* a 13. kör T-ötlete (több LLM különböző családból).
     Két *ugyanolyan* hibamintázatú forrás nem segít, ahogy itt sem;
  2. *alacsony szintű ellenőrzés:* olyan megfigyelések, amelyek közvetlenül a tagságról
     szólnak, nem a következményeiről;
  3. *kalibrált grounding-bizonyosság:* ha a probe tudja, hogy két testvérkategóriát
     nehezen választ szét, ezt a bizonytalanságot továbbadhatja.
- **A B fázisra:** az E0 grounding-mérésben nem elég az F1. Jelenteni kell a *tévesztési
  mátrixot* is. Ha a hibák rokon kategóriák között koncentrálódnak, az ARLC nem fogja
  észrevenni őket.
