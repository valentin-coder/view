# 26. kör – A „helyi kiút” és az olcsó álnevek: diagnózis, tételek, kísérlet

## Összefoglaló

1. A 19. és 20. kör azt állította, hogy a „ez a példány nem is tartozik ide” helyi kiút
   **megkerüli** a forrásellenőrzést. **Ez pontatlan volt.** A pontszám-felbontás szerint a
   rendszer *összeveti* a tagságot közlő és az ellenpéldát közlő forrás megbízhatóságát, és a
   rövidebb múltú forrást nyilvánítja tévedőnek. Ez racionális.
2. A valódi gyengeség a **friss identitások ingyenes bizalma**. Minden új forrás a teljes
   előzetes hitelességet kapja, ezért a sybil-támadás olcsó. Ez a reputációs rendszerek ismert
   „olcsó álnév” problémája.
3. A béta-binomiális kódból **zárt alakú átfordulási pontok** vezethetők le négy forgatókönyvre.
   A jóslat a 96 pontos rács **mind a 96 pontján** pontosan egyezik a mérttel.
4. **A becsületes újonc és az egyetlen támadó megfigyelés alapján megkülönböztethetetlen**
   (24/24 rácspontban azonos átfordulás). Ez a sybil-probléma szimbolikus kiúttalanságának oka,
   és megfelel Douceur 2002-es lehetetlenségi eredményének (ellenőrizendő).
5. Az újoncok kezdő bizalmának csökkentése a sybileket megállítja, de **a becsületes újoncokat
   is lassítja** („Planck-elv”). Egy finomabb támadás, a **hírnév-farmolás**, alacsony kezdő
   bizalom mellett is átjut.

## 1. Diagnózis: a pontszám felbontása

A 19. kör első változatában a tagságot (`x dax`) egy harmadik forrás (`survey`) közölte, az
ellenpéldát (`x nem mérges`) a forgatókönyv forrása. Két hipotézis tartja meg a szabályt:
„az ellenpéldák hibásak” vagy „a tagságok hibásak”. A forrásonkénti béta-binomiális bitek
(κ = 30, N = 6, R = 20, 3 anomália):

| forgatókönyv | „ellenpéldák hibásak” | „tagságok hibásak” | választás |
|---|---|---|---|
| becsületes (`field`) | **39,28** (field: 14,44) | **37,40** (survey: 10,80) | tagság |
| sybil (3 friss forrás) | 37,65 (sybilenként 3,32) | 37,62 (survey: 10,80) | tagság (0,03 bittel) |
| egyetlen támadó | **36,64** (attacker: 8,95) | 37,61 (survey: 10,80) | ellenpélda |

- **Becsületes eset:** a `field` (kb. 29 elfogadott állítás) három állításának elutasítása
  11,4 bit többletbe kerülne, a `survey` (kb. 10 állítás) háromé 9,5 bitbe. **A rendszer a
  rövidebb múltú forrást tartja tévedőnek.** Ez nem kiút, hanem bizalmi összevetés.
- **Sybil-eset:** majdnem pontos holtverseny. A három friss forrás mindegyike a teljes előzetes
  hitelességgel indul (`log₂(0,9/0,1) = 3,17` bit elutasításonként).
- **Egyetlen támadó:** a harmadik elutasítás már olcsó, mert a támadó „hazug”-sága tanulódik.

## 2. Formális levezetés

**Jelölések.** Egy forrás előzetes eloszlása `Beta(α, β)`, `α = κq₀`, `β = κ(1 − q₀)`. Ha a
forrás n állításából a hipotézis k-t utasít el, a forrás kódhossza
`L(n, k) = log₂ B(α, β) − log₂ B(α + n − k, β + k)`.

**Lemma (határköltség).** Rögzített n mellett egy további elutasítás ára
`L(n, k+1) − L(n, k) = log₂((α + n − k − 1)/(β + k))`.

*Bizonyítás.* `B(a, b)/B(a − 1, b + 1) = (a − 1)/b`, mert
`B(a, b) = Γ(a)Γ(b)/Γ(a + b)` és `Γ(a) = (a − 1)Γ(a − 1)`, `Γ(b + 1) = bΓ(b)`. ∎

