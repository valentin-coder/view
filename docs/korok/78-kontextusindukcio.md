# 78. kör – A kontextusfüggő indukció mint keresési menekülőút (előregisztrált)

## 1. rész: diagnózis és előregisztráció (a futtatás előtt commitolva)

### Diagnózis

A 77. kör feltáró ablációja szerint a második generátoron a kontextusfüggő indukció (21. kör) okozza a legnagyobb kárt
(−0,016). Négy seeden (15000–15003) megvizsgáltam: a 15003-asban indukcióval a rendszer **a tankönyvet és a
népszámlálást kontextusba izolálja**, és a pontosság 0,844-ről 0,688-ra esik. A végső hipotézisben nincs indukált
szabály. **Az indukció tehát a keresés útját változtatja meg:** az izolált kontextusban indukált szabályok életben
tartják az izoláló hipotéziseket a nyalábban, amíg azok nyernek. Ez ugyanaz a menekülőút (a félretevés izolálással),
mint az 57., 60. és 68. körben, most a keresési útvonalon keresztül.

### Javítás

`ctx_induction_sources`: kontextusfüggő indukció csak a jel által „más kontextusnak” jelzett forrás kontextusában (a 73. kör
mintájára). Jel nélkül nincs kontextusfüggő indukció.

### Elrendezés

Kód: [`run_r78.py`](../../experiments/arlc/arlc/run_r78.py). Seedek **16000–16019** (friss). Második generátor (G2):
hazug forrás, szabály-helyesbítés, torzított forrás. Első generátor (G1, A populáció): átkategorizálás, szabály-helyesbítés,
hazug forrás. 120 eset. Változatok: v4.4e (indukcióval); v4.4e − kontextusfüggő indukció; v4.4e jelzett indukcióval
(szimulált jel, a = 0,99; G2-ben nincs valódi „más kontextus”, így a jelzések csak téves riasztások).

### Hipotézisek

