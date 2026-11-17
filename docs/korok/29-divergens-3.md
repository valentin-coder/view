# 29. kör – Divergens és kritikai kör a 26–28. után

## Kritika: mit mérünk valójában?

A 26. körben a zárt alakú jóslat a 96 pontos rács mindegyikén pontosan egyezett a mérttel. Ez
kétélű. **Jó hír:** az ARLC viselkedése analitikusan érthető, a keresés megtalálja a modell
optimumát, és a levezetés lefed minden releváns alternatívát. **Rossz hír:** a játékvilágokon
végzett kísérletek egyre inkább *a saját költségmodellünket* tesztelik, nem a valóságot. Minden
újabb rács, amely egyezik a jóslattal, kevesebb új információt hordoz.

**Ebből három következmény adódik a programra:**
1. **Külső érvényesség kell.** Három forrás jöhet szóba:
   - valódi szöveg és LLM: a hálózati szabály blokkolja;
   - emberi adat: nincs, csak irodalmi összevetés (27. kör);
   - más által tervezett benchmark: a hálózat ezt is blokkolja.

   A program jelenlegi helyzetében ez a legnagyobb, és szimbolikusan nem pótolható hiány.
2. **A szimbolikus kísérletek értéke a hibafelderítés.** A 16., 19., 26. és 27. körben a
   kísérletek valódi tervezési hibákat hoztak elő: szabályszintű ütközés, a forrásellenőrzés
   félreértése, a specifikussági elv hiánya, a konfliktus-vezérelt keresés okozta kitartás. Ez
   indokolja a folytatást, de a kérdés innentől az, hogy *melyik hiányzó képesség* a
   legfontosabb, nem az, hogy egy újabb rács egyezik-e.
3. **A cáfolhatóság fókusza:** azok a jóslatok a legértékesebbek, amelyek *emberi* vagy *valódi
   LLM*-es kísérletben tesztelhetők. A 27. körben ilyen volt: „alátámasztott szabályt az ember
   kevésbé ad fel absztrakt feladatban”. Ezeket külön listán kell gyűjteni.

## Mi dőlt meg, mi feszül?

| Megállapítás | Kör | Feszültség |
|---|---|---|
| A sybil-probléma szimbolikusan megoldhatatlan | 26 | Csak külső identitás-jel segít, ami LLM-et vagy infrastruktúrát igényel |
| Gyors gestalt-váltás (kis κ) ↔ zajtűrés | 28 | Ugyanaz a paraméter (a forrás hitelvesztésének sebessége) dönt mindkettőről |
| Hiányzott a specifikussági elv | 27 | Az osztályszintű kivétel csak *megnevezett* alosztályra működik |
| Konfliktus nélkül nincs revízió | 27 | Kitartás; a forrásszintű lépés megoldja, de drágább keresést jelent |

## Új irányok (vízszintesen)

### A. Kétszintű hitelesség: elméletek mint csomagok

- **Probléma:** a gestalt-váltáshoz a forrás szabályainak csomagként kell viselkedniük (28. kör),
  és ezt most csak egy gyorsan tanuló, ezért zajérzékeny forrásmodell adja.
- **Ötlet:** hierarchikus modell. Egy *elmélet* (egy szabálycsalád) hitelessége külön paraméter,
  a forrásé külön. Az elmélet egyik szabályának cáfolata az elmélet *összes* szabályának
  hitelességét csökkenti, a forrás többi, elméleten kívüli állítását nem.
- **Rokon munka:** Thagard ECHO (koherencia mint kényszerkielégítés); hierarchikus Bayes-modellek
  az elméletváltásra (Kemp, Tenenbaum és munkatársai, „theory-based Bayesian models”, ellenőrizendő).
- **Cáfolat:** ha a kétszintű modell a 28. kör zajos kontrolljában nem ér el egyszerre ≥ 0,95
  koherenciát és ≥ 0,9 pontosságot, a feszültség nem oldható fel így.

### B. Kategória-feltalálás anomáliákból (predikátum-invenció) ★

- **Probléma:** az osztályszintű kivétel csak megnevezett alosztályra működik (27. kör). Ha az
  anomáliák egy *közös, de meg nem nevezett* tulajdonságban osztoznak (pl. mind csíkosak), a
  rendszer nem talál osztályszintű megoldást.
- **Ötlet:** az MDL-keresés új kategóriát is feltalálhat: `c' = dax ∧ F`, és `c' → ¬p`. A
  modellköltség (egy új kategória és két szabály) akkor térül meg, ha kevesebb, mint az
  egyedi kivételek összköltsége. **Ez Thagard 6. fokozata (új fogalom), amely eddig hiányzott.**
