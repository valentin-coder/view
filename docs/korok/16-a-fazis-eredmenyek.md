# 16. kör – Az A fázis első eredményei (szimbolikus mag, orákulum-groundinggal)

A 15. kör specifikációját megvalósítottam ([`experiments/arlc/`](../../experiments/arlc/)), és a 14.
kör A fázisának kísérleteit lefuttattam. **LLM nincs a hurokban:** a bemenet hibátlan, vagy
mesterségesen zajosított szimbolikus literál. Ezek az eredmények tehát csak a szimbolikus
félről szólnak. A teljes futás CPU-n kb. 1 perc. Nyers eredmények:
[`experiments/arlc/results/a-fazis/results.json`](../../experiments/arlc/results/a-fazis/results.json).

## Mit kellett közben kijavítani (ezek maguk is eredmények)

A specifikáció első változata öt ponton hibás volt. Mindegyiket a kísérlet hozta elő:

| # | Hiba | Tünet | Javítás |
|---|---|---|---|
| 1 | Korlátos mélységű javítás | N ≥ 8 alátámasztó ténynél a szabály soha nem fordult át | mohó befejezés a mélységkorlát alatt (anytime, 10. kör) |
| 2 | Hiányzott a „visszahelyezés” | egy szabály visszavonása után a miatta elutasított megfigyelések elutasítva maradtak | lokális keresés: elutasítás/kivétel/elszigetelés visszavétele, ha csökkenti a pontszámot |
| 3 | A vágás kódhosszában fölösleges `log₂ t` tag | frissítés helyett mindig revízió | a vágás idejét a későbbi megfigyelés meghatározza, nem kell kódolni |
| 4 | **Két ellentmondó általános szabály nem ütközött közvetlenül** | egy erős általános állítás soha nem fordította át a régi szabályt; mindig olcsóbb volt egy példány tagságát eldobni | szabályszintű nogood |
| 5 | Minden tény időben indexelt | „a hal mindig is hal volt” revízió nem volt kifejezhető | a nem változó csoportok tényei időtlenek |

**A 4. pont tanulsága általános:** ha a konzisztenciát csak a példányokon ellenőrizzük, egy
rendszer következetesen a legolcsóbb, *helyi* magyarázatot választja („ez a dax nem is
dax”), és a *globális* sémaváltás soha nem következik be. Az emberi sémaváltás tipikus
kudarcmódjának tűnik ez is, de ez itt csak analógia, nem bizonyíték.

## Eredmények

### E1 – Propagáció (10 seed, tiszta helyzet)

| Feladat | lookup RR | recency RR / kollat. | wms RR / kollat. | **ARLC RR / kollat.** |
|---|---|---|---|---|
| átkategorizálás, testvér (3 ripple) | 0,43 | 1,00 / 0,000 | 1,00 / 0,000 | **1,00 / 0,000** |
| unokatestvér (≈6) | 0,43 | 0,36 / 0,037 | 1,00 / 0,000 | **1,00 / 0,000** |
| másik gyökér (9) | 0,45 | 0,49 / 0,042 | 1,00 / 0,000 | **1,00 / 0,000** |
| alosztály-csere (≈13) | 0,45 | 0,38 / 0,042 | 0,59 / 0,018 | **0,98 / 0,003** |

- A `lookup` (sima memória, következtetés nélkül) RR-je kb. 0,45: csak azokat a kérdéseket
  találja el, ahol a helyes válasz „nem tudom”. **A propagáció kell.**
- A `recency` a legrégebbi megfigyelést dobja el. Az gyakran egy teljes szabály, ezért
  globális kollaterális kár keletkezik.
- **A `wms` és az ARLC különbsége csak az alosztály-cserénél jelenik meg.** Az egyszerű
  átkategorizálásra a BeliefBank-szerű súlyozott MaxSAT is elég.

### E2a – Anomália-tűrés (a beágyazottság és a váltási pont)

| N (alátámasztó tény) | 1 | 2 | 4 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|
| recency váltás | 1 | 1 | 1 | 1 | 1 | 1 |
| wms váltás | 2 | 2 | 2 | 2 | 2 | 2 |
| **ARLC váltás** | 2 | 2 | 3 | 4 | 5 | 7 |
| analitikus jóslat (`⌈(4,25 + 0,93N)/3,17⌉`) | 2 | 2 | 3 | 4 | 5 | 7 |

