# KTP – kategória-transzplantációs pilot

A 6. körben megtervezett kísérlet (`docs/neuroszimbolikus-architektura.md` és a beszélgetés
6. köre) futtatható megvalósítása. A kérdés: ha a szimbolikus réteg elrendeli, hogy
„a rigó mostantól hal”, és ezt zárt alakú, gradiens nélküli beavatkozással beírjuk a
fagyasztott LLM reziduális áramába, akkor **maga az LLM** számolja-e ki a következményeket,
jobban, mint a kontextus-injektálás (B1) vagy a kérdés-átírás (B2)?

## Állapot

- **A kód kész és a smoke teszten végigfut** (véletlen súlyú, 4 rétegű mini Qwen2 modell,
  kb. 30 s). A smoke teszt csak a mechanikát igazolja: a nulla beavatkozás nem változtat
  a kimeneten, a nem nulla igen, és az említések tokenpozíciói helyesek. A számai
  értelmetlenek.
- **Valódi modellen még nem futott.** A modell súlyai a Hugging Face-ről jönnének, ezt a
  futtató környezet hálózati szabálya jelenleg tiltja. Ehhez engedélyezni kell:
  `huggingface.co`, valamint a letöltési CDN-eket (`cdn-lfs.hf.co`, `cdn-lfs-us-1.hf.co`,
  `cas-bridge.xethub.hf.co`, `cas-server.xethub.hf.co`, `transfer.xethub.hf.co`).

## Futtatás

```bash
python -m venv .venv && .venv/bin/pip install torch transformers numpy scipy tokenizers
cd experiments/ktp

# kódellenőrzés modell nélkül
../../.venv/bin/python -m ktp.run smoke --out runs/smoke

# a teljes pilot (szűrő -> sweep -> előregisztráció -> teszt -> riport)
../../.venv/bin/python -m ktp.run all --model Qwen/Qwen2.5-0.5B --out runs/qwen05
# alsó becslés és tartalék
../../.venv/bin/python -m ktp.run all --model gpt2 --out runs/gpt2
../../.venv/bin/python -m ktp.run all --model Qwen/Qwen2.5-1.5B --out runs/qwen15
```

Lépésenként is futtatható: `filter`, `sweep` (ez írja a `preregistration.json`-t), `test`,
`report`. A `test` lépés megtagadja a futást, ha a kód a preregisztráció óta megváltozott
(kód-hash), hacsak nincs `--force`. Ilyenkor a teszt nem számít előregisztráltnak.

Várható futásidő 4 CPU-magon, Qwen2.5-0.5B-vel: nagyságrendileg fél–egy óra. Ezt még
egyetlen valódi futás sem mérte.

## Kimenetek (`--out` mappa)

| Fájl | Tartalom |
|---|---|
| `sweep.json` | a fejlesztési halmaz szűrője és a teljes réteg×mód×módszer sweep (leíró adat) |
| `preregistration.json` | a teszt előtt rögzített konfiguráció, küszöbök, seed, kód-hash |
| `test_rows.json` | minden tesztkérdés minden feltétel alatti margója (`m = logit(Yes) − logit(No)`) |
| `analysis.json`, `report.md` | mérőszámok, bootstrap, Wilcoxon, hipotézisek, a döntési fa ítélete |

## Felépítés

- `ktp/data.py` – a „Valós kategória”-világ: 6 kategória × 15 entitás (5 μ-becslésre,
  5 fejlesztésre, 5 tesztre, seed szerint keverve), 17 kategória-tulajdonság, egyéni
  tulajdonságok (szín, méret), kérdéstípusok (D, S1, S2, I, T), promptok a B0–B3
  feltételekhez.
- `ktp/core.py` – batch-elt igen/nem margó, rétegenkénti szubjektum-reprezentáció, és a
  hook, amely a kiválasztott réteg kimenetébe ír (`add`: T1; `replace`: T2, a kategória-altér
  cseréje; opcionálisan normamegtartással).
- `ktp/stats.py` – RR, CR, CR_T, F; entitás szerint klaszterezett bootstrap; Wilcoxon.
- `ktp/run.py` – a lépések, a feltételek (B0–B3, T, T_other, T_norm, T±1 réteg, C1–C4),
  a hipotézisek és a döntési fa, valamint a smoke teszt.

## Eltérések a 6. kör tervétől (őszintén)

1. **LDA helyett a centrált kategóriaátlagok altere.** A μ-mintán kevesebb a minta, mint
   a dimenzió, ezért az osztályon belüli szórásmátrix szinguláris. A T2 a 6 kategóriaátlag
   által kifeszített, legfeljebb 5 dimenziós alteret cseréli.
2. **A B2 minden említést átír, az előzménymondatban is.** Ezzel a névmásos (I) kérdésekre
   is működik. **A tervben a H5 azon állt, hogy az átírás a névmásnál elbukik. Ez így nem
   igaz,** ha az entitás neve szerepel a kontextusban. Mindkét módszer csak akkor bukna el,
   ha az entitás név nélkül, leírással szerepelne, ezt viszont a transzplantáció sem
   tudja kezelni, mert nincs mit patchelni. A H5 ezért valószínűleg elbukik, és a
   transzplantáció valódi megkülönböztető ereje az egyéni tulajdonságok megtartása (S2)
   marad.
3. **A C5 (Patchscope-dekódolás) nincs megvalósítva.** Csak diagnosztika volt, nem
   kritérium.
4. **Célkategóriák.** A közeli/távoli pár helyett minden entitás mind az 5 másik
   kategóriába átkerül (150 tesztszerkesztés a szűrő előtt). A riport a párok típusa
   szerint (állat–állat, tartományközi, tárgy–tárgy) bontja az eredményt.
5. **A C4 (szivárgás) mindig T1-típusú különbségvektorral fut.** T2 esetén α = 1-gyel,
   mert a szivárgás csak a μ_régi-n keresztül értelmezhető.
6. **Kézzel írt tények, ellenőrzés nélkül.** Az entitásokat, színeket, méreteket és
   kategória-tulajdonságokat én írtam. A biztosíték a tudásszűrő: amit a szerkesztetlen
   modell nem tud, az kiesik. Ismert gyenge pontok: a `fly` és a `cricket` többértelmű;
   az `orange` szín és gyümölcs is; a `seeds` kérdés a kókusznál és az avokádónál vitatható;
   és az „entitás vagy kategória” határok néhol elmosódnak (bálna nincs, de a `bison`
   szőrös?).
7. **A szemantika rögzített, nem validált.** Az, hogy átkategorizáláskor a szín és a méret
   megmarad, a játékvilág definíciója. Emberi annotációval még nem ellenőriztük.
