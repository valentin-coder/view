# 23. kör – Saját, fagyasztott mini-LM: ad-e az aktiváció többet a felszíni szavaknál?

## Miért

A B fázis (minden, ami valódi LLM-ről szól) hálózati okból blokkolt. A 22. kör 1. ötlete: egy
kis transzformert CPU-n betanítunk egy szintetikus korpuszon, befagyasztjuk, és a „neuro” fél
kísérleteit ezen futtatjuk. **Megvalósíthatósági próba, nem valódi LLM-eredmény.**

Megvalósítás: [`experiments/minilm/`](../../experiments/minilm/); nyers eredmények:
[`experiments/minilm/results/r23/results.json`](../../experiments/minilm/results/r23/results.json).

## Elrendezés

- **Világ:** 6 kitalált kategória, 8 tulajdonság, 60 entitás, két kontextus (észak/dél).
  Kategóriánként egy tulajdonság kontextusfüggő.
- **Források:** kontextusonként 4 forrásnév. A kontextus csak a mondatok 30%-ában szerepel
  explicit szóval („in the north , …”), máskor csak a forrás neve vagy a tartalom árulja el.
- **Mondatok:** tagság, tény, általános állítás. Típusonként 7 parafrázis-sablon, ebből 5 a
  probe-tanításé, 2 kitartott.
- **„Előtanítás”:** 40 000 mondat, minden sablonnal és forrással. Kis GPT: 3 réteg, d = 128,
  0,64M paraméter, 1500 lépés, 41 s CPU-n. Utána befagyasztva.
- **Probe-ok:** lineáris (logisztikus regresszió) a mondat utolsó tokenjének aktivációján,
  rétegválasztással. Két teszthalmaz:
  - *kitartott sablon:* a probe által nem látott parafrázisok;
  - *kitartott forrás:* a probe által nem látott forrásnevek (az LM előtanításban látta őket).
- **Alapvonalak:**
  - BoW a probe-tanító adaton (az 1. fázis K2 kontrollja);
  - **távoli felügyeletű BoW (BoW-DS):** ugyanazon az előtanító korpuszon, címkéje az explicit
    kontextus-kifejezés, amelyet a jellemzőkből kivágunk. Ez azt méri, kinyerhető-e ugyanaz
    az információ LM nélkül, puszta együttes előfordulásból.

## Eredmények (pontosság; bináris feladatoknál AUC zárójelben)

| Feladat | teszthalmaz | aktiváció | BoW | BoW-DS |
|---|---|---|---|---|
| kontextus (explicit szó nélkül) | kitartott sablon | 0,92 (0,99) | **1,00** (1,00) | **1,00** (1,00) |
| kontextus (explicit szó nélkül) | **kitartott forrás** | **0,995 (0,9999)** | 0,49 (0,47) | **1,00 (1,00)** |
| polaritás | kitartott sablon | 0,63 (0,70) | **0,77** (0,95) | – |
| polaritás | kitartott forrás | 0,95 (0,99) | **1,00** | – |
| mondattípus | kitartott sablon | 0,83 | **0,90** | – |
| tárgy | kitartott sablon | 0,87 | **1,00** | – |

## Értelmezés

1. **Az első benyomás félrevezető volt.** Új forrásnevekre a kontextus az aktivációkból szinte
   tökéletesen kiolvasható (AUC 0,9999), a BoW-ból nem (0,47). Ez úgy néz ki, mint az LLM
   hozzáadott értéke: az „előtanításból” tudja, melyik forrás hova tartozik.
2. **A tisztességes kontroll ezt eltünteti.** A távoli felügyeletű BoW, amely ugyanazt a
   korpuszt látja, de nincs benne neurális háló, AUC 1,0-t ér el. **Az LM előnye teljes egészében
   együttes-előfordulási statisztika**, LM nélkül is reprodukálható.
3. **A literálkinyerésben (polaritás, típus, tárgy) a BoW mindenhol jobb.** A sablonos
   mondatokban a felszíni szavak elegendők. A lineáris probe az utolsó token aktivációján ezt
   nem éri el.

## Mit jelent ez, és mit nem

- **Nem jelenti**, hogy valódi LLM-ek aktivációi nem adnak többet. Egy valódi LLM kompozicionális
  és világtudást kódol, amit egy sablonos játékvilág nem tud előhívni. **Ez a kísérlet a valódi
  kérdést nem tudja eldönteni.**
- **Jelenti** a következő módszertani követelményt a B fázisra:

> **A K2 kontroll (BoW a probe-adaton) nem elég. Minden „az aktivációk többet tudnak”
> állítás mellé kell egy olyan alapvonal, amely ugyanahhoz az *előtanító* adathoz fér hozzá
> neurális háló nélkül.** Valódi LLM-nél ez nem a teljes előtanító korpusz (az nem
> elérhető), hanem például egy nagy, nyilvános korpuszon számolt együttes-előfordulási vagy
> statikus szóbeágyazásos (word2vec/GloVe) alapvonal. Ha az LLM-aktiváció ezt nem veri meg,
> akkor az előnye nem a „nyelvi modell” jellegéből fakad.

- **A csővezeték működik:** tanítás, befagyasztás, aktivációk, probe-ok, alapvonalak. Valódi
  modellre egy-az-egyben átvihető.

## Következő lépés

A mini-LM-et úgy kell átalakítani, hogy a BoW-DS-t *elvben* ne lehessen elérni. Például olyan
kontextus-információval, amely csak kompozícióból következik (két mondat együtt árulja el a
kontextust, külön egyik sem). Ha az aktiváció *ott* sem jobb, a „neuro” fél ebben a keretben
reménytelen. Ez a 24. kör.
