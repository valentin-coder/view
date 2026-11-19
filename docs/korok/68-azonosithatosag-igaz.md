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

*(a futtatás után)*
