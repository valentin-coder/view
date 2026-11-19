# 86. kör – A forrástípus-prior metaadat nélkül: az új forrás gyanúsabb (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 83. kör szerint a forrástípus-prior (T, 80. kör) az általános pontossághoz nem kell, a hazug forrás felismeréséhez viszont
igen (+0,056). A T három típust különböztet meg metaadatból (gondozott, terepi, ismeretlen). A hazug forrás felismerésében
azonban csak egy megkülönböztetés számít: **az ismeretlen forrás szemét-komponensének súlya** (π = 0,9 a bevált
források 0,99–0,999-ével szemben). Ez a keverék a hazug forrás 8/8 félretevését 6,5 bitért engedi meg. A sima
béta-kódnál ez kb. 20 bit (80. kör, kódhossz-táblázat).

**Ami a T helyett megfigyelhető:** hogy egy forrás **mikor jelent meg először.** A bevált források (tankönyv,
népszámlálás, terepi források) a folyam elejétől jelen vannak. A meglepetés-források (hazug, torzított, régió, lektor,
szakértő) az aktuális időpontban jelennek meg. Ez nem orákulum, hanem a megfigyelések időbélyegéből adódik.

### Változatok (mind: v4.8-π + PK, a 81. kör szerint)

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`source_newcomer`), [`v4.py`](../../experiments/arlc/arlc/v4.py)
(`V49_N`, `V49_U`).
- **T nélkül:** béta-kód (κ = 30) minden adatforrásra.
- **T (metaadat):** a 80. kör forrástípus-priorja (a v4.9+PK).
- **N (új forrás):** minden forrás keverék-priort kap (κ₁ = 30, szemét: Beta(1, 1)). π = 0,9, ha a forrás első
  megfigyelése az aktuális időpontban van (Δ = 0), egyébként 0,999. Metaadat nem kell.
- **U (egyforma):** minden forrás ugyanazt a keveréket kapja (π = 0,9, κ₁ = 30). Ez a metaadat-mentes alapvonal: azt
  méri, hogy a keverék maga vagy az „új” megkülönböztetés számít. (A C populáción a futási idő miatt kimarad.)

Fejlesztési ellenőrzés (16000–16001, nem teszt): a G2-n az N a T-vel azonos (8/8 hazug félretéve, azonos post-acc). Az U
egy seeden rosszabb (0,885 vs. 0,923) és ötször lassabb.

### Elrendezés

- **Seedek:** 22000–22019 (friss). Esetek: **G1k** (a javított generátor, 85. kör) A: hazug forrás, átkategorizálás; G1k
  C: hazug forrás; G2: hazug forrás, torzított forrás. 100 eset; U nélkül a C-n: 380 futás.
- Kód: [`run_r86.py`](../../experiments/arlc/arlc/run_r86.py). Audit a meglepetés előtt (a C-n nincs).
- **Elemzés:** seedenként, világok szerinti klaszteres bootstrap (95%).

### Hipotézisek

A „hazug-szerű célkérdések” a hazug forrás (G1k-A, G2) és a torzított forrás (G2) célkérdései.

- **H86a:** hazug-szerű célkérdések: N − (T nélkül) > 0, a CI nem tartalmazza a nullát.
- **H86b:** hazug-szerű célkérdések: T − N ≤ 0,02 (pontbecslés). Az N a T hatásának nagy részét visszaadja.
- **H86c (G1k-C, hazug forrás, post-acc):** N − (T nélkül) > 0, a CI nem tartalmazza a nullát.
- **H86d (általános pontosság, G1k-A ∪ G2, pre-acc):** N − (T nélkül) ≥ −0,01 (pontbecslés).
- **H86e (U, hazug-szerű célkérdések):** N − U ≥ 0 (pontbecslés). Az „új” megkülönböztetés legalább annyit ér, mint az
  egyforma keverék.

**Ha H86a és H86b teljesül:** a T kiváltható, és az orákulumok száma háromról kettőre csökken (tankönyv-π és
kontextusjel).

## 2. rész: eredmények

Nyers adat: [`results/kor-86/test/`](../../experiments/arlc/results/kor-86/test/); elemzés:
[`analyze_r86.py`](../../experiments/arlc/arlc/analyze_r86.py) → `results/kor-86/analysis.json`. 380 futás, eltérés nincs.

### Célkérdés-pontosság (az új forrás félretett aránya zárójelben)

| | G1k-A hazug | G1k-C hazug | G2 hazug | G2 torzított | G1k-A átkat. |
|---|---|---|---|---|---|
| T nélkül | 0,850 (0,85) | 0,744 (0,74) | 0,919 (0,92) | 0,877 (0,89) | 0,719 |
| T (metaadat) | **0,913** (1,00) | **0,819** (1,00) | **0,956** (1,00) | 0,910 (0,99) | 0,719 |
| **N (új forrás)** | 0,906 (1,00) | 0,800 (1,00) | 0,931 (1,00) | 0,910 (0,99) | 0,688 |
| U (egyforma) | 0,900 (1,00) | – | 0,950 (1,00) | 0,901 (0,99) | 0,688 |

Általános pontosság (pre) és idő a G2-n: T nélkül 0,920 / 41 s; T 0,928 / 73 s; N 0,917 / 50 s; U 0,927 / 95 s.

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H86a:** N − (T nélkül), hazug-szerű target > 0 | **+0,034** [+0,017; +0,053] | **teljesül** |
| **H86b:** T − N ≤ 0,02 | +0,010 [−0,015; +0,033] | **teljesül** |
| **H86c (G1k-C, post):** N − (T nélkül) > 0 | +0,011 [+0,002; +0,025] | **teljesül** |
| **H86d (pre):** N − (T nélkül) ≥ −0,01 | −0,002 [−0,005; 0,000] | **teljesül** |
| **H86e:** N − U ≥ 0 | −0,001 [−0,019; +0,015] | **nem teljesül** (gyakorlatilag egyenlő) |

### Értelmezés

1. **A metaadat-orákulum (T) kiváltható.** A megfigyelhető „új forrás” jel a T hatásának kb. háromnegyedét visszaadja
   (+0,034 a +0,045-ből), és a különbség nem szignifikáns. **Az orákulumok száma háromról kettőre csökken** (tankönyv-π
   és kontextusjel).
2. **De nem az „új” megkülönböztetés a hatóanyag.** Az egyforma keverék (U: minden forrás 10% eséllyel szemét) ugyanannyit
   ér (H86e). **A hatás a szemét-komponens jelenlétéből jön:** a hazug forrás 8/8 félretevése a keverékkel olcsó. Ebben
   a benchmarkban a bevált források elég nagyok ahhoz, hogy a 10%-os szemét-esély se tegye őket bűnbakká. Az N előnye az
   U-val szemben a sebesség (G2: 50 s vs. 95 s), mert a bevált források keveréke kevesebb jelöltet tart életben.
3. **Az átkategorizálás célkérdéseinél az N és az U kicsit rosszabb** (0,688 vs. 0,719). Ott az új forrás egy *helyes*
   szakértő, akit az N 20%-ban félretesz (a T nélkül 5%). **Ez a „gyanús új forrás” ára:** a helyes új információt is
   gyanúsnak kezeli. A T ezt metaadatból tudta (a szakértő „gondozott”). Kicsi, de valódi költség.

### Döntés a befagyasztáshoz

A 88. kör befagyasztott konfigurációja: **v4.8-π + PK + N** (metaadat nélküli forrás-prior). A T-hez képest a hazug
forrásnál kb. 0,01-et, a helyes szakértőnél kb. 0,03-at veszít, viszont nem kér orákulumot, és gyorsabb.
