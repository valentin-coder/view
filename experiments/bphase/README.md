# B fázis – egylépéses futtató valódi modellre (35. kör)

Hálózat (Hugging Face) vagy saját gép kell hozzá. Itt csak véletlen súlyú mini modellen
(smoke) futott.

```bash
pip install torch transformers numpy scipy tokenizers
cd experiments/bphase
python -m bphase.run_all --smoke --out runs/smoke                                  # kódellenőrzés
python -m bphase.run_all --model Qwen/Qwen2.5-0.5B --out runs/qwen05               # valódi modell
python -m bphase.run_all --model Qwen/Qwen2.5-0.5B --random-init --out runs/qwen05-rnd   # KÖTELEZŐ kontroll
cd ../ktp && python -m ktp.run all --model Qwen/Qwen2.5-0.5B --out runs/qwen05     # KTP pilot
```

**Kötelező kontrollok minden állításhoz:**
1. **Véletlen súlyú, azonos architektúrájú modell** (`--random-init`): ha az eredmény ott is
   megvan, nem az előtanításból jön.
2. **Statikus alapvonal:** a modell saját bemeneti beágyazásainak átlaga, kontextus nélkül.
3. **BoW** a probe-tanító adaton.
4. A kontextus-jelnél **kifejezésszintű AUC és permutációs p-érték**: a hatásos mintaméret a
   kitartott kifejezések száma (16), nem a mondatoké.

Feladatok: E0 (literálkinyerés), CTX (kontextus-jel kitartott, lexikailag át nem fedő
forráskifejezésekkel; küszöb 0,95), ISZB (interventív szabálybányászat vs. promptolás), B4
(LLM-oldali hiszterézis). Részletek: `docs/korok/35-b-fazis-csomag.md`.
