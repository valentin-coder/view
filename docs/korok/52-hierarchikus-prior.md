# 52. kör – Hierarchikus prior sok világon át: a „szemét elmélet” aránya mint tanult területi paraméter

## 1. rész: terv és jóslatok (a futtatás előtt)

### Miért

A 49. kör szerint a gestalt-váltás (TFB-9) és a kis világok téves teljes tankönyv-elvetése
**ugyanaz a lépés, ugyanazzal a priorral**. A prior egy populáció-szintű paraméter: milyen gyakran
téves egészében egy elmélet ezen a területen (1 − π). A 45. kör szerint ez egyetlen világból nem
becsülhető. Sok világ együtteséből viszont igen, ha a világok egy része elég nagy ahhoz, hogy az
elméletek sorsa ott egyértelmű legyen.

### Az eljárás (kemény EM a világok szintjén)

1. Kiindulás: π₀ = 0,95 (kalibrált keverék, 48. kör).
2. Minden *tanító* világra (30 entitás) a MAP-hipotézis. Egy elmélet „szemétnek” számít, ha a MAP az
   állításai legalább 90%-át elveti, vagy a forrást izolálja.
3. π̂ = (a nem-szemét elméletek száma + 1) / (az elméletek száma + 2) (Laplace).
4. Ismétlés π̂-val a konvergenciáig (legfeljebb 3 kör).
5. A kis (12 entitásos) *teszt*világokban a rendszer π̂-val fut.

Két populáció:
- **A:** a procedurális generátor (a tankönyv sosem szemét, a szabályok 10%-a hibás);
- **B:** keverék: a világok 30%-ában a tankönyv egy másik, véletlen szabályrendszerből jön (egészében
  téves), a többi az A szerinti.

A kontextus-izolálás árát (ρ) közös hiperpriorral kötöm π-hez (49. kör): a tankönyv izolálásának
prioresélye a szemét-arány fele, ρ = (1 − π)/2, így ára −log₂ ρ (π = 0,95-nél 5,3 bit, a mostani 6 bit
közelében). A „figyelmen kívül hagyás” két magyarázata így nem árazható el egymástól függetlenül.

A deklarált q itt *feltételes*: „ha az elmélet ép, egy állítása q valószínűséggel helyes”. A keverék
ezért nem kalibrált (q₁ = q). A B populációban a kalibráció nem is volna teljesíthető, mert
π < (q − q₀)/(1 − q₀) = 0,9.

### Jóslatok

- **Korlát a futtatás előtt (saját tervhiba javítva):** Laplace-becsléssel n tanító világból
  π̂ ≤ (n + 1)/(n + 2). Az első tervben 8 világ szerepelt; ott π̂ ≤ 0,9, vagyis legalább 10%
  szemét-arány, ami **engedékenyebb**, mint a κ_T = 1 implicit kb. 5%-a. Egy ritka esemény (1%)
  megtanulásához kb. 100 világ kellene. A futás 24 tanító világgal megy (π̂ ≤ 0,96).
- **J1 (A):** π̂ ∈ [0,92; 0,96] (legfeljebb 1 világ ítélve szemétnek). **A kis világokban ez nem hoz
  érdemi javulást** (a teljes elvetés legfeljebb 1-gyel csökken), mert 4%-os szemét-arány alig
  különbözik a κ_T = 1 implicit 5%-ától. **Ha ez teljesül, a hierarchikus becslés elvben helyes, de
  ebben a méretben gyakorlatilag hatástalan.**
- **J2 (B):** π̂ ≈ 0,7 (0,5–0,85). A kis világokban a valóban szemét tankönyvet a rendszer legalább
  annyiszor veti el, mint a v4.4, a jó tankönyvet ritkábban.
- **J3 (kudarc-feltétel):** ha a tanító világokban a MAP-ítélet maga is π-függő (a 45. kör 3. állítása
  szerint a kemény hozzárendelés minden vagy semmi), az EM a kiinduló π₀-nál ragadhat. Ezt π₀ = 0,9 és
  π₀ = 0,999 indítással ellenőrzöm. Ha a két indítás más π̂-ot ad, az eljárás nem azonosít, és ezt
  eredményként jelentem.

- **J4 (a 50. kör után, még a futtatás előtt):** a 50. kör szerint a κ_T = 1 egy 50%-os szemét-arányú
  terület priorja (TFB-9: két rivális elmélet, az egyik téves). Ha az eljárás működik, a B populációban a
  teszt két szemét tankönyvét (seed 21 és 28) a rendszer elveti vagy izolálja, a többi hatot nem.

### Ismert módszerek

Ez a hierarchikus Bayes / meta-tanulás legegyszerűbb esete: egy hiperparaméter becslése sok feladat
együtteséből, kemény EM-mel. **Nem új módszer.** Az ARLC-ben az új az, hogy a 49. kör óta tudjuk,
*melyik* paraméter igényli ezt, és miért nem becsülhető egy világból.

