# 48. kör – Az elmélet-megbízhatóság priorja, állításonkénti hitelesség, és egy elfajult kivétel

A 43. körből két kérdés maradt nyitva: az elméleti hírnév-farmolás (2. hiba) és a 47. kör első
kölcsönhatása (egy forrásnak csak egy hitelessége van). Ez a kör három javaslatot vizsgál.
Kettő túlél, egy elbukik, és egy negyedik, váratlan hiba is előkerül: egy elfajult osztályszintű
kivétel, amely a 43. kör E1-diagnózisát is helyesbíti.

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`_beta_bits`: `theory_mix`, `q_groups`;
`_mods`/`_proper_sub`: `strict_specificity`), [`v4.py`](../../experiments/arlc/arlc/v4.py)
(`V43_OVERRIDES`), [`r48.py`](../../experiments/arlc/arlc/r48.py); eredmény:
[`results/kor-48/battery.json`](../../experiments/arlc/results/kor-48/battery.json).

## 1. A κ_T = 1 prior alakja és a hírnév-farmolás

A kétszintű hitelességben (32. kör) egy forrás elméleti állításainak megbízhatósága
r ~ Beta(κ_T·q, κ_T·(1 − q)), κ_T = 1, q = 0,95. Ez a béta **U alakú**: „egy elmélet vagy egészében
helyes, vagy egészében téves”. A 32. kör ezt akarta, mert így egy egész fa elvetése olcsó (TFB-9).

Egy *konkrét* elutasítási mintázat kódhossza (bit), q = 0,95:

| n | k | κ_T = 1 | κ = 30 | keverék (π = 0,9) | kalibrált keverék (π = 0,95) |
|---|---|---|---|---|---|
| 1 | 1 | 4,32 | 4,32 | 3,40 | 4,32 |
| 48 | 1 | 10,23 | 7,78 | 7,92 | 7,77 |
| 48 | 3 | 20,20 | 17,07 | 17,19 | 17,88 |
| 48 | 48 | 9,59 | 67,19 | 8,94 | 9,94 |
| 60 | 1 | 10,57 | 8,31 | 8,44 | 8,15 |

**Hírnév-farmolás.** n vitatatlan elméleti állítás után egy további elutasításának határköltsége
κ_T = 1 mellett log₂((q + n)/(1 − q)) ≈ log₂(20·n): n = 60-nál 10,25 bit, egy új szakértő magányos
állításáé 4,32 bit. κ = 30-nál 5,91 bit: a múlt számít, de csak log₂(1 + n/(κq)) bittel.

**Helyesbítés a saját vázlatomhoz.** E kör első változatában azt írtam, hogy κ_T = 1 mellett „néhány
hiba valószínűtlenebb, mint az összes” (48-ból 3 elutasítása 20,2 bit, mind a 48-é 9,6 bit). **Ez így
téves.** A táblázat egy *konkrét* mintázat kódhossza. A „pontosan 3 hiba valahol” valószínűségéhez
a C(48, 3) ≈ 2¹⁴ mintázatot össze kell adni: 2^(−20,2 + 14,1) ≈ 0,015 > 2^(−9,6) ≈ 0,0013. A prior
darabszám szerint a kevés hibát tartja valószínűbbnek. A MAP-választásban a konkrét mintázat
számít, de ott a teljes elvetés a jóslatok elvesztésével is jár, ezért a kettő nem vethető össze
csak a béta-tagon.

## 2. 1. javaslat (ELBUKOTT): keverék-prior az elméletekre

**Ötlet:** egy elmélet π valószínűséggel „nagyjából helyes, néhány hibával”
(r ~ Beta(κ₁q₁, κ₁(1 − q₁)), κ₁ = 30), 1 − π valószínűséggel „egészében téves” (r ~ Beta(1, 1)). Ez
valódi valószínűség (két béta-binomiális keveréke), és a táblázat szerint egyszerre ad
logaritmikus farmolást (κ = 30-as viselkedés kevés elutasításnál) és olcsó gestalt-váltást (a teljes
elvetés kb. 9–10 bit).

**1. hiba: kalibrálatlan.** π = 0,9, q₁ = q mellett egy magányos állítás tévedésének valószínűsége
0,9·0,05 + 0,1·0,5 = 0,095, nem a deklarált 0,05. **Kalibrált változat:** π·q₁ + (1 − π)·q₀ = q,
ehhez π ≥ (q − q₀)/(1 − q₀) kell. q = 0,95-re π ≥ 0,9.

