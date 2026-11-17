# 25. kör – Mennyit veszít az online keresés? (optimalitási rés)

## Kérdés

A 10. kör szerint az „azonnali” átrendezés ára egy esetleges optimalitási rés: az online,
nyalábos keresés rosszabb hipotézisben ragadhat, mint amit egy nagy, kötegelt keresés találna.
A 22. kör 3. ötlete („alvás”) ezt mérné ki. Ha a rés nagy, az offline újrakeresésnek van
értelme. Ha nulla, nincs.

## Elrendezés

- Ugyanazokat a megfigyeléseket háromféleképpen dolgozom fel:
  1. online, az alapbeállítással (nyaláb 8, mélység 3);
  2. nagyobb kereséssel (nyaláb 32, mélység 4);
  3. a tények három véletlen sorrendjében (a szabályok elöl maradnak).
- Esetek: hat E4-szerű zajos folyam (3 seed × ε ∈ {0,05; 0,1}, 132 megfigyelés) és két
  E2a-szerű anomália-folyam (N = 4 és 12, 7 anomáliával).
- Mérés: a végső legjobb hipotézis pontszáma bitben.
- Nyers eredmények: [`experiments/arlc/results/kor-25/results.json`](../../experiments/arlc/results/kor-25/results.json).

## Eredmény

| eset | online | nagy keresés | rés | 3 sorrend min–max |
|---|---|---|---|---|
| E4 seed0 ε 0,05 | 37,17 | 37,17 | **0** | 37,17–37,17 |
| E4 seed0 ε 0,10 | 42,35 | 42,35 | **0** | 42,35–42,35 |
| E4 seed1 ε 0,05 | 32,15 | 32,15 | **0** | 32,15–32,15 |
| E4 seed1 ε 0,10 | 48,53 | 48,53 | **0** | 48,53–48,53 |
| E4 seed2 ε 0,05 | 41,03 | 41,03 | **0** | 41,03–41,03 |
| E4 seed2 ε 0,10 | 37,17 | 37,17 | **0** | 37,17–37,17 |
| E2a N4, 7 anomália | 18,82 | 18,82 | **0** | 18,82–18,82 |
| E2a N12, 7 anomália | 29,25 | 29,25 | **0** | 29,25–29,25 |

## Értelmezés

1. **Ezeken a feladatokon az online keresés nem veszít semmit**, és a végső pontszám
   sorrendfüggetlen.
2. **A 17. körben látott sorrendhatás így nem keresési hiba.** Ott a két hipotézis (A vagy B a
   „hazug”) *azonos pontszámú*, és a sorrend csak azt dönti el, melyik optimumba kerül a
   rendszer. Ez útfüggés holtversenyes optimumok között. Offline újrakeresés ezen nem segít,
   csak egy külső jel vagy egy aktív kérdés (13. kör, A-ötlet).
3. **Korlátok:**
   - a „nagy keresés” sem kimerítő, így a rés alsó becslés;
   - ezek a feladatok helyi konfliktusokból állnak, könnyűek. A 10. kör elméleti fala
     (Σ₂ᴾ-nehézség) itt nem jelenik meg. Nehéz eseteket (sok, egymásba fonódó szabály, a
     Thagard-fokozatok 7–9) még nem teszteltünk.

## Következmény

- Az „alvás” mint offline újrakeresés **ebben a tartományban fölösleges**. Egy olyan
  benchmarkon kell újra mérni, ahol a konfliktusok összefonódnak. Ez a TFB (9. kör) 7–9.
  fokozata, ami még nincs megvalósítva.
- Az útfüggés holtversenynél **elvi**, nem algoritmikus. Ez erősíti a 20. kör állítását: a
  külső jel (az LLM vagy egy kérdés) nem kényelmi kiegészítés, hanem ott elvben szükséges.