- Spearman(N, váltás) = **0,99** az ARLC-nél. A `wms` váltási pontja konstans, a `recency`
  azonnal vált.
- **Az R4 kritérium (Spearman ≥ 0,7) teljesül.**
- **Őszinte megszorítás:** a jóslatot ugyanabból a kódhossz-modellből vezettem le, mint amit a
  kód megvalósít. A pontos egyezés azt igazolja, hogy a keresés megtalálja a modell
  optimumát, és nem azt, hogy a modell jó modellje bárminek. A váltási pont N-ben lineáris,
  nem a 11. kör csúcskatasztrófájának `a^{3/2}`-skálázása szerint nő.

### E2b – Egyetlen erős általános állítás („a daxok nem mérgesek”)

| N | 0 | 1 | 2 | 4 | 8 |
|---|---|---|---|---|---|
| recency: szükséges bit | 3,3 | 3,3 | 3,3 | 3,3 | 3,3 |
| wms: szükséges bit | 6,6 | 10,0 | 13,3 | 19,9 | > 23 |
| **ARLC: szükséges bit** | 6,6 | 10,0 | 13,3 | 19,9 | > 23 |

- Az erős állítás elfogadásához szükséges hitelesség kb. **3,3 bittel nő ellenpéldánként.**
  N = 8-nál már a 0,9999999-es hitelesség sem elég.
- **Az ARLC itt azonos a `wms`-sel.** Az ütköző tények elutasítása uralja a költséget, a
  tömörítési tagnak nincs szerepe.
- **Tanulság a célra nézve:** „egyetlen erős élmény átrendez” csak akkor igaz, ha kevés a
  közvetlen ellenpélda. Sok ellenpéldánál a rendszer kivételt tesz, vagy elutasít. Ez
  pontosan a 7. kör K\* követelménye.

### E3 – Kontextus-szétválasztás vagy elutasítás?

| c_ctx (bit) | rendszerszerű ütközés | zajos forrás |
|---|---|---|
| 6 | szétválaszt ✔ | **szétválaszt ✘** (globálisan semmit nem tud) |
| 9 | szétválaszt ✔ | elutasít ✔ |
| 12 | **elutasít ✘** | elutasít ✔ |
| 16 | elutasít ✘ | elutasít ✔ |

- **Csak egy szűk tartományban (kb. c_ctx = 9) helyes mindkét döntés.** Ez az érték a
  feladat méretétől (8 entitás) függ. Egy hangolt paraméter, nem elv.
- **Az ok:** rögzített forrás-hitelesség mellett a pontszám nem tudja, hogy a B forrás
  *rendszerszerűen* vagy *véletlenszerűen* tér el. Ez ugyanaz a probléma, mint a 12. kör
  plaszticitás–robusztusság kérdése: kell a tanult forrás-megbízhatóság (V2).
- **Mélyebb gond:** egy rendszerszerűen ellentétes forrás két, tömörítés szempontjából
  egyenértékű magyarázatot enged: „más kontextusról beszél” vagy „mindig hazudik”. Ezt az adat
  önmagában nem dönti el. Ez a 13. kör aktív kérdezésének (A-ötlet) tipikus esete.

### E4 – Zaj, meglepetés nélkül (5 seed, kb. 130 megfigyelés)

| ε | recency hamis átrend./50 | wms | **ARLC** | pontosság: recency / wms / **ARLC** |
|---|---|---|---|---|
| 0 | 0 | 0 | **0** | 1,00 / 1,00 / **1,00** |
| 0,02 | 0,30 | 0,08 | **0,08** | 0,96 / 0,96 / **0,97** |
| 0,05 | **1,44** | 0,08 | **0,08** | 0,88 / 0,84 / **0,95** |
| 0,10 | 1,74 | 0,30 | **0,23** | 0,87 / 0,83 / **0,94** |

- **Az R3 kritérium (ε = 0,05 mellett legfeljebb 1 hamis átrendezés 50 megfigyelésenként)
  az ARLC-nél teljesül (0,08), a `recency`-nél nem (1,44).**
- Az ARLC pontossága zajban 10–11 ponttal jobb a `wms`-nél. Az ok valószínűleg az, hogy a
  tömörítési tag megvédi azokat a tagságokat, amelyek sok megfigyelt tényt jósolnak, míg a
  `wms` ezeket ugyanolyan olcsón eldobja, mint bármit.
