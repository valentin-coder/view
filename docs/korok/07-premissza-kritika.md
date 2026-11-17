# 7. kör – A cél premisszájának kritikája: mit csinál valójában az emberi agy?

A feladatleírás azt állítja, hogy az emberi agy sémái „egy erős új tapasztalat után”
egyszerre alakulnak át, és ezt kéri számon a szimbolikus rétegen. Ez a kör megnézi, mennyire
igaz ez a premissza. Ha nem igaz, akkor rossz követelményre optimalizálunk.

## Mit mond az evidencia?

| Jelenség | Gyors, egyszeri átrendeződés? | Forrás (ellenőrizendő) |
|---|---|---|
| Egypróbás tanulás (ízaverzió, félelemkondicionálás) | **Igen**, egyetlen erős élmény elég. De ez asszociáció, nem sémaváltás. | Garcia–Koelling 1966 |
| Belátásos („aha”) problémamegoldás | **Igen**, a reprezentáció hirtelen vált. A váltás előtt viszont hosszú, tudattalan inkubáció van. | Kounios–Beeman 2014 |
| Identitás-leleplezés („X valójában Y”) | **Igen**, a következmények azonnal átíródnak. | klasszikus; a 2. ötlet (e-gráf) erre készült |
| Séma-konzisztens információ beépülése | **Gyors**, de ez asszimiláció, nem átrendeződés. Patkányoknál egy ülés elég. | Tse et al. 2007 |
| Séma-*inkonzisztens* információ | **Lassabb**, más agyi útvonalon megy. | van Kesteren et al. 2012 (SLIMM) |
| Predikciós hiba a lehíváskor | Rekonszolidációt indít, de csak egy bizonyos tartományban. | Sevenster–Beckers–Kindt 2013 |
| Fogalmi váltás a tanulásban (pl. hő mint anyag → hő mint energia) | **Nem**, évekig tart, a tévképzetek makacsul túlélnek. | Chi 2008; Posner et al. 1982 |
| Tudományos forradalmak | **Nem**, az anomáliák évtizedekig gyűlnek. A váltás az egyén szintjén viszont lehet hirtelen. | Kuhn 1962; Thagard 1992 |

## Következtetés

**A premissza csak részben igaz.** Az ember *képes* az azonnali átrendezésre, de
*csak bizonyos típusoknál*. Ilyen az identitás vagy a kategória cseréje, ha erős a forrás,
és a belátás. A mély ontológiai váltásnál viszont kifejezetten *ellenáll*. Ez a kettősség
nem hiba, hanem a lényeg: egy rendszer, amely minden meglepetésre azonnal átrendeződik,
manipulálható és instabil (lásd a 12. kört).

**A követelményt ezért át kell fogalmazni:**

> **K\*:** a szimbolikus réteg *képes* egyetlen megfigyelés hatására globálisan átrendeződni,
> **ha** az átrendeződés indokolt (a régi struktúra költsége a megfigyelés fényében meghaladja
> az új struktúra költségét), és *ellenáll*, ha nem az. Az ellenállás mértéke a régi
> struktúra beágyazottságával arányos, és mérhető.

Ez pontosan az ARLC MDL-triggere (4. fázis). Tehát az eredeti architektúra jó irányba
ment, de a célt a feladatleírás pontatlanul fogalmazta meg.

## Posner négy feltétele mint formális követelmény

Posner, Strike, Hewson és Gertzog 1982-es fogalmiváltás-elmélete szerint egy új fogalom
akkor vált ki egy régit, ha négy feltétel teljesül. Mindegyiknek van ARLC-beli megfelelője:

| Posner-feltétel | Jelentés | ARLC-megfelelő |
|---|---|---|
| Elégedetlenség | a régi fogalom nem kezeli az anomáliákat | felgyűlt anomália-költség: `Σ_{τ∈Anom} L(e_τ|ℋ*)` |
| Érthetőség | az új fogalom kifejezhető | ℋ' benne van a hipotézisnyelvben (Horn-szabályok, kontextusok) |
| Hihetőség | összefér a többi tudással | LLM-prior: `−λ·log P_LLM(ℋ')` (D-ötlet, 5. kör) |
| Termékenység | új dolgokat is megmagyaráz | jövőbeli kódhossz-nyereség; ezt az ARLC **nem** méri |

**Az utolsó sor új hiány.** Az ARLC csak a múltbeli megfigyelésekre számolja a
kódhosszt. A termékenység előretekintő: egy új séma azért is jó lehet, mert sok még nem
látott kérdésre ad választ. Javaslat: a pontszámba kerüljön egy `L_pred(ℋ')` tag, a
következmények várható száma a következő k lekérdezésre. Ezt egy lekérdezés-eloszlás
mintájából lehet becsülni, vagy az LLM által generált próbakérdésekből (az 5. kör
E-ötlete, az offline replay).

**Kockázat.** A termékenység-tag a nagyobb, merészebb sémákat jutalmazza, és az
ellenállás ezzel csökken. Ennek ellensúlyozása a beágyazottság. A két tag aránya
szabad paraméter, ezt a 12. kör robusztussági vizsgálata rögzíti.

## Mit vesz el ez a kör?

- Az „azonnali” mint *mindig*-követelmény elesik. Helyette: azonnali, *ha indokolt*, és
  az indokoltság mérhető.
- A KTP pilotot ez nem érinti, mert ott a sémaváltást orákulum rendeli el.
- Új mérési kötelezettség: minden kísérletben jelenteni kell az **ellenállást** is. Az
  E2 pontosan ezt méri (váltási pont a beágyazottság függvényében). Ezt a 11. kör
  kvantitatívvá teszi.