Értelmezés: a határköltség a forrás *utólagos* megbízhatóságának log-esélye, az épp vizsgált
állítás nélkül.

**1. állítás (friss identitás).** Egy múlt nélküli forrás egyetlen állításának elutasítása
`log₂(α/β) = log₂(q₀/(1 − q₀))` bitbe kerül. Ez csak az előzetes eloszlástól függ.
Anomáliánként két állítás (tagság és ellenpélda) esetén, amelyből egyet elutasítunk, a súly
`L(2,1) − L(2,0) = log₂((α + 1)/β)`. Ezért **m sybil-anomália súlya `m·log₂((α + 1)/β)`, a
történettől függetlenül.**

**2. állítás (régi forrás).** Egy R elfogadott állítás után m anomáliát hozó forrás súlya
`D(m) = Σᵢ₌₀^{m−1} log₂((α + R + m + i)/(β + i))` (anomáliánként két állítással; a pontos
alakot a `theory.py` számolja). **A becsületes, régi forrás anomáliánként kb.
`log₂((α + R)/α)` bittel többet nyom, mint egy friss.** Az elválasztás a múlt hosszával
logaritmikusan nő.

**3. állítás (újonc–támadó ekvivalencia).** Ha két forrásnak nincs múltja, ugyanazt a
deklarált hitelességet kapják, és ugyanazokat az állításokat teszik, akkor a pontszámuk és
így az átfordulási pontjuk **azonos**. *Bizonyítás:* a kódhossz csak (α, β, n, k)-tól függ,
a forrás nevétől nem. ∎ Ez triviális, de a következménye nem: **szimbolikus adatból a
becsületes újoncot a támadótól elvben nem lehet megkülönböztetni.** Ez Douceur (2002, „The
Sybil Attack”) lehetetlenségi eredményének a megfelelője: egy logikailag központi, az
identitásokat igazoló hatóság nélkül a sybil-támadás mindig lehetséges.

**4. állítás (sybil vs. egyetlen identitás, hírnév-farmolás).** A rendszer ott fordítja át a
szabályt, ahol az anomáliák elutasításának súlya eléri a szabály elvetésének költségét,
`T(N) = log₂(0,95/0,05) + N·(1 + log₂(1 − δ)) ≈ 4,25 + 0,926·N` bit.
- Magas kezdő bizalomnál (q₀ = 0,9) **a sybil a jobb támadás** (8 vs. 9 anomália N = 20-nál). A
  friss identitások mindegyike teljes súllyal indul, az egyetlen identitás pedig hazugként
  tanulódik.
- Alacsony kezdő bizalomnál (q₀ ≤ 0,7) **az egyetlen identitás a jobb** (16 vs. 18; q₀ = 0,5-nél
  24 vs. soha). Az egyetlen támadó anomáliánként egy *vitathatatlan* állítást is tesz (az új
  entitás tagságát), és ezekkel múltat épít. Az „mindent elfogadunk tőle” hipotézisben a forrás
  100%-ban helyes, az „elutasítjuk az ellenpéldákat” hipotézisben 50%-ban. Pesszimista
  előzetes eloszlás mellett a hosszú, hibátlan sorozat egyre valószínűbbé teszi az elsőt.
  **Ez a reputációs rendszerekből ismert hírnév-farmolás.**

## 3. Kísérlet (r26)

- **Elrendezés:** N ∈ {6, 12, 20} alátámasztó tény, a régi forrás múltja R ∈ {20, 80}, és a
  nem ellenőrzött források kezdő bizalma q₀ ∈ {0,9 (deklarált); 0,8; 0,7; 0,5}.
  Négy forgatókönyv: becsületes régi forrás, becsületes *új* forrás, sybil, egyetlen támadó.
  Mindkét állítást (tagság és ellenpélda) a forgatókönyv forrása közli. κ = 30.
- Nyers eredmény: [`experiments/arlc/results/kor-26/results.json`](../../experiments/arlc/results/kor-26/results.json);
  jóslatok: [`experiments/arlc/arlc/theory.py`](../../experiments/arlc/arlc/theory.py).