- **Rokon munka:** predikátum-invenció az induktív logikai programozásban (Muggleton,
  Cropper); Kemp és Tenenbaum strukturális formái; magyarázat-alapú kategóriaképzés.
- **Cáfolat:** ha a feltalált kategória nem általánosít új, nem látott példányokra (a
  következő csíkos daxról nem jósolja, hogy nem mérges), akkor ez csak kivétel-tömörítés, nem
  fogalomalkotás.

### C. Többágenses ARLC: polarizáció (társadalmi ismeretelmélet) ★

- **Probléma:** a 17. kör gyenge előzetes eloszlásnál megerősítési torzítást mutatott: az első
  forrás nyer, a második „hazug” lesz. Ha több ARLC-ágens egymás forrásai, ez csoportszinten
  **polarizációt** okozhat.
- **Rokon munka:** a Laputa-modell (Olsson 2013, „A Bayesian simulation model of group
  deliberation and polarization”, ellenőrizendő): olyan ágensek, amelyek a forrásaik
  megbízhatóságát is tanulják, racionálisan polarizálódhatnak. Jern, Chang és Kemp 2014: a
  hiedelem-polarizáció nem mindig irracionális.
- **Kísérlet:** N ágens, közös igazság, mindegyik kap privát zajos megfigyeléseket és a többiek
  állításait. Mérés: a végső hiedelmek kettéválása κ és a kommunikációs hálózat függvényében.
- **Cáfolat:** ha egyetlen κ mellett sem lép fel polarizáció, a 17. kör sorrendhatása egyéni
  műtermék, csoportszinten nincs következménye.

### D. Tömörítés és felejtés („alvás” mint konszolidáció)

- **Probléma:** az ARLC minden megfigyelést megőriz, a memória korlátlanul nő.
- **Ötlet:** időnként a jól tömörített megfigyelések (amelyeket egy szabály jósol) törlődnek,
  csak a szabály és a kivételek maradnak. A komplementer tanulórendszerek (McClelland és munkatársai,
  1995) gyors–lassú elválasztásának szimbolikus változata.
- **Kockázat:** a törölt evidencia hiányzik egy későbbi revízióból. Ha a szabály később hibásnak
  bizonyul, a törölt alátámasztás miatt *alulbecsüljük* a feladás költségét.
- **Mérés:** pontosság és revíziós viselkedés a memóriaméret függvényében.

### E. Kritikai javaslat: a program fókuszának váltása

A 23–24. kör szerint a „neuro” fél súlypontja a KTP (következmény-motor), és az valódi LLM-et
igényel. A szimbolikus fél jól megértett. **A legnagyobb haszon tehát a B fázis
előkészítéséből jönne:** egy olyan csomagból, amely hálózat esetén egy lépésben lefuttatja az E0,
KTP, ISZB és B4 kísérleteket a valódi modelleken, minden kontrollal együtt, köztük a 23. kör
távoli felügyeletű alapvonalával. Ez nem divergens ötlet, hanem a legolcsóbb út a külső
érvényességhez, amint a hálózat elérhető.

## Rangsor és rombolás

| ötlet | érték | megvalósítható most? | rombolás |
|---|---|---|---|
| B. kategória-feltalálás | **magas**: hiányzó Thagard-fokozat, mély MDL-kérdés | igen | Kockázat: a keresési tér robbanása (minden attribútum-kombináció jelölt). Védekezés: csak az anomáliák közös attribútumai jelöltek. **Túléli.** |
| C. polarizáció | **magas**: vízszintes, tesztelhető jóslat; csoportszintű következmény | igen | Kockázat: a Laputa-modell már megmutatta, ez átcímkézés. Válasz: az ARLC-ben a polarizáció a *szabályokra* és a *forrásokra* együtt hat (sémák polarizálódnak, nem csak egy hiedelem). **Részben átcímkézés, de érdemes.** |
| A. kétszintű hitelesség | közepes-magas | igen | A B és C után |
| D. tömörítés | közepes | igen | A 4. kockázat valódi, külön kör |
| E. B fázis csomag | magas, de csak hálózattal ér valamit | a kód igen, a futás nem | Párhuzamosan, kisebb körökben |

**Következő körök:** 30. kör: kategória-feltalálás (B); 31. kör: többágenses polarizáció (C);
32. kör: kétszintű hitelesség (A); 33. kör: a B fázis egylépéses csomagja (E); 34. kör:
divergens és kritikai kör.
