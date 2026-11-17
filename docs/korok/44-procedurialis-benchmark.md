# 44. kör – Procedurálisan generált, előre rögzített benchmark

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 34. kör szerint a 26–42. kör kilenc új mechanizmust adott a maghoz, mindegyiket a saját,
kézzel tervezett feladatán értékelve. Ez túlillesztés-gyanús. Ez a kör egy olyan benchmarkon
méri a befagyasztott ARLC v4-et, **amelynek a generátorát és az elemzési tervét a futtatás
előtt rögzítem**, és utána sem a generátoron, sem a v4-en nem változtatok.

### A befagyasztott v4

[`experiments/arlc/arlc/v4.py`](../../experiments/arlc/arlc/v4.py), `V4` szótár: tanult
megbízhatóság (κ_S = 30, κ_T = 1), kivétel-prior ε = 0,05, osztályszintű kivétel,
kategória-feltalálás visszavétellel, forrásszintű lépés, kontextusfüggő indukció, teljes
visszahelyezés, helyi becslésű mohó lépés, javítási mélység 2.

### A generátor

[`experiments/arlc/arlc/procedural.py`](../../experiments/arlc/arlc/procedural.py). Eltér a korábbi
kézzel tervezett feladatoktól:
- **véletlen kategória-DAG:** 3 felső, 5 középső, 8 levél kategória; 25% eséllyel két szülő
  (többszörös öröklés, Nixon-gyémántok);
- **szabályok:** kategóriánként 2 véletlen tulajdonság, véletlen előjellel, bármely szinten; az
  igazság **specifikus öröklés** (a legközelebbi szabály dönt; egyforma távolságú ellentmondásnál nem
  definiált, és kimarad);
- **valódi kivételek** (kb. 3% tulajdonságonként);
- **a tankönyv a szabályok 10%-át hibásan közli**; a terepi tények 5%-ban zajosak;
- **30 entitás**, entitásonként 3 megfigyelt tény;
- **meglepetés**, öt típus:
  - átkategorizálás: egy entitás másik levélbe kerül;
  - szabály-helyesbítés: egy *hibásan közölt* tankönyvi szabályt egy ellenőrzés helyesbít, a világ
    nem változik;
  - kivételes alfaj: négy új, „megjelölt” tag, amelyeknél egy öröklés szerint hamis tulajdonság igaz;
  - hazug forrás: 8 hamis tény egy új forrásból;
  - más régió: egy forrás egy másik régióról beszél, ahol egy szabály ellenkező; a helyi igazság nem
    változik.

### Módszerek

`lookup`, `recency`, `wms` (BeliefBank-szerű), `arlc` (a mag alapértelmezése, ez a v3) és `v4`.

### Elemzési terv

- **Világok:** a 1000–1029 seedek, meglepetéstípusonként (5 × 30 = 150 eset), minden módszerrel.
- **Mérőszámok:**
  - *pre-acc:* pontosság a meglepetés előtt, az igazi világhoz mérve (a tankönyvi hibák javítását is méri);
  - *post-acc:* pontosság a meglepetés után, minden definiált kérdésen;
  - *target-acc:* a típusra jellemző célkérdéseken;
  - a meglepetés feldolgozási ideje.
- **Fő végpont:** a post-acc átlaga mind a 150 esetre.
- **Hipotézisek** (95%-os, világok szerinti bootstrap-intervallummal):
  - **H44a:** v4 > wms, legalább 0,02-vel, és a konfidenciaintervallum nem tartalmazza a nullát;
  - **H44b:** v4 > arlc (v3), és a konfidenciaintervallum nem tartalmazza a nullát. **Ha ez nem
    teljesül, a 26–42. kör mechanizmusai ezen a független benchmarkon nem indokoltak**, ezt
    eredményként jelentem, nem hangolok utána;
  - **H44c:** a target-acc típusonként; a v4 a „hazug forrás” és a „más régió” típusban jobb a
    wms-nél (ezeket a tanult megbízhatóság és a forráslépés célozza).
- **Nem változtatok** a generátoron, a v4-en vagy a mérőszámokon az eredmények megtekintése után.
  Ha hibát találok a generátorban, azt külön, a hibával együtt jelentem, és mindkét változat
  eredményét közlöm.

## 2. rész: eredmények

*(a futtatás után kerül ide)*
