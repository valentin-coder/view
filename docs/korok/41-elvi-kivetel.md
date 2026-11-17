# 41. kör – Elvi kivétel: abnormalitás-prior a világméret-függő bit-tag helyett

## Probléma

A 15. kör óta egy példányszintű kivétel ára `log₂|E|` bit volt (|E| az entitások száma). Ez kétszer
is műterméket okozott:
- a 27. körben az Elio–Pelletier-típusú döntés kis világban (|E| ≤ 8) mindig a kivétel lett;
- a 40. körben egy eset tanúinak összsúlyát a világ mérete korlátozta.

Ráadásul a 36. kör ProbLog-ellenőrzése a kivételeket nem fedte le, tehát ez a tag a célfüggvény
nem igazolt része volt.

## Javítás (függőleges)

McCarthy körülírásának (1980, 1986) és az abnormalitás-predikátumnak a valószínűségi változata:
minden (szabály, jelölt tag) pár egy rejtett `ab(r, e)` változó, ε előzetes valószínűséggel.
- Kivétel: `−log₂ ε` bit.
- Nem kivételes alkalmazás: `−log₂(1 − ε)` bit.
- A szabály csak a nem abnormális tagokra érvényes.

A kivételek *viszonylagos* ára így `log₂((1 − ε)/ε)` lesz, a világ méretétől függetlenül.
Megvalósítás: `Memory.exc_prior` ([`core.py`](../../experiments/arlc/arlc/core.py)).

**Ellenőrzés ProbLoggal:** a generatív modellbe bekerült az `ε::ab(r, e)` tény, a szabály pedig
`rule_has(X, …) :- rel(r), isa(X, …), \+ ab(r, X)` alakú lett. 15 véletlen feladat 150 hipotézisén,
véletlen kivételhalmazokkal, az ARLC-pontszám és a ProbLog `−log₂ P` **pontosan egyezik** (legnagyobb
eltérés 1,4·10⁻¹⁴ bit). A kivételekkel együtt tehát a célfüggvény egy generatív modell MAP-célja.
Eredmény: [`results/kor-36/problog_with_exceptions.json`](../../experiments/arlc/results/kor-36/problog_with_exceptions.json).

## Eredmények

**Elio–Pelletier-feladat** (szabály + tény + ellentmondás; 9 hitelesség-kombináció cellánként):

| alátámasztás | log₂|E| szerinti kivétel | ε = 0,05 | ε = 0,2 |
|---|---|---|---|
| 0 | \|E\| = 4: 9 kivétel; \|E\| ≥ 16: 5 szabály, 3 tény, 1 ellentmondás | **minden \|E\|-re:** 5 szabály, 3 tény, 1 ellentmondás | minden \|E\|-re: 9 kivétel |
| 2 vagy 5 | \|E\| ≤ 8: kivétel; nagyobb: 6 tény, 3 ellentmondás | **minden \|E\|-re:** 6 tény, 3 ellentmondás | minden \|E\|-re: 9 kivétel |

**Tanúk** (40. kör, szilárd tagság mellett; hány eredeti eset kell):

| N | jóslat (naiv / származás) | mért, r = 1 és 3 (naiv / származás) |
|---|---|---|
| 4 | 2 / 3 | 2 / 3 |
| 8 | 3 / 4 | 3 / 4 |
| 16 | 5 / 7 | 5 / 7 |

(jóslat: `⌈T(N) / min(tanúk · 3,17; log₂(19))⌉`, a korlát most log₂((1 − ε)/ε) = 4,25 bit)

Eredmények: [`results/kor-41/`](../../experiments/arlc/results/kor-41/).

## Értelmezés

1. **A világméret-függés eltűnt.** Az eredmény |E| = 4 és |E| = 256 között azonos.
2. **Helyette egy tartalmas paraméter dönt: ε, a terület kivétel-gazdagsága.** Kis ε (szigorú
   törvények) mellett egy ellentmondás vagy a tényt, vagy a szabályt dönti meg. Nagy ε (sok kivétellel
   élő általánosítás, pl. „a madarak repülnek”) mellett a kivétel az alapválasz. Ez a generikus
   állítások szemantikájának ismert kérdése: „a madarak repülnek” kivételt tűr, „a háromszög
   szögösszege 180°” nem.
3. **Az Elio–Pelletier-jelenség mindkét formája megjelenik:** kis ε mellett a szabály *feladása*,
   nagy ε mellett a szabály *gyengítése*. Egy emberi kísérletben ez tesztelhető: **a szabály tartalma
   (szigorú törvény vagy tipikus általánosítás) befolyásolja-e, hogy feladják vagy gyengítik?**
   Ellenőrizendő, létezik-e erre adat.
4. **Hume korlátja (40. kör) elvi alakot kapott:** egyetlen eset tanúinak összsúlya legfeljebb
   `log₂((1 − ε)/ε)`. Ez annak a log-esélye, hogy egy eset kivételes. Egy szigorú törvényt (kis ε)
   egyetlen eset sok tanúja is többet nyom, egy laza általánosítást (nagy ε) kevésbé.

## Javaslat

Az ARLC v4-ben a kivétel-prior legyen az alapértelmezés, szabálytípusonkénti ε-nal. A szabály
„szigorúsága” a ε. Ennek forrása lehet:
- a szöveg nyelvi jele („mindig” vagy „általában”);
- az LLM tudása arról, hogy egy általánosítás mennyire tűr kivételt. Ez a 20. kör „neuro”-helyeinek
  egy újabb eleme, és egy valódi LLM-mel tesztelhető.
