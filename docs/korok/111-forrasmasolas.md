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

## 2. rész: eredmények

Nyers adat: [`results/kor-111/test/`](../../experiments/arlc/results/kor-111/test/); elemzés:
[`analyze_r111.py`](../../experiments/arlc/arlc/analyze_r111.py) → `results/kor-111/analysis.json`. 120 futás; mind a 20 seedben
volt hibás f4-jelentés a célkérdések között.

**Pontosság a hibás részhalmazon** (ahol az f4 hibásan jelentett), a meglepetés előtt → után:

| | bevált másoló | független megerősítő | az új forrás félretett állításai (másoló / megerősítő) |
|---|---|---|---|
| v3 | 0,62 → **0,00** (−0,62) | 0,62 → 0,87 (+0,25) | 0 / 0,45 |
| FROZEN_91 | 0,59 → **0,00** (−0,59) | 0,59 → 0,77 (+0,18) | 0 / 2,3 |
| F91_Q | 0,80 → 0,41 (**−0,39**) | 0,80 → **0,97** (+0,17) | 4,1 / 0,15 |

| hipotézis | eredmény | ítélet |
|---|---|---|
| **H111a:** FROZEN_91 esése ≥ 0,1 | −0,59 | **teljesül** |
| **H111b:** a megerősítő után nő (mindhárom) | +0,25; +0,18; +0,17 | **teljesül** |
| **H111c:** FROZEN_91 esése ≤ v3 esése | 0,59 ≤ 0,62 | **teljesül** (épphogy) |
| **H111d:** F91_Q esése ≤ FROZEN_91 esése | 0,39 ≤ 0,59 | **teljesül** |

### Értelmezés

1. **A függetlenségi feltevés megsértése a sorozat legsúlyosabb mért sebezhetősége.** Ha egy új forrás egy bevált
   forrás hibáit ismétli, a v3 és a FROZEN_91 is **minden** érintett kérdésben a hibás értékre vált (0,00). A másoló
   egyetlen állítását sem teszi félre. **Az N prior itt nem segít,** mert a másoló állításai egy bevált forrással
   *egyeznek*: nem ütköznek semmivel, amit a rendszer elfogad, és a két „független” forrás együtt legyőzi a szabályt.
2. **Az óvatos hitelesség (F91_Q) részben ellenáll** (az érintett kérdések 41%-a marad helyes, és a másoló állításainak
   kb. 40%-át félreteszi), mert a forrásokat eleve kevésbé hiszi, és a szabályok relatíve erősebbek. Ez a 102. kör óvatos
   változatának újabb érve.
3. **Ismert probléma, ismert irodalommal.** Az igazság-felderítésben a forrásfüggőség felismerése (Dong, Berti-Équille és
   Srivastava, 2009: „Integrating conflicting data: the role of source dependence”) arra épül, hogy **a hamis értékekben való
   egyezés erős bizonyíték a másolásra.** Két független forrás ritkán téved ugyanabban, egy másoló mindig. Ez az ARLC-ben
   egy új hipotézis-komponens volna: „s₂ az s₁ másolata”. Ekkor s₂ állításai nem számítanak külön bizonyítéknak.
4. A sorozat végén ez a forrás-modell utolsó, eddig nem mért feltevése volt, és **itt a modell elvi korlátja mutatkozott
   meg,** nem egy hangolási kérdés.
