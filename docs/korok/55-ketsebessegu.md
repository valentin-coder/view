# 55. kör – Kétsebességű rendszer: stabil alap, gyors helyi revízió

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

Az 50. kör ismétlése szerint a v4.4-egyszintű a célzott képességben (hazug forrás, más régió) nagyot nyer,
de az általános pontosságban nem múlja felül biztosan a v3-at. Ennek oka a ritka, de katasztrofális
félretevés és összeomlás. Az 54. kör javaslata: **két rendszer egyszerre**. Egy lassan változó, stabil alap
(v3) tartja a hiedelembázist, és egy gyorsan reagáló, forrásérzékeny rendszer (v4.4e) csak ott dönt, ahol a
meglepetés hat. Ez a komplementer tanulórendszerek (McClelland et al. 1995) és a Kahneman-féle 1/2-es
rendszer gondolatának egyszerű, mérhető változata. **Nem új ötlet;** a kérdés, hogy itt működik-e.

### A rendszer

Kód: [`run_r55.py`](../../experiments/arlc/arlc/run_r55.py). Ugyanarra a folyamra két memória fut.
- **H1 („kúp”):** a meglepetés kúpjában a v4.4e válasza, máshol a v3-é. A kúp: a meglepetés megfigyeléseinek
  alanyai, plusz a meglepetésben szereplő szabályok törzskategóriáinak tagjai (a v4.4e zárása szerint).
- **H2 („kúp + visszaesés”):** mint H1, de ha a v4.4e a meglepetés után a tankönyv legalább 90%-át elveti,
  vagy a tankönyvet izolálja, minden kérdésre a v3 válaszol.

### Populációk és seedek

- **A:** a 44. kör generátora változatlanul, **seed 4000–4029** (friss, egyik korábbi körben sem
  használt), 5 meglepetéstípus, 150 eset.
- **B:** ugyanaz, de seedenként 30% eséllyel **egészében téves tankönyv** (minden tulajdonság-szabály
  előjele véletlen, mint az 52. körben). A 4000–4029 seedekből a sorsolás szerint 15 szemét (50%; a
  véletlen a vártnál többet adott, nem változtatok rajta).
- Másodlagosan (feltáró): ugyanez a 44. és 50. kör seedjein, ha az idő engedi.

### Hipotézisek (95%, világok szerinti klaszteres bootstrap, mint a 44. körben)

- **H55a (A):** H2 − v3 (post-acc) > 0, és a CI nem tartalmazza a nullát.
- **H55b (A):** H2 − v4.4e (post-acc) ≥ 0 (pontbecslés), vagyis a visszaesés nem rontja a v4.4e-t átlagban.
- **H55c (A):** a H2 célkérdés-pontossága (target-acc) legfeljebb 0,02-vel marad el a v4.4e-étől.
- **H55d (B):** H1 − v3 (post-acc) > 0, és a CI nem tartalmazza a nullát.
- **H55e (B, kudarc-jóslat):** H2 − H1 (post-acc) < 0 a B-ben: a visszaesési szabály a *helyes* félretevést
  is visszafordítja, mert nem tudja, hogy a területen vannak szemét elméletek. Ha ez teljesül, a
  visszaesési szabály a terület priorja nélkül nem biztonságos (52. kör).

**Ha H55a nem teljesül,** a kétsebességű megoldás ebben a formában nem hozza a v3 stabilitását és a v4.4e
célzott képességét egyszerre, és ezt jelentem.

## 2. rész: eredmények

*(a futtatás után)*
