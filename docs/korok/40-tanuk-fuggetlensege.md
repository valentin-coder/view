# 40. kör – Tanúk, hallomás és Hume csodái: mennyit ér sok tanú egyetlen esetről?

## Kérdés (vízszintes)

- **Condorcet esküdtszéki tétele:** független, a véletlennél jobb tanúk evidenciája összeadódik.
  Korrelált tanúknál a hatásos tanúszám kisebb (Ladha 1992, ellenőrizendő).
- **Hallomás-szabály a jogban:** egy másodkézből továbbadott állítás nem önálló tanúvallomás. Ez a
  31. kör származás-problémája.
- **Hume (1748, „Of Miracles”):** egy tanúvallomás egy csodát csak akkor igazol, ha a tanúvallomás
  hamissága nagyobb csoda volna, mint az esemény.

Függőleges kérdés: egy ARLC-szabályt („dax mérges”, N alátámasztással) k független eredeti eset
támad, és mindegyik esetet r további forrás „továbbad”. Hány eredeti eset kell a szabály feladásához,
naiv (minden továbbadó új forrás) és származás-tudatos (a továbbadott állítás az eredetié) módban?

Kód: [`witnesses.py`](../../experiments/arlc/arlc/witnesses.py); eredmény:
[`results/kor-40/results.json`](../../experiments/arlc/results/kor-40/results.json).

## Első eredmény: a tagság elutasítása mindent semlegesít

Ha az eset tagsága („x_j egy dax”) szokásos hitelességű (0,9), a továbbadóknak **semmilyen hatása
nincs** (N = 4, 8, 16; r = 0…7: mindig 3, 4, 7 eredeti eset). A szabály megtartásához elég
*egyszer* kimondani, hogy „x_j nem is dax”, és ez az összes tanút semlegesíti. Ez a 19–26. kör helyi
kiútja, és **egy eset bármennyi tanújára igaz**.

## Második eredmény: szilárd tagság mellett is telítődik

Szilárd tagsággal (0,999):

| N | r = 0 | r = 1 | r = 3 | r = 7 |
|---|---|---|---|---|
| 4 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| 8 | 4 / 4 | 4 / 4 | 4 / 4 | 4 / 4 |
| 16 | 7 / 7 | **5** / 7 | **5** / 7 | **5** / 7 |

(cellák: naiv / származás-tudatos; az átfordításhoz szükséges eredeti esetek száma)

## Levezetés

A „szabály megtartása” hipotézisben minden esetet valahogy semlegesíteni kell, és a rendszer a
legolcsóbb módot választja:

`w(eset) = min( tanúk_száma · log₂(q/(1−q)),  log₂|E| (kivétel),  log₂(q_tag/(1−q_tag)) (újraértelmezés) )`

A szabály akkor esik, ha `Σ w(eset) ≥ T(N) = log₂(19) + N·(1 + log₂ 0,95)`.

| N | T(N) | |E| | w naiv (r ≥ 1) | w származás | jósolt k (naiv / származás) | mért |
|---|---|---|---|---|---|---|
| 4 | 8,0 | 9 | 3,17 | 3,17 | 3 / 3 | 3 / 3 |
| 8 | 11,7 | kb. 14 | 3,81 | 3,17 | 4 / 4 | 4 / 4 |
| 16 | 19,1 | kb. 23 | 4,52 | 3,17 | 5 / 7 | 5 / 7 |

A jóslat minden cellában egyezik.

## Értelmezés

1. **Egyetlen eset tanúvallomásainak súlyát felülről korlátozza az eset kivétellé nyilvánításának
   ára.** Sok tanú egy esetről legfeljebb `log₂|E|` bitet ér. Ez **Hume érvelésének** formális
   alakja: egy egyetlen kivételes eseményről szóló tanúvallomás akkor sem dönt meg egy jól
   alátámasztott törvényt, ha sok a tanú, mert olcsóbb az eseményt kivételnek tekinteni. Egy
   törvényt *sok független eset* dönt meg.
2. **A naiv (hallomás-) számolás kára ezért korlátos.** A 31. kör visszhang-polarizációjában azért volt
   nagy, mert ott a társak *sok különböző entitásról* mondtak levezetett állítást. Ott minden eset
   külön számított, és a korlát nem érvényesült.
3. **A korlát függ a világ méretétől (|E|).** Ez valószínűleg a kivétel-kódolás műterméke (27. kör
   Elio–Pelletier-megjegyzése). Egy jobb modellben a kivétel ára az eset *előzetes valószínűségétől*
   függene, nem a világ méretétől.

## Kapcsolódás

- Hume 1748; a modern bayesi olvasatot ellenőrizni kell (pl. Earman 2000, *Hume's Abject Failure*).
- Condorcet; Ladha 1992 (korrelált szavazók).
- Bovens és Hartmann 2003 (*Bayesian Epistemology*): tanúk megbízhatósága és koherencia. Ők
  megmutatták, hogy a koherencia nem mindig igazságjelző. Ez a 28. kör gestalt–zaj feszültségének
  rokona.
