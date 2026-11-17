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

## Következő körök (tervezett)

1. **26. kör:** a „helyi kiút” MDL-ből levezetett javítása (20. kör, nyitott kérdés).
2. **27. kör:** tipikusság (fokozatos tagság) prototípus-változata, és hatása a 19. kör támadásaira.
3. **28. kör:** a TFB-benchmark (Thagard 9 fokozata) generátora, a nehéz (7–9.) fokozatokkal; az optimalitási rés újramérése ott.
4. **29. kör:** új divergens és kritikai kör.
