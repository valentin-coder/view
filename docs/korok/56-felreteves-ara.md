# 56. kör – A félretevés ára: egy téves premissza, és a valódi döntő tényező

## 1. A premissza, és miért téves

Az 54. kör javaslata (5.2) szerint a félretevés azért olcsó, mert az árából hiányzik a jóslatvesztés: egy
elvetett vagy izolált tankönyv után a tények „csak 1 bitbe” kerülnek. **Ez téves.** A pontszámban egy szabály
által nem jósolt tény 1 bit (P = ½), egy jósolt −log₂(1 − δ) ≈ 0,074 bit. A tankönyv jóslati értéke tehát
tényenként 0,93 bit, és ez **a lehető legnagyobb**: bármely jobb nullmodell (például kategóriánkénti
gyakoriságok szabály nélkül) a nem jósolt tényeket *olcsóbbá* tenné, és ezzel a félretevést is. A
jóslatvesztés tehát már teljes súllyal benne van az árban. Ezt a futtatás előtt, elemzéssel ismertem fel,
ezért a tervezett kísérletet nem futtattam.

## 2. A valódi döntő tényező: egy 2 bites különbség

A 50. kör ismétlésében a v4.4-egyszintű egy világban (3024) félretette a tankönyvet. A pontszám felbontása
([`diag_r56.py`](../../experiments/arlc/arlc/diag_r56.py)):

| hipotézis | összesen | béta (megbízhatóság) | többi | elvetett / izolált | jósolt / nem jósolt tény | pre-acc |
|---|---|---|---|---|---|---|
| online (félretevő) | **216,2** | 9,9 | 206,3 | tankönyv és népszámlálás **izolálva** (2 × 6 bit) | 0 / 90 | 0,57 |
| tankönyv megtartva (5 hibás szabály + 13 terepi tény elvetve) | 218,3 | 81,3 | 136,9 | – | 62 / 15 | **0,81** |

**A döntést 2 bit dönti el**, és ezt a kontextus-izolálás fix ára (6 bit forrásonként) adja. A tankönyv
megtartása itt valóban drága (81 bit megbízhatósági költség, mert a világban sok valódi anomália van), de az
izolálás ennél csak alig olcsóbb. Ez a 49. és 51. kör megállapítása egy konkrét esetben: **a félretevés
ára nem függ attól, mit tesz félre, és két nagyon különböző hiedelemállapot (pontosság 0,57 vs. 0,81)
2 biten belül van.**

## 3. Egy forrástípus-prior hatása (feltáró, ugyanezen a seeden)

Ha a gondozott források (tankönyv, népszámlálás) „más helyzetről szól” prioresélye 1/64 helyett kb. 1/1000
(kontextusár 10 bit, a többi forrásé marad 6):

| | pre-acc | post-acc (hazug forrás) |
|---|---|---|
| v4.4-egyszintű (50. kör) | 0,57 (félretéve) | ≈ 0 (összeomlás) |
| + gondozott forrásra 10 bit | **0,80** | **0,79** |

**Ez nem független eredmény:** a paramétert ennek a seednek a diagnózisa után választottam. A „más régió”
típusban a régióforrás nem gondozott, ezért az ő izolálása 6 bit marad. Egy B-szerű populációban (szemét
tankönyv) a félretevés útja megmarad, csak 10 bitbe kerül.

## 4. Következmény

- A forrástípus (gondozott vs. nem) **deklarált metaadat** kellene legyen, ahogy a q is az. A B fázisban ezt
  az LLM a szövegből becsülhetné (51. kör, 4.2).
- **Az 57. kör** előregisztrálja ezt a változatot (v4.7 = v4.4-egyszintű + gondozott forrás kontextusa 10 bit)
  friss seedeken, A és B populáción, a v3, a v4.4e és az 55. kör kétsebességű rendszere mellett.
