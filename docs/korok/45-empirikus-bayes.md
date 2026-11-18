# 45. kör – Empirikus Bayes az ε és κ paraméterekre, és egy harmadik programhiba

A 34. kör kritikája szerint a v4 paraméterei (ε = 0,05, κ_S = 30, κ_T = 1) kézzel vannak beállítva.
Ha a célfüggvény egy generatív modell MAP-célja (36. kör), a paraméterek elvben az adatból
becsülhetők: ez az empirikus Bayes (II. típusú maximum-likelihood). Ez a kör megvizsgálja, mit
becsül valójában ez az eljárás ebben a modellben. A jóslatokat a futtatás *előtt* írtam le (1–3. pont),
az eredmények az 5. pontban vannak.

Kód: [`empirical_bayes.py`](../../experiments/arlc/arlc/empirical_bayes.py).

## 1. Az eljárás

- **A cél:** L\*(θ) = min_H L(H; θ), ez a −log₂ P(D | θ) max-közelítése (a marginális összeg
  helyett a legjobb hipotézis). A becslés: θ̂ = argmin_θ L\*(θ).
- **Olcsó, pontos újrapontozás.** Egy H pontszáma ε-ban és κ-ban zárt alakú. A többi tag nem
  függ tőlük:
  `L(H; ε, κ) = R(H) + A(H; ε) + B(H; κ)`,
  ahol A az abnormalitás-tag, B a béta-binomiális forráskód. R(H)-t egyszer számolom, ezért egy
  sűrű (ε, κ)-rács minden pontja egyetlen keresés jelöltjeiből kiértékelhető. Ellenőrzés: a zárt
  alakú és a közvetlenül újraszámolt pontszám eltérése 0 (12 véletlen (H, ε, κ) hármason).
- **Jelöltek:** valódi keresés három ε-ponton (0,01; 0,05; 0,2), mindegyik teljes nyalábjával.
  L\*(θ) így felső becslés: csak a gyűjtött jelöltek fölött minimalizál.

## 2. Elmélet: mit becsül az eljárás?

### 2.1. A naiv becslés elfajul (1. állítás)

A mag pontszámában (41. és 43. kör) **minden** (jelentett szabály, entitás) pár egy
abnormalitás-változó, a meg nem figyeltek is:

`A_naiv(H; ε) = k·(−log₂ ε) + (N_all − k)·(−log₂(1 − ε))`,  N_all ≈ |jelentett szabály| · |entitás|.

Egy rögzített H-ra a minimum helye ε = k / N_all. Egy 20 entitásos procedurális világban
N_all ≈ 60 · 20 = 1200, k ≈ 5, ezért **ε̂ ≈ 0,004**, és a becslés N_all-lal fordítottan arányos.
Ez a 41. körben megszüntetett világméret-műtermék a becslésben: **ugyanaz a terület nagyobb
világban kisebb ε̂-ot kapna.**

A hipotézisválasztást ez nem érinti, mert a tag H-tól független része konstans. Paraméterbecslésre
viszont alkalmatlan.

### 2.2. A marginális változat

A generatív modellben egy meg nem figyelt alkalmazás abnormalitás-változója kiösszegezhető:
ε + (1 − ε) = 1. A helyes tag tehát csak a megfigyeléssel érintett alkalmazásokat számolja:

`A_marg(H; ε) = k·(−log₂ ε) + N_rel(H)·(−log₂(1 − ε))`,

ahol N_rel az elfogadott, szabály által jósolt tények száma. Ezzel ε̂ = k / N_rel, ami a látható
kivételarány becslése.

*Közelítés:* az alosztály-szabályok normál alkalmazásait nem számolom (csak a kivételeiket). Egy
alosztály-alkalmazás hatása több lépésben terjed, a pontos marginalizálás drága.

### 2.3. Azonosíthatatlanság egyszeri méréssel (2. állítás)

Ha minden (e, p) tényről egyetlen forrás egyetlen jelentése szól, egy szabálynak ellentmondó
jelentés valószínűsége a generatív modellben:

`c = ε/2 + (1 − ε)·[r·δ + (1 − r)/2]`,

ahol r a forrás megbízhatósága. **Az adat csak c-t határozza meg; ε és r külön nem azonosítható**,
csak a prior (q, κ) rögzíti őket. Egy ellentmondó tény két olcsó magyarázata:
- kivétel: log₂((1 − ε)/ε) ≈ 4,25 bit (ε = 0,05);
- a forrás hibája: log₂((κq + n − k − 1)/(κ(1 − q) + k)) ≈ 4,25 bit (κ = 30, q = 0,9, n ≈ 90, k ≈ 3).

A befagyasztott v4-ben a kettő **véletlenül majdnem pontosan egyenlő**, így a döntés kis
különbségeken múlik.