**2. hiba (elvi, ezen bukik el): hibaküszöb.** A keverék minden elméleti állításra
(1 − π)·(1 − q₀) alsó hibavalószínűséget kényszerít (π = 0,95-nél 0,025). Egy q = 0,999-es
szakértői szabályra a kalibráció nem teljesíthető (q₁ > 1). A szakértő magányos szabályának
elutasítása így 9,97 bit helyett kb. 5,3 bitbe kerül. **Az E1 alosztály-cseréjében a rendszer ezért
a szakértőt utasítja el** (125,03 bit, szemben a tankönyvi szabály elvetésének 126,55 bitjével): az
alosztály-csere RR-je mind az 5 seeden 0. Ha π-t a deklarált q-tól tennénk függővé, a keverék
értelmét veszítené.

**Mért (ellenőrző csomag):** a nem kalibrált keverék E1-en 0,75, TFB-9-en 0,96. A kalibrált
keverék önmagában a TFB-9-en 0,88-ra rontja a pontosságot, és **17%-ban aktív marad a vesztes
fa**, vagyis gyengíti a gestalt-váltást. Elvetve, ahogy a 43. kör v4.1-ét.

**Ismert modellek:** a „jó munkás vs. spammer” keverék-priorok (Raykar et al. 2010,
ellenőrizendő) elméletszintű megfelelője. Itt ugyanaz a hiba áll fenn: a keverék a jó komponensnek
is küszöböt szab.

## 3. 2. javaslat (TÚLÉLT): deklarált hitelesség szerinti csoportok (`q_groups`)

A béta-kód forrásonként egyetlen előzetes q-t használt, a forrás első megfigyelésének q-ját. A
javaslat szerint **egy forrás eltérő deklarált hitelességű állításai külön csoportot alkotnak**, saját
múlttal. Ez konjugált marad, és a téma szerinti felbontás (47. kör, 2. javaslat) legegyszerűbb esete,
ahol a „téma” a deklarált bizonyosság.

**Mért:** A7 0,70 → **1,00**, minden más mérőszám változatlan. A 47. kör 1. kölcsönhatása ezzel
megszűnt.

**Gyengéje:** a csoportok közt nincs információmegosztás, egy forrás 0,9-es hibái nem rontják a
0,95-ös állításai hitelét. Ez hierarchikus priorral javítható volna.

## 4. Negyedik hiba (TÚLÉLT JAVÍTÁS): elfajult osztályszintű kivétel (`strict_specificity`)

**A 43. kör diagnózisa nem volt teljes.** Ott az E1 alosztály-csere RR-jét a κ_T = 1-nek
tulajdonítottam. Komponensenként, a tanult megbízhatóságból (κ = 30) indulva:

| konfiguráció | alosztály-csere RR (5 seed) |
|---|---|
| v3 + béta | 1, 1, 1, 1, 1 |
| + κ_T = 1 | 0,4; 0,5; 0,5; 0,5; 0,5 |
| + kivétel-prior | 1, 1, 1, 1, 1 |
| **+ osztályszintű kivétel** | **0; 0,25; 0; 0; 0** |
| + feltalálás / forráslépés / kontextusindukció / mélység 2 | 1, 1, 1, 1, 1 |

A fő ok az osztályszintű kivétel. **A rendszer a szakértő új szabályát („R2bb ⊂ R1a”) a régi szülőre
vonatkozó osztálykivétellel semlegesíti:** „az R2bb-k R1a-k, kivéve azokat, amelyek R2b-k”. Minden
R2bb R2b, tehát a szabály üres. Ez **álcázott elutasítás** a hitelesség-ellenőrzés megkerülésével,
0,47 bittel olcsóbban a valódinál. Ugyanaz a mintázat, mint a 19. és 26. kör „helyi kiútja”.

**Javítás:** a specifikussági elv szerint (Touretzky) osztályszintű kivétel csak a szabály törzsének
**szigorú alosztályára** adható. Egy feltalált c′ = b ∧ F kategória definíció szerint b alosztálya.

**Mért:** E1 RR 0,76 → **0,845** (alosztály-csere kb. 0,05 → 0,38), kis kollaterális hatással
(0,002). A maradék hiba már **nem elfajult**. Két minimális alternatíva marad:
- osztálykivétel a szakértő által hozott új szülő felfelé vezető szabályán („R2ba olyan R0b, amely
  nem R0”), szabályos specifikusság;
- a tagsági tények elutasítása („ezek mégsem R2bb-k”).

