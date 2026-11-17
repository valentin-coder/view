# 43. kör – ARLC v4: befagyasztott specifikáció és ablációs tábla

## A v4 komponensei

A 15. kör ARLC v3 specifikációját a 16–42. kör tapasztalatai alapján bővítettem. A v4 minden
komponense egy konkrét hibára vagy hiányra felelt. A konfiguráció
[`experiments/arlc/arlc/v4.py`](../../experiments/arlc/arlc/v4.py)-ban van, és a 44. kör
előregisztrációjával együtt befagyasztottam.

| komponens | beállítás | indok (kör) | ellenőrzés | nyitott kockázat |
|---|---|---|---|---|
| szabályszintű ütközés | mindig | két ellentmondó általános szabály nem ütközött (16) | E2b | – |
| visszahelyezés | teljes | szabály-elvetés után a korábbi elutasítások ragadtak (16); a szűkített változat optimalitási rést okozott (36) | kimerítő ellenőrzés | lassú (42) |
| tanult forrás-megbízhatóság | béta, κ_S = 30 | kontextus vagy zaj döntése méretfüggetlen (17) | E3b, E5, r26 (96/96) | a „kontextus vagy hazug” elvben nem dönthető el (17) |
| kétszintű hitelesség | κ_T = 1 az elméletekre | gestalt–zaj feszültség (28, 32) | TFB-9, zajjal | a szabálycsaládot a forrás azonosítja |
| kivétel-prior | ε = 0,05 | a log₂\|E\|-tag világméret-műterméket okozott (27, 40, 41) | ProbLog (pontos egyezés) | a terület ε-ja paraméter |
| osztályszintű kivétel (specifikusság) | be | összebékítő alternatíva nem volt kifejezhető (27) | Chinn–Brewer, Quine (47/48) | csak megnevezett alosztályra |
| kategória-feltalálás + visszavétel | be | Thagard 6. fokozata; korai elméletfeladás útfüggése (30) | általánosítás 1,00/1,00 | szigorú jelöltgenerálás |
| forrásszintű lépés, indukált szabály elhagyása | be | konfliktus nélkül nem volt revízió (hiedelem-kitartás, 27) | debriefing-kísérlet | drágább keresés |
| kontextusfüggő indukció | be | a szétválasztott hipotézis tömörítési hátránya (21) | E3 | – |
| helyi becslésű mohó lépés, mélység 2 | be | 42. kör: kb. 25-ször gyorsabb | kimerítő ellenőrzés 25/25 | nagyobb feladatokon nem ellenőrzött |
| frissítés (vágás) | ha a csoport változhat | revízió vs. frissítés (13, 16) | A7 | a változékonysági prior orákulum |

**Nincs a v4-ben** (kapcsolóként elérhető, de alapból ki van kapcsolva): újonc-prior (26), evidencia-öregedés
(27, nem normatív), használatfüggő beágyazottság (11, 16), felejtés (37).

## Ablációs tábla (az első, még hibás maggal)

Az ellenőrző csomag a korábbi körök feladataiból áll ([`v4.py`](../../experiments/arlc/arlc/v4.py),
`battery`). Eredmény: [`results/kor-43/ablation.json`](../../experiments/arlc/results/kor-43/ablation.json).

| | E1 RR | E4 hamis átr./50 | A7 | TFB-9 pont. | TFB-9 vesztes fa aktív | feltalálás |
|---|---|---|---|---|---|---|
| **v4 (befagyasztott)** | **0,57** | 1,52 | 0,70 | 0,73 | 1,00 | 0,50 |
| − kivétel-prior | 0,76 | – | – | – | – | – |
| bármely más egyedi abláció | 0,57 | – | – | – | – | – |

**A v4 rosszabb volt, mint a komponensei egyenként a saját feladataikon** (az ARLC v3 E1 RR-je
1,00, E4-e 0,15, A7-e 1,00 volt). Egyetlen abláció sem állította helyre, mert **két független ok**
volt.

## Diagnózis: két hiba és két kölcsönhatás

A v3-ból indulva, egyenként hozzáadott komponensekkel (E1 alosztály-csere RR):

