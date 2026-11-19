# 79. kör – Divergens és kritikai kör (11.): a 74–78. kör mérlege, és mi marad két generátor után

## 1. A 74–78. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 74 | mi a legjobb konfiguráció, és mire támaszkodik | v4.8-π + jelzett elsőbbség + nyaláb-átlag; két orákulumon (forrástípus, kontextusjel) |
| 75 | a legjobb konfiguráció előregisztrált mérése (G1: A, C) | **minden hipotézis teljesül:** +0,170 a v3-hoz, +0,112 a v4.4e-hez képest |
| 76 | szabályszintű zárás-memó | halasztva |
| 77 | második, független generátor (G2) | **az általános pontosság rosszabb a v3-énál** (−0,033); a forrás-felismerés átvihető (+0,07) |
| 78 | a G2-lemaradás oka | a kontextusfüggő indukció **nem** (friss seedeken 0,000); **a béta-megbízhatóság bűnbak-hatása** (modellhiba, a teljes lemaradás) |

## 2. Mi marad két generátor után

| állítás | G1 | G2 | státusz |
|---|---|---|---|
| hazug/torzított forrás felismerése (tanult megbízhatóság + forráslépés) | +0,15 (64. kör) | +0,07 – +0,09 (77. kör) | **áll mindkét generátoron** |
| általános pontosság a v3 fölött | +0,048 (57. kör, A ∪ B) | −0,020 (78. kör) | **generátorfüggő; nem általános** |
| a v3 fölötti általános előny forrása | specifikusság, osztálykivétel, feltalálás | ezek a G2-n inaktívak | **a G2 nem teszteli ezeket**: értékük továbbra is egyetlen generátoron áll |
| rivális elméletek kezelése metaadat-π-vel | +0,25 (60., 70., 75. kör) | a G2-ben nincs rivális elmélet | **külsőleg nem tesztelt** |
| Brier-javulás nyaláb-átlaggal | három mérésben (50., 63., 75. kör) | a v3 Brier-je jobb (0,065 vs. 0,074) | **csak G1-en** |
| a nyaláb nem poszterior-minta | 63., 67. kör | – | áll (elemzés) |

**Összegzés:** két generátor után egyetlen képesség áll erősen: **a megbízhatatlan forrás felismerése.** Ez a sorozat
eredeti célkitűzésének (meglepő információra azonnali, gradiens nélküli átrendeződés) pont egy darabja. A többi
javulás vagy egy generátoron áll, vagy a G2-n nem aktiválódik. Ez nem cáfolat, de **a v4 újításainak nagy része
továbbra sincs külső teszten.**

## 3. Kritika

### 3.1. A „menekülőút” valójában a félrespecifikált Bayes ismert jelensége

A sorozatban most negyedszer jelent meg ugyanaz a minta:

| kör | menekülőút | amit a modell nem tud kifejezni |
|---|---|---|
| 57, 60 | rivális tankönyvek izolálása kontextusba | „az egyik elmélet egészében téves” |
| 68 | két hamis magyarázat a helyes kontextus helyett | szabályszintű kontextus |
| 77–78 | indukció izolált kontextusban (ritka) | – |
| 78 | **bűnbak-forrás** (népszámlálás vagy tankönyv tömeges félretevése) | rejtett családprioritás |

A közös ok: **a világ olyan szerkezetet tartalmaz, amelyet a hipotézistér nem fejez ki, és a MAP a legközelebbi
kifejezhető magyarázatra fut.** Ez a KL-vetület egy félrespecifikált modellcsaládra. Minél rugalmasabb egy kód (béta,
kontextus, indukció), annál több olcsó „közeli” magyarázat van, és ezek egyike nyer. **Ez nem az ARLC sajátja, hanem a
félrespecifikált Bayes-következtetés ismert jelensége** (Grünwald és van Ommen, 2017: a poszterior félrespecifikált
modellben a „rossz” komplex magyarázatra koncentrálódhat; javaslatuk a temperált, η < 1-es likelihood, a SafeBayes). Az
eddigi javításaim (π metaadatból, jelzett kontextus, a 80. kör forrástípus-priorja) **mind esetenkénti árazások**: egy
konkrét menekülőutat drágítanak. A SafeBayes általános ellenszer volna, és nem kér metaadatot.

