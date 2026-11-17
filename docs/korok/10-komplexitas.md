# 10. kör – Komplexitás: mennyire lehet „azonnali” egy globális átrendezés?

A cél „azonnali” átstrukturálást kér. Ez a kör megnézi, mit enged meg ebből a
számításelmélet, és hogyan kell ennek fényében átalakítani az ARLC v2-t.

## Az elméleti fal

- **A propozicionális hiedelemrevízió általában nehéz.** Eiter és Gottlob (1992) szerint a
  legtöbb ismert revíziós operátorra (Dalal, Satoh, Winslett, Ginsberg stb.) annak eldöntése,
  hogy egy formula következik-e a revideált tudásbázisból, Σ₂ᴾ-teljes vagy Π₂ᴾ-teljes. Ez a
  P≠NP feltevés mellett szuperpolinomiális időt jelent.
- **A minimális hitting set (Reiter-diagnózis) NP-nehéz.** Ha a felsorolandó diagnózisok
  mérete legfeljebb k, a futásidő `O(n^k)`.
- **Az ATMS címkéi exponenciálisan nőhetnek** a feltevések számában.
- **Az ARLC MDL-pontszáma** a kontextus-szétválasztásnál min-cut-ot és egy ezen felüli
  keresést is tartalmaz, tehát legalább ugyanilyen nehéz.

**Következmény:** a tetszőleges tudásbázison végzett, globálisan optimális azonnali
átrendezés nem lehetséges. A cél csak az alábbi három út valamelyikén érhető el.

## Három út az „azonnalisághoz”

### 1. Korlátozott nyelv

- **Horn-szabályok** mellett a következtetés lineáris időben fut (unit propagation), az
  ATMS-propagáció polinomiális marad a címkeméretben.
- **Korlátozott revízióméret:** csak legfeljebb k = 2–3 feltevés visszavonása jöhet szóba.
  Ez `O(n^k)` jelöltet ad, ami kis k-ra kezelhető.
- **Ára:** a 9. körben a 9. fokozatú változás már így sem ment. A korlátozott k a
  többfeltevéses kuhni váltást is kizárja. Az előző körben bevezetett második rendű
  feltevés (σ) itt segít: egy σ-csere *egyetlen* feltevés, de sok szabályt mozdít.
  **Ez a második rendű feltevések számítási indoklása:** a nagy változást egy kis
  revízióba sűrítik.

### 2. Előre számolt alternatívák (az A13 tagadása, 1. fázis)

- A rendszer B darab versengő hipotézist tart karban a háttérben, és mindegyikre
  inkrementálisan frissíti a pontszámot.
- Az átrendezés ilyenkor csak *kiválasztás*: O(B) művelet.
- **A költség áthelyeződik:** a lekérdezésre adott válasz gyors, de a háttérben futó
  karbantartás drága. Pontosan ezt jósolja Kounios–Beeman a belátásra: hosszú, tudattalan
  inkubáció után hirtelen váltás (7. kör).
- **Kockázat:** ha egyik előre számolt alternatíva sem jó, az átrendezés vagy lassú,
  vagy nem történik meg.

### 3. Anytime revízió

- Az átrendezés azonnal visszaad egy *elfogadható* megoldást (pl. mohó hitting set),
  aztán a háttérben javítja.
- A javításnak le kell mondania az optimalitásról, de monoton javul.
- **Formális követelmény:** az első megoldás az időben legfeljebb `O(|Cone|)`, a
  kúpmérettel lineáris. A javítások az MDL-pontszámot monoton csökkentik.

## Javasolt ARLC v3 számítási modell

A három út együtt:

| Komponens | Mit csinál | Költség |
|---|---|---|
| Horn-mag + korlátos k | következtetés és visszavonás | polinomiális |
| Második rendű feltevések (σ) | a nagy változásokat egyetlen feltevés cseréjébe sűríti | egy σ-csere O(1) revízió, a kúp szerint lineáris propagáció |
| B elemű nyaláb | előre számolt alternatívák | háttérben O(B·propagáció) megfigyelésenként |
| Anytime revízió | ha egyik alternatíva sem elég jó | mohó első megoldás, háttérbeli javítás |

**A cél újrafogalmazása számítási szempontból:**
> Az átrendezés *döntése* és *végrehajtása* a kúpmérettel lineáris időben fut, ha a
> szükséges alternatíva a nyalábban van. Ha nincs, a válasz egy anytime közelítés, amely
> a háttérben javul.

## Ellenőrizhető állítások és mérések

- **M1 – skálázás:** a kúpméret (10, 100, 1000, 10 000 következmény) függvényében mért
  falióra-idő. Lineáris kell legyen, ha az alternatíva a nyalábban van.
- **M2 – nyalábtalálat:** a TFB (9. kör) feladatain hányszor van a helyes alternatíva a
  B elemű nyalábban. B = 4, 16, 64 mellett.
- **M3 – anytime minőség:** az első, mohó megoldás MDL-pontszáma hány %-ban marad el az
  optimumtól (kis feladatokon az optimum kimerítő kereséssel ellenőrizhető).
- **Cáfolat:** ha a nyalábtalálat B = 64 mellett is 50% alatt van a TFB 5–8. fokozatán,
  akkor az „előre számolt alternatíva” út nem működik, és az azonnaliság csak a Horn-mag
  triviális eseteire igaz.

## Kapcsolódó munkák

- Eiter–Gottlob 1992 (a revízió komplexitása); Reiter 1987; de Kleer 1986.
- Anytime algoritmusok: Dean–Boddy 1988; Zilberstein 1996.
- **Ellenőrizendő:** léteznek-e Horn-revízióra polinomiális operátorok, amelyek az AGM
  posztulátumok gyengített változatát teljesítik (Delgrande–Peppas és mások, Horn belief
  change, 2010-es évek).
