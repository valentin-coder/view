# Mini-LM – saját, fagyasztott kis nyelvi modell (23. kör)

A B fázis (valódi LLM) hálózati okból blokkolt. Ez a mappa egy CPU-n betanított, majd
befagyasztott kis GPT-n futtatja a „neuro” fél kísérleteit egy szintetikus korpuszon.
Megvalósíthatósági próba, valódi LLM-ről nem mond semmit. Értelmezés: `docs/korok/23-mini-lm.md`.

```bash
cd experiments/minilm
OMP_NUM_THREADS=4 python -m minilm.probe_exp --out results/r23 --steps 1500 --n-pretrain 40000   # kb. 1–2 perc
```

- `minilm/corpus.py` – kétkontextusú Nonce-világ, források, parafrázis-sablonok (kitartottakkal).
- `minilm/model.py` – kis GPT (3 réteg, d = 128), tanítás, befagyasztás, rétegenkénti aktivációk.
- `minilm/probe_exp.py` – lineáris probe-ok az aktivációkon; BoW és távoli felügyeletű BoW alapvonal.
