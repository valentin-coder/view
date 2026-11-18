# 64. kör – Divergens és kritikai kör (8.): az 55–63. kör mérlege, és mit mér valójában a célkérdés-pontosság

## 1. A célkérdés-pontosság visszamenőleges érvényessége

A 62. kör szerint a „más régió” meglepetés egy 0,04–0,43 bites holtverseny: a target-acc erre a típusra
bitnyi különbségek véletlenjét méri. Ezért a korábbi célkérdés-előnyöket újraszámoltam e típus nélkül
(világok szerinti klaszteres bootstrap):

| állítás | minden típus | „más régió” nélkül | csak „hazug forrás” |
|---|---|---|---|
| 50. kör ismétlés: v4.4e − v3 (target) | +0,113 [+0,082; +0,143] | **+0,041** [+0,010; +0,070] | **+0,150** [+0,079; +0,225] |
| 57. kör A: v4.4e − v3 (target) | +0,097 [+0,059; +0,138] | **+0,070** [+0,040; +0,102] | – |

**Ítélet:** a célzott képesség előnye megmarad, de a korábban közölt nagyság (a „más régió” +0,40-e) **túlzó
volt**. A robusztus rész a hazug forrás felismerése (+0,15). A „más régió”-ra vonatkozó állításokat (50., 55.,
57., 60. kör) visszavonom, és holtversenyként kezelem.

## 2. Az 55–63. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 55 | kétsebességű rendszer | a gyengébb rendszert tartotta meg alapnak; a fordított változat ígéretes, de nem tesztelődött döntően |
| 56 | hiányzik-e a jóslatvesztés a félretevés árából | **téves premissza**, elemzéssel cáfolva |
| 57 | kombinált benchmark | a javított változat jobb a v3-nál (A ∪ B); rivális elméleteknél csak a kétszintű prior vált helyesen |
| 58 | a hierarchikus π kiindulásfüggő-e | nem, de a becslő felbontása miatt rossz fixpontra fut |
| 60 | metaadat-π és jelhez kötött kontextus | **a π feloldja a gestalt–stabilitás feszültséget**; a 0,9-es jel árt |
| 61 | a B fázis két LLM-feladata | kód kész; a smoke teszt egy szivárgást fogott meg |
| 62 | a 60. kör régió-kudarca | holtverseny, nem mechanizmus |
| 63 | bizonytalanság-jelzés | *(lásd a 63. kört)* |

## 3. Kritika

1. **Az eddigi legjobb eredmény (60. kör) orákulum-metaadaton áll.** A π-t a populáció *ismert* szemét-arányából
   adtam meg. A rendszer ezt nem tanulta, hanem kapta. Az 52. és 58. kör szerint a tanulása korlátos. A 61. kör
   szerint egy LLM a forrástípusból becsülhetné, de ez nem futott. **Az eredmény tehát feltételes:** *ha* a forrás
   típusa ismert, a rendszer mindkét végponton jól viselkedik.
2. **A benchmark-generátor egyre többet hordoz a saját feltevéseimből.** A, B, C populáció, „más régió”, hazug
   forrás: mindegyiket én terveztem, a C-t egy ismert gyengeség köré. A 62. kör megmutatta, hogy egy típus
   (más régió) alulhatározott, és ezt 18 körön át nem vettem észre. **Minden meglepetéstípushoz kellene egy
   „azonosíthatósági” ellenőrzés:** az igaz és a legjobb hamis magyarázat bit-különbsége. Ha ez kicsi, a típus
   nem alkalmas rangsorolásra.
3. **A futási idő romlik:** a C-esetek a v4.8-cal egy magon percekig tartanak. Az eredeti cél („azonnali”
   átrendeződés) egyre távolabb van. A 46. kör inkrementális terve a valódi szűk keresztmetszetre (zárás,
   jelöltenkénti konfliktuskeresés) nem valósult meg.
4. **A konténer gyakori újraindulása** miatt minden hosszú futás folytatható lett. Ez jó gyakorlat, de minden
   újraindulás eltérést okoz a tervhez képest (dokumentálva).

## 4. Divergens irányok

1. **Azonosíthatósági előszűrés minden benchmark-típusra:** a generátor kiszámolja az igaz hipotézis és a
   legjobb alternatíva pontszám-különbségét, és csak a kellően azonosítható eseteket használja rangsorolásra. A
   holtversenyes eseteket külön, Brier-pontszámmal értékeli.
2. **A π tanulása független jelből, szimulált LLM-pontossággal:** a 61. kör SRC-feladatának várható pontosságát
   (pl. 0,8; 0,9; 0,99) szimulálva mérhető, milyen pontosságú forrástípus-felismerés kell a 60. kör eredményéhez.
   Ez a 21. kör kontextusjel-követelményének párja a π-re.
3. **Az inkrementális zárás megvalósítása** (46. kör), a C populáció futási idejének mérésével.

## 5. A következő körökre

- **65. kör:** kontextuson belüli elsőbbség jó jellel (a 62. kör nyitott kérdése).
- **66. kör:** szimulált forrástípus-pontosság (4.2), előregisztrálva.
- **67. kör:** azonosíthatósági előszűrés (4.1) a benchmark-generátorhoz.
- **69. kör:** divergens és kritikai kör.
