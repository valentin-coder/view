# 98. kör – A G1 ritkábban mért meglepetéstípusai a FROZEN_91-gyel (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 85–96. kör a G1k-n csak a hazug forrást és az átkategorizálást mérte. A sorozat korábbi állításai közül három típus
újramérése maradt el a javított generátoron és a mai konfigurációval: a **szabály-helyesbítés**, a **kivételes alfaj**
(kategória-feltalálás) és a **más régió** (kontextus, a 73. kör jelhez kötött elsőbbségével).

### Elrendezés

- **Seedek:** 32000–32019 (friss), G1k A populáció; szabály-helyesbítés, kivételes alfaj, más régió. 60 eset × 3.
- **Módszerek:** v3; FROZEN_91; FROZEN_91 + jel (szimulált kontextusjel a = 0,99, jelzett elsőbbség; 73. kör).
- Kód: [`run_r98.py`](../../experiments/arlc/arlc/run_r98.py). Világok szerinti klaszteres bootstrap.

### Hipotézisek

- **H98a (post-acc, a három típus együtt):** FROZEN_91 − v3 > 0, a CI nem tartalmazza a nullát.
- **H98b (kivételes alfaj, target):** FROZEN_91 − v3 ≥ 0 (pontbecslés).
- **H98c (más régió, target):** (FROZEN_91 + jel) − FROZEN_91 > 0, a CI nem tartalmazza a nullát (a jel továbbra is segít).
- **H98d (más régió, target):** FROZEN_91 − v3 ≥ −0,02 (pontbecslés; jel nélkül holtverseny, 62. kör).

## 2. rész: eredmények

Nyers adat: [`results/kor-98/test/`](../../experiments/arlc/results/kor-98/test/); elemzés:
[`analyze_r98.py`](../../experiments/arlc/arlc/analyze_r98.py) → `results/kor-98/analysis.json`. 180 futás, eltérés nincs.

| típus | v3 post / target | FROZEN_91 post / target | FROZEN_91 + jel post / target |
|---|---|---|---|
| szabály-helyesbítés | 0,841 / **0,871** | **0,887** / 0,743 | 0,887 / 0,743 |
| kivételes alfaj | 0,806 / **0,749** | 0,874 / 0,725 | **0,874** / 0,737 |
| más régió | 0,765 / 0,225 | **0,881 / 0,850** | 0,881 / 0,850 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H98a (post):** F91 − v3 > 0 | **+0,077** [+0,047; +0,119] | **teljesül** |
| **H98b (kivételes alfaj, target):** F91 − v3 ≥ 0 | −0,024 [−0,056; 0,000] | **nem teljesül** |
| **H98c (más régió, target):** jel − F91 > 0 | 0,000 [0; 0] | **nem teljesül** |
| **H98d (más régió, target):** F91 − v3 ≥ −0,02 | **+0,625** [+0,425; +0,825] | **teljesül** |

### Értelmezés

1. **A „más régió” típust az N prior jel nélkül kezeli.** A régióforrás új, ezért a keverék szemét-komponense olcsón
   félreteszi az állításait. A célkérdések a fő világ igazságát kérdezik, így ez itt helyes válasz (0,85 vs. a v3 0,225,
   amely háromszor izolál). **A jelhez kötött kontextus (73. kör) ezért fölösleges lett:** a jel semmit nem változtat. A
   62. kör óta tudott, hogy ez a típus az eredeti értelmében (más kontextus) alulhatározott. Most egy egyszerűbb
   mechanizmus („új forrás gyanús”) adja ugyanazt az eredményt.
2. **A szabály-helyesbítésnél a FROZEN_91 a célkérdésekben jelentősen rosszabb a v3-nál** (−0,128 [−0,259; −0,018]). A
   helyesbítést hozó lektor új forrás, egyetlen állítással, 0,995-ös deklarált hitelességgel. Az N keverékében ennek
   félretevése a szemét-komponensen keresztül kb. log₂(1/0,1) + 1 ≈ 4,3 bit. A becsületes komponens szerint
   −log₂(0,005) ≈ 7,6 bit volna. A rendszer ezért a helyes helyesbítést gyakran elutasítja. **Ez a „gyanús új forrás” ára,
   eddig a legnagyobb:** E1 (92. kör), jó specialista (−0,09, 93. kör), átkategorizálás (−0,03 – −0,11), most a
   helyesbítés (−0,13). **Egyetlen állításból egy jó és egy rossz új forrás metaadat nélkül elvileg nem különböztethető
   meg.** A különbséget csak a többi bizonyíték adhatja (megerősíti-e a terep a helyesbítést). Ezt a mostani N nem
   használja.
3. **A kivételes alfajnál kis veszteség** (−0,024): a négy laborforrás is új, ezért gyanús.

### Következmény

Az N egy elvi korláttal működik: az új forrás bizalmát csak a deklarált hitelességtől függetlenül, egyformán csökkenti.
Két elvi javítási irány: (a) a szemét-komponens súlya függjön a forrás *megerősítettségétől* (hány állítását támasztja
alá más forrás vagy szabály; a 43. kori „corroboration” ötlet forrás-szinten); (b) a deklarált hitelesség maga is
metaadat, így a 0,995-ös lektor π-je lehetne nagyobb. A (b) visszahozná a T orákulumot. Az (a) adatból dolgozik.