### 3.2. A második generátor sem független

A G2 szerkezete más (kereszt-osztályozás, rejtett prioritás, kalibrálatlan források), de **ugyanaz tervezte, ugyanabban a
nyelvben** (Obs, Rule, deklarált q). A forrás-megbízhatóság bevallott, számszerű q-ja például a valóságban nem létezik:
azt is egy LLM-nek kellene becsülnie. Valódi függetlenséget csak külső adat ad (B fázis, vagy egy valódi ütköző
tudásbázis). Ez hálózat nélkül blokkolt.

### 3.3. A feltáró ablációk kétszer vezettek félre

A 77. kör ablációja (kumulatív, 20 seed, egy típus) a kontextusfüggő indukciót nevezte fő kárnak. A 78. kör friss
seedjein ez nulla, és a tényleges ok a béta-megbízhatóság. A 77. kör kumulatív sorrendje (a v3-hoz egyenként hozzáadva)
elrejtette a kölcsönhatást. **Szabály mostantól:** feltáró ablációból oki állítás csak egyet-elhagyó (LOO) formában és
friss seedes megerősítés után kerül a mérlegbe.

### 3.4. Harmadik orákulum

A 80. körre tervezett javítás (forrástípus-prior) egy harmadik metaadat-orákulum: a forrás típusa (gondozott, terepi,
ismeretlen). Az első kettő a tankönyv-π (60. kör) és a kontextusjel (73. kör) volt. **A rendszer egyre nagyobb része a B
fázis LLM-jére hárított metaadatban él,** és egyiket sem mértük valódi modellen. A 61. kör SRC-feladata a forrástípust már
méri, ha egyszer futhat.

## 4. Divergens irányok

1. **Tanult szabályprioritás.** A G2 hiányzó primitívje: „az F_i család szabályai felülírják az F_j-éit”. Egyetlen
   hipotézis-komponens, ára log₂(párok száma), és minden kereszt-osztályozási ütközést egyszerre old fel kivételek
   tömege helyett. **Átcímkézés-ellenőrzés:** ez a prioritásos alapértelmezett logika (Brewka, 1989) és a „preferred
   subtheories”; a specifikusság (49. kör) ennek speciális esete (a specifikusabb nyer). Jóslat: a bűnbak-nyomás
   megszűnik, mert a prioritás olcsóbb magyarázat.
2. **SafeBayes / temperált likelihood** (3.1): a megfigyelés-illeszkedés kódját η < 1-gyel súlyozva a szerkezeti árak
   relatíve nőnek, és a rugalmas menekülőutak drágulnak. Grünwald η-t az adatból (szekvenciális predikcióval) választja.
   Ez metaadat nélküli alternatíva a 80. kör típus-priorjára; a kettő közvetlenül összevethető.
3. **Menekülőút-audit mint standard mérőszám.** A generátor ismeri az igazságot, ezért minden rugalmas mechanizmusra
   mérhető a **hamis használati arány**: izolálás valódi kontextus nélkül, gondozott forrás tömeges félretevése valódi
   hiba nélkül, feltalált kategória rejtett kategória nélkül. Ez a 64. és 67. kör azonosíthatósági ellenőrzésének
   általánosítása, és minden jövőbeli mérésben a pontosság mellé kerül.
4. **Időben változó világ (harmadik generátor).** Mindkét generátor statikus világot ír le egy egyszeri meglepetéssel. A
   valódi „meglepő információ” gyakran változás (a 11. kör vágási pontjai). Egy harmadik generátor, amelyben a szabályok
   időben sodródnak, a vágási mechanizmust tesztelné, amelyet a 44. kör óta nem mértem.

## 5. A következő körökre

- **80. kör:** forrástípus-prior a bűnbak-forrás ellen (előregisztrált, mindkét generátor friss seedjein).
- **81. kör:** menekülőút-audit (4.3) mindkét generátoron, a meglévő konfigurációkra.
- **82. kör:** tanult szabályprioritás (4.1), előregisztrálva a G2-n.
- **83. kör:** SafeBayes (4.2) a típus-prior metaadat nélküli alternatívájaként.
- **84. kör:** divergens és kritikai kör.
