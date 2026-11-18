# 61. kör – A B fázis csomagja a két LLM-feladatra (forrástípus és kontextusjel)

(Tervezési és kódkör; a valódi modell a hálózati korlát miatt nem fut. A smoke teszt egy véletlen súlyú
mini modellen fut, ez csak a kódot és a szivárgásmentességet ellenőrzi.)

## Miért ez a két feladat

A 44–60. kör szerint a szimbolikus mag két döntése adatból nem dönthető el:
1. **„Más kontextusról szól-e ez a forrás?”** (17., 57. kör). Jel nélkül a kontextus-izolálás a rivális
   elméletek általános menekülőútja.
2. **„Milyen gyakran téves egészében egy ilyen forrás?”** (49–52., 57. kör). Ez a keverék-prior területi π-je.
   Egy világból nem, sok világból is csak korlátozottan tanulható.

Mindkettő a forrás **szövegéből** becsülhető, és független a hiedelembázis saját döntéseitől. Az 52. kör
szerint éppen ez a feltétele annak, hogy a tanulás ne a modell hibás módusát rögzítse. **Ez az LLM legkonkrétabb,
mérhető szerepe az architektúrában.** Nem a tények kinyerése, mert a 23–24. kör szerint abban egy BoW is
versenyképes, hanem a forrás *metaadatának* becslése.

## Az SRC feladat

Kód: [`bphase/tasks.py`](../../experiments/bphase/bphase/tasks.py) (`SRC_TYPES`, `src_statements`, `src_task`).
- 4 forrástípus, típusonként 20 bevezető kifejezés („The standard textbook states that …”, „A rival school
  claims that …”, „A senior researcher explained that …”, „A nosy neighbour heard that …”). Az utolsó 8
  kitartott, és tartalmi szavuk nem szerepel a tanítókban (a modul ellenőrzi; a kezdeti listában 4 átfedést
  találtam és javítottam).
- **Szivárgás, amelyet a smoke teszt fogott meg:** az első változatban a gondozott kifejezések mind „The”-val, a
  többiek „A/An”-nal kezdődtek. Véletlen súlyú modellen és a statikus alapvonalon is AUC = 1,0 lett. Javítva:
  minden típusban váltakozó névelő, azonos szerkezet. Utána véletlen súlyú modellen: gondozott AUC 0,55
  (aktiváció), 0,58 (statikus), 0,42 (BoW), a négyosztályos pontosság 0,25–0,34, vagyis a véletlen szintje.
  **Ez a 35. kör tanulsága harmadszor: a véletlen súlyú kontroll nélkülözhetetlen.**
- Mérőszámok: kifejezésszintű négyosztályos pontosság, „gondozott vs. nem” kifejezésszintű AUC permutációs
  p-vel (a hatásos mintaméret a 32 kitartott kifejezés), és kifejezésenként a becsült típusból jövő π
  (gondozott 0,999; rivális iskola 0,5; szakértő 0,95; pletyka 0,7).

## A híd a szimbolikus maghoz

A valódi futás után:
1. a CTX kifejezésszintű pontossága lesz a 60. kör kontextusjelének a pontossága;
2. az SRC π-hozzárendelése forrásonként a `theory_pi`;
3. a 60. kör v4.8-a ezekkel fut az A, B és C populáción.

A 21. kör szerint a kontextusjelnek kb. 0,95-ös pontosság kell. A 60. kör a = 0,9-cel méri, hogy ennél
kisebb pontosság is elég-e, ha a jel Bayes-szerint árazott.

## Kötelező kontrollok (változatlanul)

Véletlen súlyú, azonos architektúrájú modell; statikus beágyazás-alapvonal; BoW; kifejezésszintű AUC
permutációs p-vel. **Egy SRC-eredmény csak akkor számít az LLM érdemének, ha mindhárom kontrollt
felülmúlja.**
