# 108. kör – Reprodukálhatósági pillanatkép

Ez a kör nem mér semmit. Összegyűjti, mi van a kódban, mi melyik körből jön, és hogyan futtatható újra.

## 1. Megnevezett konfigurációk (`experiments/arlc/arlc/v4.py`)

| név | tartalom | státusz | kör |
|---|---|---|---|
| `V44E_OVERRIDES` | v4.4e: béta-megbízhatóság (κ = 30), kivétel-prior, specifikusság, osztálykivétel, q-csoportok, feltalálás | régi alap | 50 |
| `FROZEN_88` | + tankönyv-keverék (π metaadatból) + PK + N | **elvetve** (G3-on a v3 alatt; az E1-et elrontja) | 88, 92 |
| **`FROZEN_91`** | `FROZEN_88` + hibrid megbízhatóság + eseményenkénti vágásár | alapértelmezés a 91–111. körben („bízó”) | 91, 92 |
| **`F91_Q`** | `FROZEN_91` + óvatos hitelesség ((1 − q) × 2) | **megnevezett alternatíva („óvatos”)** | 102, 105 |
| `F91_DK` | + lassan tanuló bevált forrás (κ = 300) | elvetve | 96 |
| `F91_C` | + megerősítés-függő új-forrás bizalom | elvetve (fejlesztési negatív) | 100 |
| `V5_CORE` | − q-csoport, − indukált kivétel-ár, − forráslépés | elvetve (A7) | 103 |
| `F91_R` | + szabályok időbeli vágása | elvetve (A7) | 107 |
| `source_changepoints` | forrás-változáspont | kikapcsolva (fejlesztési negatív) | 97 |
| `FROZEN_112` (= `F91_D`) | `FROZEN_91` + másolásfelismerés horgony-újraindítással | alapértelmezés a 112–114. körben | 111, 112 |
| **`FROZEN_115`** (= `F112_RO`) | `FROZEN_112` + általános újranyitó keresés + szabály-vágás (frissítés–revízió szemantikával) | **alapértelmezés a 115. kör óta** (kb. 2,5× lassabb) | 107, 115 |

Minden kapcsoló kikapcsolva bitre azonos a korábbi viselkedéssel. Ellenőrzés:
`PYTHONHASHSEED=0 python -m arlc.equiv_check check <referencia.json>` (a referencia a 72. kori kódból mentve).

## 2. Generátorok és érvényességi eszközök

| generátor | modul | megjegyzés |
|---|---|---|
| G1 | `procedural.py` (+ `run_r55.make_case`) | **hibás:** a világok 96%-a ellentmondásos (82., 87. kör); csak a régi eredmények reprodukálásához |
| **G1k** | `g1k.py` | a G1 javítása (85. kör) |
| **G2** | `generator2.py` | kereszt-osztályozás, rejtett prioritás (77. kör) |
| **G3** | `generator3.py` | időben változó világ; `make_case3(seed, kind, upd)`. Az előregisztrált 88. kör upd = 0,05-tel futott (rosszul kalibrált), a későbbiek 0,3-mal |
| **G4** | `generator4.py` | forrásfüggőség és -változás (93. kör) |

| eszköz | modul | mire |
|---|---|---|
| generátor-egységteszt | `gen_check.py` | megengedett-e az igaz hipotézis (87. kör) |
| igaz-hipotézis-ár | `gen_check.admissible(..., return_h=True)`, `true_cost_r87.py` | keresési vagy modellhiba (81. kör) |
| menekülőút-audit | `audit_truth.py` | a félretevések helyessége forrásonként (82. kör) |
| feladatcsomag | `v4.battery` | a korai körök kézi feladatai (92. kör óta a befagyasztás feltétele) |
| bootstrap | `analyze_r44.boot_diff` | világok szerinti klaszteres 95%-os CI |

## 3. A fő előregisztrált mérések újrafuttatása

Minden futtató folytatható (esetenként egy fájl), és az elemző a futtató kimenetéből dolgozik. A munkakönyvtár az
`experiments/arlc`.

| állítás | kör | futtatás | elemzés |
|---|---|---|---|
| a hibrid+V mindhárom generátoron a v3 fölött | 91 | `python -m arlc.run_r91` | `python -m arlc.analyze_r91` |
| megismétlés friss seedeken (négy generátor) | 96 | `python -m arlc.run_r96` | `python -m arlc.analyze_r96` |
| biztonsági ellenőrzés (B, C, feladatcsomag) | 92 | `python -m arlc.run_r92` | `python -m arlc.analyze_r92` |
| negyedik generátor | 93 | `python -m arlc.run_r93` | `python -m arlc.analyze_r93` |
| prior-érzékenység | 101 | `python -m arlc.run_r101` | `python -m arlc.analyze_r101` |
| óvatos hitelesség | 102 | `python -m arlc.run_r102` | `python -m arlc.analyze_r102` |
| generátor-egységteszt | 87 | `python -m arlc.gen_check` | (a kimenet maga) |

A nyers eredmények a `results/kor-NN/` könyvtárakban vannak, commitolva. Egy újrafuttatás ugyanazt adja, mert a seedek
rögzítettek, és a futtatók nem használnak `hash()`-t (66. kör).

## 4. Ami nem reprodukálható

- **A B fázis** (61. kör kódja): futtatatlan, mert a környezetnek nincs hálózata modellt letölteni.
- **Futási idők:** gépfüggők. A G1k-C esetei kb. 150 s, a többi 10–60 s egy magon.
