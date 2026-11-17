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

## Következő körök (tervezett)

1. **15. kör:** az ARLC v3 szimbolikus magjának formális specifikációja (adatszerkezetek,
   operátorok (a)–(e), pontszám, nyaláb), és mely AGM/KM-posztulátumokat teljesíti vagy sérti.
2. **16. kör:** az A2 kísérlet megvalósítása orákulum-groundinggal (ez modell nélkül fut),
   és az első valódi eredmények.
3. **17. kör:** a TFB-benchmark szimbolikus változatának adatgenerátora.
4. **18. kör:** az A5 hiszterézis- és az A6 robusztussági kísérlet.
5. **19. kör:** a frissítés vs. revízió (U-ötlet) feladatkészlete.
6. **20. kör:** új divergens kör: a 15–19. eredményei után mi dőlt meg, és mi következik.
