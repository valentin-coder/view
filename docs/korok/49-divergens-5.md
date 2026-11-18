# 49. kör – Divergens és kritikai kör (5.): a hibák mintázata, egy szisztematikus kereső, és a specifikus öröklés hiánya

(Minden ötödik kör kritikai. Ez a harmadik ilyen kör a kísérleti szakaszban, a 29. és 34. után.)

Kód: [`audit.py`](../../experiments/arlc/arlc/audit.py),
[`small_worlds.py`](../../experiments/arlc/arlc/small_worlds.py),
[`search_vs_prior.py`](../../experiments/arlc/arlc/search_vs_prior.py), `core.py` (`auto_specificity`);
eredmény: [`results/kor-49/`](../../experiments/arlc/results/kor-49/).

## 1. A hibalista

| kör | hiba | típus | ki fogta meg |
|---|---|---|---|
| 36 | szűkített visszahelyezés: optimalitási rés | keresés | kimerítő ellenőrzés |
| 43 | ingyenes kivételek alosztály-szabályon és levezetett tagságon | pontszám | ablációs tábla (nem a ProbLog-ellenőrzés) |
| 43 | elméleti hírnév-farmolás (κ_T = 1) | modellezés | ablációs tábla; **nyitott** |
| 45 | ingyenes kivételek indukált és feltalált szabályon | pontszám | célzott egységteszt |
| 46 | holtverseny-feloldás `str(kulcs)` szerint: a frozensetek sorrendje a hash-seedtől függ | reprodukálhatóság | ekvivalencia-ellenőrzés |
| 48 | felső osztályra adott osztályszintű kivétel: álcázott elutasítás | lépéskészlet | komponensenkénti abláció |
| 48 | a 43. kör E1-diagnózisa hiányos volt | saját elemzés | komponensenkénti abláció |
| 48 | a saját vázlatom állítása (mintázat vs. darabszám) | saját elemzés | önellenőrzés |
| 49 | **a specifikus öröklés hiánya** (lásd 4. pont) | modellezés | kis világok + felülírás-számlálás |

**Mintázat.** Egyik hibát sem a meglévő validációs csomag fogta meg, mindegyiket egy *újonnan írt*,
célzott vizsgálat. A validáció (kimerítő keresés, ProbLog) csak azt a lépés- és szabálytípust fedte
le, amely a véletlen feladataiban szerepelt. Minden új lépéstípus (kivétel, osztálykivétel,
indukció, feltalálás, kontextus) egy új, olcsóbb utat nyitott egy hiedelemállapothoz, amelyet a
rendszer addig csak hitelesség-ellenőrzött lépéssel érhetett el.

Ez szerkezeti ok. Az ARLC költségmodellje lépésenként, kézzel árazott tagok összege. Egy valódi
generatív modellben egy hiedelemállapot valószínűsége nem függ attól, melyik lépés vezetett oda. Itt
viszont függ, mert minden lépéstípus saját, külön kitalált árat kapott.

## 2. Szisztematikus kereső: megfigyelési ekvivalencia-audit

Egy elfogadott o állítás elutasítása egy meghatározott hiedelemállapotot ad (a fő kontextus
zárását). Ha egy *más* lépés ugyanezt a zárást adja, akkor ugyanazt az állapotot más áron fejezi ki.
- **Erős ekvivalencia:** a másik lépés minden jövőbeli entitásra is ugyanazt adja (felső osztályra
  adott kivétel; egy egész forrás kontextusba izolálása a forrás összes állításának elutasítása
  helyett). Ha ez olcsóbb, a hitelesség-ellenőrzés megkerülhető. **Ez hiba.**
- **Gyenge ekvivalencia:** csak a meglévő entitásokra (példánykivétel minden alkalmazásra; egy
  alosztályra adott kivétel). Ez valódi alternatíva más általánosítással, nem hiba.

**Eredmény 8 kis procedurális világon** (12 entitás, seed 21–28):

| | v4 | v4.3 |
|---|---|---|
| nem-alosztályos (álcázott) osztálykivétel **a végső hipotézisben** | **4 világban** (21, 23, 24, 25) | 0 (tiltva) |
| erősen ekvivalens, olcsóbb alternatíva elérhető a pontszámban | 8–16 állításnál világonként | ugyanannyi, de a keresés nem lép rá |
| gyengén ekvivalens, olcsóbb alternatíva | az auditált állítások 50–75%-a | ugyanígy |
| egész forrás: izolálás (6 bit) vs. összes állítás elutasítása | izolálás 6 bit; elutasítás 30–60 bit | ugyanígy |

