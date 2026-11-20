# 111. kör – Forrásmásolás bevált forrásról: a függetlenségi feltevés próbája (előregisztrált)

## 1. rész: terv és előregisztráció (a futtatás előtt commitolva)

### Miért

Az ARLC a forrásokat függetlennek tekinti: két egyező állítás két független bizonyíték. A 93. kör „visszhang” típusa ezt nem
tesztelte valóban, mert ott a hazug forrás és a másoló is új volt, és mindkettőt egyformán gyanúsnak kezelte a rendszer. A valódi
próba: **egy új forrás egy *bevált* forrás hibáit ismétli.** Ez a sorozat utolsó, még nem mért forrás-modell-feltevése (109.
kör, 5.4).

### A két új G4-típus

Kód: [`generator4.py`](../../experiments/arlc/arlc/generator4.py) (`KINDS4_EXTRA`; a meglévő típusok változatlanok).
- **bevált másoló:** egy új forrás („mirror”) a leggyengébb bevált terepforrás (f4, valódi megbízhatóság 0,65) 10
  jelentését ismétli, köztük legfeljebb 5 hibásat;
- **független megerősítő (kontroll):** egy új forrás ugyanarra a 10 kérdésre a valódi értéket közli.

Egységteszt: mindkét típus 10/10 világban megengedett, a meglepetés előtt és után.

### Mérés

A célkérdések közül azok, ahol az f4 hibásan jelentett („hibás részhalmaz”): a pontosság **a meglepetés előtt és után.**
Seedek 38000–38019 (friss); v3, FROZEN_91, F91_Q. Kód: [`run_r111.py`](../../experiments/arlc/arlc/run_r111.py).

### Hipotézisek

- **H111a (a függetlenség megsértése árt):** a FROZEN_91 pontossága a hibás részhalmazon a bevált másoló után legalább
  0,1-gyel kisebb, mint előtte (pontbecslés).
- **H111b (kontroll):** a független megerősítő után a hibás részhalmaz pontossága nő (pontbecslés), mindhárom módszernél.
- **H111c (az N prior korlátozza a kárt):** a FROZEN_91 esése a bevált másolónál legfeljebb akkora, mint a v3-é (pontbecslés).
- **H111d:** az F91_Q esése legfeljebb akkora, mint a FROZEN_91-é (pontbecslés).
