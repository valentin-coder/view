# 38. kör – Quine hiedelemhálója: melyik szabály esik egy lánc mentén?

## Kérdés (vízszintes kapcsolat)

Quine (1951, „Two Dogmas of Empiricism”; Quine–Ullian 1970, *The Web of Belief*) szerint a
hiedelmek hálót alkotnak. Egy ütköző tapasztalat a periférián okoz módosítást, a magot csak végső
esetben érinti (*minimális csonkítás*, konzervativizmus). **Az ARLC-ben megfelel-e ennek a
viselkedés, és ha igen, pontosan mi a „mag”?**

## Elrendezés

- **Lánc:** S = „dax ⊂ állat” (taxonómia), G = „állat → élő” (biológia), mindkettő q = 0,95.
- **Alátámasztás:** n_S megfigyelt dax „élő” ténnyel (ezt S és G együtt jósolja), és n_G megfigyelt,
  nem dax állat „élő” ténnyel (ezt csak G jósolja).
- **Anomália:** m darab „x_j egy dax, és nem élő”, mindegyik más friss forrásból.
- **Lehetséges revíziók:** S feladása; G feladása; G hatókörének szűkítése a daxokra (osztályszintű
  kivétel, 27. kör); példány-kivételek; az anomáliák elutasítása.
- 48 konfiguráció: n_S, n_G ∈ {0, 2, 6, 12}, m ∈ {1, 3, 6}, osztályszintű kivétellel és nélküle.

Kód: [`quine.py`](../../experiments/arlc/arlc/quine.py); eredmény: [`results/kor-38/`](../../experiments/arlc/results/kor-38/).

## Zárt alakú jóslat

A „mindent megtart, az anomáliákat elutasítja” hipotézishez képest a jelöltek többletköltsége
(bitben; L₀ = log₂(q/(1 − q)) = 4,25 a szabály forrásköltsége, ℓ = 1 + log₂(1 − δ) = 0,93 egy
elvesztett jóslat ára):

| revízió | költség |
|---|---|
| anomáliák elutasítása | m · log₂(0,9/0,1) = 3,17·m |
| S feladása | L₀ + n_S · ℓ |
| G feladása | L₀ + (n_S + n_G) · ℓ |
| G hatókör-szűkítése | log₂|C| + 1 + n_S · ℓ |
| példány-kivételek | m · log₂|E| |

**Tétel (a „mag” védelme).** Ha egy G szabály jóslati kúpja tartalmazza egy S szabályét, és egyforma
a hitelességük, akkor az ARLC G-t soha nem adja fel S előtt. *Bizonyítás:* a két elvetés költsége
`L₀ + |kúp|·ℓ`, és `|kúp(S)| ≤ |kúp(G)|`. Ha valamelyik elvetés megszünteti az ütközést, S
elvetése is megszünteti (S a láncban G előtt áll, ugyanazokra az anomáliákra hat). ∎

**A „mag” itt tehát pontos fogalom: a nagyobb jóslati kúpú szabály.** A periféria a kisebb kúpú
szabály vagy a hatókör-szűkítés.

## Eredmény

| | jóslat = mért | a választások megoszlása |
|---|---|---|
| osztályszintű kivétellel | **47/48** | G hatókör-szűkítése 30, elutasítás 13, példány-kivétel 5, **G feladása 0** |
| osztályszintű kivétel nélkül | **46/48** | S feladása 24, elutasítás 18, példány-kivétel 6, **G feladása 0** |

**Mind a három eltérés pontos holtverseny** (elutasítás és példány-kivétel egyaránt 3,17 bit, mert
log₂|E| = log₂ 9). A holtversenyeken kívül a jóslat mindenhol egyezik.

## Értelmezés

1. **A minimális csonkítás az ARLC-ben következmény, nem beépített elv.** G-t egyetlen
   konfigurációban sem adja fel. A perifériát módosítja: osztályszintű kivétellel a „dax állat, de az
   élő-szabály nem vonatkozik rá” megoldást választja, anélkül az alosztály-kapcsolatot dobja el.
2. **A két változat különbsége tanulságos.** Osztályszintű kivétellel megmarad a taxonómia (a dax
   állat), és csak egy szabály hatóköre szűkül. Anélkül a taxonómiát kell feladni. **A
   specifikussági elv (27. kör) tehát a taxonómiai tudást is védi.**
3. **Sok alátámasztás mellett (n_S = 12) kevés anomáliát (m ≤ 3) a rendszer egyszerűen
   elutasít.** Ez Kuhn „normál tudománya”, a 7. kör K\*-követelményének megfelelően.

## Kapcsolódás és megszorítás

- **Quine** a hálót metaforaként írta le. Itt egy *mérhető* változat jön ki: a mag a nagy jóslati
  kúpú szabály, a csonkítás mértéke bit.
- **AGM-beágyazottság** (Gärdenfors–Makinson 1988, ellenőrizendő): az epistemikus beágyazottság egy
  rendezés, amelyet az AGM *adottnak* vesz. Itt a rendezés a jóslati kúpból és a hitelességből
  *következik*. Ez az MDL-alapú revízió egyik valódi értelmezési haszna.
- **Megszorítás:** csak lineáris lánc, egy anomália-típus. Elágazó hálókban (egy tény két független
  úton is levezethető) a kúpok átfedése bonyolultabb; a tétel ott nem közvetlenül alkalmazható.
