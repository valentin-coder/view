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

Nyers adat: [`results/kor-55/`](../../experiments/arlc/results/kor-55/) (A, B: esetenként); elemzés:
[`analyze_r55.py`](../../experiments/arlc/arlc/analyze_r55.py) → `analysis.json`.

| | A post | A target | B post | B target | B szemét post | B jó post |
|---|---|---|---|---|---|---|
| v3 | 0,762 | 0,617 | 0,606 | 0,482 | 0,414 | 0,798 |
| v4.4e | **0,802** | 0,691 | **0,634** | 0,557 | 0,410 | **0,858** |
| H1 (kúp) | 0,772 | 0,691 | 0,616 | 0,558 | 0,420 | 0,812 |
| H2 (kúp + visszaesés) | 0,774 | **0,694** | 0,614 | 0,524 | 0,416 | 0,812 |

| hipotézis | különbség | 95% CI | eredmény |
|---|---|---|---|
| **H55a:** H2 − v3 (A, post) > 0 | +0,012 | [+0,008; +0,018] | **teljesül** |
| **H55b:** H2 − v4.4e (A, post) ≥ 0 | **−0,028** | [−0,063; +0,012] | **nem teljesül** |
| **H55c:** H2 target ≥ v4.4e target − 0,02 (A) | +0,003 | [−0,014; +0,024] | **teljesül** |
| **H55d:** H1 − v3 (B, post) > 0 | +0,010 | [+0,005; +0,015] | **teljesül** |
| **H55e:** H2 − H1 (B, post) < 0 | −0,002 | [−0,005; +0,001] | irányában igen, **nem szignifikáns** |

A visszaesési szabály az A-ban az esetek 9%-ában lépett életbe, a B jó tankönyves világaiban egyszer sem, a
B szemét tankönyves világaiban 88%-ban.

### Értelmezés

1. **Az alapfeltevés ezeken a seedeken nem állt:** a v4.4e itt *általánosan* is jobb a v3-nál (0,802 vs.
   0,762; az 50. kör 3000-es seedjein +0,024 volt, itt +0,04). A kúpon kívül a v3 válasza így rontja az
   eredményt (H55b). **A kétsebességű rendszer abban a formában, ahogy terveztem, a gyengébb rendszert
   tartja meg alapnak.**
2. **Feltáró (nem előregisztrált), fordított felállás:** H3 = a v4.4e válasza mindenhol, kivéve ha a v4.4e
   félretette a tankönyvet; akkor a v3-é. Az A-ban **0,819**: +0,058 a v3-hoz [+0,032; +0,086], +0,018 a
   v4.4e-hez képest [−0,000; +0,047]. A 14 visszaesett esetben a v3 0,586-ot, a v4.4e 0,395-öt ad. Ezt az 57.
   körben, annak adatai előtt, előregisztrált hipotézisként vettem fel (H57e, H57f).
3. **A B populáció ebben a formában nem diszkriminatív.** A szemét tankönyves világokban mindegyik módszer
   0,41–0,42 körül áll, pedig a tankönyvet a v4.4e 75-ből 66-szor, a v3 71-szer félreteszi (a v3 is, mert a
   véletlen előjelű szabályok tömegesen ütköznek). Félretevés után nincs más tudásforrás, amely a meg nem
   figyelt tényeket megjósolná, ezért a helyes félretevés nem javít a pontosságon. **A gestalt-váltás
   értékét csak akkor lehet mérni, ha van rivális, helyes elmélet** (TFB-9). Ezt az 57. kör C populációja
   pótolja (kiegészítés az adatai előtt).
4. **A B jó tankönyves világaiban a v4.4e egyszer sem tette félre a tankönyvet**, az A-ban 150-ből 14-szer.
   A különbség a seedek véletlenjéből adódik (más világok), nem a populációból.
