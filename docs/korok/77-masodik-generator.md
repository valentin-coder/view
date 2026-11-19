# 77. kör – Egy második, független benchmark-generátor (előregisztrált)

## 1. rész: előregisztráció (a futtatás előtt commitolva)

### Miért

A 74. kör szerint a legnagyobb hiányosság, hogy a 44. kör óta minden mérés ugyanabból a procedurális generátorból jön,
amelyre a v4.x kapcsolóit hangoltam. Ez a kör egy **szerkezetében eltérő** generátoron méri a változatokat. **Egyetlen
kapcsolót sem hangolok rá**, sem a futtatás előtt, sem utána.

### A generátor ([`generator2.py`](../../experiments/arlc/arlc/generator2.py))

- **Kereszt-osztályozás, hierarchia nélkül:** 3 család × 3 kategória; minden entitás családonként egy kategóriába
  tartozik. A kategóriák szabályai ütközhetnek, és az igazságot egy **rejtett családprioritás** dönti el. Az ARLC ezt
  nem ismeri: a specifikusság itt nem segít, mert nincs alosztály-reláció.
- **Rosszul kalibrált források:** két terepforrás, mindkettő 0,9-et deklarál, a valódi megbízhatóság 0,97, illetve 0,8.
- **Meglepetések:** hazug forrás (8 hamis tény); tankönyvi szabály helyesbítése; „prioritás-szakértő” (8 helyes érték
  ütköző szabályú entitásokra); „torzított forrás” (egy optimista forrás 10 hamis „igaz” tényt jelent).
- 30 entitás, entitásonként 4 tény; a tankönyv a szabályok 10%-át hibásan közli.

### Elrendezés

Seedek **15000–15019**, 4 típus: 80 eset. Módszerek: wms, v3, v4.4e, v4.8-π (a tankönyv π-je 0,999, „gondozott”). Kód:
[`run_r77.py`](../../experiments/arlc/arlc/run_r77.py).

### Hipotézisek (95%, világok szerinti klaszteres bootstrap)

- **H77a:** v4.8-π − v3 (post-acc) > 0, a CI nem tartalmazza a nullát (a javítások külső érvényessége).
- **H77b:** v4.4e − wms (post-acc) > 0, a CI nem tartalmazza a nullát.
- **H77c:** a „hazug forrás” célkérdésein v4.8-π − v3 > 0 (pontbecslés).
- **H77d (kudarc-jóslat):** a „prioritás-szakértő” célkérdésein mindegyik ARLC-változat target-acc-ja ≤ 0,6, mert a
  rejtett prioritás a modell nyelvén nem fejezhető ki (példánykivételekkel csak darabonként).

**Ha H77a nem teljesül,** a 44–75. kör javításai legalább részben az első generátorra illesztett hatások.

## 2. rész: eredmények

*(a futtatás után)*