- **Megszorítás:** a zaj itt független és egyenletes. Az 1. fázis szerint a valódi grounding-hiba
  korrelált (parafrázisok, rokon fogalmak). Ez kedvezőtlenebb eset, és még nem teszteltük.

### A5 – Hiszterézis

| η | lecsengés | tartózkodás 0 | tartózkodás 3 | tartózkodás 10 |
|---|---|---|---|---|
| 0 | – | +1 (holtverseny) | +1 | +1 |
| 0,2 | nincs (1,0) | **−5** | −3 | 0 |
| 0,2 | 0,9 | −3 | −1 | **+1** |
| 0,4 | nincs | **−17** | −12 | 0 |
| 0,4 | 0,7 | −1 | 0 | **+1** |

(hiszterézis = visszaváltáshoz szükséges többlet mínusz odaváltáshoz szükséges többlet)

- **A 11. kör jóslata, hogy a használatfüggő beágyazottság hiszterézist ad, így nem
  igaz.** Lecsengés nélkül az ellenkezője történik: **elsőbbségi hatás.** A régi séma hosszú
  uralma alatt felgyűlt használat a visszaváltást *könnyebbé* teszi (−5, −17).
- Gyenge, pozitív hiszterézis (+1) csak akkor jelenik meg, ha a használat lecseng, **és** az új
  séma egy ideig uralmon van (tartózkodás 10).
- **Új, cáfolható jóslat a 11. kör helyett:** a hiszterézis szélessége a tartózkodási időtől
  függ. Ez a csúcskatasztrófa-modellben nincs benne. Ha az LLM-oldali kísérletben (B4) a
  hiszterézis nem függ a tartózkodástól, akkor az ARLC és az LLM másként viselkedik.

### A7 – Frissítés vs. revízió

| Mód | lakhely most | lakhely a múltban | kategória most | kategória a múltban |
|---|---|---|---|---|
| recency | 1,0 | **0,0** | 1,0 | 1,0 |
| wms | 0,2 | 0,8 | 1,0 | 1,0 |
| arlc-nocut | 0,2 | 0,8 | 1,0 | 1,0 |
| **ARLC** | **1,0** | **1,0** | **1,0** | **1,0** |

- Az ARLC a lakhelyet *frissíti* (5 vágás), a kategóriát *revideálja*, és mindkét időpontra
  helyesen válaszol. Ez a 13. kör U-ötletének első igazolása.
- **Megszorítás:** a változékonysági priort (`π`) orákulumként kaptuk meg. A 13. kör szerint
  ezt az LLM-től kellene kérdezni. Ez a B fázis feladata.

## Összegzés

| Állítás | Állapot |
|---|---|
| A szimbolikus mag globálisan átrendez, kollaterális kár nélkül | **igazolva** (E1), szimbolikus bemeneten |
| Az ARLC többet ad, mint a súlyozott MaxSAT (R2) | **részben**: alosztály-csere (E1), anomália-tűrés (E2a), zajtűrés (E4). Az egyszerű átkategorizálásban és az erős állításnál (E2b) nincs különbség. |
| Az ellenállás a beágyazottsággal arányos (R4) | **igazolva**, de lineárisan, nem csúcskatasztrófa-szerűen |
| Kontextus-szétválasztás helyesen | **nem**: hangolt paramétertől függ. Tanult forrás-megbízhatóság kell. |
| Hiszterézis használatból | **cáfolva** az eredeti formában; lecsengés és tartózkodás kell hozzá |
| Frissítés vs. revízió | **igazolva** orákulum-priorral |

**Mi nem következik ebből:** semmi a fagyasztott LLM-ről. Ez a kör az R2, R3 és R4 kritériumot
teszteli a szimbolikus félen. Az R0, R1 és R5 (a „neuro” fél) továbbra is nyitott.

## Következő lépések

1. Tanult forrás-megbízhatóság (12. kör V2), és az E3 újrafuttatása vele.
2. Korrelált zaj az E4-ben (rokon kategóriák összetévesztése).
3. A TFB-benchmark (9. kör) szimbolikus generátora.
4. E5: ellenséges injektálás (12. kör).