- **Jóslat vs. mért: 96/96 egyezés.**

**Átfordulási pontok, N = 20, R = 80** (hány anomália kell):

| q₀ | becsületes régi | becsületes új | sybil | egyetlen támadó |
|---|---|---|---|---|
| 0,9 | **5** | 9 | 8 | 9 |
| 0,8 | **5** | 12 | 12 | 12 |
| 0,7 | **5** | 16 | 18 | 16 |
| 0,5 | **5** | 24 | **soha** | 24 |

## 4. Értelmezés

1. **A becsületes régi forrás hatása nem függ q₀-tól** (mindig 5), mert az ő bizalma a múltjából
   jön. A kezdő bizalom csak az újoncokat érinti. Ez a javasolt védekezés lényege.
2. **A sybil-támadás q₀ = 0,5 mellett nem jut át**, mert a friss identitások súlya 0.
3. **Ennek ára a „Planck-elv”:** a becsületes újonc 9 helyett 24 anomáliát kell hozzon. Ha az
   újonc csak az ellenpéldákat közli, vitathatatlan kísérőállítások nélkül, *soha* nem jut át
   (ugyanaz, mint a sybil). Azoulay, Fons-Rosen és Graff Zivin (2019, „Does Science Advance One
   Funeral at a Time?”) empirikus eredménye szerint a tudományban a meghatározó szereplők
   halála után az újonnan belépők hozzájárulásai jobban érvényesülnek (ellenőrizendő a pontos
   állítás).
4. **A hírnév-farmolás alacsony q₀ mellett is átjut**, mert a vitathatatlan, de ellenőrizetlen
   állítások építik a támadó hírnevét. Védekezés: csak az *ellenőrzött* (más forrás által
   megerősített) állítások számítsanak a múltba. Ez a következő körökre vár.

## 5. Kapcsolódás más területekhez

| Terület | Kapcsolat |
|---|---|
| Elosztott rendszerek | Douceur 2002: központi hatóság nélkül a sybil-támadás nem zárható ki. Itt: szimbolikus adatból az újonc és a támadó nem különíthető el (3. állítás). |
| Reputációs rendszerek | Friedman–Resnick 2001 (az olcsó álnevek társadalmi költsége): az újoncoknak a legalacsonyabb hírnévvel kell indulniuk, különben a kitiltás után új néven visszatérés kifizetődő. Itt: q₀ < q. Kamvar et al. 2003 (EigenTrust): a bizalom a megbízhatóknak tulajdonított bizalomból terjed; ez a „csak ellenőrzött állítás számít” javítás általánosítása. |
| Tudományszociológia | Planck-elv; Azoulay et al. 2019. |
| Ismeretelmélet | A tanúságtétel ismeretelmélete: mikor bízzunk egy szakértőben (Goldman 2001, „Experts: which ones should you trust?”, ellenőrizendő). A 3. állítás szerint a múlt nélküli tanú hitelességét a tartalomból nem lehet megállapítani. |

## 6. Következmények az architektúrára

1. **Hibajegyzék:** a 19. kör „a helyi kiút megkerüli a forrásellenőrzést” állítása helyesen:
   *a helyi kiút a tagság forrását teszi felelőssé, ha annak rövidebb a múltja.* A 20. kör
   „strukturális gyengeség 1.” pontja ennek megfelelően gyengül. A valódi gyengeség az
   újoncok bizalma.
2. **ARLC v4:** hierarchikus forrás-előzetes. Az ellenőrzött források a deklarált hitelességet
   kapják, a többiek a populáció becsült átlagát, alacsony indulással. A múltba csak a
   megerősített állítások számítanak.
3. **A sybil-probléma szimbolikusan megoldhatatlan** (3. állítás és Douceur). Ez a 20. kör
   függetlenségi jelének *elvi* indoka: identitás- vagy függetlenségi jel kell kívülről.
   Ilyen lehet a stílus vagy a tartalom hasonlósága, amit egy LLM adhat.
4. **Kísérleti megszorítás:** a világ egy szabályból áll. Ha több szabály van, és a támadó
   közben máshol is hírnevet épít, a hírnév-farmolás erősebb lehet. Ezt még nem teszteltem.
