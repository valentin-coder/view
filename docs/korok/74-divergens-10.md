# 74. kör – Divergens és kritikai kör (10.): a 65–73. kör mérlege és a jelenlegi legjobb konfiguráció

## 1. A 65–73. kör mérlege

| kör | kérdés | eredmény |
|---|---|---|
| 66 | milyen pontos forrástípus kell | 0,9 átlagban elég; a téves típus esetenként összeomlást okoz |
| 67 | a nyaláb-margó azonosíthatósági mérték-e | **nem**; a pontosság a margóval csökken |
| 68 | azonosíthatóság az igaz hipotézisből | a mérőeszköz hibás (ellenőrző jóslat); a „más régió”-ban a helyes kontextus drágább két hamisnál |
| 70 | típusbizonytalanság továbbítása | kis, kétirányú csere; a 60. kör C-hatása friss seedeken megismétlődik |
| 71 | elsőbbség + jó jel | +0,20 a „más régió”-ban; jel nélkül árt |
| 72 | entitásonkénti zárás-memó | bitre azonos, 1,6–2,4× gyorsabb |
| 73 | jelhez kötött elsőbbség | a kár megszűnik; a hatás friss seedeken kisebb (+0,06) |

## 2. A jelenlegi legjobb konfiguráció

**v4.8-π + jelzett elsőbbség (+ nyaláb-átlagolt válasz):**
1. **v4.4e alap:** tanult forrás-megbízhatóság (κ_S = 30), kivétel-prior (ε = 0,05), automatikus specifikusság,
   szigorú osztálykivétel, q-csoportok, kategória-feltalálás visszavétellel, az indukált szabályok kivételei árazva.
2. **Keverék-prior az elméletekre, forrásonkénti π-vel** a forrás típusából (metaadat vagy LLM-becslés). Ez kezeli a
   gestalt-váltás és a stabilitás feszültségét.
3. **Kontextus csak jellel olcsó** (Bayes-árazás), és **elsőbbség csak jelzett forrásra**.
4. **Nyaláb-átlagolt válasz** a kalibrációért (Brier).
5. **Entitásonként memoizált zárás** a sebességért.

**Ami bizonyítottan működik** (előregisztrált, friss seedeken): a rivális elméletek kezelése a metaadat-π-vel
(60. és 70. kör: C-ben 0,61–0,66 a 0,38–0,41 helyett); a v3 fölötti általános előny (57. kör, A ∪ B: +0,048); a hazug forrás
felismerése (+0,15); a Brier-javulás az átlagolással.

**Ami nem bizonyított:** a „más régió” kezelése (két halmazon egy irányba mutat, de bizonytalan nagyságú); a jel értéke
pontatlan jellel (0,9-nél árt); az egész konfiguráció egyetlen nagy, előregisztrált mérése (a 75. kör ezt pótolja).

## 3. Kritika

1. **A konfiguráció két orákulumra támaszkodik:** a forrástípusra (π) és a kontextusjelre. Mindkettő a B fázis
   LLM-feladata volna, és egyik sem futott valódi modellen. A 66. és 60. kör szerint a pontosságukra érzékeny:
   kb. 0,9-es típuspontosság és kb. 0,99-es kontextusjel kell.
2. **A rendszer egyre összetettebb:** a v4.8 kb. 15 kapcsolóból áll, mindegyik egy konkrét hibára válaszolt. A 34. kör
   túlillesztési aggálya most is érvényes. Az előregisztrált, friss seedes mérések ezt részben kezelik, de minden
   kapcsoló egy generátoron lett hangolva.
3. **A generátoron kívül semmit nem mértem.** A 22. kör Wikipedia-benchmark ötlete és a valódi szövegek (B fázis) nélkül
   minden eredmény a saját világmodellemről szól.

## 4. Divergens irány: egy második, független generátor

A legnagyobb hiányosság, hogy minden mérés ugyanabból a procedurális generátorból jön. **Egy második, független
generátor** (más szerkezetű világ: nem fa-taxonómia, hanem például ok-okozati gráf vagy időben változó attribútumok,
más zajmodell, más meglepetéstípusok) a 44. kör óta a legerősebb külső érvényességi teszt volna. Ezt a 77. körre
javaslom. Előregisztrálva: a konfiguráció egyetlen kapcsolóját sem hangolom rá.

## 5. A következő körökre

- **75. kör:** a legjobb konfiguráció nagy, előregisztrált összevetése (A + C).
- **76. kör:** szabályszintű, hatókör-érzékeny zárás-memó.
- **77. kör:** egy második, független benchmark-generátor (terv és előregisztráció).
- **79. kör:** divergens és kritikai kör.
