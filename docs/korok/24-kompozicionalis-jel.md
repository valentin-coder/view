# 24. kör – Kompozicionális kontextus-jel: van-e LM-specifikus előny?

## Kérdés

A 23. körben az aktivációk minden előnye reprodukálható volt egy távoli felügyeletű, LM nélküli
BoW-val. Most olyan jelet építettem be, amelyet egy *lineáris* felszíni modell elvben nem
reprezentálhat. Ha a fagyasztott mini-LM aktivációiból egy lineáris probe ezt kiolvassa, akkor az
LM legalább *lineárisan hozzáférhetővé* tesz valamit, ami a szavakban csak kombinációként van jelen.

## Elrendezés (XOR-világ)

- Minden mondat elején: „at the {hely} in {évszak} ,”. A hely kétféle (marsh, ridge), az
  évszak kétféle (spring, autumn).
- **A kontextus = XOR(hely, évszak).** Egyik szó sem informatív önmagában.
- A forrásnevek véletlenszerűek, explicit kontextusszó nincs.
- A kontextus-feladatban csak olyan mondatok szerepelnek, amelyek tartalma nem árulja el a
  kontextust (nincs bennük kontextusfüggő tulajdonság).
- **Kontrollok:** lineáris BoW, BoW páronkénti szorzatjellemzőkkel (lineáris modell), és egy
  kis MLP a BoW-on (nemlineáris).
- Nyers eredmények: [`experiments/minilm/results/r24-xor/results.json`](../../experiments/minilm/results/r24-xor/results.json).

## Eredmények (pontosság)

| Módszer | kitartott sablon | kitartott forrás |
|---|---|---|
| lineáris BoW | 0,51 | 0,52 |
| **aktiváció, lineáris probe** | **0,83** (AUC 0,93) | **0,95** (AUC 0,99) |
| BoW + páronkénti jellemzők | 0,99 | 1,00 |
| MLP a BoW-on | 1,00 | 1,00 |

## Értelmezés

1. **Az LM a kompozicionális jelet részben lineárisan hozzáférhetővé teszi.** A lineáris BoW
   véletlenszintű (0,51), az aktivációk lineáris probe-ja 0,83–0,95. Ez az LM reprezentációinak
   ismert tulajdonsága: nemlineáris jellemzőket lineárisan elérhetővé tesz.
2. **Egy egyszerű nemlineáris felszíni modell jobb nála** (0,99–1,0). Az LM-reprezentáció a
   kitartott sablonokon ráadásul nem is teljesen sablonfüggetlen (0,83).
3. **A 21. kör küszöbét (kb. 0,95) az aktiváció csak a kitartott forrásokon éri el**, a kitartott
   sablonokon nem.

## Összesített tanulság a 23–24. körből

A játékvilágban **nincs olyan jel, amelyben a fagyasztott mini-LM aktivációi túlteljesítenék a
megfelelő, LM nélküli alapvonalat**, sem az előtanítási tudásban (23. kör), sem a
kompozícióban (24. kör). Ez nem meglepő: egy szintetikus világban minden jel a felszíni
statisztikából következik, és azt egy megfelelő felszíni modell is megtanulja.

**Ebből következik, hol lehet egyáltalán LLM-specifikus előny:** csak olyan jelben, amely
*nincs benne* az adott szövegben vagy egy elérhető korpusz egyszerű statisztikájában, de benne
van egy nagy előtanított modell tudásában. Valódi LLM-mel a mérendő:
- **LLM-aktiváció vs. statikus szóbeágyazás (GloVe/word2vec) + nemlineáris fej.** A
  kontextuális és a nem kontextuális beágyazások probe-összevetéseiből (pl. Tenney et al. 2019,
  „What do you learn from context?”) az ismert eredmény, hogy a kontextuális előny a
  szintaktikai feladatokon nagy, a szemantikaiakon kisebb. **Az ellenőrzendő elvárás: a
  kontextus-jelben az LLM előnye a statikus alapvonallal szemben kicsi lesz.**

## Mit változtat ez a programon?

A „neuro” fél három kijelölt helye (20. kör) közül a **kontextus-jel** és a **függetlenségi jel**
a játékvilágban felszíni modellel is előállítható. A **következmény-motor** (KTP, 6. kör) az
egyetlen, ahol az LLM valóban olyan tudást használna, amely nincs a szövegben: például hogy a
halnak kopoltyúja van. **A program „neuro” felének súlypontja ezért a KTP felé tolódik.** A KTP
viszont valódi előtanított modellt igényel, mert egy mini-LM nem tud olyan világtudást, amelyet
nem mi tettünk bele.
