"""A B fázis egylépéses futtatója.

    python -m bphase.run_all --model Qwen/Qwen2.5-0.5B --out runs/qwen05 --layer 12
    python -m bphase.run_all --smoke --out runs/smoke      # véletlen súlyú mini modell, csak kódellenőrzés

A KTP pilot külön fut: experiments/ktp (python -m ktp.run all --model ...).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import torch

from . import tasks as T

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ktp"))
from ktp.core import load_model, prepare  # noqa: E402


def tiny(seed=0):
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast, Qwen2Config, Qwen2ForCausalLM
    texts = [s.text for s in T.statements(seed)[:4000]] + [s.text for s in T.statements(seed, True)[:4000]]
    texts += [T.D.FEWSHOT, "Source says the is a . Question: Answer: Yes No"]
    for e in T.D.build_entities(seed).values():
        texts += [e.name] + [r.text for r in T.D.render_neutral(e.name)]
    for p in T.D.PROPERTIES.values():
        texts += [p[0], p[1], p[2]]
    texts += T.D.CATEGORIES
    words = sorted({w for t in texts for w in re.findall(r"\w+|[^\w\s]+", t)})
    vocab = {"[PAD]": 0, "[UNK]": 1, "[EOS]": 2}
    for w in words:
        vocab.setdefault(w, len(vocab))
    tk = Tokenizer(models.WordLevel(vocab, unk_token="[UNK]"))
    tk.pre_tokenizer = pre_tokenizers.Whitespace()
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, pad_token="[PAD]", unk_token="[UNK]", eos_token="[EOS]")
    torch.manual_seed(seed)
    cfg = Qwen2Config(vocab_size=len(vocab), hidden_size=64, intermediate_size=128, num_hidden_layers=4,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=512)
    return prepare(Qwen2ForCausalLM(cfg).eval(), tok)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B")
    ap.add_argument("--out", default="runs/bphase")
    ap.add_argument("--layer", type=int, default=None, help="ISZB réteg (alapból a KTP sweep választása vagy L/2)")
    ap.add_argument("--n-max", type=int, default=3000)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--random-init", action="store_true",
                    help="kontroll: ugyanaz az architektúra véletlen súlyokkal (Hewitt–Liang-típusú kontroll)")
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.smoke:
        model, tok = tiny()
    elif a.random_init:
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
        torch.manual_seed(0)
        model = AutoModelForCausalLM.from_config(AutoConfig.from_pretrained(a.model)).eval()
        model, tok = prepare(model, AutoTokenizer.from_pretrained(a.model))
    else:
        model, tok = load_model(a.model)
    L = len(T.get_layers(model))
    layer = a.layer if a.layer is not None else L // 2
    res = {"model": "TINY-RANDOM (smoke)" if a.smoke else a.model + (" [VÉLETLEN SÚLYOK]" if a.random_init else ""),
           "layer": layer}
    t0 = time.time()
    res["E0_CTX"] = T.e0_and_ctx(model, tok, n_max=600 if a.smoke else a.n_max)
    print("E0/CTX kész", round(time.time() - t0), "s", flush=True)
    res["SRC"] = T.src_task(model, tok, n_max=600 if a.smoke else a.n_max)   # 61. kör: forrástípus
    print("SRC kész", round(time.time() - t0), "s", flush=True)
    res["ISZB"] = T.iszb(model, tok, layer)
    print("ISZB kész", round(time.time() - t0), "s", flush=True)
    res["B4"] = T.hysteresis(model, tok)
    print("B4 kész", round(time.time() - t0), "s", flush=True)
    (out / "results.json").write_text(json.dumps(res, indent=1, default=float))
    # rövid összefoglaló
    ctx = res["E0_CTX"]["CTX"]["fikció vs. tény (kitartott forráskifejezés)"]
    for f in ("aktiváció", "statikus", "BoW"):
        print(f"kontextus-jel [{f}]: mondatszintű AUC {ctx[f].get('auc'):.3f}; kifejezésszintű AUC "
              f"{ctx[f].get('kifejezésszintű_auc'):.3f} ({ctx[f].get('kifejezések_száma')} kifejezés, "
              f"p = {ctx[f].get('permutációs_p'):.3f}); a 21. kör küszöbe 0.95")
    src = res["SRC"]
    for f in ("aktiváció", "statikus", "BoW"):
        print(f"forrástípus [{f}]: 4 osztály (kifejezésszintű) {src[f]['kifejezésszintű_4_osztály_acc']:.3f}; "
              f"gondozott AUC {src[f]['gondozott_kifejezésszintű_auc']:.3f} (p = {src[f]['permutációs_p']:.3f})")
    iia = [r["iia"] for r in res["ISZB"]]
    pc = [r["prompt_correct"] for r in res["ISZB"]]
    print(f"ISZB: átlagos IIA {sum(iia) / len(iia):.3f}; promptolás helyes {sum(pc) / len(pc):.3f}")


if __name__ == "__main__":
    main()
