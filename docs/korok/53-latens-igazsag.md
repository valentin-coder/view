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

*(az ismételt mérésű 18 világ a v4.6-tal; a futtatás után)*

**Jóslat (a futtatás előtt):** a látens igazsággal ismételt méréssel a marginális ε̂ a látható kivételaránnyal
nő (corr > 0,5), és nem a zajjal; az illesztett k-ban több a nem nulla érték, mint a v4.4-egyszintűvel
(ott a medián 0).
