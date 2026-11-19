# 67. kör – Azonosíthatóság: döntési margó meglepetéstípusonként (feltáró)

## 1. rész: terv és jóslat (a futtatás előtt)

A 62. kör szerint a „más régió” eset holtverseny. A 64. kör javaslata: minden meglepetéstípusra mérni kell, mennyire
dönti el az adat a célkérdést. Olcsó közelítés a **döntési margó**: L(H\*) − L(MAP), ahol H\* a nyaláb legjobb olyan
hipotézise, amely legalább egy célkérdésre mást válaszol. Ha nincs ilyen, a nyaláb teljes szórása alsó becslés.
**Korlát:** a 63. kör szerint a nyaláb nem poszterior-minta, ezért a margó felülbecsülheti az azonosíthatóságot,
ha a nyaláb nem tartalmazza a versengő magyarázatot.

Kód: [`run_r67.py`](../../experiments/arlc/arlc/run_r67.py). A populáció, seed 9000–9014 (friss), 5 típus, v4.8-π.

**Jóslatok (a futtatás előtt):**
- **J1:** a „más régió” típus medián margója a legkisebb (< 1 bit).
- **J2:** a target-acc a margóval nő: a < 1 bites esetekben legfeljebb 0,6, a > 3 bitesekben legalább 0,8.

## 2. rész: eredmények

75 eset (A populáció, 15 seed × 5 típus); nyers adat: [`results/kor-67/`](../../experiments/arlc/results/kor-67/).

| típus | medián margó (bit) | nincs ellenkező a nyalábban | target-acc |
|---|---|---|---|
| hazug forrás | 0,93 | 5/15 | 0,750 |
| kivételes alfaj | 1,55 | 10/15 | 0,748 |
| más régió | 1,55 | 5/15 | 0,528 |
| szabály-helyesbítés | 0,93 | 9/15 | 0,855 |
| átkategorizálás | 0,96 | 8/15 | 0,609 |

| margó | esetek | target-acc |
|---|---|---|
| < 1 bit | 19 | 0,725 |
| 1–3 bit | 9 | 0,644 |
| > 3 bit | 10 | **0,389** |
| nincs ellenkező a nyalábban (alsó korlát medián 1,18) | 37 | 0,781 |

- **J1 nem teljesül:** a „más régió” margója nem a legkisebb.
- **J2 fordítva áll:** a célkérdés-pontosság a margóval **csökken**.

### Értelmezés

**A nyaláb-alapú döntési margó nem azonosíthatósági mérték.** A nagy margó a *magabiztos tévedés* jele (például egy
teljes félretevés vagy egy rossz oldalra billent holtverseny után a nyaláb minden tagja ugyanazt a hibás döntést
hordozza, és a legközelebbi ellenkező hipotézis messze van). Ez a 63. kör megállapításának („a nyaláb nem
poszterior-minta”) második, független megerősítése. A nyaláb a keresés útjának környezetét tükrözi, nem a
magyarázatok terét.

**Ami helyette kell:** az igaz hipotézis és a MAP pontszám-különbsége. Ehhez a generátornak meg kell adnia az igaz
hipotézist (mely jelentések megbízhatatlanok, mely alkalmazások kivételek, melyik forrás szól más kontextusról). A
56. kör diagnózisa egyetlen esetre ezt kézzel tette meg. A 68. kör ezt általánosítja.