| v3 + … | RR |
|---|---|
| tanult megbízhatóság (κ = 30) | 1,00 |
| **kétszintű, κ_T = 1** | **0,47** |
| **kivétel-prior** | **0,08** |
| osztályszintű kivétel / feltalálás / forrásszintű lépés / kontextusfüggő indukció / mélység 2 + olcsó mohó lépés | 1,00 |

**1. hiba (programhiba): ingyenes kivételek a kivétel-prior mellett.** A 41. körben a „jelölt
alkalmazások” listája csak azokat a (szabály, entitás) párokat tartalmazta, ahol a tagság
*állított* volt, és csak tulajdonság-szabályokra. Az alosztály-szabályok és a *levezetett* tagságok
kivételei így **ingyenesek** voltak, és a rendszer revízió helyett ingyenes kivételekkel oldotta
fel az ütközéseket. **A 41. kör ProbLog-ellenőrzése ezt nem fogta meg, mert a véletlen
feladatokban nem volt alosztály-szabály: lefedettségi rés a validációban.**
*Javítás:* minden (szabály, entitás) pár egy abnormalitás-változó (a generatív modellből
következően); a ProbLog-modell kiterjesztve alosztály- és negatív szabályokra, levezetett
tagsággal. Ellenőrzés: 2 × 120 hipotézisen pontos egyezés (≤ 3·10⁻¹⁴). A javítás után a v3 +
kivétel-prior E1-eredménye minden típusban 1,00.

**2. hiba (modellezési hiba): a meg nem kérdőjelezett állítások hírneve elméleti szinten.**
κ_T = 1 mellett egy kb. 60 szabályos tankönyv minden *nem vitatott* szabálya sikernek számít a
múltjában. Egy szabály elutasítása így kb. 10,2 bitbe kerül, többe, mint egy új szakértői szabály
elutasítása (kb. 10 bit), ezért a rendszer a szakértőt utasítja el. Ez a 26. kör
hírnév-farmolása elméleti szinten. **Nincs még javítva** (lásd v4.1 lent).

**1. kölcsönhatás:** a tanult megbízhatóság az A7 revízió-ágát rontja (kategória most és múlt:
1,0 → 0,4). Ok: még nem azonosítva.

**2. kölcsönhatás:** a forrásszintű lépés a feltalálás általánosítását felezi (1,00 → 0,50). Ok: még
nem azonosítva.

## A javított v4 (a kód javítva, a konfiguráció változatlan)

| | E1 RR | E4 pontosság / hamis átr. | A7 | TFB-9 pont. / vesztes fa | TFB-2 | feltalálás |
|---|---|---|---|---|---|---|
| v4, javított kivétel-prior | 0,76 | 0,94 / **0,00** | 0,70 | **0,98 / 0,00** | 0,80 | 0,50 |
| v4.1 (+megerősítés-alapú múlt) | 0,76 | 0,84 / 0,00 | 0,70 | 0,72 / 0,80 | 1,00 | 0,50 |

- A kivétel-prior javítása után a v4 a nehéz feladaton (TFB-9, zajjal) kiváló: 0,98 pontosság,
  teljesen koherens váltás, és nincs hamis átrendezés.
- **A v4.1 (csak a más forrás vagy szabály által megerősített állítás épít múltat, Popper
  megerősítés-fogalma szerint) nem javít, sőt ront** (TFB-9: 0,72; E4: 0,84). Ebben a formában elvetve.
  Valószínű ok: a megerősítés a terepforrást is gyengíti, amelynek tényei sokszor csak egymást
  erősítik meg.

## Tanulság

1. **A mechanizmusok egyenként helyesek voltak, együtt nem.** Ez a 34. kör aggályának
   megerősítése, és az előre rögzített benchmark (44. kör) szükségességét igazolja.
2. **A validáció lefedettsége a véletlen feladatok szerkezetétől függ.** A ProbLog-ellenőrzés csak
   azt igazolta, ami a feladatokban előfordult. Mostantól a véletlen feladatok minden
   szabálytípust tartalmaznak.
3. **Nyitott:** a 2. hiba elvi javítása, és a két kölcsönhatás oka. Ez a 47–48. kör.
