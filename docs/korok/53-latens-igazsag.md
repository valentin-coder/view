# 53. kör – A generatív v5 első lépése: közös látens igazság

(Az 51. kör tervének első, szűk megvalósítása. A szűkítés oka: a 45. kör J3-kudarca egyetlen, jól
körülhatárolt modellezési hibára vezethető vissza.)

## 1. A hiba

A 45. kör szerint ismételt méréssel (két független forrás ugyanarról a tényről) ε és a forráshiba elvben
szétválasztható, a gyakorlatban mégsem vált szét. **Ok:** a pontszámban minden elfogadott jelentés külön
fizeti az „igazság-tagot” (−log₂(1 − δ), ha szabály jósolja, egyébként 1 bit). **Két egyező jelentés így nem
magyarázza egymást:** a második ugyanannyiba kerül, mint az első. Egy generatív modellben a második
jelentés a közös igazságból következik, és csak a saját megbízhatóságába kerül.

## 2. A javítás (`latent_truth`)

Tényenként (e, p) egy látens igazság T(e, p):
- ha aktív szabály jósolja: P(T = jóslat) = 1 − δ; ha nem: ½;
- egy megbízható jelentés értéke T; egy megbízhatatlané véletlen (½);
- egy (e, p)-ről szóló, csak megbízhatatlan jelentés esetén T kiösszegezve (szorzó 1).

A pontszámban ez annyit jelent, hogy az igazság-tag **literálonként egyszer** fizetendő (kontextusonként és
időpontonként). Kapcsoló: `latent_truth`; a v4.6 = v4.4-egyszintű + látens igazság.

## 3. Ellenőrzés

- **ProbLog** ([`problog_check.py`](../../experiments/arlc/arlc/problog_check.py), `latent=True`): a modell
  közvetlenül felírva (`agree`, `coin`, `tval`). 12 véletlen feladat ismétlődő jelentésekkel (két forrás
  ugyanarról a tényről, 80%-ban egyezően), alosztály- és negatív szabályokkal, 120 konzisztens hipotézisen:
  **pontos egyezés** (≤ 3·10⁻¹⁴), ε nélkül és ε = 0,05-tel is. A régi, jelentésenkénti szemantika a saját
  kódolásával szintén egyezik ([`problog_latent_truth.json`](../../experiments/arlc/results/kor-36/problog_latent_truth.json)).
- **A teszt diszkriminatív:** 106 konzisztens hipotézisből 78-ban a két szemantika pontszáma eltér.
- **Ellenőrző csomag:** a v4.6 minden mérőszáma azonos a v4.4-egyszintűével (ezekben a feladatokban nincs
  ismétlődő jelentés).

## 4. A J3 újrafuttatása

**Jóslat (a futtatás előtt):** a látens igazsággal ismételt méréssel a marginális ε̂ a látható kivételaránnyal
nő (corr > 0,5), és nem a zajjal; az illesztett k-ban több a nem nulla érték, mint a v4.4-egyszintűvel.

**Első futás: a jóslat nem teljesült, és egy hibát találtam a becslőben.** Látens igazsággal ε̂ szinte mindig
0,002 lett. Egy mikroteszt (egy entitás, két egyező, a szabálynak ellentmondó jelentés) szerint a látens
igazság a terv szerint működik: a kivételt preferálja, 1,5 bittel olcsóbban, mint a régi szemantika. A hiba
az EB-kódban volt: **a marginális tag N_rel-je jelentéseket számolt, nem különböző (e, p) literálokat.** Az
abnormalitás-változó (szabály, entitás) páronként egy, ezért ismételt mérésnél a −log₂(1 − ε) tag duplázódott,
és ε̂ lefelé torzult. Ez a 45. kör ismételt mérésű J3-ját is érintette.

**A javított becslővel** (ugyanaz a 18 ismételt mérésű világ):

| | n_rel > 0 | corr(ε̂, kivételarány) | corr(ε̂, zaj) | k > 0 | EB − befagyasztott pontosság |
|---|---|---|---|---|---|
| v4.4-egyszintű (45. kör, hibás N_rel) | 13/18 | 0,32 | −0,28 | 6 | – |
| **v4.4-egyszintű, javított N_rel** | 13/18 | **0,96** | −0,08 | 9 | **+0,048** |
| v4.6 (látens igazság), javított N_rel | 14/18 | 0,81 | +0,03 | 4 | −0,009 |

Eredmény: [`results/kor-53/`](../../experiments/arlc/results/kor-53/) (`parts_v44e_fixed`, `parts_fixed`).

**Ítélet:**
1. **A 45. kör J3-ja a javított becslővel teljesül**, mindkét szemantikával: ismételt méréssel ε̂ a kivételarányt
   követi, nem a zajt. A 2.3. pont elmélete tehát helyes volt, a mérés volt hibás.
2. **Az 53. kör saját jóslata (több k ≠ 0 a látens igazsággal) nem teljesül:** 4 vs. 9. A magas kivételarányú
   világok közül háromban a v4.6-tal a tankönyv félretéve (n_rel = 0).
3. **Értelmezés:** a régi szemantika a két egyező jelentést a tankönyv mellett *kétszer* számolta. Ez ugyanaz
   a visszhanghatás, mint a 31. kör kettős számolása, itt egyetlen ágensen belül. A látens igazság ezt
   megszünteti: egy tény ennyit ér, akárhányan jelentik. Így a tankönyv támogatottsága ismételt mérésnél a
   felére esik, és a magas kivételarányú világokban előjön a félretevés (45., 49., 50. kör). **A régi
   szemantika jobb viselkedése részben kétszer számolt evidencián állt.** A helyes modell nem ad jobb
   pontosságot, csak őszintébbet. A félretevés ellen a félretevés árát kell helyesen modellezni (51. kör),
   nem az evidenciát kétszer számolni.
