# 104. kör – Divergens és kritikai kör (16.): a tárcsák köre

## 1. A 99–103. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 100 | megerősítés-függő új-forrás bizalom | fejlesztési negatív; **elvi korlát:** egyetlen állításból jó és rossz új forrás metaadat nélkül nem különböztethető meg |
| 101 | prior-érzékenység | a π_új tárcsa monoton, de szűk; **a deklarált hitelesség kalibrációja a legérzékenyebb pont,** aszimmetrikusan |
| 102 | óvatos hitelesség | a generatív világokon javít, a korai kézi feladatokon ront → **a konzervativizmus tárcsája** |
| 103 | egyszerűsítés | a q-csoport helyességi javítás; a „hatástalan” ítélet generátor-relatív volt |

## 2. A közös szerkezet: a maradék problémák tárcsák

A 89. kör óta minden nyitott probléma ugyanilyen alakú. Egy paraméter két jó tulajdonság között választ, és a helyes
értéke **a környezettől** függ:

| tárcsa | egyik vége | másik vége | kör |
|---|---|---|---|
| adaptív vs. rögzített forrás-kód | hazug forrás felismerése | bűnbak-forrás elkerülése | 89, 91 |
| κ a bevált forrásra | rosszul kalibrált forrás megtanulása (G4) | bűnbak elkerülése (G3) | 96 |
| π_új | hazug új forrás | jó új forrás (helyesbítés, specialista) | 100, 101 |
| q_temper | zajtűrés (generatív világok) | gyors átrendeződés (kézi feladatok) | 102 |

**Ez nem a rendszer hibája, hanem a feladat természete.** Egy meglepő megfigyelés lehet igaz (ekkor át kell
rendeződni) vagy zaj/hazugság (ekkor nem). A kettő közötti választás a környezet *alapgyakoriságaitól* függ: milyen
gyakran hazudnak az új források, milyen zajosak a bevált források, milyen gyakran változik a világ. A sorozat ezeket mindig
rögzített priorként adta meg (a sémában vagy a konfigurációban), és a benchmarkok más-más alapgyakoriságokat valósítottak
meg. **Ezért nincs olyan rögzített konfiguráció, amely minden benchmarkon jobb.** A G4 és a G3 (96. kör), a generatív és a
kézi feladatok (102. kör) közötti ellentét ezt mutatja.

**Elvi következmény:** a tárcsák helyes értékét **tanulni** kell, de nem egyetlen epizódon belül (ott az adat kevés, és a
MAP a saját hibáit erősíti: 78., 88. kör), hanem **epizódokon át**. Egy ágens, amely sok világot lát ugyanabból a
környezetből, megtanulhatja, hogy ott milyen gyakran igazak a meglepetések. Ez hierarchikus Bayes (empirikus Bayes az
epizódok szintjén), és az eredeti feladat „befagyasztott LLM” keretében is természetes: az LLM a világról szóló háttértudást
hordozza, az epizódokon átívelő kalibráció pedig a szimbolikus réteg hosszú távú memóriája.

## 3. Kritika

1. **A 95. kör konszolidációja túl gyors ítéletet hozott** („hatástalan”), és a 103. kör kellett hozzá, hogy kiderüljön: a
   q-csoport helyességi javítás. **A generátorok lefedettsége hiányos.** Minden forrás egyforma q-val jelent bennük, nincs
   bennük többlépéses hierarchia-változás, és nincs feltalálás. A feladatcsomag (a korai körök kézi feladatai) ezért nem
   régiség, hanem a lefedettség része.
2. **A korai kézi feladatok egy része nem a deklarált priorok szerinti MAP-választ várja** (102. kör, TFB-2). Ezek a
   feladatok *intuíciót* kódolnak („egy ellenpélda valódi kivétel”). A rendszer pedig MAP-ot számol. A kettő eltérése nem
   mindig a rendszer hibája.
3. **Hat kör (98–103) óta nem született új befagyasztott konfiguráció.** A jelöltek (DK, C, Q, V5_CORE) mind egy-egy
   előregisztrált kritériumon buktak el. Ez az előregisztráció működését mutatja, de azt is, hogy **a FROZEN_91 egy lokális
   optimum,** amelyet egyetlen tárcsa mozgatásával nem lehet minden mércén javítani.

## 4. Divergens irányok

1. **Epizódokon átívelő kalibráció (meta-kalibráció):** a q_temper és a π_új empirikus Bayes-becslése korábbi epizódok
   kimeneteléből. Benchmark: egy sor világ ugyanabból a környezetből (pl. 10 G4-világ egymás után). Az ágens minden epizód
   után megtudja az igazságot (vagy annak egy részét), és frissíti a tárcsákat. Előregisztrálható jóslat: a tanult tárcsákkal
   a G4-környezetben a q_temper nő, a G1-kézi környezetben nem. Az utolsó epizódokon a pontosság eléri a környezethez
   utólag legjobban illő rögzített tárcsa pontosságát.
2. **Tartózkodás és kérdezés** (13. kör ötlete): ha két magyarázat közel van (kis pontszám-különbség), a rendszer ne válasszon,
   hanem jelezze a bizonytalanságot, vagy kérdezzen. Ez a tárcsák helyett a döntést hárítja át. A 63. és 67. kör szerint a
   nyaláb nem poszterior-minta, ezért ehhez a pontszám-különbséget kell használni, nem a nyaláb-gyakoriságot.
3. **A szabályok időbeli vágása** (G3 szabályváltozás), a régóta halasztott primitív.

## 5. A következő körökre

- **105. kör:** meta-kalibráció epizódokon át (tervezés és előregisztráció).
- **106. kör:** tartózkodás a pontszám-különbség alapján, Brier- és szelektív-pontosság-méréssel.
- **107. kör:** a szabályok időbeli vágása.
- **109. kör:** divergens és kritikai kör.
