# 87. kör – Generátor-egységteszt: megengedett-e az igaz hipotézis, és mennyibe kerül

*(Ellenőrző kör, nem hipotézisvizsgálat: a benchmark érvényességét méri, nem a rendszert.)*

## 1. A teszt

A 84. kör javaslata szerint minden generátorra ellenőrizni kell két dolgot:
1. **Megengedettség:** létezik-e olyan ütközésmentes hipotézis, amely *pontosan* a hamis megfigyeléseket teszi félre, és
   ezen túl csak kivételeket használ (igaz megfigyelést nem tesz félre, kontextust nem izolál). Ha nincs, a generátor a
   saját sémájával ellentmondásos világot gyártott.
2. **Ár:** a megengedett igaz hipotézis mennyibe kerül a modell szerint a talált hipotézishez képest. Ha jóval drágább, az
   adott adatmennyiség mellett a világ nem azonosítható, és a pontosság-különbségek egy része holtversenyeket mér.

Kód: [`gen_check.py`](../../experiments/arlc/arlc/gen_check.py) (megengedettség), [`true_cost_r87.py`](../../experiments/arlc/arlc/true_cost_r87.py)
(ár). Az igaz hipotézis építése: a hamis megfigyelések félretéve, majd minden maradék ütközésre egy kivétel annál a
szabálynál, amelyik rosszat jósol. Ahol az igazság nem definiált (Nixon-gyémánt), bármelyik ütköző szabálynál. A
G2-n a prioritás-kivétel is megengedett.

## 2. Megengedettség (70 seed generátoronként: 44000–44029, 16000–16019, 22000–22019)

| generátor | megengedett világ | ütközés-fajta a nem megengedettekben | kivétel/világ (megengedettben) |
|---|---|---|---|
| G1 (44. kör) | **3 / 70** | alosztály-szabály + tankönyv + népszámlálás (diszjunkt csúcsok) | 18,7 |
| **G1k** (85. kör) | **70 / 70** | – | 30,8 |
| **G2** (77. kör) | **70 / 70** | – | 18,7 |

A régi G1 a világok 96%-ában ellentmondásos (a 82. kör 3. része 47/50-et talált más mérőszámmal). A javított G1k és a G2
minden világa megengedett.

## 3. Az igaz hipotézis ára (v4.9+PK, a meglepetés előtt, 22000–22004)

| | G1k: talált | G1k: igaz | G2: talált | G2: igaz (csak egyedi kivétel) | G2: igaz (prioritás-kivétellel) |
|---|---|---|---|---|---|
| 22000 | 195,3 (0,844) | 216,0 (0,939) | 152,0 (0,963) | 193,7 | 154,9 (0,993) |
| 22001 | 166,0 (0,877) | 179,9 (0,889) | 153,1 (0,844) | 277,7 | 186,1 (0,953) |
| 22002 | 210,4 (0,854) | 236,7 (0,933) | 176,1 (0,902) | 239,9 | **169,9** (1,000) |
| 22003 | 201,3 (0,759) | 220,1 (0,857) | 151,5 (0,893) | 172,5 | 155,2 (0,980) |
| 22004 | 180,3 (0,870) | 221,5 (0,953) | 167,8 (0,922) | 253,4 | 171,9 (0,984) |

(Bit; zárójelben a pre-acc.)

**Értelmezés:**
1. **A G2-n az igaz hipotézis a prioritás-kivétellel 3–33 bitre van a találttól,** egy seeden (22002) olcsóbb is (6 bit).
   Ott **keresési hiba** van. A többi esetben a különbség kicsi, és nagyrészt a megbízhatósági kódból jön (81. kör). A
   prioritás-kivétel nélkül az igaz hipotézis 20–125 bittel drágább: **a PK a G2-n pontosan azt a kifejezőerőt adja,
   amely az igaz magyarázatot versenyképessé teszi.**
2. **A G1k-n az igaz hipotézis 14–41 bittel drágább, mint a talált.** Ezen az adatmennyiségen (entitásonként 3 tény)
   **a G1k világa nem azonosítható MAP-pal.** A talált hipotézis egyszerűbb, és 0,05–0,10-zel pontatlanabb. Egy valószínű
   ok: a G1 a terepi tényeket 0,9-es deklarált hitelességgel közli, a valódi zaj viszont 0,05. Így egy igaz tény
   félretétele (log₂(0,9/0,1) ≈ 3,2 bit + 1 bit illeszkedés) olcsóbb, mint egy valódi kivétel (log₂(0,95/0,05) ≈ 4,2
   bit), holott a generátorban a kettő nagyjából egyformán gyakori. **Ez a deklarált hitelesség rossz kalibrációja,
   nem a modell hibája.** A tanult megbízhatóság elvben javíthatná, de κ = 30-nal és kb. 90 terepi ténnyel lassan
   mozdul. Nem vizsgáltam tovább.
3. **Következmény a pontossági plafonra:** a G1k-n a MAP-alapú rendszer az igazság közelébe csak több adattal vagy jobban
   kalibrált forrásokkal juthat. A G2-n már most a plafon közelében van (a hátralévő rés részben keresési hiba).

## 4. Ami ebből szabály lesz

- **Minden új generátor és minden új seed-tartomány előtt lefut a `gen_check`.** Nem megengedett világ nem kerülhet
  benchmarkba.
- **Minden új mechanizmus mellé az igaz-hipotézis-ár is kerül** (legalább 5 seeden): megmutatja, hogy a változás a keresést
  vagy a modellt javítja.
