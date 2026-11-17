# ARLC – szimbolikus mag és az A fázis kísérletei

A 15. kör specifikációjának megvalósítása (`docs/korok/15-arlc-spec.md`) és a 14. kör A
fázisának kísérletei. LLM nincs a hurokban: a bemenet orákulum-literál, opcionálisan
mesterséges zajjal. Eredmények és értelmezés: `docs/korok/16-a-fazis-eredmenyek.md`.

## Futtatás

```bash
pip install scipy
cd experiments/arlc
python -m arlc.experiments --out results/a-fazis            # minden, kb. 1 perc CPU-n
python -m arlc.experiments --out runs/x --only e1 e4        # csak egyes kísérletek
```

## Felépítés

- `arlc/core.py` – a mag: literálok, szabályok, megfigyelések; hipotézis (elutasítás, kivétel,
  elszigetelés, vágás, indukció); zárás támaszhalmazokkal; konfliktus (példány- és
  szabályszinten); MDL-pontszám; javító keresés (korlátos mélység + mohó befejezés +
  visszahelyezés); nyaláb. Alapvonalak ugyanezen a gépezeten: `lookup`, `recency`, `wms`.
- `arlc/experiments.py` – E1 (propagáció), E2a (anomália-tűrés), E2b (erős általános állítás),
  E3 (kontextus vagy elutasítás), E4 (zaj), A5 (hiszterézis), A7 (frissítés vs. revízió).
- `results/a-fazis/results.json` – az utolsó teljes futás nyers eredményei.