**Értelmezés:**
1. **A felső osztályos kiskapu a v4-ben nem ritka különlegesség,** hanem a kis világok felében aktív.
2. **A gyenge alternatíva többnyire olcsóbb az elutasításnál.** Egy tankönyvi szabály szűkítése
   osztálykivétellel 5–7,8 bit, az elutasítása a hírnév-farmolás (κ_T = 1) miatt 9,9–12,7 bit. A
   rendszer ezért **inkább szűkíti egy hibás szabály hatókörét, mint hogy elvesse**. Ez a Lakatos-féle
   védőöv viselkedése, és a farmolás mérhető nyoma.
3. **A kontextus-izolálás ára a forrás méretétől független** (6 bit). Egy 48 állításos tankönyv vagy egy
   36 tényes terepforrás „más kontextusról beszél” magyarázata ugyanannyiba kerül. A π = 0,999-es
   keverékkel (lásd 3. pont) a rendszer pontosan erre tér át: elvetés helyett izolál.

## 3. A „teljes elvetés” kis világokban

8 kis világból a v4 3-ban, a v4.3 4-ben **a teljes tankönyvet elveti** (pontosság 0,52–0,63, szemben a
többi világ 0,80–0,90-ével):

| világ (seed) | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | átlag | teljes elvetés |
|---|---|---|---|---|---|---|---|---|---|---|
| v4 | 0,87 | 0,57\* | 0,90 | 0,80 | 0,89 | 0,52\* | 0,86 | 0,52\* | 0,740 | 3 |
| v4.3 | 0,87 | 0,57\* | 0,90 | 0,81 | **0,63\*** | 0,52\* | 0,86 | 0,52\* | 0,710 | 4 |
| v4.3 + keverék π = 0,999 | 0,87 | 0,57ⁱ | 0,90 | 0,83 | 0,63ⁱ | 0,52ⁱ | 0,86 | 0,52ⁱ | 0,712 | 0 (de 4 izolálás) |
| v4.3 + keverék π = 0,999 + gondozott forrás kontextusára 10 bit | 0,87 | **0,74** | 0,90 | 0,83 | 0,63\* | 0,52\* | 0,86 | 0,52\* | 0,733 | 3 |
| **v4.4 = v4.3 + automatikus specifikusság** | 0,87 | 0,57\* | 0,90 | 0,79 | **0,91** | 0,52\* | **0,91** | 0,52\* | **0,747** | 3 |

(\*: a teljes tankönyv elvetve; ⁱ: tankönyv és népszámlálás kontextusba izolálva)

**Keresési hiba vagy valódi optimum?** A 22-es világban a „csak a hibás tankönyvi szabályok elvetve”
hipotézis mohó befejezéssel 104,8 bit, az online talált teljes elvetés 91,6 bit. **A teljes elvetés
valódi MDL-optimum, nem keresési hiba.** Oka a κ_T = 1 U alakú priorja: minden további elvetett
szabály 4–6 bitbe kerül, ezért 9 elvetett szabály (kb. 45 bit) drágább, mint az egész tankönyv
elvetése (kb. 10 bit) plusz 36 tény jóslatvesztése (kb. 33 bit).

**A 25-ös világ esete a legtanulságosabb.** A v4 egy álcázott osztálykivétellel (31, T0) megtartja a
tankönyvet (0,89). A v4.3-ban ez a kiskapu zárva van, és a rendszer elveti az egészet (0,63). **A
kiskapu egy nagyobb hibát takart.** Az automatikus specifikusság (4. pont) ezt a világot 0,91-re hozza.

## 4. A specifikus öröklés hiánya (új modellezési hiba)

A procedurális generátor igazság-szemantikája **specifikus öröklés**: egy alkategória ellentétes
szabálya felülírja az ősét, és ez *normális*, nem kivétel. Az ARLC-ben ugyanez **ütközés**, amelyet
árazott lépéssel kell feloldani: osztálykivétellel (kb. 5 bit), elutasítással vagy példánykivételekkel.
A kis világokban a tankönyv szerinti felülírás-párok száma:

| seed | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|---|---|---|---|---|---|---|---|---|
| felülírás-pár (tagokkal érintett) | 6 | 3 | 3 | 3 | 6 | **7** | 4 | **7** |
| tankönyvi hibák | 4 | 5 | 4 | 4 | 2 | 6 | 2 | 8 |
| v4 teljes elvetés | | igen | | | | igen | | igen |

A teljes elvetés a sok felülírással vagy sok hibával terhelt világokban jelenik meg.

**Javítás (`auto_specificity`):** ha két ellentétes előjelű szabály ugyanazt a tulajdonságot jósolja
egy entitásra, és az egyik törzse a másikénak szigorú alosztálya (az elfogadott alosztály-szabályok
szerint), a specifikusabb ingyen nyer. Ez Touretzky (1986) öröklési hálóinak specifikussági elve, és
a nem monoton logikák „specifikusság szerinti prioritása” (ellenőrizendő: Touretzky 1986; Horty,
Thomason és Touretzky 1990). **Nem új:** ez a klasszikus öröklési hálók alapértelmezése. A 27. körben
az osztályszintű kivétel árazott lépésként került be. Ez a hiba egyik forrása volt: amit a
szakirodalom alapértelmezésnek tekint, azt az ARLC kivételnek árazta.

