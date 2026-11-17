# 21. kör – Követelmény-levezetés: milyen pontos legyen egy LLM-ből jövő kontextus-jel?

## Kérdés

A 20. kör szerint az LLM-re ott van szükség, ahol a szimbolikus adat nem dönt. Az első ilyen
hely a kontextus-jel: más kontextusról beszél-e egy forrás, vagy téved/hazudik (17. kör).
**Milyen pontos jel kell ahhoz, hogy az ARLC döntése megbízhatóan helyes legyen?** Ez modell
nélkül is megmérhető, szimulált jellel.

## Elrendezés (E3c)

- Két forrás ütközik, n entitáson, n ∈ {4, 8, 16, 32} véletlenszerűen.
- Fele-fele arányban rendszerszerű ütközés (a helyes döntés: szétválasztás) és zajos forrás
  (a helyes döntés: a zajos állítások elutasítása).
- **Szimulált jel** a B forrásra: „más kontextus” vagy „ugyanaz”, a pontossággal.
  A szétválasztás költsége `c_ctx₀ − log₂ LR`, ahol `LR = a/(1−a)` a jel valószínűséghányadosa
  (és fordítva, ha a jel „ugyanaz”).
- 24 próba pontosságonként; mélység 3, nyaláb 4 (a 17. kör rácsán 27/27 egyezés a
  mélység 3 / nyaláb 8 beállítással, kétszer gyorsabban).
- Nyers eredmények: [`experiments/arlc/results/kor-17-21/e3c/results.json`](../../experiments/arlc/results/kor-17-21/e3c/results.json).

## Eredmények (helyes döntések aránya; 24 próba, a standard hiba kb. ±0,07)

| a jel pontossága | 0,5 (nincs jel) | 0,6 | 0,7 | 0,8 | 0,9 | 0,95 | 0,99 |
|---|---|---|---|---|---|---|---|
| rögzített megbízhatóság | 0,83 | 0,88 | 0,96 | 0,79 | 0,88 | **1,00** | **1,00** |
| tanult megbízhatóság (κ = 30) | 0,92 | 0,88 | 0,88 | 0,83 | 0,79 | 0,96 | **1,00** |

## Értelmezés

1. **Jel nélkül is 83–92% helyes.** A hibák főleg a kis (n = 4) rendszerszerű esetekből jönnek,
   ahol kevés az evidencia a szétválasztáshoz.
2. **A közepes pontosságú jel (0,7–0,9) nem segít, sőt ronthat.** Egy téves jel a határeseteket
   rossz irányba billenti, és ezt a jó jelek nem ellensúlyozzák. A görbe nem monoton; ez részben
   a kis mintából jön, részben valódi: egy 2–3 bites jel csak határeseteken számít, és ott
   ugyanakkora eséllyel árt, mint használ.
3. **Csak a nagyon pontos jel (≥ 0,95, kb. ≥ 4,2 bit) emeli a döntést megbízhatóan 95% fölé.**

## A követelmény

> **A B fázisban egy LLM-ből jövő kontextus-jelnek legalább kb. 0,95-ös pontosságot (AUC)
> kell elérnie *a jelöletlen esetekben*, különben az ARLC-ben nincs haszna.**

Ezzel az R5 kritérium élesebb lett: nem elég, ha az LLM-jel „jobb a véletlennél” vagy „jobb a
BoW-nál”. Egy konkrét küszöböt kell átlépnie, amelyet a downstream döntés határoz meg.

## Mellékeredmény: a 17. kör egyik feltevésének cáfolata

A 17. kör azt gyanította, hogy a κ = 10-nél látott sorrendhatást a csak globális indukció
okozza. A magba bekerült a **kontextusfüggő indukció** (kapcsolóval: az izolált kontextusban
indukált szabály oda szkópolódik). **A döntések egyik rácspontban sem változtak**, a sorrendhatás
megmaradt. A szétválasztott hipotézisek viszont gazdagabbak lettek: mindkét kontextus saját
szabályt kap (A-ban „mérges”, B-ben „nem mérges”). A sorrendhatás oka tehát a hazug-tanulás és a
holtverseny, nem az indukció.
