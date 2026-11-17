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

## Következő körök (tervezett)

1. **17. kör:** tanult forrás-megbízhatóság (12. kör V2) a magban; az E3 újrafuttatása vele.
2. **18. kör:** korrelált zaj (rokon kategóriák összetévesztése) az E4-ben.
3. **19. kör:** E5 ellenséges injektálás és a V1–V5 védekezések.
4. **20. kör:** a TFB-benchmark (Thagard 9 fokozata) szimbolikus generátora és első futása.
5. **21. kör:** új divergens kör: a 16–20. eredményei után mi dőlt meg, és mi következik.
