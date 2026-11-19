# 71. kör – Kontextuson belüli elsőbbség a v4.8-π-ben (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 68. kör szerint a „más régió” helyes magyarázata (a forrás más kontextusról szól) drágább, mint két hamis. A
69. kör diagnózisa: az izolált kontextusban a régióforrás saját szabálya ütközik az örökölt tankönyvi szabállyal,
és ennek feloldása drága. Az 50. kör „kontextuson belüli elsőbbség” mechanizmusa (`ctx_override`: az izolált forrás a
saját kontextusában felülír; minden felülírás egy kivétel árú eltérés) éppen ezt kezelné. Ott a kétszintű v4-gyel
nem segített, mert a fő hiba a tankönyv teljes félretevése volt. A v4.8-π-ben (metaadat-π) ez a hiba kisebb.

### Elrendezés

Kód: [`run_r71.py`](../../experiments/arlc/arlc/run_r71.py). A populáció, seedek **12000–12019** (friss), típusok:
szabály-helyesbítés, hazug forrás, más régió (60 eset). Változatok: v4.8-π; v4.8-π + elsőbbség; v4.8-π + elsőbbség +
kontextusjel (a = 0,99, a 60. kör Bayes-árazásával).

### Hipotézisek

- **H71a:** a „más régió” célkérdésein a „+elsőbbség+jel” target-acc-ja legalább 0,2-vel nagyobb a v4.8-π-énél.
- **H71b:** a „+elsőbbség” (jel nélkül) a „más régió”-ban nem javít legalább 0,1-gyel (jel nélkül a kontextus 6 bitje
  drága marad).
- **H71c (kár):** a szabály-helyesbítés és hazug forrás típusban a „+elsőbbség+jel” post-acc-ja legfeljebb 0,02-vel
  marad el a v4.8-π-étől.

Az ellenőrző csomag E3-ja (kontextus vagy elutasítás) az 50. körben 0,75-ről 0,5-re esett az elsőbbséggel. Ezt a futás
után a v4.8-π-vel is megnézem.

## 2. rész: eredmények

*(a futtatás után)*
