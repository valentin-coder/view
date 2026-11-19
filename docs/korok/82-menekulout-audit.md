# 82. kör – Menekülőút-audit: a félretevések minősége a generátor igazsága alapján (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

A 79. kör szerint a sorozat visszatérő hibamintája a menekülőút: a rendszer egy kifejezhetetlen szerkezetet egy olcsó,
de hamis magyarázattal helyettesít (izolálás, bűnbak-forrás). Eddig ezt csak közvetve, a pontosságon keresztül láttam,
és esetenként kézzel diagnosztizáltam (78., 81. kör). A generátorok ismerik az igazságot, ezért **minden félretevésről
eldönthető, hogy helyes volt-e.** Ez egy pontosságtól független, mechanizmus-szintű mérőszám.

### Mérőszámok

Kód: [`audit_truth.py`](../../experiments/arlc/arlc/audit_truth.py). Minden megfigyelésre a meglepetés előtti világ
szerint: igaz, hamis vagy nem definiált. A végső hipotézisben forrásonként és fajtánként (szabály/tény):
- **helyes félretevés:** hamis állítás félretéve;
- **téves félretevés:** igaz állítás félretéve (ez a menekülőút közvetlen mértéke);
- **elmulasztott:** hamis állítás elfogadva;
- a félretevés **pontossága:** helyes / (helyes + téves);
- izolált források, osztály- és egyedi kivételek száma.

### Elrendezés

- **Seedek:** 19000–19019 (friss). Típus: hazug forrás. G2; G1 A és B populáció (B-ben a 19007, 19013, 19016, 19017-es
  seed szemét-tankönyves).
- **Módszerek:** v3, v4.9, v4.9+PK (81. kör). Kód: [`run_r82.py`](../../experiments/arlc/arlc/run_r82.py). 180 eset.

### Hipotézisek

- **H82a (G2, a meglepetés előtt):** a tankönyvi szabályok átlagos téves félretevése a v4.9+PK-nál legfeljebb fele a
  v4.9-ének.
- **H82b (G2, v4.9):** a tankönyvi szabályok félretevésének pontossága < 0,5 (a tankönyv bűnbak: több igaz szabályt
  tesz félre, mint hamisat).
- **H82c (G2):** a fieldB helyes félretevéseinek átlaga a v4.9+PK-nál legalább akkora, mint a v3-nál (a tanult
  megbízhatóság a valóban rossz terepforrást találja meg).
- **H82d (G1-A):** a v4.9 és a v4.9+PK az esetek legalább 95%-ában egyetlen forrást sem izolál (ezekben az esetekben
  nincs valódi kontextus).
- **H82e (mindhárom halmaz):** a hazug forrás félretett aránya a v4.9-nél és a v4.9+PK-nál ≥ 0,9, a v3-nál kisebb.

Leíró (nem hipotézis): a G1-B szemét-tankönyves seedjein a tankönyv félretevésének pontossága; a G1-A-ban a tankönyvi
téves félretevések száma (van-e ott is bűnbak).