- **H78a (G2):** (v4.4e − ki) − v4.4e (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H78b (G1):** (v4.4e − ki) − v4.4e (post-acc) ≥ −0,01 (pontbecslés).
- **H78c (G2):** |jelzett indukció − indukció nélkül| < 0,01 (pontbecslés).

## 2. rész: eredmények

Nyers adat: [`results/kor-78/`](../../experiments/arlc/results/kor-78/); összesítés: `analysis.json`.

### Az előregisztrált összevetés

| | G2 pre | G2 post | G2 target | G1 pre | G1 post | G1 target |
|---|---|---|---|---|---|---|
| v4.4e | 0,894 | 0,893 | 0,887 | 0,827 | 0,809 | 0,731 |
| v4.4e − kontextusfüggő indukció | 0,894 | 0,893 | 0,887 | 0,827 | 0,809 | 0,731 |
| v4.4e, jelzett indukció | 0,894 | 0,893 | 0,887 | 0,827 | 0,809 | 0,731 |

**A három változat mind a 120 esetben bitre azonos eredményt ad** (minden különbség 0,000 [0; 0]).

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H78a (G2):** (− ki) − v4.4e > 0 | 0,000 [0; 0] | **nem teljesül** |
| **H78b (G1):** (− ki) − v4.4e ≥ −0,01 | 0,000 | teljesül (triviálisan) |
| **H78c (G2):** \|jelzett − (− ki)\| < 0,01 | 0,000 | teljesül (triviálisan) |

**Értelmezés:** a 15003-as seed esete és a 77. kör ablációs kára (−0,016) **ritka, seedfüggő keresési útvonal-hatás**
volt, nem rendszeres mechanizmus. Friss seedeken a kontextusfüggő indukció egyszer sem változtat a kimeneten. **A 77. kör
„fő kár” attribúcióját visszavonom.** A kis seedszámú feltáró ablációk (a 77. körben 4 seed eltérése alapján) itt is
félrevezettek. Ez ugyanaz a hiba, amelyet a 69. kör 3.2. pontja leírt.

### Feltáró: egyet-elhagyó abláció a G2-n (nem előregisztrált)

Mivel az előregisztrált hipotézis nem magyarázza a G2-beli lemaradást, ugyanazokon a seedeken (16000–16019, hazug forrás,
pre-acc) minden v4.4e-komponenst egyenként kikapcsoltam. Kód: [`loo_r78.py`](../../experiments/arlc/arlc/loo_r78.py).

| változat | pre-acc |
|---|---|
| v3 | 0,914 |
| v4.4e | 0,894 |
| **− tanult megbízhatóság** | **0,915** |
| − kivétel-prior | 0,898 |
| − osztálykivétel, − aut. specifikusság, − feltalálás, − forráslépés, − q-csoportok, − mohó/mélység 2 | 0,894 (mind azonos) |

- (− tanult megbízhatóság) − v4.4e = **+0,021** [+0,009; +0,033];
- (− tanult megbízhatóság) − v3 = +0,002 [−0,002; +0,004];
- v4.4e − v3 = −0,020 [−0,030; −0,008].

**A G2-beli teljes lemaradás a tanult (béta-binomiális) forrás-megbízhatóságból jön.** Nélküle a v4.4e a v3 szintjén
van. A többi komponens a G2-n semleges: nincs hierarchia, ezért a specifikusság, az osztálykivétel és a feltalálás nem
aktiválódik. Ez egyben azt is jelenti, hogy **a G2 a v4 újításainak nagy részét nem teszteli.**

### A mechanizmus: bűnbak-forrás

Három seeden összevetettem a végső hipotéziseket (félretett megfigyelések forrásonként):

| seed | béta (v4.4e) | rögzített megbízhatóság |
|---|---|---|
| 16016 | tankönyv 8, fieldA 1, fieldB 2 | tankönyv 6, **fieldB 7**, fieldA 1 |
| 16000 | **népszámlálás 6**, tankönyv 7, 2 kivétel | tankönyv 6, **fieldB 7**, népszámlálás 2, fieldA 2 |
| 16002 | **népszámlálás 27**, tankönyv 2 | **fieldB 9**, tankönyv 6, népszámlálás 4, fieldA 1 |

A helyes magyarázat szerint a valóban 0,8-as fieldB hibás jelentéseit kell félretenni. A béta-kód ehelyett
**egyetlen forrásra (a népszámlálásra vagy a tankönyvre) koncentrálja a félretevést.**

**Keresési vagy modellhiba?** Mindkét végső hipotézist mindkét kóddal pontoztam:

| seed | béta-kód: H_béta | béta-kód: H_rögz | rögzített kód: H_béta | rögzített kód: H_rögz |
|---|---|---|---|---|
| 16016 | **146,6** | 150,2 | 162,1 | **159,3** |
| 16000 | **160,1** | 164,9 | 173,3 | **170,2** |
| 16002 | **181,9** | 185,0 | 222,6 | **189,9** |
| 16013 | **170,7** | 181,7 | 200,6 | **193,6** |

**Modellhiba.** A béta-kód szerint a bűnbak-hipotézis 3–11 bittel jobb. A kereső tehát a saját kódja szerint helyesen
dönt.

**Miért?** A béta-binomiális kód a félretevések számában konkáv: n megfigyelésből k félretétele kb. n·H(k/n) bit, és
ez mindig olcsóbb a rögzített k·log₂(1/(1−q)) + (n−k)·log₂(1/q) kódnál. Az olcsóság egy forráson belül nő a k-val.
Ez a Pólya-urna „a gazdag gazdagabb lesz” tulajdonsága (ugyanaz, ami a Dirichlet-folyamatos klaszterezésben a nagy
klasztereket favorizálja). **Ez nem új felfedezés, hanem a béta-binomiális kód ismert tulajdonsága.** A hazug forrásnál
pont erre van szükség (sok félretevés egy forrásban olcsó). A háttérforrásoknál viszont menekülőút. Hogy miért éppen a
népszámlálás: a G2-ben a kategóriák szabályai a rejtett családprioritás szerint rendszeresen ütköznek, és az ARLC ezt
csak kivételekkel tudja kifejezni. Egy tagsági állítás félretétele egyszerre több ütközést old fel. **A béta-kód tehát
olcsó kiutat ad egy olyan szerkezethez (szabályprioritás), amelyet a hipotézistér nem tud kifejezni.** Ez a
sorozatban a negyedik menekülőút-minta (izolálás: 57., 60., 68. kör; indukciós útvonal: 77–78. kör; bűnbak-forrás: most).

### Következmények

1. A 80. kör tárgya pontosítva: **nem a rosszul kalibrált forrás tanulása a gond** (a fieldB-t a béta-kód nem tanulja
   meg rosszabbnak, mert nem kell), **hanem a háttérforrás bűnbakká tétele.** Javítási jelöltek: (a) a forrásokra is
   keverék-prior („becsületes, kalibrálatlan” vagy „hazug”), metaadatból jövő π-vel, ahogy az elméleteknél (60. kör);
   (b) nagyobb κ_S a gondozott forrásokra.
2. A G2 hiányzó primitívje a **tanult szabályprioritás** (családok közötti elsőbbség). Ez ismert formalizmus: prioritásos
   alapértelmezett logika (Brewka, 1989), illetve „preferred subtheories”. A 79. kör tárgyalja.

