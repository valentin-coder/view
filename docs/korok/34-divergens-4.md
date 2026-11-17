# 34. kör – Divergens és kritikai kör (a 30–42. kör után)

(A körszámozás a terv szerinti. A 35–42. kör a 34. előtt készült el, mert a 32–33. kör hosszú
futásai alatt párhuzamosan haladtak.)

## Mi lett erősebb?

| állítás | kör | állapot |
|---|---|---|
| A célfüggvény egy generatív modell MAP-célja, a kivételekkel együtt | 36, 41 | **ProbLoggal igazolva** |
| A nyalábkeresés megtalálja az optimumot (kis feladatokon) | 36 | **kimerítően igazolva**, egy hiba után |
| A beágyazottság, a küszöbök és a Quine-féle mag zárt alakban jósolhatók | 26, 38, 40, 41 | 96/96, 47/48 (a maradék holtverseny), 24/24 |
| Fogalomalkotás anomáliákból, általánosítással | 30 | igen, visszavétellel |
| A gestalt-váltás és a zajtűrés összeegyeztethető | 32 | **igen**, kétszintű hitelességgel |
| A visszhang-polarizáció megszüntethető | 33 | **igen**, származás-tudattal |

## Mi gyengült vagy dőlt meg?

| állítás | kör | állapot |
|---|---|---|
| Az átrendezés „azonnali” | 42 | **ebben a megvalósításban nem.** Egy hétköznapi megfigyelés 0,1–0,7 ms, egy meglepetés 0,15–24 s. |
| Az ARLC új következtetési módszer | 36 | **nem.** Egy valószínűségi logika MAP-következtetése. |
| A 21. körös gyorsítás helyes | 36 | **nem**, optimalitási rést okozott |
| A felejtés semleges tömörítés | 37 | **nem**, a konkrét ütközési szerkezet elvész |

## A legfontosabb önkritika: a kutatói szabadságfokok

A 26–42. körben a magba **kilenc új kapcsoló** került: újonc-prior, forrás-hiteltelenítés,
forrásszintű lépés, evidencia-öregedés, osztályszintű kivétel, kategória-feltalálás és visszavétel,
kétszintű hitelesség, felejtés, kivétel-prior. Mindegyiket egy-egy *saját* játékfeladat hibája
indokolta, és mindegyiket ugyanazon a feladaton értékeltem ki. **Ez a túlillesztés klasszikus
receptje** („garden of forking paths”, Gelman–Loken 2013). A javítások talán csak a saját
feladataimra jók.

**Amit ez a programra jelent:**
1. **Be kell fagyasztani egy ARLC v4 konfigurációt**, minden kapcsolóval és paraméterrel, *mielőtt*
   újabb feladatokon mérünk.
2. **Kell egy olyan feladatkészlet, amelyet nem én terveztem kézzel:** egy *procedurálisan
   generált* benchmark véletlen szabályvilágokkal és véletlen meglepetésekkel, amelynek generátorát
   a v4 rögzítése előtt írom meg, és csak utána nézek rá az eredményekre.
3. **A paramétereket (ε, κ_T, κ_S, c_ctx) adatból kell becsülni** (empirikus Bayes, marginális
   valószínűség), nem kézzel hangolni. Ez a paraméterek hangolásából eredő szabadságfokot csökkenti.

## Új irányok

| | ötlet | tudományág | érték | rombolás |
|---|---|---|---|---|
| A | **ARLC v4 befagyasztott specifikáció és ablációs tábla** | módszertan | magas | nem ad új eredményt, de minden további kör alapja |
| B | **Procedurálisan generált, előre rögzített benchmark** | módszertan | **nagyon magas** | a generátor is az én döntésem; de legalább nem a v4 után készül |
| C | **Empirikus Bayes az ε, κ paraméterekre** | statisztika | magas | a marginális valószínűség a hipotézistér felett nehéz; közelítés: a legjobb nyalábon |
| D | **Inkrementális pontozás** | algoritmusok | magas (a „azonnali” állítás miatt) | mérnöki munka; a helyességét a 36. kör kimerítő ellenőrzésével kell igazolni |
| E | **Az átrendezett állapot és a magyarázat (39. kör) visszaírása az LLM promptjába** | „neuro” fél | magas, de B fázist igényel | – |

## Őszinte helyzetkép az újdonságról

Ha ezt a munkát ma össze kellene foglalni, a **nem újdonságok:** a valószínűségi logika, a
hiedelemrevízió, a forrás-megbízhatóság, a predikátum-invenció, az oksági absztrakció. Mindegyik
ismert. **A lehetséges hozzájárulások:**
1. egy **jelenségtár**: tizenöt-húsz revíziós jelenség (anomália-tűrés, Quine-mag, Hume-korlát,
   olcsó álnevek, visszhang-polarizáció, gestalt–zaj feszültség, felejtés-interferencia,
   korai elméletfeladás) **egyetlen generatív modellből levezetve**, zárt alakú küszöbökkel;
2. az **identifikálhatósági térkép**: hol nem dönt az adat elvben (kontextus vagy hazug; újonc vagy
   támadó), és ezért hol *kell* külső (neurális) jel;
3. **módszertani ellenőrzések** a B fázishoz (35. kör): statikus alapvonal, véletlen súlyú kontroll,
   kifejezésszintű statisztika, lexikai átfedés.

Hogy ezek közül bármelyik új-e, irodalomkutatás nélkül nem tudom eldönteni. **Ellenőrizendő.**

## Következő körök

43. ARLC v4 befagyasztott specifikáció és ablációs tábla (A).
44. Procedurálisan generált benchmark, előre rögzített generátorral és elemzési tervvel (B).
45. Empirikus Bayes az ε, κ paraméterekre (C).
46. Inkrementális pontozás és újramérés (D).
47. Divergens és kritikai kör.
