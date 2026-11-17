# 22. kör – Divergens kör a kísérletek után

A 16–21. kör eredményei több feltevést megdöntöttek. Ez a kör abból indul ki, ami megdőlt, és
mindegyikhez új irányt keres.

## Mi dőlt meg?

| Feltevés | Mi lett belőle | Kör |
|---|---|---|
| A használatfüggő beágyazottság hiszterézist ad | elsőbbségi hatást ad; hiszterézis csak lecsengéssel és tartózkodással, gyengén | 16 |
| A kontextus-szétválasztás „magától” helyesen dönt | elvben nem dönthető el (kontextus vagy hazug); külső jel kell | 17 |
| A κ = 10-nél látott sorrendhatást a csak globális indukció okozza | **nem**: kontextusfüggő indukcióval is megmarad; a hazug-tanulás és a holtverseny okozza | 21 |
| A tanult megbízhatóság véd a támadás ellen | csak az ismétlődő támadó ellen; a sybilek ellen alig | 19 |
| A forrásellenőrzés mindig érvényesül | a „ez nem is tartozik ide” helyi kiút megkerüli | 19 |

## Új irányok

### 1. Saját, fagyasztott mini-LM (a B fázis blokkolásának megkerülése) ★

- **Probléma:** a B fázis (minden, ami az LLM-ről szól) a hálózati szabály miatt blokkolt.
- **Ötlet:** egy kis transzformert (2–4 réteg, néhány millió paraméter) CPU-n betanítunk egy
  szintetikus korpuszon, amely a Nonce-világ állításait tartalmazza, *forrás- és
  kontextusjelölőkkel* és parafrázisokkal. Utána **befagyasztjuk**, és a B fázis kísérleteit
  (grounding probe-okkal, KTP-transzplantáció, kontextus-jel, függetlenségi jel) ezen futtatjuk.
- **Mit ad:** a teljes „neuro” csővezeték végponttól végpontig tesztelhető, ismert
  igazsággal. Például: kiolvasható-e lineárisan a kontextus-jel az aktivációkból, és eléri-e a
  21. kör által megkövetelt pontosságot?
- **Mit nem ad:** semmit a *valódi*, előtanított LLM-ekről. A mini-LM pontosan azt tudja, amit
  beletettünk. Egy pozitív eredmény itt csak *megvalósíthatósági* bizonyíték, egy negatív
  viszont erős: ha ott sem működik, ahol mi építettük be a jelet, akkor valódi modellen sem
  várható.
- **Cáfolat:** ha a mini-LM aktivációiból a kontextus-jel lineáris probe-bal 0,9 alatti
  AUC-val olvasható ki, miközben a korpuszban explicit jelölő van, akkor a „jel az
  aktivációkból” út gyakorlatilag reménytelen.

### 2. Tipikusság a kivételek helyett (kognitív pszichológia: Rosch-féle prototípuselmélet)

- **Probléma:** az ARLC-ben egy anomália vagy kivétel (diszkrét), vagy a tagság elvetése. Az
  ember inkább azt mondja: „ez egy atipikus dax”.
- **Ötlet:** a tagság fokozatos tipikussággal: `isa(e, c, τ)`. Egy anomália a τ-t csökkenti,
  nem a tagságot veti el. A szabályok súlya a tipikussággal arányos.
- **Mit oldana meg:** a helyi kiutat (19. kör), mert a tagság nem esik ki, csak gyengül. Így
  az anomália forrásának megbízhatósága mérlegre kerül.
- **Ára:** a Horn-mag és a kemény nogood-ok elvesznek; a 10. kör polinomiális garanciái is.
- **Legközelebbi munka:** Rosch 1975; prototípus- és exemplármodellek; valószínűségi
  logikák (ProbLog, MLN). **A fokozatos tagság és az MDL-revízió összekötése átcímkézés-gyanús,
  ellenőrizni kell.**

### 3. Offline újrakeresés („alvás”) a sorrendhatás ellen

- **Megfigyelés:** a béta-binomiális kód cserélhető (a megfigyelések sorrendjétől független),
  ezért a pontszám sorrendfüggetlen. A κ = 10-nél látott sorrendhatás tehát **a keresés útjából
  és a holtversenyből** jön, nem a célfüggvényből.
- **Ötlet:** időnként egy nagy mélységű, kötegelt újrakeresés az összes megfigyelésen.
  Valódi holtversenynél ez sem dönt, viszont kimutatja, ha a nyaláb egy rosszabb
  hipotézisben ragadt.
- **Kísérlet:** a végső hipotézis pontszáma online vs. kötegelt keresés után, a 16–19. kör
  összes kísérletén. **Ha a különbség nulla, a nyaláb elég; ha nem, a „gyors átrendeződés”
  ára egy mérhető optimalitási rés.** Ez a 10. kör M3 mérése.

### 4. Hőmérséklet a revízióban (fizika: szimulált hűtés)

- **Ötlet:** a nyaláb mellett egy alacsony valószínűséggel rosszabb hipotézist is elfogad
  (Metropolis-lépés), ami a 11. kör kritikus lassulásához is kapcsolódik: a hőmérséklet a
  bizonytalanság mértéke.
- **Átcímkézés?** Igen, szimulált hűtés a hipotézistérben. Csak a 3. ponttal együtt érdemes.

### 5. Valódi szöveges benchmark: Wikipedia-javítások és -változások

- **Ötlet:** a Wikipedia szerkesztési története tartalmaz *javításokat* (a régi állítás hibás
  volt: revízió) és *frissítéseket* (a világ megváltozott: update). Ebből egy természetes,
  címkézett adatkészlet építhető a 13. kör U-ötletéhez.
- **Akadály:** hálózat kell hozzá, és a javítás/frissítés címkézése nem triviális.
- **Legközelebbi munka:** időérzékeny QA-adatkészletek (pl. TimeQA, SituatedQA),
  WikiFactDiff-szerű munkák. **Ellenőrizendő.**

## Rangsor

| Ötlet | Érték | Költség | Most megvalósítható? |
|---|---|---|---|
| 1. mini-LM | **magas**: feloldja a B fázis blokkolását, legalább megvalósíthatósági szinten | közepes | **igen** (torch és CPU van) |
| 3. offline újrakeresés | közepes: méri az online keresés optimalitási rését | alacsony | igen |
| 2. tipikusság | magas, de nagy átírás | magas | részben |
| 4. hőmérséklet | alacsony | alacsony | igen |
| 5. Wikipedia | magas | magas | **nem** (hálózat) |

**Következő:** a 23. kör az 1. ötlet terve és első megvalósítása. A 24. kör a 3. ötlet.
