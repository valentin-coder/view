# 68. kör – Azonosíthatóság az igaz hipotézisből

## 1. rész: terv és jóslatok (a futtatás előtt)

A 67. kör szerint a nyaláb-alapú margó nem mér azonosíthatóságot. Itt az igaz magyarázatból indulok. Esetenként
felépítem az **igazhoz horgonyzott hipotézist**:
- elvetve: a tankönyv hibásan közölt szabályai, a zajos terepi tények, a hazug forrás tényei;
- kontextusba izolálva: a „más régió” forrás;
- a maradék ütközéseket (valódi kivételek, felülírások, átkategorizálás) mohó befejezés oldja fel, utána a
  visszahelyező lépés (36. kör) kidobja a felesleges elutasításokat. (Az első futásban a visszahelyezés nélkül a mohó
  lépés 14 felesleges elutasítást adott, és a horgonyzott hipotézis target-acc-ja 0,5 lett. A J3 ezt fogta meg; a
  futást 43 eset után leállítottam, és ezzel a javítással újraindítottam.)

A **rés** = L(H_igaz) − L(MAP) bitben:
- > 0: a modell egy hamis magyarázatot tart olcsóbbnak (**modellhiba**);
- < 0: az igaz magyarázat olcsóbb, de a keresés nem találta meg (**keresési hiba**);
- |rés| < 1 bit: **alulhatározott**.

Kód: [`run_r68.py`](../../experiments/arlc/arlc/run_r68.py). A populáció, seed 10000–10014 (friss), 5 típus, v4.4e.

**Jóslatok:**
- **J1:** a „más régió” esetek legalább felében |rés| < 1 bit.
- **J2:** a rés az esetek többségében (> 50%) pozitív: a modell hibája gyakoribb, mint a keresésé (a 36. és 42. kör
  kimerítő ellenőrzése kis feladatokon nem talált keresési rést).
- **J3:** az igazhoz horgonyzott hipotézis target-acc-ja minden típusban legalább 0,9 (a horgonyzás ellenőrzése).

## 2. rész: eredmények

75 eset; nyers adat: [`results/kor-68/`](../../experiments/arlc/results/kor-68/).

| típus | rés medián (bit) | rés > 0 | target-acc: horgonyzott / MAP | post-acc: horgonyzott / MAP | többletelutasítás |
|---|---|---|---|---|---|
| hazug forrás | 10,2 | 15/15 | 0,825 / 0,692 | 0,833 / 0,827 | 8,4 |
| kivételes alfaj | 13,4 | 15/15 | **0,578** / 0,758 | 0,832 / 0,798 | 10,7 |
| más régió | 13,0 | 15/15 | **0,798 / 0,219** | 0,834 / 0,797 | 13,7 |
| szabály-helyesbítés | 8,3 | 15/15 | 0,848 / 0,824 | 0,850 / 0,843 | 8,3 |
| átkategorizálás | 10,7 | 15/15 | 0,617 / 0,575 | 0,814 / 0,821 | 8,9 |

- **J1 nem teljesül:** egyetlen „más régió” esetben sem |rés| < 1 bit.
- **J2 teljesül** (75/75 pozitív rés), de lásd a J3-at.
- **J3 nem teljesül:** a horgonyzott hipotézis target-acc-ja 0,58–0,85, a „kivételes alfaj”-ban rosszabb, mint a MAP.
  **A horgonyzás tehát nem állítja elő az igaz magyarázatot.** A mohó kitöltés a valódi kivételek és felülírások
  helyett terepi tényeket utasít el (visszahelyezés után is átlagosan 8–14 többletelutasítás).

### Értelmezés

1. **A mért rés felső korlát, nem az azonosíthatóság mértéke.** Az igaz magyarázattal konzisztens hipotézisek *legjobbja*
   olcsóbb lehet, mint az itt horgonyzott, mert a horgonyzott hipotézis egy rossz mohó kitöltést hordoz. Az
   azonosíthatóság helyes méréséhez korlátozott optimalizálás kell: a teljes keresés futtatása úgy, hogy az igaz
   magyarázat elemei rögzítettek. Ez ebben a kódban nem triviális, és nem valósítottam meg.
2. **Egy jel mégis erős:** a „más régió” típusban az igazsággal konzisztens hipotézis célkérdés-pontossága 0,80, a MAP-é
   0,22, és az igaz magyarázat (a régióforrás izolálása) legfeljebb kb. 13 bittel drágább. A 62. kör holtversenye (0,04–0,43
   bit) a két *hamis* magyarázat között volt (a régióforrás téved vagy a tankönyv téved); a *helyes* magyarázat (más
   kontextus) ezeknél drágább. **A modell a helyes kontextus-magyarázatot drágábbnak tartja, mint két hamisat.** Ez a 17.,
   57. és 60. kör kontextus-problémájának legközvetlenebb mérése: jel nélkül a kontextus-magyarázat nem nyer.
3. **Módszertani tanulság:** egy ellenőrző jóslat (J3) nélkül a 75/75-ös pozitív rés könnyen „a modell mindig hibás”
   következtetéshez vezetett volna. A J3 megmutatta, hogy a mérőeszköz maga hibás.
