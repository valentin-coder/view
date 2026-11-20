# 114. kör – Divergens és kritikai kör (18.): tárcsák és szerkezeti bizonyítékok

## 1. A 109–113. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 109 | plató | nyolc jelöltből egy sem lett alapértelmezés; a maradék döntések alapgyakoriság-függők |
| 110 | összefoglaló jelentés | az 1–109. kör egy dokumentumban |
| 111 | bevált forrás másolója | **a legsúlyosabb mért sebezhetőség:** minden érintett kérdés hibásra fordul |
| 112 | másolásfelismerés + horgony-újraindítás | **minden kritérium teljesül;** új alapértelmezés: FROZEN_112 |
| 113 | hamis riasztás független tanúknál | 0/28; bitre azonos |

## 2. A plató után: mi különbözteti meg a sikeres jelöltet

A 109. kör szerint a 96–107. kör jelöltjei mind tárcsák voltak. A 112. kör jelöltje egy **szerkezeti bizonyítékot** használ.
A két csoport közötti különbség a sorozat egyik legtisztább tanulsága:

| | tárcsa (pl. π_új, q_temper, ρ_r) | szerkezeti bizonyíték (pl. másolás, prioritás, eseményenkénti vágás) |
|---|---|---|
| mit dönt el | egy állítás hihetőségét kevés bizonyíték alapján | sok állítás közös mintázatának legjobb magyarázatát |
| a helyes érték függ | a környezet alapgyakoriságaitól | a mintázattól (a kódhossz eldönti) |
| előregisztrált sikerek | 0 a 96–107. körben | PK (81), hibrid + V (91), másolás (112) |
| tipikus kudarc | egy benchmarkon javít, egy másikon ront | a kereső nem találja meg (horgony kell) |

**Következtetés:** a hipotézistér bővítése akkor ér valamit, ha olyan szerkezetet fejez ki, amely sok megfigyelést egyszerre
magyaráz (egy prioritás sok ütközést, egy másolás sok egyezést, egy vágás egy esemény összes régi jelentését). Ilyenkor az MDL
magától dönt, és nem kell alapgyakoriságot tudnia. **Ahol a döntés egyetlen állításon múlik, ott nincs szerkezet, csak
prior,** és ott a neurális háttértudás (a B fázis) kell.

## 3. Kritika

1. **A horgony-újraindítás egy speciális keresési trükk** (a forrás első megjelenése előtti hipotézis). Működik, de nem
   általános elv. Valószínűleg a 97. kori forrás-változáspont és a 107. kori szabály-vágás is ugyanezen bukott el: a kereső nem
   nyitja újra a korábbi döntéseket. **Egy általános „újranyitó” keresés** (minden új szerkezeti komponensnél egy
   horgonyból is újraindulni) a következő értelmes lépés, és visszamenőleg érdemes lenne a 97. és 107. kör jelöltjeit is
   újramérni vele.
2. **A 111–113. kör a G4 kiegészítésein futott,** amelyeket a 111. körben a FROZEN_91 ismeretében írtam. A 88. kori
   befagyasztási elv szerint egy *újabb*, a FROZEN_112 után írt generátor kellene a függetlenségi eredmény külső
   érvényességéhez.
3. A jelentés (110. kör) után a 111–113. kör egy új sebezhetőséget talált és javított. **A „plató” tehát a tárcsákra volt
   igaz, nem a szerkezeti bővítésekre.** Ezt a 109. körben nem láttam előre.

## 4. Divergens irányok

1. **Általános újranyitó keresés** (3.1): minden javasolt új szerkezeti komponensnél (másolás, változáspont, szabály-vágás,
   prioritás) a javítás a komponenst érintő források első megjelenése előtti horgonyból is induljon. Előregisztrálható
   jóslat: a 97. és a 107. kör jelöltjei vele javulnak.
2. **Ötödik generátor a FROZEN_112 után** (3.2): többforrású világ valós mintázatokkal (másolási láncok, részleges másolás,
   egymást idéző források). Ez a 88. kori befagyasztási elv alkalmazása az új komponensre.
3. **A szerkezeti bizonyíték kifejezőerejének határa:** milyen további, sok megfigyelést egyszerre magyarázó szerkezetek
   hiányoznak még (pl. „egy forrás egy témában megbízható, másikban nem”; „egy kategória egy régióban más”)? A 69. kori
   kontextusfüggő szabály ennek egy példája volt, amely forrás-szinten túl durván valósult meg.

## 5. A következő körökre

- **115. kör:** általános újranyitó keresés, a 97. és 107. kör jelöltjeinek újramérésével, előregisztrálva.
- **116. kör:** ötödik generátor (forrásfüggőségi hálózatok) a FROZEN_112 után, előregisztrálva.
- **119. kör:** divergens és kritikai kör.
