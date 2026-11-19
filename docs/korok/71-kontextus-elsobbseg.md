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

59 eset (egy „szabály-helyesbítés” eset nem fejeződött be a kiértékelésig); nyers adat:
[`results/kor-71/`](../../experiments/arlc/results/kor-71/).

| típus | v4.8-π (post / target) | + elsőbbség | + elsőbbség + jel (0,99) | régióforrás izolálva |
|---|---|---|---|---|
| hazug forrás | 0,788 / 0,719 | 0,788 / 0,719 | 0,802 / 0,744 | – |
| **más régió** | 0,767 / 0,345 | 0,768 / 0,375 | 0,774 / **0,543** | 1 → 1 → **6** (20-ból) |
| szabály-helyesbítés | 0,810 / 0,776 | 0,810 / 0,776 | 0,811 / 0,776 | – |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H71a:** más régió target: +elsőbbség+jel − v4.8-π ≥ 0,2 | **+0,197** [+0,053; +0,382] | **épphogy nem teljesül** (szignifikáns javulás, a küszöb alatt 0,003-mal) |
| **H71b:** +elsőbbség jel nélkül < +0,1 | +0,030 [0,000; +0,090] | **teljesül** |
| **H71c:** nincs kár a többi típusban (≥ −0,02) | +0,008 [0,000; +0,022] | **teljesül** |

**Ellenőrző csomag** ([`battery.json`](../../experiments/arlc/results/kor-48/battery.json)): a v4.8-π (π = 0,9) a TFB-9-et
helyesen kezeli (0,96, a vesztes fa nem aktív), az E1-et 0,75-tel. Az elsőbbséggel az **E3 0,75-ről 0,5-re esik**, mint az
50. körben. Az E3 a „kontextus vagy elutasítás” döntést méri jel nélkül.

### Értelmezés

1. **A 69. kör diagnózisa igazolódik:** a helyes kontextus-magyarázat két dolgon múlt, a kontextuson belüli elsőbbségen
   (az izolált forrás saját szabálya felülírhatja az örököltet) és a jó jelen. Együtt a „más régió” célkérdés-pontossága
   0,35-ről 0,54-re nő, és a régióforrást 6-szor annyiszor izolálja. Külön-külön egyik sem elég (a 62. kör: a jel
   elsőbbség nélkül; itt: az elsőbbség jel nélkül).
2. **Jel nélkül az elsőbbség árt** (E3). A helyes kialakítás tehát: **az elsőbbség csak jelzett forrásra érvényes.** Jel
   nélkül a forrás-szintű kontextus maradjon drága, mert a 17. kör szerint ilyenkor adatból nem dönthető el.
3. **Ez a B fázis második LLM-feladatának (kontextusjel, 61. kör) közvetlen értéke:** kb. 0,99-es kontextusjel mellett
   +0,2 a helyes kontextus-magyarázaton, jel nélkül semmi.
