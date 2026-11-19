# 66. kör – Milyen pontos forrástípus-felismerés kell? (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 60. kör legjobb eredménye (a gestalt–stabilitás feszültség feloldása) **orákulum-metaadaton** áll: a π-t a
populáció ismert szemét-arányából kapta a rendszer (64. kör, 3.1). A 61. kör szerint egy LLM a forrás típusát a
szövegből becsülhetné. Ez a kör azt méri, milyen pontosságú becslés kell ahhoz, hogy az eredmény megmaradjon. Ez a
21. kör kontextusjel-követelményének párja a π-re.

### Elrendezés

Kód: [`run_r66.py`](../../experiments/arlc/arlc/run_r66.py).
- **Valódi típus:** A-ban a tankönyv „gondozott” (π = 0,999); C-ben mindkét tankönyv „rivális iskola” (π = 0,5).
- **Szimulált osztályozó:** a pontossággal a valódi típust adja, különben a másik három egyikét. A π a *felismert*
  típusból jön (gondozott 0,999; rivális iskola 0,5; szakértő 0,95; pletyka 0,7). A szintek beágyazottak, és a
  húzás folyamatfüggetlen (crc32).
- **Pontosság:** a ∈ {0,8; 0,9; 1,0}. Téves típusok száma: A-ban 8/30 és 3/30; C-ben 13/60 és 5/60.
- **Seedek 8000–8009** (friss), típusok: átkategorizálás, szabály-helyesbítés, hazug forrás. A és C: 60 eset.
  Alapvonal: v4.4e.

### Hipotézisek

- **H66a (C):** a helyes gestalt-váltások aránya a = 0,9-nél legalább 80%-a az a = 1,0-énak.
- **H66b (C):** a post-acc a = 0,8-nál is nagyobb a v4.4e-énál (világok szerinti bootstrap, a CI nem tartalmazza
  a nullát).
- **H66c (A):** a post-acc a = 0,8-nál legfeljebb 0,01-gyel marad el a v4.4e-étől (pontbecslés).

**Jóslat a mechanizmusra:** a C-ben egy tankönyv téves „gondozott” vagy „szakértő” típusa (π ≥ 0,95) a gestalt-váltást
akadályozza, ha éppen a szemét tankönyvről van szó. Az A-ban a „rivális iskola” téves típus (π = 0,5) a teljes
félretevést olcsóbbá teszi, de a 49. kör szerint ehhez kevés adat vagy sok hiba is kell.

## 2. rész: eredmények

60 eset (A és C, 30–30); nyers adat: [`results/kor-66/`](../../experiments/arlc/results/kor-66/). Eltérés: a konténer
egyszer újraindult (14/30 C-esetnél), a futtató folytatta.

| | C post | C helyes gestalt-váltás | A post | A tankönyv félretéve |
|---|---|---|---|---|
| v4.4e | 0,412 | – | 0,655 | – |
| v4.8-π, a = 0,8 | 0,489 | 13/30 | 0,644 | 12/30 |
| v4.8-π, a = 0,9 | 0,469 | 12/30 | 0,654 | 11/30 |
| v4.8-π, a = 1,0 | 0,519 | 12/30 | 0,660 | 10/30 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H66a (C):** helyes váltás a = 0,9-nél ≥ 80% az a = 1,0-énak | 12 vs. 12 | **teljesül** |
| **H66b (C):** a = 0,8 post > v4.4e | +0,078 [−0,008; +0,170] | **nem teljesül** (irányában igen; 10 seed) |
| **H66c (A):** a = 0,8 post ≥ v4.4e − 0,01 | −0,011 | **épphogy nem teljesül** |

### Értelmezés

1. **Ezen a seed-halmazon a hatás kisebb, mint a 60. körben.** A = 1,0 mellett is csak 12/30 (40%) a helyes gestalt-
   váltás a C-ben (a 60. körben 67/100), és az A-ban a tankönyv 10/30 esetben félretéve (a v4.4e is gyenge: 0,655).
   A 8000-es seedek nehéz világok. Egy 10 seedes kör egy-egy rossz világra érzékeny.
2. **A téves típus nem fokozatosan, hanem esetenként, nagyot rombol.** A C-ben a = 0,9 mellett az 5 tévesen
   osztályozott esetben a post-acc **0,006**, szemben az a = 1,0 mellett mért 0,306-tal: egy szemét tankönyv „gondozott”
   címkével a rendszer a jó tankönyvet veti el. Az A-ban a 8 téves típusú esetből 5-ben nincs hatás, 2-ben esés
   („pletyka” 0,73 → 0,42; „szakértő” 0,69 → 0,51).
3. **Követelmény:** a 0,8–0,9-es forrástípus-pontosság átlagban nagyjából megtartja a hatást, de a tévesen
   osztályozott esetekben katasztrofális lehet. Egy valódi rendszernek a típusbecslés *bizonytalanságát* is
   továbbítania kellene (π a típusok valószínűségével súlyozva), nem a legvalószínűbb típust. Ez a 21. kör
   kontextusjel-tanulságának párja: **egy diszkrét, magabiztos metaadat-hiba nagyobb kárt okoz, mint az
   átlagos pontosság sugallja.**
