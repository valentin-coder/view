# 117. kör – A másolásfelismerés javítása és gyorsítása (előregisztrált)

## 1. rész: fejlesztés és előregisztráció (a futtatás előtt commitolva)

### A két probléma (116. kör)

1. **Másolási kör:** a G5 háttérbeli függőségi hálózatában a végső hipotézisek 73%-ában a másolási reláció körös (o3 → c1 →
   c2 → o3), így az eredeti forrás állításai is elnyelődnek.
2. **Futási idő:** a FROZEN_115 a G5-ön esetenként 16–27 perc (40–60× lassabb a FROZEN_91-nél).

### Fejlesztési lépések (a G5 42000–42003 seedjein, a részleges új másoló típuson; nem teszt)

| változtatás | idő/eset | pre | target | észlelt másolások (példa) |
|---|---|---|---|---|
| FROZEN_91 (referencia) | 21–66 s | 0,867 / 0,867 / 0,922 / 0,922 | 0,575 (átlag) | – |
| FROZEN_115 (42000, hazug) | 1127 s | 0,778 | – | kör |
| + aciklikus gráf (`copy_acyclic`) | 1034 s | 0,822 | – | c1←o3, c2←c1 |
| + legalább 3 közös állítás, egyszeri újraindítás (`copy_min_shared`, `reseed_once`) | 160–243 s | 0,833 / 0,778 / 0,933 / 0,956 | 0,575 | néha fordított irány (c1←c2, o3←partial) |
| + időrend (`copy_time_order`: a másoló nem előzheti meg az eredetit) | 135–195 s | ugyanaz | 0,575 | partial←o3 helyes; az azonos idejű c1/c2 kétértelmű |
| **+ csak új forrás részvételével (`copy_new_only`)** | **55–113 s** | 0,867 / 0,867 / 0,922 / 0,867 | **0,675** | partial←o3 |

**Tanulság:** a háttérben lévő, bevált források közötti másolási láncok elnyelése ezeken a seedeken többet árt (a 0,7-es
o3 egyetlen tanúja marad), mint használ. A 112. kör igazolt esete (egy *új* forrás másol egy bevált forrást) viszont
megmarad. **Az F115_N** (FROZEN_115 + a fenti öt kapcsoló) a jelölt. Minden kapcsoló kikapcsolva bitre azonos
(ekvivalencia: EGYEZIK).

### Előregisztráció

Kód: [`run_r117.py`](../../experiments/arlc/arlc/run_r117.py).
- **G5** (3 típus, 44000–44014): FROZEN_91 vs. F115_N. A FROZEN_115 a G5-ön használhatatlanul lassú, és a 116. kör már mérte.
- **G4 bevált másoló** (44100–44119): FROZEN_115 vs. F115_N.
- **A 107. kör esetei** (a 9 alaptípus + G3 szabályváltozás + G1k szabály-helyesbítés, 44200–44211): FROZEN_115 vs. F115_N.
- **Feladatcsomag:** FROZEN_115, F115_N.

**Hipotézisek:**
- **H117a (G5 részleges másoló, target):** F115_N − FROZEN_91 > 0, a CI nem tartalmazza a nullát.
- **H117b (G5, pre):** F115_N − FROZEN_91 ≥ −0,01 (pontbecslés).
- **H117c (G4 bevált másoló, a hibás részhalmaz a meglepetés után):** F115_N − FROZEN_115 ≥ −0,05 (pontbecslés).
- **H117d (a 107. kör esetei):** post-acc: F115_N − FROZEN_115 ≥ −0,01 mind a négy generátoron; G3 szabályváltozás
  target: ≥ −0,05 (pontbecslés).
- **H117e (sebesség, a 107. kör esetein):** az F115_N átlagos ideje ≤ a FROZEN_115-é.
- **H117f (feladatcsomag):** egyetlen pontossági tétel sem rosszabb 0,05-nél többel.

**Döntési szabály:** ha mind teljesül, az F115_N lesz az új befagyasztott konfiguráció (FROZEN_117).
