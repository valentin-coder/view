# 82. kör – Menekülőút-audit: a félretevések minősége a generátor igazsága alapján (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 79. kör szerint a sorozat visszatérő hibamintája a menekülőút: a rendszer egy kifejezhetetlen szerkezetet egy olcsó,
de hamis magyarázattal helyettesít (izolálás, bűnbak-forrás). Eddig ezt csak közvetve, a pontosságon keresztül láttam,
és esetenként kézzel diagnosztizáltam (78., 81. kör). A generátorok ismerik az igazságot, ezért **minden félretevésről
eldönthető, hogy helyes volt-e.** Ez egy pontosságtól független, mechanizmus-szintű mérőszám.

### Mérőszámok

Kód: [`audit_truth.py`](../../experiments/arlc/arlc/audit_truth.py). Minden megfigyelésre a meglepetés előtti világ
szerint: igaz, hamis vagy nem definiált. A végső hipotézisben forrásonként és fajtánként (szabály/tény):
- **helyes félretevés:** hamis állítás félretéve;
- **téves félretevés:** igaz állítás félretéve (ez a menekülőút közvetlen mértéke);
- **elmulasztott:** hamis állítás elfogadva;
- a félretevés **pontossága:** helyes / (helyes + téves);
- izolált források, osztály- és egyedi kivételek száma.

### Elrendezés

- **Seedek:** 19000–19019 (friss). Típus: hazug forrás. G2; G1 A és B populáció (B-ben a 19007, 19013, 19016, 19017-es
  seed szemét-tankönyves).
- **Módszerek:** v3, v4.9, v4.9+PK (81. kör). Kód: [`run_r82.py`](../../experiments/arlc/arlc/run_r82.py). 180 eset.

### Hipotézisek

- **H82a (G2, a meglepetés előtt):** a tankönyvi szabályok átlagos téves félretevése a v4.9+PK-nál legfeljebb fele a
  v4.9-ének.
- **H82b (G2, v4.9):** a tankönyvi szabályok félretevésének pontossága < 0,5 (a tankönyv bűnbak: több igaz szabályt
  tesz félre, mint hamisat).
- **H82c (G2):** a fieldB helyes félretevéseinek átlaga a v4.9+PK-nál legalább akkora, mint a v3-nál (a tanult
  megbízhatóság a valóban rossz terepforrást találja meg).
- **H82d (G1-A):** a v4.9 és a v4.9+PK az esetek legalább 95%-ában egyetlen forrást sem izolál (ezekben az esetekben
  nincs valódi kontextus).
- **H82e (mindhárom halmaz):** a hazug forrás félretett aránya a v4.9-nél és a v4.9+PK-nál ≥ 0,9, a v3-nál kisebb.

Leíró (nem hipotézis): a G1-B szemét-tankönyves seedjein a tankönyv félretevésének pontossága; a G1-A-ban a tankönyvi
téves félretevések száma (van-e ott is bűnbak).

## 2. rész: eredmények

Nyers adat: [`results/kor-82/test/`](../../experiments/arlc/results/kor-82/test/); elemzés:
[`analyze_r82.py`](../../experiments/arlc/arlc/analyze_r82.py) → `results/kor-82/analysis.json`. 180 eset, eltérés nincs.

### Félretevések a meglepetés előtt (átlag esetenként; zárójelben a pontosság: helyes / összes félretevés)

**G2:**

| | pre | tankönyv: helyes / téves | fieldB: helyes / téves / elmulasztott | fieldA: helyes / téves | népszámlálás: téves | osztálykivétel |
|---|---|---|---|---|---|---|
| v3 | **0,921** | 1,45 / 4,30 (0,25) | 6,95 / **0,20** / 5,00 (**0,97**) | 1,55 / 0,25 | 1,35 | 0 |
| v4.9 | 0,871 | 1,35 / 6,35 (0,18) | 5,90 / 9,65 / 6,05 (0,38) | 0,60 / 0,20 | 0,25 | 0 |
| v4.9+PK | 0,920 | 1,35 / **2,10** (**0,39**) | 7,50 / 4,90 / 4,45 (0,61) | 0,75 / 0,20 | 0,45 | 4,5 |

**G1-A:**

| | pre | tankönyv: helyes / téves | field: helyes / téves / elmulasztott | izolál (esetarány) |
|---|---|---|---|---|
| v3 | 0,824 | 1,15 / 4,95 (0,19) | 1,95 / 3,20 / 2,95 (0,38) | 0 |
| v4.9 | 0,833 | 0,95 / 3,20 (0,23) | 0,85 / 1,70 / 4,05 (0,33) | 0,05 |
| v4.9+PK | 0,830 | 0,90 / 3,10 (0,23) | 0,90 / 1,80 / 4,00 (0,33) | 0,05 |

**A hazug forrás félretett aránya:** v3: 0,74 (G2), 0,54 (G1-A), 0,41 (G1-B); v4.9 és v4.9+PK: **1,00 mindenhol.**

### A hipotézisek

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H82a (G2):** tankönyvi téves félretevés PK ≤ ½ · v4.9 | 2,10 ≤ 3,18 | **teljesül** |
| **H82b (G2, v4.9):** tankönyvi pontosság < 0,5 | 0,18 | **teljesül** |
| **H82c (G2):** fieldB helyes félretevés PK ≥ v3 | 7,50 ≥ 6,95 | **teljesül**, de l. lent |
| **H82d (G1-A):** ≥ 95%-ban nincs izolálás | 95% (v4.9 és PK is) | **teljesül** (épp a határon) |
| **H82e:** hazug arány v4.9, PK ≥ 0,9 > v3 | 1,00 vs. 0,41–0,74 | **teljesül** |

