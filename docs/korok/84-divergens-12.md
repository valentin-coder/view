# 84. kör – Divergens és kritikai kör (12.): a 79–83. kör mérlege, és egy 40 körön át rejtve maradt generátorhiba

## 1. A 79–83. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 79 | mi marad két generátor után | csak a megbízhatatlan forrás felismerése áll erősen; a menekülőút a félrespecifikált Bayes ismert jelensége |
| 80 | forrástípus-prior (T) | a hazug forrás felismerése +0,08 – +0,10 mindkét generátoron; a G2-n semleges |
| 81 | tanult szabályprioritás + kódhossz-javítás (PK) | **minden hipotézis teljesül; először van v4-változat a G2-n a v3 fölött** (pre +0,023, post +0,052) |
| 82 | menekülőút-audit | a fieldB másodlagos bűnbak (pontosság 0,61 vs. a v3 0,97); **a G1 generátor logikailag ellentmondásos világokat gyárt** (47/50) |
| 83 | kell-e még a T | csak a hazug forrás felismeréséhez (+0,056); a PK a rivális elméleteknél semleges |

**A jelenlegi legjobb konfiguráció: v4.9+PK** = v4.4e + tankönyv-keverék metaadat-π-vel + forrástípus-prior +
prioritás-kivétel javított kódhosszal (+ jelzett kontextus-elsőbbség és nyaláb-átlag, ahol releváns).

## 2. A fő kritika: a generátorhiba és amit a módszerről mond

A G1 generátor (44. kör) minden csúcskategória-párt diszjunktnak mond, a többszörös szülők viszont két csúcsot is
összekötnek. **A világok 94%-a logikailag ellentmondásos, és ez 40 körön át rejtve maradt.** Hogyan?

1. **Az előregisztráció nem véd a benchmark érvényességi hibái ellen.** Az előregisztráció az elemzési szabadságot zárja
   ki (melyik mérőszám, melyik seed, melyik összevetés). Azt nem ellenőrzi, hogy a benchmark azt méri-e, amit gondolok.
   A 62. kör („más régió” holtverseny) és most a 82. kör ugyanennek a hibatípusnak két esete: **a generátor
   tulajdonságait soha nem teszteltem közvetlenül.**
2. **A hibát csak az „igaz hipotézis pontozása” találta meg** (81. kör eszköze, a G1-en a 85. kör előkészítésekor). Ez
   egyben a hiányzó egységteszt: **minden generátorra ellenőrizni kell, hogy az igaz hipotézis megengedett-e
   (ütközésmentes), és mennyibe kerül a modell szerint.** Ha nem megengedett, a generátor hibás. Ha drágább a talált
   hipotézisnél, a benchmark (az adott adatmennyiség mellett) nem azonosítható, és a pontosság-különbségek a
   holtversenyek véletlenjét mérik.
3. **Mi következik a 44–83. kör G1-es eredményeire?** Az összevetések egyenlő feltételek mellett zajlottak, ezért a
   rangsorok valószínűleg megmaradnak. Ezt a 85. kör méri. Az abszolút számok viszont torzak, és nem zárható ki, hogy egyes
   mechanizmusok (pl. az osztálykivétel, a szigorú specifikusság, a feltalálás) részben az ellentmondásos világok
   elvágási kényszerére adott válaszként „segítettek”. **Ezeket a G1k-n újra kell mérni, mielőtt bármelyiket általános
   javulásnak nevezem.**

## 3. További kritika

1. **Foltozás-veszély.** A 78–81. kör minden diagnózisa egy-egy kódhossz- vagy árazási hibát talált (Pólya-urna,
   osztálykivétel-ár), és mindegyik javítás helyi. A konfiguráció most kb. 20 kapcsolóból áll. A friss seedes
   előregisztráció a seed-illesztést zárja ki, a **generátor-illesztést nem**: a PK-t a G2-n diagnosztizáltam és ott is
   mértem. Csak egy harmadik, a konfiguráció befagyasztása *után* épített generátor adhat erről választ.
2. **A plafon.** Az igaz hipotézis pontossága a G2-n 0,97–1,00, a G1k-n 0,93–0,98. A talált hipotéziseké 0,92 (G2),
   illetve 0,84–0,97. A különbség nagy része az azonosíthatósági határ (entitásonként 3–4 tény mellett az igaz
   hipotézis nem MDL-optimális, 81. kör). **A MAP-alapú rendszer ezen a határon nem tud túllépni.** A nyaláb-átlag (50.,
   63. kör) a Brier-t javította, a pontosságot nem. Ha a cél a pontosság, egy valódi poszterior-közelítés kellene (pl.
   MCMC a hipotézistéren), ami a futási idő miatt eddig kívül esett.
3. **Az eredeti cél kétharmada továbbra is hiányzik.** A feladat egy *befagyasztott LLM aktivációiból* felépülő
   szimbolikus struktúra volt. 84 kör után a szimbolikus revíziós motor (ARLC) érett, a neurális oldal (B fázis) egyetlen
   valódi futást sem kapott, mert a környezetnek nincs hálózata modellt letölteni. A 61. kör kódja kész, és ezt a
   korlátot minden kritikai kör megnevezi. **A sorozat ma egy hiedelemrevíziós motorról szól, nem egy
   neuroszimbolikus architektúráról.**
4. **Futási idő.** A G1-C egy esete a legjobb konfigurációval 135 s, a G2-é 58 s. Az „azonnali” átrendeződés célja
   (jelenleg kb. 0,1–1 s egy megfigyelésre) a kis világokban teljesül, a nagyobbakban nem. A 46. és 72. kör gyorsított, a
   76. kör (szabályszintű memó) halasztva van.

## 4. Divergens irányok

1. **Generátor-egységteszt** (2.2): az igaz hipotézis megengedettsége és ára minden generátorra és seedre, a benchmark
   részeként. Ez olcsó, és visszamenőleg is lefuttatható.
2. **A T tanulható változata** (83. kör döntése): a forrás „múltja” (első megjelenés ideje, megerősített állítások
   aránya) mint megfigyelhető jel a π-hez. Ez az orákulumok számát háromról kettőre csökkentené.
3. **Harmadik generátor, befagyasztott konfigurációval** (3.1): időben sodródó szabályok (a 11. kör vágási pontjait
   teszteli), más zajmodell, és a konfigurációt **a generátor megírása előtt** commitolom.
4. **Poszterior-közelítés MAP helyett** (3.2): a nyaláb diverzifikálása helyett véletlen újraindításos lokális keresés
   vagy egyszerű MCMC a hipotézistéren, az azonosíthatósági határon lévő esetekre. Költséges, de a plafon-kérdést csak így
   lehet megválaszolni.

## 5. A következő körökre

- **85. kör (fut):** G1 vs. G1k, előregisztrált.
- **86. kör:** a T tanulható változata a forrás múltjából, előregisztrált, G1k + G2.
- **87. kör:** generátor-egységteszt (igaz hipotézis) mindkét generátorra, minden eddigi seedre.
- **88. kör:** a konfiguráció befagyasztása, és csak utána a harmadik generátor megtervezése.
- **89. kör:** divergens és kritikai kör.
