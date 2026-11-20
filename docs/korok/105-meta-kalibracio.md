# 105. kör – Meta-kalibráció epizódokon át: a fejlesztési ellenőrzés szerint nincs mit kalibrálni

## 1. A terv

A 104. kör szerint a maradék problémák tárcsák, és a helyes értékük a környezettől függ. A javaslat: tanulja meg a rendszer
a q_temper-t epizódokon át (rács: × 0,5; 1; 2; 4; minden epizód után az eddig legjobban teljesítő érték a következőre). Ez
csak akkor értelmes, ha **különböző környezetek különböző optimumot kívánnak.** Ezt ellenőriztem először.

## 2. Fejlesztési ellenőrzés (már felhasznált seedeken; nem teszt)

Kód: [`dev_r105.py`](../../experiments/arlc/arlc/dev_r105.py). Két szándékosan ellentétes környezet:
- **„igaz meglepetések” (G1k):** átkategorizálás, szabály-helyesbítés, kivételes alfaj. Minden meglepetés igaz, ezért itt a
  gyors átrendeződést vártam előnyösnek (kis q_temper);
- **„zajos források” (G4):** hazug, jó specialista, romló forrás, visszhang.

| q_temper | igaz meglepetések post / target | zajos források post / target |
|---|---|---|
| × 0,5 | 0,836 / **0,792** | 0,811 / 0,735 |
| × 1 (FROZEN_91) | 0,842 / **0,792** | 0,919 / 0,922 |
| **× 2** | **0,862** / 0,776 | **0,948 / 0,965** |
| × 4 | 0,812 / 0,707 | 0,911 / 0,936 |

**Mindkét környezet post-optimuma a × 2.** Az igaz-meglepetés környezetben a célkérdéseken a × 1 (és a × 0,5) kissé jobb
(0,792 vs. 0,776). A különbség kicsi, és az általános pontosság itt is a × 2-t kedveli. Az óvatos hitelesség a háttérvilág
zajos tényeit kezeli jobban, és ez az igaz meglepetések mellett is számít.

## 3. Következmény

1. **A tervezett meta-kalibrációs teszt nem informatív:** a generatív környezetekben, amelyeket építeni tudok, a
   tárcsa optimuma ugyanott van. A 102. kör ellentéte (generatív vs. kézi feladatok) **csak a kézzel írt korai feladatokban
   jelenik meg.** Azok a 102. kör szerint részben nem a deklarált priorok szerinti MAP-választ várják.
2. **Ezért nem írom felül utólag a 102. kör döntését** (az F91 + Q ott két előre rögzített kritériumon elbukott). Ehelyett a
   választás **specifikációs döntés**, amelyet az alkalmazásnak kell meghoznia. Két megnevezett konfiguráció marad:
   - **FROZEN_91** („bízó”): a kézi feladatcsomagon teljes, a generatív világokon jó;
   - **FROZEN_91 + Q** („óvatos”, `F91_Q`): a generatív világokon mindenhol jobb (102. kör, friss seedeken: +0,01 – +0,03; a
     forrás-célkérdéseken +0,05; először a v3 fölött a G4-en). A kevés bizonyítékból való átrendeződésben (TFB-2,
     feltalálás) gyengébb.
3. A B fázis szempontjából az óvatos változat a biztonságosabb: a 101. kör szerint a hitelesség túlbecslése sokkal
   veszélyesebb, mint az alulbecslése. Egy LLM-ből jövő hitelesség-becslésnél ez a döntő szempont.
