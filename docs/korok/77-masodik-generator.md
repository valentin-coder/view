# 77. kör – Egy második, független benchmark-generátor (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 74. kör szerint a legnagyobb hiányosság, hogy a 44. kör óta minden mérés ugyanabból a procedurális generátorból jön,
amelyre a v4.x kapcsolóit hangoltam. Ez a kör egy **szerkezetében eltérő** generátoron méri a változatokat. **Egyetlen
kapcsolót sem hangolok rá**, sem a futtatás előtt, sem utána.

### A generátor ([`generator2.py`](../../experiments/arlc/arlc/generator2.py))

- **Kereszt-osztályozás, hierarchia nélkül:** 3 család × 3 kategória; minden entitás családonként egy kategóriába
  tartozik. A kategóriák szabályai ütközhetnek, és az igazságot egy **rejtett családprioritás** dönti el. Az ARLC ezt
  nem ismeri: a specifikusság itt nem segít, mert nincs alosztály-reláció.
- **Rosszul kalibrált források:** két terepforrás, mindkettő 0,9-et deklarál, a valódi megbízhatóság 0,97, illetve 0,8.
- **Meglepetések:** hazug forrás (8 hamis tény); tankönyvi szabály helyesbítése; „prioritás-szakértő” (8 helyes érték
  ütköző szabályú entitásokra); „torzított forrás” (egy optimista forrás 10 hamis „igaz” tényt jelent).
- 30 entitás, entitásonként 4 tény; a tankönyv a szabályok 10%-át hibásan közli.

### Elrendezés

Seedek **15000–15019**, 4 típus: 80 eset. Módszerek: wms, v3, v4.4e, v4.8-π (a tankönyv π-je 0,999, „gondozott”). Kód:
[`run_r77.py`](../../experiments/arlc/arlc/run_r77.py).

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H77a:** v4.8-π − v3 (post-acc) > 0, a CI nem tartalmazza a nullát (a javítások külső érvényessége).
- **H77b:** v4.4e − wms (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H77c:** a „hazug forrás” célkérdésein v4.8-π − v3 > 0 (pontbecslés).
- **H77d (kudarc-jóslat):** a „prioritás-szakértő” célkérdésein mindegyik ARLC-változat target-acc-ja ≤ 0,6, mert a
  rejtett prioritás a modell nyelvén nem fejezhető ki (példánykivételekkel csak darabonként).

**Ha H77a nem teljesül,** a 44–75. kör javításai legalább részben az első generátorra illesztett hatások.

## 2. rész: eredmények

80 eset; nyers adat és elemzés: [`results/kor-77/`](../../experiments/arlc/results/kor-77/).

| | pre-acc | post-acc | target-acc | Brier |
|---|---|---|---|---|
| wms | 0,864 | 0,857 | 0,805 | 0,094 |
| **v3** | **0,905** | **0,901** | 0,867 | **0,065** |
| v4.4e | 0,890 | 0,885 | **0,907** | 0,074 |
| v4.8-π | 0,874 | 0,867 | 0,890 | 0,085 |

| típus (target-acc) | wms | v3 | v4.4e | v4.8-π |
|---|---|---|---|---|
| hazug forrás | 0,663 | 0,788 | **0,881** | 0,856 |
| torzított forrás | 0,630 | 0,749 | **0,814** | 0,804 |
| szabály-helyesbítés | 0,927 | 0,933 | 0,941 | 0,914 |
| prioritás-szakértő | 1,000 | 1,000 | 0,994 | 0,988 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H77a:** v4.8-π − v3 (post) > 0 | **−0,033** [−0,056; −0,013] | **nem teljesül, fordítva** |
| **H77b:** v4.4e − wms (post) > 0 | +0,028 [+0,000; +0,050] | **épphogy teljesül** |
| **H77c:** hazug forrás target: v4.8-π − v3 > 0 | **+0,069** [+0,019; +0,119] | **teljesül** |
| **H77d:** prioritás-szakértő target ≤ 0,6 | 0,99–1,00 | **nem teljesül; a típus tervezési hibája:** a célkérdések pontosan a szakértő által közölt tények, ezért triviálisak |

### Feltáró abláció (a meglepetés előtti pre-acc, 20 seed, a v3-hoz egyenként hozzáadva)

| v3 + … | pre-acc |
|---|---|
| semmi (v3) | **0,905** |
| tanult megbízhatóság (β, κ = 30) | 0,893 (−0,012) |
| + kivétel-prior | 0,890 |
| + osztálykivétel | 0,895 |
| + automatikus specifikusság / feltalálás / forráslépés / q-csoportok | 0,893 (nincs további hatás) |
| **+ kontextusfüggő indukció** | **0,877 (−0,016)** |

### Értelmezés

1. **A külső érvényesség próbája részben elbukott.** A független generátoron a v4.x-változatok általános pontossága rosszabb a
   v3-énál (−0,02 – −0,03), már a meglepetés előtt is. **A 44–75. kör általános pontossági javulásainak egy része az első
   generátorra illesztett hatás.** Ez pontosan az a kockázat, amelyet a 34. és 74. kör megnevezett.
2. **Ami átvihető: a forrás-tanulás.** A hazug és a torzított forrás felismerése az új generátoron is jobb (+0,07–0,09 a
   v3-hoz képest a célkérdéseken). Ez a tanult megbízhatóság és a forráslépés érdeme, és mindkét generátoron megjelenik.
3. **Ami nem vihető át:** a **kontextusfüggő indukció** (21. kör) az új generátoron a legnagyobb egyedi kár. A
   kereszt-osztályozásban a források tényei véletlenül is mutatnak forrásspecifikus mintázatot, és a kontextusfüggő
   indukció ezeket „kontextusként” tanulja meg. A tanult megbízhatóság kis kára (−0,012) valószínűleg a rosszul kalibrált
   0,97-es forrás alulbecslése: a κ = 30-as prior a deklarált 0,9 felé húz.
4. **A 75. kör eredménye ezért feltételes:** a legjobb konfiguráció az első generátor populációin (A, C) nagyot nyer, a
   másodikon az általános pontosságban veszít, a forrás-felismerésben nyer.
