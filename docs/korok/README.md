# Tervezési körök – index

Az alapdokumentum: [`../neuroszimbolikus-architektura.md`](../neuroszimbolikus-architektura.md)
(1–4. fázis). Az 5. kör (az LLM nélkülözhetetlensége, ARLC v2) és a 6. kör (KTP pilot
terve) a beszélgetésben készült. A 6. kör megvalósítása: [`../../experiments/ktp/`](../../experiments/ktp/).

| Kör | Fájl | Fő kimenet |
|---|---|---|
| 7 | [07-premissza-kritika.md](07-premissza-kritika.md) | Az „azonnali átrendeződés” emberi premisszája csak részben igaz. Új követelmény: K\* (azonnali, ha indokolt; ellenálló, ha nem). Posner négy feltétele; hiányzik a termékenység-tag. |
| 8 | [08-oksagi-absztrakcio.md](08-oksagi-absztrakcio.md) | A szimbolikus réteg mint a fagyasztott LLM online oksági absztrakciója. Interventív szabálybányászat (ISZB). Legközelebbi munkák: Geiger et al., DAS, RAVEL. |
| 9 | [09-thagard-taxonomia.md](09-thagard-taxonomia.md) | Thagard 9 fokozata: az ARLC 5-öt kezel, 1-et részben, 3-at nem. Második rendű feltevések a fafelcseréléshez. TFB-benchmark. |
| 10 | [10-komplexitas.md](10-komplexitas.md) | A globálisan optimális revízió Σ₂ᴾ-nehéz. Azonnaliság csak korlátozott nyelvvel, előre számolt alternatívákkal vagy anytime revízióval. |
| 11 | [11-katasztrofa-modell.md](11-katasztrofa-modell.md) | Csúcskatasztrófa-modell: J1–J4 jóslatok. Hiszterézis csak használatfüggő beágyazottsággal. LLM-oldali kísérlet. |
| 12 | [12-robusztussag.md](12-robusztussag.md) | Elválasztó jel nélkül a plaszticitás és a robusztusság ugyanaz a szám. Védekezések V1–V6, robusztussági margó, E5. |
| 13 | [13-meta-axiomak.md](13-meta-axiomak.md) | Az ARLC v2 saját axiómái. Legfontosabb új hiány: frissítés vs. revízió (Katsuno–Mendelzon). Aktív kérdezés. |
| 14 | [14-utiterv.md](14-utiterv.md) | Útiterv kapukkal. Az ARLC szimbolikus fele LLM nélkül, orákulum-groundinggal most is tesztelhető. |
| 15 | [15-arlc-spec.md](15-arlc-spec.md) | Az ARLC v3 szimbolikus magjának formális specifikációja; viszony az AGM/KM posztulátumokhoz (nem priorizált, hitelességkorlátos revízió). |
| 16 | [16-a-fazis-eredmenyek.md](16-a-fazis-eredmenyek.md) | **Első valódi eredmények** (szimbolikus bemeneten): R2 részben, R3 és R4 teljesül; a kontextusdöntés hangolt paramétertől függ; a használatfüggő hiszterézis-jóslat cáfolva; frissítés vs. revízió működik. |
| 17 | [17-tanult-megbizhatosag.md](17-tanult-megbizhatosag.md) | Tanult forrás-megbízhatóság: a kontextusdöntés méretfüggetlen lesz (κ = 30–100). Gyenge prior mellett megerősítési torzítás. A „kontextus vagy hazug” adatból elvben nem dönthető el. |
| 18 | [18-korrelalt-zaj.md](18-korrelalt-zaj.md) | A konzisztencia-alapú revízió a korrelált grounding-hibára vak; két ugyanolyan hibamintázatú forrás sem segít. |
| 19 | [19-ellenseges-injektalas.md](19-ellenseges-injektalas.md) | A „ez nem is tartozik ide” helyi kiút megkerüli a forrásellenőrzést. Tanult megbízhatóság + múlt: valódi elválasztás, de a sybilek ellen alig véd. |
| 20 | [20-szintezis.md](20-szintezis.md) | Újrakeretezés: az LLM ott kell, ahol a szimbolikus adat információelméletileg kevés (kontextus-, függetlenségi, változékonysági jel). |
| 21 | [21-kovetelmeny-levezetes.md](21-kovetelmeny-levezetes.md) | Szimulált jellel: egy LLM-kontextusjelnek kb. 0,95-ös pontosság kell; a közepes jel nem segít. |
| 22 | [22-divergens-2.md](22-divergens-2.md) | Divergens kör a kísérletek után: mini-LM, tipikusság, offline újrakeresés, hőmérséklet, Wikipedia-benchmark. |
| 23 | [23-mini-lm.md](23-mini-lm.md) | Saját fagyasztott mini-LM: az aktivációk „előnye” egy távoli felügyeletű BoW-val teljesen reprodukálható; a literálkinyerésben a BoW jobb. Új módszertani követelmény a B fázisra. |
| 24 | [24-kompozicionalis-jel.md](24-kompozicionalis-jel.md) | XOR-kontextus: az LM lineárisan hozzáférhetővé teszi (0,83–0,95), de egy nemlineáris felszíni modell jobb. A „neuro” fél súlypontja a következmény-motor (KTP) felé tolódik. |
| 25 | [25-optimalitasi-res.md](25-optimalitasi-res.md) | Az online keresés optimalitási rése 0 bit a tesztelt feladatokon; a sorrendhatás holtversenyes optimumok közti útfüggés, nem keresési hiba. |
| 26 | [26-olcso-alnevek.md](26-olcso-alnevek.md) | A „helyi kiút” valójában bizalmi összevetés (hibajegyzék a 19–20. körhöz). Zárt alakú tételek: friss identitás, sybil vs. egyetlen, múlt, újonc ≡ támadó; 96/96 jóslat egyezik. Planck-költség, hírnév-farmolás. |
| 27 | [27-emberi-adatok.md](27-emberi-adatok.md) | Elio–Pelletier, Hogarth–Einhorn, Chinn–Brewer, Ross–Lepper–Hubbard szimbolikusan. Két tervezési hiba: hiányzó specifikussági elv (osztályszintű kivétel bevezetve) és a konfliktus-vezérelt keresés okozta kitartás. |
| 28 | [28-tfb-benchmark.md](28-tfb-benchmark.md) | TFB 1–9. fokozat. A 7. kifejezhető; a 9. (fafelcserélés) rögzített megbízhatósággal inkoherens hibridet ad, koherens váltás csak csomagszintű (tanult) hitelességgel. Gyors váltás ↔ zajtűrés feszültség. |
| 29 | [29-divergens-3.md](29-divergens-3.md) | Kritika: a kísérletek egyre inkább a saját költségmodellt tesztelik; külső érvényesség hiányzik. Új irányok: kategória-feltalálás, polarizáció, kétszintű hitelesség, B fázis csomag. |
| 30 | [30-kategoria-feltalalas.md](30-kategoria-feltalalas.md) | Kategória-feltalálás anomáliákból: általánosít új példányokra (1,00/1,00); korai elméletfeladás útfüggést okoz (visszavétel kell); vegyes jelnél helyesen „kizárás”. |
| 31 | [31-polarizacio.md](31-polarizacio.md) | Többágenses ARLC: két külön polarizációs mechanizmus – visszhang/kettős számolás (100%, κ-független) és bizalomtanulás (csak kis κ, gyenge evidencia). A származás elsőrendű. |
| 32 | [32-ketszintu-hitelesseg.md](32-ketszintu-hitelesseg.md) | Kétszintű hitelesség (elmélet κ_T ≈ 1, adat κ_S ≈ 30) feloldja a gestalt–zaj feszültséget; a kaszkád zárt alakú küszöbe. |
| 33 | [33-szarmazas.md](33-szarmazas.md) | Származás-tudatos kommunikáció: polarizáció egyetlen konfigurációban sincs, a nyers továbbadásnál is jobb. |
| 34 | [34-divergens-4.md](34-divergens-4.md) | Kritika: kilenc új kapcsoló, saját feladatokon értékelve – túlillesztés-veszély. Befagyasztott v4, procedurális benchmark, empirikus Bayes, inkrementális pontozás. Őszinte újdonság-helyzetkép. |
| 35 | [35-b-fazis-csomag.md](35-b-fazis-csomag.md) | A B fázis egylépéses csomagja; a smoke futás három módszertani hibát szűrt ki (szivárgás, kifejezésszintű mintaméret, lexikai átfedés) és a véletlen súlyú kontroll szükségességét. |
| 36 | [36-validacio.md](36-validacio.md) | Kimerítő ellenőrzés: egy valódi optimalitási rés a 21. körös gyorsítás miatt (javítva). ProbLog: a célfüggvény pontosan egy generatív modell MAP-célja. |
| 37 | [37-felejtes.md](37-felejtes.md) | Felejtés összesítővel: a beágyazottság megmarad, a konkrét ütközési szerkezet nem (komplementer tanulórendszerek). |
| 38 | [38-quine-halo.md](38-quine-halo.md) | Quine hiedelemhálója: a „mag” a nagyobb jóslati kúpú szabály; tétel és 47/48 egyezés (a maradék holtverseny). |
| 39 | [39-magyarazatok.md](39-magyarazatok.md) | Ellentényes magyarázatok: túldetermináltság; az elégséges magyarázat a rögzített háttértől függ, és helyesen a küszöböt adja. |
| 40 | [40-tanuk-fuggetlensege.md](40-tanuk-fuggetlensege.md) | Egy eset sok tanújának súlya korlátos (Hume csodái); hallomás és Condorcet. |
| 41 | [41-elvi-kivetel.md](41-elvi-kivetel.md) | Abnormalitás-prior a log₂|E| helyett: a világméret-műtermék eltűnik; ProbLoggal igazolva; ε mint a terület kivétel-gazdagsága. (Egy hibáját a 43. kör találta meg és javította.) |
| 42 | [42-azonnalisag.md](42-azonnalisag.md) | Az átrendezés a lassú út (0,15–24 s vs. 0,1–0,7 ms); mélység 2 + helyi becslésű mohó lépés kb. 25× gyorsít, optimalitásvesztés nélkül a tesztelt méreten. |
| 43 | [43-arlc-v4.md](43-arlc-v4.md) | ARLC v4 befagyasztva; az abláció szerint együtt rosszabb, mint a komponensek külön. Két hiba (ingyenes kivételek – javítva; elméleti hírnév-farmolás κ_T = 1-nél – nyitott); a v4.1 (megerősítés-alapú múlt) nem javít. |
| 44 | [44-procedurialis-benchmark.md](44-procedurialis-benchmark.md) | Előre rögzített procedurális benchmark (1. rész: előregisztráció; 2. rész: folyamatban). |
| 46 | [46-inkrementalis-terv.md](46-inkrementalis-terv.md) | Inkrementális zárás és pontozás terve; rejtett akadály: a konfliktus kiválasztásának sorrendje. |
| 47 | [47-kolcsonhatasok.md](47-kolcsonhatasok.md) | A két kölcsönhatás oka: homogén forrásmodell × állításonkénti hitelesség; az elhagyó lépés helyesbíti a 30. kört (a feltalált szabály 7 anomáliától éri meg, alatta kizárás). |
| – | [ellenorizendo.md](ellenorizendo.md) | Az összes ellenőrizendő hivatkozás és nyitott irodalmi kérdés körök szerint. |

## Következő körök (tervezett)

1. **44. kör, 2. rész:** a procedurális benchmark eredményei (fut; az előregisztrációtól való eltérés: a kód javítva, a konfiguráció változatlan).
2. **45. kör:** empirikus Bayes az ε, κ paraméterekre (kód kész: `empirical_bayes.py`).
3. **48. kör:** állításonkénti hitelesség a tanult forrásmodellben (47. kör, 1. kölcsönhatás); az elméleti hírnév-farmolás elvi javítása (43. kör, 2. hiba).
4. **46. kör (megvalósítás):** inkrementális pontozás kanonikus konfliktussorrenddel, kapcsolóként.
5. **49. kör:** divergens és kritikai kör.
