# 112. kör – Másolásfelismerés mint hipotézis-komponens (előregisztrált)

## 1. rész: terv, fejlesztési ellenőrzés és előregisztráció (a futtatás előtt commitolva)

### Miért

A 111. kör szerint egy bevált forrás hibáit ismétlő új forrás minden érintett kérdést a hibás értékre fordít (0,59 → 0,00).
Az ismert ellenszer a forrásfüggőség felismerése (Dong és mtsai, 2009): a szó szerinti, különösen a hamis értékekben való
egyezés a másolás bizonyítéka.

### A mechanizmus (`copy_detection`)

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`Hyp.dup`, `_absorbed`, `copy_detection`, `copy_prior`),
`v4.py` (`F91_D`).
1. **Új hipotézis-komponens:** dup = {(s₂, s₁)}, „s₂ az s₁ másolója”, ára −log₂ ρ_c (ρ_c = 0,01) páronként.
2. **Elnyelés:** s₂ azon állításai, amelyek szó szerint egyeznek s₁ egy állításával, nem független bizonyítékok: kimaradnak a
   zárásból és a pontszámból.
3. **Javaslat:** ha egy ütközésben szereplő állítást egy másik forrás is szó szerint megtett, a kereső mindkét irányú
   másolást javasolja.
4. **Horgony-újraindítás:** a fejlesztés közben derült ki, hogy a 3. pont önmagában keveset ér. A másoló állításai egyenként
   érkeznek, és az elsőket olcsóbb egyenként kezelni, mint a másolást feltételezni. Ezek a döntések a nyalábban
   megmaradnak. Az igaz-hipotézis-próba szerint a „meglepetés előtti legjobb + másolás” hipotézis jobb a találtnál (163,1
   vs. 164,2 bit), de a kereső nem találja meg. Ezért **a kereső minden új forrás első megjelenése előtti legjobb
   hipotézisét horgonyként megőrzi.** Ha egy jelölt másolást feltételez, a javítás a horgony + másolás hipotézisből is
   újraindul.

Kikapcsolva bitre azonos (ekvivalencia: EGYEZIK).

### Fejlesztési ellenőrzés (G4, 28000–28005; nem teszt)

| | bevált másoló: célzott (hibás részhalmaz) | független megerősítő: célzott | észlelt másolás |
|---|---|---|---|
| FROZEN_91 | 0,000 | 0,867 | – |
| F91_D (horgony nélkül; 28000–28003) | 0,100 | 0,900 | 3/4 |
| **F91_D (horgonnyal)** | **0,433** | **0,867** (azonos) | 5/6 |

### Előregisztráció

- **Másoló/megerősítő:** friss seedek 39000–39019; v3, FROZEN_91, F91_D. **Károsodás-ellenőrzés:** a 96. kör 9 típusa a négy
  generátoron, 39100–39111; FROZEN_91, F91_D. **Feladatcsomag:** FROZEN_91, F91_D.
- Kód: [`run_r112.py`](../../experiments/arlc/arlc/run_r112.py).

**Hipotézisek:**
- **H112a (bevált másoló, hibás részhalmaz, utána):** F91_D − FROZEN_91 > 0, a CI nem tartalmazza a nullát.
- **H112b:** az F91_D pontossága a hibás részhalmazon a másoló után legfeljebb 0,15-tel marad el a FROZEN_91 másoló előtti
  pontosságától (pontbecslés).
- **H112c (független megerősítő, target utána):** F91_D − FROZEN_91 ≥ −0,02 (pontbecslés).
- **H112d (károsodás, post):** F91_D − FROZEN_91 ≥ −0,01 mind a négy generátoron (pontbecslés).
- **H112e (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel.

**Döntési szabály:** ha mind teljesül, az F91_D lesz az új befagyasztott konfiguráció (FROZEN_112).

## 2. rész: eredmények

Nyers adat: [`results/kor-112/`](../../experiments/arlc/results/kor-112/); elemzés:
[`analyze_r112.py`](../../experiments/arlc/arlc/analyze_r112.py) → `results/kor-112/analysis.json`. 120 + 216 futás +
feladatcsomag, eltérés nincs.

| hibás részhalmaz (előtte → utána) | bevált másoló | független megerősítő | észlelt másolás (másoló) |
|---|---|---|---|
| v3 | 0,56 → 0,00 | 0,56 → 0,92 | 0/20 |
| FROZEN_91 | 0,46 → 0,00 | 0,46 → 0,78 | 0/20 |
| **F91_D** | 0,46 → **0,50** | 0,46 → 0,78 (azonos) | **17/20** |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H112a:** F91_D − FROZEN_91 (utána) > 0 | **+0,498** [+0,36; +0,64] | **teljesül** |
| **H112b:** F91_D utána ≥ FROZEN_91 előtte − 0,15 | +0,04 (a meglepetés előtti szint fölött) | **teljesül** |
| **H112c (megerősítő):** ≥ −0,02 | 0,000 (bitre azonos) | **teljesül** |
| **H112d (a többi 9 típus, post):** ≥ −0,01 | 0,000; 0,000; +0,000; 0,000 | **teljesül** |
| **H112e (feladatcsomag):** | egyetlen tétel sem változott | **teljesül** |

**A döntési szabály szerint az F91_D az új befagyasztott konfiguráció (`FROZEN_112`).** Ez a 91. kör óta az első, és a
96–111. kör kilenc jelöltje közül az egyetlen, amely minden előre rögzített kritériumon átment.

### Értelmezés

1. **A 111. kör legsúlyosabb sebezhetősége kezelhető, metaadat nélkül.** A másolást a rendszer 20-ból 17 esetben felismeri,
   és az érintett kérdéseken a meglepetés előtti szintre áll vissza.
2. **Miért működik, ahol a tárcsák nem (104., 109. kör)?** A másolás **nem alapgyakoriság-kérdés,** hanem szerkezeti
   bizonyíték. Az egyezés mintázata (szó szerint ugyanazok az állítások, a hibásak is) a világ alapgyakoriságaitól
   függetlenül olcsóbb magyarázat. A tárcsákkal szemben (jó vagy rossz új forrás egyetlen állításból) itt **sok állítás
   együttes mintázata** dönt. Ez a 100. kör korlátjának pozitív párja: ahol a bizonyíték szerkezete elég gazdag, a
   szimbolikus réteg önmagában is dönt.
3. **A horgony-újraindítás nélkül a mechanizmus keveset ért** (fejlesztés: 0,10). Ez a 81. kör óta harmadszor mutatja:
   **a keresés útja ugyanolyan fontos, mint a kódhossz.** Egy új hipotézis-komponens csak akkor ér valamit, ha a kereső a
   régi döntéseket is újra tudja nyitni.
4. **Nem ártalmatlan minden helyzetben:** egy valóban független forrás, amely egy bevált forrással sok állításban szó szerint
   egyezik (mert mindkettő igazat mond), másolónak minősülhet. A megerősítő kontrollban ez nem történt meg, mert ott az
   egyezések nem okoztak ütközést (a javaslat csak ütközésből indul). Egy egyező, de ütköző független forrás (pl. két
   független forrás ugyanabban téved) ritka, de lehetséges eset.