### Amit az audit megmutatott, és amit a pontosság elrejtett

1. **A 81. kör egyik állítását visszavonom.** Ott azt írtam, hogy a v4.9+PK „a valóban rossz fieldB-t teszi félre
   (9,75; a várható hibaszám kb. 11)”. Az audit szerint ennek csak 61%-a helyes. Esetenként 4,9 *igaz* fieldB-jelentést
   is félretesz, a v3 viszont 0,2-t (pontosság 0,97). **A tanult megbízhatóság a fieldB-t másodlagos bűnbakká
   teszi:** ha egy forrás megbízhatósága lecsökken, az igaz jelentéseinek félretevése is olcsóbb lesz. Ez ugyanaz a
   Pólya-urna-tulajdonság (78. kör), csak kisebb mértékben. A rögzített megbízhatóságú v3 ebben pontosabb.
2. **A tankönyvi félretevések többsége minden módszernél téves, mindkét generátoron** (pontosság 0,18–0,39). A G1-A-ban
   is esetenként kb. 3 igaz szabály esik ki kb. 1 valódi hibára. Hat G1-A seeden megnéztem, mik ezek: 17 téves
   félretevésből **13 alosztály-szabály** (isa), 4 pedig olyan tulajdonság-szabály, amelynek egy tagjánál valódi egyedi
   kivétel van. **Egy alosztály-kapcsolat elvágása új menekülőút:** egyetlen lépéssel eltünteti az összes örökölt
   ütközést (pl. többszörös öröklésnél), ahelyett hogy a rendszer az ütköző tulajdonságot kezelné. A pontosságban ez
   azért nem látszik nagyon, mert egy elvágott kapcsolat csak a levélkategória tagjait érinti. Ez a sorozat ötödik
   menekülőút-mintája.
3. **A szemét-tankönyves G1-B seedeken a mérőszám félrevezető:** a v4.9 az egész tankönyvet félreteszi (helyesen, mert a
   tankönyv nem hordoz információt). A véletlenül igaz szabályok félretevése így „tévesnek” számít (pontosság 0,29). Az
   igazság-alapú audit **informatív forrásokra** érvényes. Egy információmentes forrás teljes félretevése akkor is
   helyes, ha néhány állítása véletlenül igaz. A v3 ezekben a seedekben két forrást izolál, és a hazug forrást egyszer
   sem teszi félre (post 0,26 vs. 0,57).

### Következmények

- **Az audit mostantól minden mérés mellé kerül.** Két hibát talált, amelyet a pontosság elrejtett: a fieldB másodlagos
  bűnbakká tételét és az alosztály-kapcsolat elvágását.
- **Nyitott kérdés (a 85. körre):** miért olcsóbb az alosztály-kapcsolat elvágása, mint a prioritás-kivétel? A PK mellett
  is csak 0,4 osztálykivétel van esetenként a G1-A-ban. Ehhez az igaz-hipotézis-pontozás (81. kör) G1-es változata kell.
- **A tanult megbízhatóság ára:** pontosabb felismerés az *új*, rossz forrásoknál (hazug: 1,00 vs. 0,4–0,7), pontatlanabb
  félretevés a *régi*, közepesen rossz forrásoknál (fieldB: 0,61 vs. 0,97). A kettő ugyanaz a mechanizmus. Egy jó
  megoldásnak a béta-kód rugalmasságát a hazug-szerű (szinte minden állítása hamis) esetre kellene korlátoznia.

## 3. rész: javítás – az „alosztály-elvágás” nem menekülőút, hanem a G1 generátorhibája

*(A 83. kör futása alatt, a 85. kör diagnózisának előkészítésekor derült ki.)*

A G1-en összeraktam az igaz hipotézist (a hamis megfigyelések félretéve). Ez **nem ütközésmentes:** például a 19000-es
seedben az M1 középkategóriának két szülője van, T0 és T1, és a séma szerint **minden csúcskategória-pár diszjunkt**.
A generátor (44. kör, `procedural.generate_world`) a középkategóriáknak 25% eséllyel két csúcs-szülőt ad, a
diszjunktságot viszont minden csúcspárra kimondja. **Az ilyen világ logikailag ellentmondásos:** egy M1-be tartozó
entitás egyszerre tartozik T0-ba és T1-be, ami tilos. A rendszernek egy igaz alosztály-kapcsolatot (vagy egy igaz
tagságot) kötelezően félre kell tennie.

**Mérték:** 50 G1-világból (a 44. és a 82. kör seedjei) **35 ellentmondásos**, és az entitások **27%-át érinti.**

**Következmények:**
1. **A 2. rész 2. pontját visszavonom.** Az „alosztály-kapcsolat elvágása mint ötödik menekülőút” nem a modell hibája:
   a világ ellentmondásos, és az elvágás a legolcsóbb (és logikailag kikényszerített) válasz. Az audit ezeket „téves
   félretevésnek” számolta, mert az igazság-függvény a diszjunktságot nem veszi figyelembe.
2. **A 44. óta minden G1-mérés ezt a hibát hordozza.** Az összehasonlítások egyenlő feltételek mellett zajlottak (minden
   módszer ugyanazokat a világokat kapta). Az abszolút pontosságok viszont alacsonyabbak a kelleténél, és nem zárható ki,
   hogy a módszerek az elvágás *módjában* (melyik kapcsolat esik ki) különböznek, és ez a különbségek egy részét adja.
   Az előregisztrált eredményeket nem írom át. A javított generátoron (85. kör) újramérem a fő összevetést.
3. **A javítás minimális:** két csúcskategória csak akkor diszjunkt, ha nincs közös középkategória-gyerekük. A 85. kör
   ezt „G1k” néven használja, és a régi G1-et változatlanul hagyja.
