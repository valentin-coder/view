# 48. kör – Az elmélet-megbízhatóság priorja: a κ_T = 1 három hibája és a keverék-prior

A 43. kör második hibája (elméleti hírnév-farmolás) és a 47. kör első kölcsönhatása (egy forrásnak
csak egy hitelessége van) nyitva maradt. A 45. kör egy kis világos próbája egy harmadik tünetet is
mutatott. Ez a kör megmutatja, hogy a három tünetből kettő **ugyanannak a paraméternek a
következménye**, és ad rá egy elvi javítást.

Kód: [`core.py`](../../experiments/arlc/arlc/core.py) (`_beta_bits`: `theory_mix`, `q_groups`),
[`r48.py`](../../experiments/arlc/arlc/r48.py); eredmény: [`results/kor-48/`](../../experiments/arlc/results/kor-48/).

## 1. A κ_T = 1 prior alakja

A kétszintű hitelességben (32. kör) egy forrás elméleti állításainak megbízhatósága
r ~ Beta(κ_T·q, κ_T·(1 − q)), κ_T = 1, q = 0,95. Ez a béta **U alakú**: a tömege r ≈ 1 és r ≈ 0
körül van. Jelentése: „egy elmélet vagy teljesen helyes, vagy teljesen téves”. A 32. kör éppen ezt
akarta, mert így egy egész fa elvetése olcsó (gestalt-váltás, TFB-9).

Az n állításból k elutasításának kódhossza (bit), q = 0,95:

| n | k | κ_T = 1 | κ = 30 | keverék (1. javaslat) |
|---|---|---|---|---|
| 48 | 0 | 0,32 | 2,13 | 2,26 |
| 48 | 1 | 10,23 | 7,78 | 7,92 |
| 48 | 3 | **20,20** | 17,07 | 17,19 |
| 48 | 24 | 53,79 | 64,39 | 53,81 |
| 48 | 48 | **9,59** | 67,19 | 8,94 |
| 60 | 1 | 10,57 | 8,31 | 8,44 |
| 60 | 60 | 9,90 | 74,43 | 9,25 |

## 2. A három tünet

**(a) Hírnév-farmolás (43. kör, 2. hiba).** Egy elmélet n vitatatlan állítása után egy további
állítás elutasításának határköltsége κ_T = 1 mellett log₂((q + n)/(1 − q)) ≈ log₂(20·n). Ez
n = 60-nál 10,25 bit, többe kerül, mint egy új szakértő egyetlen állításáé (kb. 4,3 bit). **A
vitatatlan tömeg a vitatott állításokat is védi.** κ = 30-nál a határköltség 5,91 bit: a múlt
számít, de csak logaritmikusan, log₂(1 + n/(κq)) bittel.

**(b) „Kevés hiba drágább, mint az összes” (új).** κ_T = 1 mellett 48 állításból 3 elutasítása 20,2
bit, mind a 48-é 9,6 bit. **A prior szerint egy elmélet, amelyben néhány hiba van, kevésbé valószínű,
mint egy teljesen téves.** A procedurális világban a tankönyv a szabályok 10%-át hibásan közli, tehát
ez éppen a tipikus eset, és a prior ezt tartja a legkevésbé valószínűnek.

**(c) Kevés adatnál az egész elmélet elvetése (45. kör).** Egy 10 entitásos (30 terepi tényes)
procedurális világban a v4.2 ε = 0,01 mellett **a tankönyv mind a 48 állítását elveti**, ε = 0,05
mellett a tankönyvet és a népszámlálást kontextusnak izolálja. Mindkét esetben a pontosság 0,48. A (b)
következménye: kevés terepi tény mellett a teljes elvetés kb. 9,6 bitje plusz a jóslatvesztés olcsóbb,
mint a 3 hibás szabály egyenkénti elvetése.

**(a) és (b) ugyanannak a priornak két oldala.** Ha az U alakú prior r ≈ 1 tömegét erősítjük, a
farmolás nő; ha a gestalt-váltást olcsón tartjuk, a „néhány hiba” drága marad. Egyetlen κ_T-vel a
kettő nem választható szét.

## 3. Javaslat: keverék-prior

Egy elmélet két állapot egyikében van:
- **nagyjából helyes, néhány hibával** (π valószínűséggel): r ~ Beta(κ₁·q, κ₁·(1 − q)), κ₁ = 30;
- **egészében téves** (1 − π): r ~ Beta(κ₀·q₀, κ₀·(1 − q₀)), q₀ = 0,5, κ₀ = 2 (egyenletes: a téves
  elmélet állításai érdektelenek).

A kódhossz `−log₂[π·BB(n, k; κ₁, q) + (1 − π)·BB(n, k; κ₀, q₀)]`. Ez valódi valószínűség (két
béta-binomiális keveréke), tehát a 36. kör értelmében egy generatív modell része marad. π = 0,9.

**A táblázat utolsó oszlopa:** kevés elutasításnál a keverék a κ = 30-as költséget adja (a farmolás
logaritmikus, (a) megszűnik), teljes elutasításnál a κ_T = 1-est (a gestalt-váltás olcsó marad), és a
„néhány hiba” nem drágább, mint az „összes” ((b) megszűnik).

**Ismert modellek:** ez egy kétkomponensű keverék-prior a forrás-megbízhatóságra, a
crowdsourcing-irodalom „spammer vs. jó munkás” modelljeinek (Raykar et al. 2010, ellenőrizendő)
elméletszintű megfelelője. Nem új módszer, de a hiba-diagnózis (a κ_T = 1 kettős szerepe) a mi
rendszerünkben új.

## 4. Állításonkénti hitelesség (47. kör, 1. kölcsönhatás)

A béta-kód forrásonként egyetlen előzetes q-t használ, az első megfigyelését. **Javaslat
(`q_groups`):** egy forrás eltérő deklarált hitelességű állításai külön csoportot alkotnak, saját
múlttal. Jelentése: „egy forrás 0,95-ös állításai és 0,9-es állításai külön mérhető minőségűek”. Ez
konjugált marad, és a téma szerinti felbontás (47. kör, 2. javaslat) egyszerű esete, ahol a „téma” a
deklarált bizonyosság. Gyengéje: a csoportok közt nincs információmegosztás (egy forrás 0,9-es
hibái nem rontják a 0,95-ös állításai hitelét). Ez hierarchikus priorral volna javítható.

## 5. Eredmények

*(az ellenőrző csomag futtatása után)*
