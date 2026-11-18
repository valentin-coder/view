# 54. kör – Divergens és kritikai kör (6.): mit tanultunk a független benchmarkból?

(Minden ötödik kör kritikai. Ez az első kritikai kör, amely mögött egy előregisztrált, független mérés és
annak előregisztrált ismétlése áll.)

## 1. A mérleg számokban

| állítás | honnan | eredmény |
|---|---|---|
| a 26–42. kör mechanizmusai együtt (v4) jobbak a kiinduló v3-nál | 44. kör, előregisztrált | **cáfolva:** −0,084 [−0,142; −0,030] |
| … és jobbak egy egyszerű súlyozott alapvonalnál (wms) | 44. kör, előregisztrált | **cáfolva:** −0,063 [−0,125; −0,004] |
| a diagnózis után javított v4.4e jobb a v3-nál | 50. kör, előregisztrált ismétlés | **nem igazolt:** +0,024 [−0,009; +0,053] |
| a v4.4e jobb a wms-nél | 50. kör, előregisztrált ismétlés | **igazolt:** +0,052 [+0,014; +0,083] |
| a célzott képesség (hazug forrás, más régió) jobb | 44. és 50. kör | **igazolt, nagy hatással:** target-acc 0,75 vs. 0,60 és 0,54 vs. 0,14 a v3-hoz képest |
| a nyaláb-átlagolás javít | 50. kör, előregisztrált | **igazolt, kicsi:** Brier −0,005 |
| az „azonnali” átrendeződés | 42., 44. kör | **nem teljesül:** a meglepetés feldolgozása átlag 11 s, a wms-é 0,6 s |

**Röviden:** a rendszer *azt* tudja jobban, amire tervezték (források megbízhatóságának és kontextusának
felismerése), de ezt az általános tudás rovására teszi. A v3 általános pontosságát a sok javítás után sem
múlja felül biztosan. Ez a 12. kör plaszticitás–robusztusság dilemmája, most mérve.

## 2. Mi működött a módszertanban

1. **Az előregisztráció kétszer is megakadályozta az önámítást.** A 44. kör nélküle valószínűleg nem derült
   volna ki: a saját ellenőrző csomagon a v4 jól teljesített. Az 50. kör ismétlése megmutatta, hogy a 44. kör
   seedjein mért +0,037-es másodlagos előny felerészben illesztés volt.
2. **A célzott egységteszt és a megfigyelési ekvivalencia-audit** több hibát talált, mint bármelyik
   validációs csomag (49. kör táblázata). A 45–53. körben négy újabb hibát találtam, ebből kettő a *saját
   mérőeszközömben* volt (az EB N_rel-je és a 45. kör egyik állítása), nem a modellben.
3. **Az „eredmény a célfüggvény és a lépéskészlet együttes terméke”** tanulsága (47. kör) a 48–50. körben
   újra és újra igazolódott: minden új lépés új kiskaput nyitott.

## 3. Mi nem működött

1. **A kézzel árazott lépések elve.** A 44. kör két fő hibája (teljes elmélet elvetése kb. 10 bitért,
   egész forrás izolálása 6 bitért) ugyanaz: a félretevő lépés ára nem függ attól, mennyit tesz félre. A
   generatív v5 (51. kör) ezt szerkezetileg kezelné, de csak az első szűk lépése készült el (53. kör).
2. **A saját feladatokra illesztett paraméterek.** A κ_T = 1-et a 32. kör a TFB-9 alapján választotta. Ez egy
   olyan terület priorja, ahol az elméletek fele téves, és egy olyan benchmarkon bukott el, ahol egyik sem.
   **A TFB-9 nem volt rossz feladat, csak egy terület egyik végpontját mérte, és a paramétert erre a végpontra
   állítottuk.**
3. **Az empirikus és hierarchikus becslés a modell hibás módusát tanulja.** A 45. körben a κ̂ = 1, az 52.
   körben az A populáció π̂ = 0,885-je a rendszer saját félretevéseit a világ tulajdonságának tekinti. **A
   saját MAP-ítéletekből tanulni csak akkor biztonságos, ha a tanítójel független a tévedés módusától.**
