# 14. kör – Kutatási útiterv kapukkal

A 7–13. kör sok új kísérletet és bővítést hozott. Ez a kör sorrendbe teszi őket, és
minden lépéshez rögzíti, melyik eredmény mit zár ki.

## Fontos gyakorlati felismerés

**Az ARLC szimbolikus fele LLM nélkül is tesztelhető.** Az 1. fázis K1 kontrollja, az
orákulum-parser, pontosan ezt teszi: a grounding helyett hibátlan literálok mennek be,
és ehhez mesterséges zaj adható (ε = 0…0,1). Ez **most, ebben a környezetben is
futtatható**, mert nem kell hozzá modell, csak CPU. Így az LLM-től független állítások
(a szimbolikus átrendezés minősége, a komplexitás, a hiszterézis, a robusztusság)
szétválaszthatók a groundingtól függőktől.

## Fázisok

### A fázis – csak szimbolikus, modell nélkül (ebben a környezetben futtatható)

| Lépés | Tartalom | Kör | Kapu (ha bukik) |
|---|---|---|---|
| A1 | Az ARLC v3 szimbolikus magjának specifikációja: Horn-mag, ATMS, nyaláb, MDL-pontszám, (a)–(e) operátorok | 4., 10., 13. | – |
| A2 | Megvalósítás és E1–E4 orákulum-groundinggal, zajinjekcióval | 4. | **R2:** ha a BeliefBank-szerű MaxSAT 3 ponton belül van → a többletgépezet felesleges, egyszerűsíteni kell |
| A3 | TFB-benchmark szimbolikus változata (a 9 Thagard-fokozat) | 9. | ha az 1–3. fokozaton a hozzáfűzés ugyanolyan jó → a benchmark túl könnyű |
| A4 | Komplexitás-mérések M1–M3 | 10. | nyalábtalálat < 50% B = 64 mellett → az azonnaliság csak triviális esetekre igaz |
| A5 | Hiszterézis: statikus vs. használatfüggő beágyazottság | 11. | ha a használatfüggő sem hiszterézises → a csúcskatasztrófa-modell nem írja le |
| A6 | E5 ellenséges injektálás, V1–V5 védekezések | 12. | ha egyik védekezés sem választ el → a plaszticitás–robusztusság átváltás alapvető korlát |
| A7 | Revízió vs. frissítés (U-ötlet) | 13. | ha nincs 20 pontos nyereség → az (e) operátor elhagyható |

### B fázis – LLM kell hozzá (hálózati engedély vagy saját gép)

| Lépés | Tartalom | Kör | Kapu |
|---|---|---|---|
| B1 | E0 grounding-F1 a kitartott sablonokon | 1. fázis | **R0:** F1 < 0,9 → az aktivációs grounding nem működik, a B fázis többi része a generált logikai formával megy tovább (K3) |
| B2 | KTP pilot | 6. | a 6. kör döntési fája |
| B3 | ISZB (interventív szabálybányászat) | 8. | ha nem jobb a promptolásnál → szabályok promptolással |
| B4 | LLM-oldali hiszterézis (B1 kontextus, k ellentmondó mondat) | 11. | ha nincs bistabilitás → az LLM-et nem lehet a váltás jelére használni |
| B5 | D-útválasztás (kettős meglepetés) a grounding-zaj ellen | 5. | R7 |
| B6 | Több LLM mint több szem | 13. | ha a hibakorreláció nem kisebb → elhagyandó |

### C fázis – integráció

- C1: ARLC v3 az A és B fázis túlélő elemeiből, teljes TFB-benchmark LLM-groundinggal.
- C2: Az L1 lyuk végső tesztje: az IIA a revízió után (8. kör). Ha a revízió után
  jelentősen esik, a szimbolikus réteg elvált az LLM-től.

## Mi zárja ki az egész programot?

| Eredmény | Következmény |
|---|---|
| A2-ben az ARLC nem jobb, mint a BeliefBank-szerű MaxSAT | a szimbolikus fél nem új; a program legfeljebb egy ismert módszer LLM-es alkalmazása |
| B1 + B2 + B3 együtt bukik | az LLM-aktivációk feleslegesek; a program egy LLM-parser és egy szimbolikus rendszer |
| A6-ban nincs elválasztó védekezés | a „hirtelen átrendeződés” alapvetően veszélyes, csak megbízható forrás mellett használható |

## Becsült költség

- **A fázis:** a szimbolikus mag megvalósítása néhány nap fejlesztés; a kísérletek CPU-n
  percektől órákig.
- **B fázis:** a 6. kör becslése szerint a KTP kb. 1–1,5 óra. A többi B-lépés hasonló
  nagyságrendű. A becslések egyetlen valódi futással sincsenek alátámasztva.

## A következő köteg tervezett témái

Lásd `README.md` a „Következő körök” résznél.
