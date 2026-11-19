# 69. kör – Divergens és kritikai kör (9.): a 60–68. kör mérlege

## 1. Mi áll meg és mi nem

| állítás | kör | státusz |
|---|---|---|
| a metaadatból jövő π egyetlen kóddal kezeli a rivális elméleteket és az egyetlen jó elméletet | 60 | **áll** (C: +0,247; A: −0,003), de **orákulum-metaadaton** |
| ehhez kb. 0,9-es forrástípus-pontosság elég | 66 | **átlagban áll; esetenként a téves típus összeomlást okoz** |
| a jelhez kötött kontextus segít | 60, 62 | **nem** (a 0,9-es jel árt; a 0,99-es sem segít) |
| a nyaláb-átlag javítja a kalibrációt | 50, 63 | **áll** (Brier, három független mérésben) |
| a nyaláb a bizonytalanságot jelzi | 63, 67 | **nem**: a nyaláb a keresés útja, nem poszterior-minta |
| a „más régió” target-acc rangsorolásra alkalmas | 50–62 | **visszavonva** (62, 64) |
| a modell a helyes kontextus-magyarázatot választja | 68 | **nem**: drágábbnak tartja, mint két hamisat |

## 2. A sorozat legmélyebb nyitott problémája: a kontextus

A 17. kör óta kilenc kör érintette a kontextus-mechanizmust (17, 21, 49, 50, 57, 60, 62, 65 terv, 68). Az eredmény
következetes:
- **jel nélkül** a kontextus vagy menekülőút (57. kör: két rivális tankönyv mindkettő izolálva), vagy vesztes
  (68. kör: a helyes „más régió” magyarázat drágább két hamisnál);
- **jellel** a téves riasztás katasztrofális (60. kör), és még a jó jel sem segít (62. kör), mert az izolált kontextuson
  belül az örökölt szabályokkal ütközés támad (50. kör: kontextuson belüli elsőbbség).

**Diagnózis:** a „kontextus” az ARLC-ben egy forrás-szintű kapcsoló: egy forrás *összes* állítása vagy a fő világról
szól, vagy egy másikról. A valóságban (és a generátorban) a „más régió” forrás *egyetlen szabályt* módosít egy másik
helyen. A helyes modell **kontextusfüggő szabály**: „ez a szabály ott érvényes, itt nem” (a 21. kör
kontextusfüggő indukciója ennek egy darabja volt). A forrás-szintű izolálás túl durva, ezért vagy túl drága (helyes
esetben), vagy túl olcsó (menekülőútként).

## 3. Kritika a módszerről

1. **Kerti utak:** a 60–68. körben négyszer kellett menet közben javítanom a mérőeszközt (63: a nyaláb nem minta; 66:
   `hash()` nem determinisztikus; 67: a margó fordítva mér; 68: a horgonyzás rossz). Mindegyiket egy előre leírt
   ellenőrző jóslat vagy egy smoke teszt fogta meg, és mindegyiket dokumentáltam. **Az ellenőrző jóslatok (mint a 68.
   kör J3-ja) legalább olyan értékesek, mint a fő hipotézisek.**
2. **Egyre kisebb seed-halmazok** (10–15 seed) a futási idő miatt. A 66. kör megmutatta, hogy egy 10 seedes halmaz egy-két
   nehéz világ miatt jelentősen eltérhet egy másiktól. A szignifikáns állításokhoz legalább 20–30 seed kell.
3. **Futási idő:** a C-populáció egy esete a v4.8-cal percekig tart. A 46. kör inkrementális zárása továbbra sem valósult
   meg, és ma ez korlátozza leginkább a kísérletek méretét.

## 4. Divergens irányok

1. **Kontextusfüggő szabály forrás-szintű izolálás helyett:** a „más régió” forrás *egyetlen* szabálya kap
   kontextus-címkét („ott érvényes”), nem az egész forrás. Ez a 21. kör kontextusfüggő indukciójának általánosítása, és a
   generatív v5-ben (51. kör) egy látens változó szabályonként.
2. **Inkrementális zárás** (46. kör) a futási idő miatt: ez ma a kísérleti kapacitás szűk keresztmetszete.
3. **Típusbizonytalanságot továbbító π** (70. kör): π = Σ P(típus | szöveg) · π(típus), a 66. kör esetenkénti
   összeomlásai ellen.
4. **Diverz nyaláb** (63., 67. kör): a nyaláb mindig tartalmazza a két legjobb, egymásnak ellentmondó magyarázatot, és
   ha ezek közel vannak, a rendszer jelez vagy kérdez (13. kör).

## 5. A következő körökre

- **70. kör:** típusbizonytalanságot továbbító π, előregisztrálva.
- **71. kör:** kontextusfüggő szabály (4.1), előregisztrálva a „más régió” és a C populáción.
- **72. kör:** inkrementális zárás, viselkedésmegőrzően (ekvivalencia-ellenőrzéssel).
- **74. kör:** divergens és kritikai kör.