### Kapcsolat a B fázissal

Ha a forrás *típusa* (tankönyv, szakértő, pletyka) a szövegből felismerhető, a π típusonként tanulható,
és a típus becslése az LLM feladata lehet (51. kör, 4.2). A B fázis blokkolt, ezért itt a típus orákulum.

## 2. rész: eredmények

Kód: [`hier.py`](../../experiments/arlc/arlc/hier.py); eredmény:
[`results/kor-52/`](../../experiments/arlc/results/kor-52/) (`A_pi095.json`, `B_pi095.json`, esetenkénti gyorsítótár).
Eltérés: a konténer az A populáció 1. iterációja közben újraindult. A 0. iteráció eredményeit a naplóból
töltöttem vissza, a futás folytatható gyorsítótárral folytatódott. Az esetek determinisztikusak.

### A kemény EM

| populáció | iteráció | π | szemétnek ítélt (24-ből) | valódi szemét | új π̂ |
|---|---|---|---|---|---|
| A | 0 | 0,95 | 2 (mindkettő hamis pozitív) | 0 | 0,885 |
| A | 1 | 0,885 | 2 (ugyanaz a két világ) | 0 | **0,885** (fixpont) |
| B | 0 | 0,95 | 9 (8 találat, 1 hamis pozitív, 1 tévesztés) | 9 | 0,615 |
| B | 1 | 0,615 | 10 (8 találat, 2 hamis pozitív) | 9 | 0,577 |
| B | 2 | 0,577 | 10 | 9 | **0,577** (fixpont) |

### Teszt: 8 kis (12 entitásos) világ a becsült π̂-val

| seed | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | átlag |
|---|---|---|---|---|---|---|---|---|---|
| v4.4 (49. kör, π nélkül) | 0,87 | 0,57\* | 0,90 | 0,79 | 0,91 | 0,52\* | 0,91 | 0,52\* | 0,747 |
| A, π̂ = 0,885 | 0,87 | 0,57\* | 0,90 | 0,83 | 0,91 | **0,72** | 0,91 | 0,51\* | **0,777** |
| B, π̂ = 0,577 (21 és 28 szemét) | 0,58\*ˢ | 0,57\* | 0,90 | 0,83 | 0,91 | 0,52\* | 0,91 | 0,51\*ˢ | 0,716 |

(\*: tankönyv félretéve; ˢ: a tankönyv valóban szemét)

### Ítélet a jóslatokról

| jóslat | eredmény | ítélet |
|---|---|---|
| **J1 (A):** π̂ ∈ [0,92; 0,96], érdemi javulás nélkül | π̂ = **0,885**; félretevés 3 → 2, átlag +0,03 | **π̂ nem teljesül** (lefelé sodródik); a javulás kicsi, de nem nulla |
| **J2 (B):** π̂ ≈ 0,7 (0,5–0,85) | π̂ = **0,577** (valódi arány 0,625) | **teljesül** |
| **J3:** a kiindulástól függ-e | nem futtattam (idő) | **nyitott** |
| **J4 (B):** a szemét tankönyvet elveti, a jót ritkábban | szemét 2/2 félretéve; jó 2/6 félretéve | **részben**; a jó tankönyvek félretevése nem ritkább, mint az A-ban |

### Értelmezés

1. **A populáció-szintű becslés működik, ha a populációban valóban vannak szemét elméletek** (B: 0,577 vs.
   0,625). Ott, ahol nincsenek (A), a becslés a rendszer saját hibáit (2 hamis félretevés) a populáció
   tulajdonságának tekinti, és **rossz fixponton áll meg** (0,885 a valódi 1,0 helyett). Ez a kemény EM
   önmegerősítő torzítása, ugyanaz a mintázat, mint a 45. kör κ̂ = 1-e: **a módszer a modell hibás módusát
   tanulja meg, mint a világ tényét.**
2. **Az A-ban mégis kicsi javulás van** (0,747 → 0,777). Ennek oka nem π̂, hanem a keverék másik
   komponense (κ₁ = 30: a néhány hiba olcsóbb, kisebb a farmolás) és a π-hez kötött kontextusár. A 26-os
   világ így tartja meg a tankönyvet.
3. **A 22-es és 28-as világ félretevése minden változatban megmarad.** A 49. kör szerint ez valódi
   MDL-optimum ezen a priorcsaládon. Ezt csak a félretevés *árának* helyes modellezése változtathatja meg,
   ami a jóslatvesztést is magában foglalja (51. kör).
4. **Gyakorlati tanulság:** a „szemét elmélet” prior sok világon át tanulható, de **a tanítójelnek
   függetlennek kell lennie a modell saját döntéseitől** (pl. orákulum- vagy külső címkék a forrás
   minőségéről, vagy a B fázisban az LLM-től származó forrástípus). A saját MAP-ítéletekből tanulva a hiba
   rögzül.