**Mért:** a 25-ös és 27-es világ 0,89/0,63 → 0,91, illetve 0,86 → 0,91; az átlag 0,740 → 0,747. A
teljes elvetés a 22-es, 26-os és 28-as világban megmarad. Ott az ok a 3. pontbeli prior (a sok
tankönyvi hiba), nem a felülírás.

## 5. A gestalt-váltás és a téves teljes elvetés ugyanaz a lépés

A 48. kör keverék-priorja kis π-vel (π = 0,99 vagy 0,999, a „szemét elmélet” prioresélye 1%, illetve
0,1%) a teljes elvetést 12–16 bitre drágítja. Ez a hírnév-farmolást is csökkenti (6 bit n = 60-nál),
és az E1-et 0,845-ről 0,875-re javítja. **De a TFB-9 gestalt-váltását tönkreteszi:**

| | TFB-9 pontosság | vesztes fa aktív |
|---|---|---|
| v4.3 (κ_T = 1) | 0,977 | 0,00 |
| v4.3 + keverék π = 0,99 | 0,796 | 0,60 |
| v4.3 + keverék π = 0,999 | 0,807 | 0,83 |

**A TFB-9 helyes teljes elvetése és a kis világok téves teljes elvetése ugyanaz a lépés, ugyanazzal a
priorral.** Hogy melyik a helyes, az attól függ, milyen gyakran téves egészében egy elmélet a
területen. Ez a populáció-szintű π, és **egyetlen világból nem becsülhető** (45. kör, J4). Ez a 28.
kör „gyors váltás ↔ zajtűrés” feszültségének elméletszintű változata. Egyetlen rögzített prior nem
oldja fel, csak a terület alapgyakoriságának ismerete (vagy sok világon át tanult hierarchikus prior).

## 6. Kritika: mit jelent ez az egész sorozatra?

1. **A rendszer viselkedését ma inkább a lépésárak egymáshoz viszonyított értéke határozza meg, mint
   az adat.** A 22., 25. és 48. kör döntései 0,5–3 bites különbségeken múltak, és ezek a különbségek
   kézzel választott konstansokból jönnek (c_ctx = 6, log₂|C| + 1, κ_T = 1).
2. **A 44. kör benchmarkja szerkezeti hátrányt mér:** a generátor specifikus öröklést használ, amelyet a
   befagyasztott v4 nem tud ingyen kifejezni. Ezt az előregisztráció előtt nem vettem észre. A
   benchmark így a v4 *ezen* hiányát is méri, nem csak a revíziós képességét.
3. **A legerősebb javaslat a 34. kör óta: a v5 ne lépésenként árazott pontszám legyen, hanem egy
   explicit generatív modell** (például ProbLog-program), és a keresés csak ennek MAP-közelítése. Ekkor
   egy hiedelemállapot ára nem függ a lépéstől, a kiskapuk *szerkezetileg* nem létezhetnek, a
   specifikus öröklés pedig a modell része. A 36. kör megmutatta, hogy a mag erre lefordítható. A
   kivétel, a kontextus, a feltalálás és a tanult megbízhatóság még nem.
4. **MAP vagy átlagolás.** Ha a minőségileg eltérő hiedelemállapotok 0,5–3 bitre vannak egymástól, a
   MAP-válasz sorsszerű. A nyaláb poszterior-súlyú átlaga (w_H ∝ 2^(−L)) kalibrált bizonyosságot és
   „nem tudom”-ot adna. Ezt a 44. kör v4.3-as másodlagos futása feltáró jelleggel méri.
5. **Reprodukálhatóság:** a mohó lépés holtversenyeit a frozensetek `str` sorrendje dönti el, és ez a
   hash-seedtől függ. 4 kis világon az eredmény ettől független volt, de ez nem garancia. A v5-höz
   kanonikus holtverseny-feloldás kell (ez a 46. kör inkrementális tervének is feltétele).

## 7. A következő körökre

- **50. kör:** a v4.4 (automatikus specifikussággal) az ellenőrző csomagon és a kimerítő
  ellenőrzésen; a 44. kör eredménye a v4-re (előregisztrált), a v4.3-ra és a v4.4-re (másodlagos).
- **51. kör:** a generatív v5 vázlata: melyik ARLC-lépés milyen látens változó, és mi az ára.
- **52. kör:** hierarchikus prior sok világon át (π, c_ctx, ε), avagy meta-tanulás.