**Ismételt méréssel (két független forrás ugyanarról a tényről)** a két magyarázat szétválik. Egy
kivételnél mindkét jelentés ellentmond a szabálynak; zajnál általában csak az egyik. Ekkor ε és r
azonosítható.

### 2.4. Kemény hozzárendelés: „minden vagy semmi” (3. állítás)

A max-közelítés minden ellentmondást vagy kivételnek, vagy elutasításnak sorol be. Rögzített
c ellentmondás mellett, ha j-t magyaráz kivétel, a költség

`f(j) = N_rel·h(j/N_rel) + B_forrás(c − j)`,

ahol h a bináris entrópia (a profilozott ε-tag). Mindkét tag konkáv a darabszámban (a béta-binomiális
kód is), ezért **a minimum a végpontokon van**: vagy minden ellentmondás kivétel (ε̂ ≈ c/N_rel),
vagy egyik sem (ε̂ a rács alja). Ez a kemény EM ismert torzítása (osztályozó EM; Celeux és Govaert
1992, ellenőrizendő).

## 3. Jóslatok (a futtatás előtt)

- **J1:** a naiv ε̂ minden világban a rács aljához közeli (≤ 0,005), a valódi kivételaránytól függetlenül.
- **J2:** egyszeri méréssel a marginális ε̂ nem követi a valódi kivételarányt; ha követ valamit, az a
  kivétel és a zaj együttese (c). A becslés kétcsúcsú: k ≈ 0 vagy k ≈ az összes ellentmondás.
- **J3:** ismételt méréssel a marginális ε̂ a látható kivételaránnyal nő.
- **J4:** κ̂-ra egyetlen terepforrásból nincs stabil becslés. A κ a forrásokat összekötő
  populáció-paraméter (mennyire térnek el a források a deklarált hitelességüktől), egyetlen forrás
  egyetlen mintát ad belőle. Várhatóan κ̂ a rács valamelyik szélére esik.
- **J5:** az empirikus Bayes-szel illesztett paraméterekkel mért pontosság nem jobb lényegesen a
  befagyasztott v4-énél.

## 4. A harmadik programhiba: ingyenes kivételek az indukált és feltalált szabályokon

Az 1. rész megírása közben a pontszám tagjait egyenként ellenőriztem, és egy újabb hibát találtam.
A kivétel-prior „jelölt alkalmazásai” (43. kör) csak a *megfigyelt* (jelentett) szabályokat
tartalmazzák. **Az indukált, a feltalált és a kétfeltételes szabályok kivételei ezért ingyenesek.**

**Célzott teszt:** 8 normál és 8 csíkos, nem mérges dax után a v4 feltalálja a „csíkos dax nem
mérges” szabályt. Ezután három új csíkos dax érkezik, amelyek mérgesek, vagyis ellenpéldák.

| | 1. ellenpélda | 2. | 3. |
|---|---|---|---|
| v4 (befagyasztott) | ingyenes kivétel a feltalált szabályon, a szabály marad | 2 ingyenes kivétel | 3 ingyenes kivétel |
| v4.2 (javítva) | **a feltalált szabály kiesik** (kizárás), a kategória marad | ugyanaz | ugyanaz |

**A hiba súlya:** egy feltalált vagy indukált szabály a v4-ben **ellenpéldákkal nem cáfolható**,
mert minden ellenpéldát ingyen kivétellé tesz. Ez pontosan az a dogmatizmus, amely ellen az
architektúra készült.

**Miért helyes a v4.2 döntése:** a feltalált szabály haszna 8 anomáliánál
8·0,926 − 6 ≈ 1,4 bit (47. kör), egy kivétel ára 4,25 bit. Egyetlen ellenpélda után az elhagyás
olcsóbb.

**Javítás** (`ind_exc_cost` kapcsoló, a v4.2-ben bekapcsolva):
- a jelöltlistán kívüli szabályok kivétele ugyanazt a határköltséget kapja, mint egy tankönyvi
  szabályé: log₂((1 − ε)/ε);
- a normál alkalmazásaik nem kapnak tagot (a 2.2. pont marginális szemlélete). Így nem tér vissza a
  világméret-műtermék, amelyet egy alkalmazásonkénti −log₂(1 − ε) tag okozna (egy indukált szabály
  30 entitásnál kb. 2,2 bittel drágulna).

**A 44. kör benchmarkját ez nem érinti:** az előregisztrált futás a befagyasztott v4-gyel megy
tovább, a kapcsoló alapból ki van kapcsolva. A procedurális világokban (seed 1000, 1001) a v4 nem
indukált szabályt, így ott a hiba várhatóan ritkán aktív. A v4.2-t másodlagos, címkézett
változatként futtatom.

**A validációs lefedettség negyedszer:** sem a kimerítő ellenőrzés, sem a ProbLog-összevetés nem
tartalmazott indukált vagy feltalált szabályt, ezért egyik sem foghatta meg a hibát. A célzott
egységteszt igen.

## 5. Eredmények

*(a futtatás után kerül ide)*
