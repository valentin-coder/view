# 12. kör – Robusztusság: ha egy erős élmény átrendez, akkor egy hamis is

## A probléma

A cél egy olyan rendszer, amely egyetlen erős, meglepő információ hatására átrendezi a
sémáit. **Pontosan ez a tulajdonság teszi támadhatóvá:** egy szándékosan megírt, hamis,
„erős” állítás ugyanúgy átrendez, mint egy igaz. Ez a kör a fenyegetési modellt, a
támadási költséget és a védekezést formalizálja.

## Fenyegetési modell

A támadó szöveges állításokat injektál a megfigyelési folyamba. Célja az egyik:
- **T1 – célzott váltás:** egy kiválasztott séma átbillentése („a vakcina X”);
- **T2 – maximális kollaterális:** olyan állítás, amelynek a függőségi kúpja a lehető
  legnagyobb;
- **T3 – tartós rejtőzés:** egy kontextus-szétválasztást kikényszeríteni, hogy az igaz
  tudás egy elszigetelt kontextusba kerüljön.

**Támadási felületek:**
1. **Hitelesség-hamisítás:** ha a forrás hitelességét maga az állítás deklarálja („a
   tudósok bebizonyították”), egyetlen állítás elég. Ez triviális támadás, ha a
   konfidenciát a szövegből olvassuk.
2. **Felhalmozás:** sok alacsony hitelességű állítás, amelyek a CUSUM-statisztikát
   (11. kör, b paraméter) a küszöb fölé tolják.
3. **Grounding-támadás:** olyan szövegezés, amelyet a probe-ok félreolvasnak. Ez a
   „neuro” rész támadása, aktivációs szintű ellenséges példa.
4. **Prior-kihasználás:** ha a hamis állítás egybeesik az LLM tévképzeteivel
   (TruthfulQA-típusú tévhitek, Lin et al. 2022), akkor a D-ötlet LLM-prior tagja
   (5. kör) a *támadót* segíti.

## Kulcsfelismerés: plaszticitás és robusztusság ugyanaz a szám

Az MDL-trigger szerint a váltás akkor történik, ha a felgyűlt anomália-bitek meghaladják
a szerkezeti költségkülönbséget. **Ebből következik:**

> Ha a rendszernek nincs olyan jele, amely a becsületes evidenciát a támadótól
> megkülönbözteti, akkor a becsületes váltáshoz szükséges bitmennyiség és a támadó
> költsége ugyanaz a mennyiség. A plaszticitás és a robusztusság között így tiszta
> átváltás van, ingyen ebéd nincs.

**A kettőt csak egy elválasztó jel tudja szétválasztani.** Három ilyen jel jöhet szóba:
- a forrás múltbeli megbízhatósága;
- független megerősítés több forrásból;
- empirikus ellenőrizhetőség (Posner termékenysége, 7. kör): az új séma olyan jóslatot
  tesz, amelyet a rendszer ellenőrizni tud.

## Védekezési mechanizmusok

| # | Mechanizmus | Formalizálás | Ára |
|---|---|---|---|
| V1 | **Forrás mint feltevés** | minden forrás egy ATMS-feltevés, `src(s)`. Minden tőle jövő tény ebben a környezetben él. | Ha egy forrásról kiderül, hogy hazudott, minden állítása egyszerre visszavonódik. **Ez maga is egy sémaváltási típus:** „az újság hazudott”. |
| V2 | **Tanult hitelesség** | forrásonként béta–binomiális becslés a múltbeli ellenőrzött állításokból; `ε(új tény) ∝ E[hitelesség]` | az új forrás hitelessége ismeretlen, ilyenkor a priort kell önkényesen megadni |
| V3 | **Független megerősítés** | magas beágyazottságú séma csak legalább k független forrás után vált | **Sybil-probléma:** honnan tudjuk, hogy a források függetlenek? |
| V4 | **Ideiglenes állapot** | a váltás először „provizórikus”: a régi hipotézis a nyalábban marad, lecsengő súllyal. Csak akkor véglegesedik, ha az új séma legalább egy ellenőrizhető jóslata bejön. | lassítja a véglegesítést, de a válaszok azonnal az új sémát tükrözik |
| V5 | **Refrakter periódus** | egy séma váltása után T ideig a visszaváltás küszöbe megemelkedik | ez ugyanaz, mint a 11. kör hiszterézise; a támadó is profitál belőle, ha ő váltott elsőként |
| V6 | **Korai figyelmeztetés** | a 11. kör J4 jele: ha egy séma kritikusan lassul, növekedjen az ellenőrzés | csak felhalmozásos támadás ellen hat, egylépéses ellen nem |

## Formális robusztussági margó

Minden ℋ* hipotézisre:
`ρ(ℋ*) = min_{ℋ'} [L_struct(ℋ') − L_struct(ℋ*)] − Σ_{τ∈Anom} [L(e_τ|ℋ*) − L(e_τ|ℋ')]`

Ennyi bitet kell még a támadónak befektetnie a legolcsóbb alternatívába való átbillentéshez.
**Ezt a rendszer jelentheti** sémánként. A V2 forrás-hitelesség mellett a támadó bitjei
`(1 − hitelesség)` arányban értékelődnek le.

## Kísérlet: E5 – ellenséges injektálás

- **Világ:** a Nonce- és a Valós kategória-világ.
- **Támadások:** a T1–T3 célok mindhárom felületen (hitelesség-hamisítás, felhalmozás,
  prior-kihasználás). A grounding-támadás külön kísérlet, mert ellenséges szöveg
  keresése kell hozzá.
- **Becsületes párhuzam:** ugyanannyi igaz, meglepő állítás.
- **Mérés:** a hamis és az igaz váltások aránya. Ebből ROC-görbe: plaszticitás (igaz
  váltások aránya) a robusztusság (1 − hamis váltások aránya) függvényében, a védekezések
  kombinációi mellett.
- **Cáfolat:** ha egy védekezés a hamis váltások számát X%-kal csökkenti, de az igaz
  váltásokét is legalább X%-kal, akkor nem választ el, csak a küszöböt tolja el, és
  értéktelen.

## Kapcsolódó munkák

- RAG-mérgezés: PoisonedRAG [Zou et al. 2024].
- Tudásszerkesztés elleni támadások: BadEdit [Li et al. 2024].
- Félreinformálás LLM-kontextusban [Pan et al. 2023].
- **Igazságfeltárás több ütköző forrásból** [Yin, Han, Yu 2008, TruthFinder; Li et al. 2016
  áttekintés]. Ez a V2–V3 legközelebbi előzménye, onnan kell átvenni a forrás-megbízhatósági
  becslést.
- Hiedelemrevízió megbízhatósággal: Booth–Hunter 2018 körüli „trust-sensitive belief
  revision” munkák, ellenőrizendő.
