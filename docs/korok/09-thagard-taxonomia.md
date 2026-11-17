# 9. kör – Mit jelent az „átrendeződés”? Thagard kilenc fokozata mint benchmark

Eddig az „átstrukturálás” szót egyetlen fogalomként kezeltük. Thagard (*Conceptual
Revolutions*, 1992) a fogalmi változás kilenc fokozatát különbözteti meg, az egyszerűtől a
radikálisig. Ez a kör minden fokozathoz megmondja, hogy az ARLC v2 meg tudja-e csinálni,
melyik operátorával, és milyen tesztfeladat mérné.

## A kilenc fokozat leképezése

| # | Thagard-fokozat | ARLC v2 operátor | Képes rá? | Tesztfeladat (Nonce- vagy Valós kategória-világ) |
|---|---|---|---|---|
| 1 | új példány hozzáadása | asszimiláció (új tény, nincs nogood) | igen | „a blik egy wug” → öröklött tulajdonságok |
| 2 | új gyenge szabály | szabály-feltevés alacsony beágyazottsággal | igen | „a wugok néha zöldek” (kivételekkel) |
| 3 | új erős szabály | szabály-feltevés magas beágyazottsággal | igen | „minden wug mérges” → minden példány mérges |
| 4 | új rész–egész reláció | **nincs**: az ARLC-nek nincs mereológiai relációja | **nem** | „a wugnak van egy fep része” → a fep tulajdonságai öröklődnek-e a részre/egészre? |
| 5 | új fajta-reláció (specializáció) | új kategória-szabály | igen | „a wug a dax egy fajtája” |
| 6 | új fogalom | új atom; a grounding nem ismeri | **részben** | új szó, amit a probe-ok nem kódolnak; az LLM-ben nincs iránya |
| 7 | hierarchia-rész összeomlasztása, megkülönböztetés feladása | e-gráf merge (2. ötlet); az ARLC-ben nincs | **nem** | „a wug és a dax valójában ugyanaz” |
| 8 | ágátugrás (fogalom áthelyezése a fában) | kategória-szabály visszavonása + új; KTP-transzplantáció | **igen** (ez a KTP) | „a bálna nem hal, hanem emlős” |
| 9 | fafelcserélés (a hierarchia szervezőelvének cseréje) | **nincs** | **nem** | „az állatokat ne élőhely, hanem leszármazás szerint osztályozd” |

## Elemzés

**Az ARLC v2 a 9 fokozatból 5-öt kezel, 1-et részben, 3-at egyáltalán nem.** A legfontosabb
hiányok:

1. **A 7. fokozat (összeomlasztás).** Az e-gráf (2. ötlet) pont ezt tudta, és a 4. fázisban
   kiesett, mert monoton és sérülékeny. Javaslat: az egyenlőség maradjon az ARLC-ben, mint
   *visszavonható* feltevés: `eq(a,b)` egy assumption, és a kongruencia-zárás csak az ATMS
   környezetein belül fut. Így az összeomlasztás visszavonható, és a 2. ötlet fő gyengesége
   megszűnik. Ára a címkeméret további növekedése.
2. **A 9. fokozat (fafelcserélés).** Ez a mélyreható sémaváltás, Chi „ontológiai
   váltása”. Ehhez a hipotézisnyelvnek saját magán kellene operálnia: nem egy szabályt cserél,
   hanem azt, *mi alapján* készülnek a kategóriák. Az ARLC-ben ehhez **második rendű
   feltevések** kellenének: `szervezőelv = élőhely` vagy `szervezőelv = leszármazás`, és
   minden kategória-szabály ennek függvényében érvényes.
   - Formálisan: a kategória-szabályok egy szervezőelv-paraméterrel indexelt családot
     alkotnak, `R_σ`, és σ maga is assumption.
   - A σ cseréje egyszerre vonja vissza az egyik család összes szabályát, és vezeti be a
     másikat. Ez az ATMS-ben egyetlen feltevés cseréje, tehát mechanikusan olcsó.
   - **A nehéz rész az, honnan jön `R_σ'`.** Ha a rendszer előre ismeri, akkor ez csak
     előre gyártott alternatíva (A13 tagadása, 1. fázis). Ha nem ismeri, akkor szabályindukció
     kell egy új szervezőelv szerint, és ez a gyors átrendezésnek nem része.
   - **Őszintén: a valódi 9. fokozatú változást ez a terv nem tudja.** Csak akkor váltja,
     ha az alternatív fa már létezik. Az ember valószínűleg ugyanígy van ezzel: a
     forradalom előtt az alternatív elmélet már ki van dolgozva (Kuhn).
3. **A 4. fokozat (rész–egész).** Mechanikusan könnyű: kell egy `part_of` reláció a saját
   öröklési szabályaival. Nem elvi probléma, csak a hipotézisnyelv bővítése.

## Benchmark-javaslat: TFB (Thagard-fokozat benchmark)

- **Felépítés:** minden fokozatra 20 feladat, a Nonce-világban (ott az LLM nem tud
  előzetesen semmit) és a Valós kategória-világban (ott van előzetes tudás, amit felül kell
  írni).
- **Feladatonként:** előtörténet (5–20 állítás), egy kiváltó állítás, 10–30 lekérdezés.
  Ismert a várt válasz a változás előtt és után.
- **Mérőszámok:** ripple-recall, kollaterális, és a 7. kör szerinti *ellenállás*: hány
  anomália kell a váltáshoz alacsony forráshitelesség mellett.
- **Alapvonalak:** csak hozzáfűzés, BeliefBank-szerű MaxSAT, és a kontextusba írás.
  Nagyobb modelleknél egy LLM, amely a teljes előtörténetet a kontextusban kapja.
- **Elvárt eredmény (előzetes jóslat):** az ARLC v2 az 1–3., 5. és 8. fokozaton jó, a 7.
  fokozaton a javítás után jó, a 4. fokozaton a nyelv bővítése után jó, a 6. fokozaton
  gyenge, a 9. fokozaton csak előre gyártott alternatívával megy.
- **Cáfolat:** ha az 1–3. fokozaton a hozzáfűzés-alapvonal ugyanolyan jó, a benchmark
  túl könnyű. A fokozatoknak a nehézség sorrendjében kell nehezedniük, különben a
  taxonómia nem tükrözi a valódi nehézséget.

## Kapcsolódó munkák

- Thagard 1992; Chi 2008 (ontológiai kategóriaváltás); Posner et al. 1982.
- Gépi tanulásban a fokozatok közül a 8. a „counterfactual knowledge editing” (CounterFact,
  Meng et al. 2022). A 7. az entitásegyesítés. A 9.-re **nem ismerek benchmarkot**, ellenőrizni kell.