Mindkettő 0,5–1 bitre van a „költözéstől”. **Az E1 alosztály-esetében a helyes válasz az adatból nem
dönthető el**, mert az érintett tagokról nincs tény. A „költözés” értelmezést csak az egyszülős
taxonómia hallgatólagos konvenciója indokolja, és ez a modellben nincs meg. A procedurális benchmark
többszörös öröklést is tartalmaz, ezért ezt nem teszem alapértelmezéssé. **Ez az E1 mérőszám
tervezési hibája, nem a rendszeré:** egy alulhatározott esetet egyetlen „helyes” válaszhoz mér.

## 5. Az ellenőrző csomag

| | E1 RR | A7 | TFB-9 pont. / vesztes fa | E4 pont. / hamis átr. | többi |
|---|---|---|---|---|---|
| v4 (befagyasztott) | 0,762 | 0,70 | 0,977 / 0,00 | 0,938 / 0,00 | = |
| v4.2 (3. hiba javítva, 45. kör) | 0,762 | 0,70 | 0,977 / 0,00 | 0,938 / 0,00 | = |
| v4.2 + q-csoportok | 0,762 | **1,00** | 0,977 / 0,00 | = | = |
| v4.2 + szigorú specifikusság | **0,845** | 0,70 | 0,977 / 0,00 | = | = |
| v4.2 + keverék (nem kalibrált) | 0,75 | 0,70 | 0,960 / 0,00 | = | = |
| v4.2 + kalibrált keverék | 0,75 | 0,80 | **0,882 / 0,17** | = | = |
| **v4.3 = v4.2 + q-csoportok + szigorú specifikusság** | **0,845** | **1,00** | **0,977 / 0,00** | 0,938 / 0,00 | = |
| v4.3 + kalibrált keverék | 0,75 | 1,00 | 0,977 / 0,00 | = | = |

(„=”: E2a, E3, TFB-2, TFB-8, Quine és feltalálás minden változatban azonos.)

## 6. Ami nyitva marad

- **A hírnév-farmolás (43. kör, 2. hiba) nincs javítva.** Az egyetlen kipróbált elvi javítás
  (keverék) elbukott. A κ_T = 1 megmarad, és vele a farmolás is (n = 60-nál 10,25 bit). Egy jobb
  irány: a vitatatlan állítás ne számítson *bizonyított* sikernek, csak a független forrás által
  megerősített. Ez a v4.1 volt, és a 43. körben rontott. A kettő közötti út (a vitatatlan állítás
  részleges súllyal) egy újabb hangolható paraméter volna.
- **A kis világos teljes elvetés** (45. kör, 10 entitás): adatszűkös MDL-hatás. Ha a tankönyv jóslati
  nyeresége (kb. 0,93 bit tényenként) összemérhető a hibái javításának árával, az elvetés (vagy a 2 × 6
  bites kontextus-izolálás) optimális. A különbség 1–3 bit. Ezt semmilyen kipróbált változat nem
  javítja, mert a prior (egy tankönyv egészében téves vagy más kontextusról szól) nem illik a
  generátorhoz. Egy világból nem becsülhető (lásd a 45. kör J4-ét), csak sok forrás vagy sok világ
  együtteséből: ez a hierarchikus (meta-) tanulás kérdése.
- **Validációs lefedettség:** egy új lépéstípus (osztályszintű kivétel) újabb elfajult utat nyitott.
  Ugyanez történt a 19., 26. és 45. körben. Minden új lépéshez kell egy teszt arra, hogy **nem
  helyettesít-e olcsóbban egy hitelesség-ellenőrzött lépést** (elutasítást). A 49. kör ezt
  rendszerezi.

## Függelék (a 49. kör után)

- **Kis π-vel a keverék kalibrálható** (π = 0,999-nél a q = 0,999-es szakértő is), és a farmolás
  n = 60-nál 5,9 bitre csökken. **Ára a gestalt-váltás:** a TFB-9-en a pontosság 0,81, a vesztes fa
  83%-ban aktív marad. A teljes elvetés helyes (TFB-9) és téves (kis világok) esete ugyanaz a lépés,
  ugyanazzal a priorral. Lásd [49-divergens-5.md](49-divergens-5.md), 5. pont.
- **A v4.3 egy kis világban rosszabb a v4-nél** (25-ös seed: 0,89 → 0,63). A v4 egy álcázott
  osztálykivétellel tartotta meg a tankönyvet. A kiskapu bezárása egy mélyebb hibát tett láthatóvá: a
  specifikus öröklés hiányát (49. kör, 4. pont).