4. **Az immediacy nem teljesült.** Az eredeti feladat „azonnali” átrendeződést kért. A 42. kör gyorsított,
   de egy 30 entitásos világban egy meglepetés átlagosan még mindig kb. 11 s. A 46. kör profilja szerint a
   zárás és a mohó befejezés a szűk keresztmetszet, nem a pontozás.

## 4. Az újdonság őszinte helyzete (a 34. kör óta)

| elem | újdonság? |
|---|---|
| a következtető (MDL = MAP egy valószínűségi logikában) | **nem** (36. kör; ProbLog-egyezés) |
| tanult forrásmegbízhatóság béta-binomiális kóddal | **nem** (igazságfeltárás-irodalom, crowdsourcing) |
| specifikusság, abnormalitás-prior | **nem** (Touretzky; McCarthy) |
| keverék-prior az elméletekre, hierarchikus becslés | **nem** (Raykar et al.; hierarchikus Bayes) |
| a félretevő lépések nem skálázódó ára mint *rendszerszintű* hibamód | **talán**: az irodalomban nem láttam így megfogalmazva (ellenőrizendő) |
| a megfigyelési ekvivalencia-audit mint kiskapu-kereső | **talán**: metamorf tesztelés ismert, ez a hiedelemrevíziós alkalmazása |
| a „szemét elmélet” arány mint a gestalt–robusztusság feszültség területi paramétere | **talán**: a Kuhn-féle paradigmaváltás és a Bayes-féle elméletválasztás irodalmában lehet előzménye (ellenőrizendő) |

**Az eredeti cél** (fagyasztott LLM aktivációiból felismert szimbolikus szerkezet, azonnali átrendeződéssel)
**szimbolikus fele egy kézzel írt valószínűségi logika lett**, amelynek viselkedését megértettük, de nem
múlja felül egy jó alapvonal általános pontosságát. A B fázis (valódi LLM) a hálózati korlát miatt nem
futott, így a „neuro” fél állítása továbbra is a 23–24. kör mini-LM-jére és a 35. kör csomagjára épül.

## 5. Divergens irányok

1. **Kétsebességű rendszer.** A v3 általános pontossága és a v4.4e célzott képessége kombinálható: a v3
   tartja a hiedelembázist, a v4.4e-mechanizmusok (forrás-megbízhatóság, kontextus) csak akkor
   aktiválódnak, ha egy új forrás ellentmond. Ez Kahneman-féle 1/2-es rendszer, és a 13. kör „aktív
   kérdezés”-ével együtt egy döntési szabályt ad: mikor éri meg a drága revízió. Mérhető: post-acc *és*
   target-acc egyszerre.
2. **A félretevés árának a jóslatvesztést tartalmaznia kell.** Ma egy elmélet elvetése után a tényei
   „1 bitbe” kerülnek, ami a legrosszabb esetben is kicsi. Egy erősebb kódolás a tények *együttes*
   valószínűségét nézné szabály nélkül (pl. egy egyszerű kategória-alapú modell alatt). Ez a
   félretevést drágítaná ott, ahol az adat szabályos, és olcsón hagyná ott, ahol nem.
3. **Az LLM új, konkrét szerepe:** nem tények kinyerése, hanem a *forrástípus* becslése (tankönyv,
   szakértő, pletyka, más régió). A 52. kör szerint a félretevés-prior forrástípusonként tanulható, ha a
   tanítójel független. A forrástípus szövegből becsülhető, és független a hiedelembázis döntéseitől.
4. **A benchmark kiterjesztése** olyan populációra, ahol az elméletek egy része valóban téves (B). A 44. kör
   benchmarkja csak az egyik végpontot méri, ahogy a TFB-9 a másikat. Egy jó rendszernek mindkettőn jól kell
   teljesítenie, ugyanazzal a mechanizmussal, a területi priort tanulva.

## 6. A következő körökre

- **55. kör:** kétsebességű rendszer (5.1), előregisztrálva a 44. és 50. kör seedjein *és* egy B-szerű
  populáción.
- **56. kör:** a félretevés árának jóslatvesztést tartalmazó kódolása (5.2), ProbLog-ellenőrzéssel.
- **57. kör:** a kombinált benchmark (A + B populáció) előregisztrációja.
- **59. kör:** divergens és kritikai kör.
