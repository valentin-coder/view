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

*(a futtatás után)*
