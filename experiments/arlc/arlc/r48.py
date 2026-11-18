"""48. kör: keverék-prior az elmélet-megbízhatóságra és deklarált hitelesség szerinti csoportok.
Az ellenőrző csomag (v4.battery) a változatokra."""
from __future__ import annotations

import json
import os
import sys
import time

from . import v4 as V4

VARIANTS = {
    "v4 (befagyasztott)": {},
    "v4.2 (3. hiba javítva)": dict(V4.V42_OVERRIDES),
    "v4.2 + keverék-prior": {**V4.V42_OVERRIDES, "theory_mix": V4.MIX},
    "v4.2 + q-csoportok": {**V4.V42_OVERRIDES, "q_groups": True},
    "v4.2 + szigorú specifikusság": {**V4.V42_OVERRIDES, "strict_specificity": True},
    "v5 jelölt (mind a négy, nem kalibrált keverék)": {**V4.V5_OVERRIDES, "theory_mix": V4.MIX},
    "v4.2 + kalibrált keverék": {**V4.V42_OVERRIDES, "theory_mix": V4.MIX_CAL},
    "v5 jelölt (kalibrált keverék)": dict(V4.V5_OVERRIDES),
    "v4.3 + keverék π=0,99": {**V4.V43_OVERRIDES, "theory_mix": V4.MIX_CAL99},
    "v4.3 + keverék π=0,999": {**V4.V43_OVERRIDES, "theory_mix": V4.MIX_CAL999},
    "v4.4 (+ automatikus specifikusság)": dict(V4.V44_OVERRIDES),
    "v4.4 egyszintű (κ_T nélkül)": {**V4.V44_OVERRIDES, "theory_kappa": None},
    "v4.5 egyszintű (+ kontextus-elsőbbség)": {**V4.V45_OVERRIDES, "theory_kappa": None},
    "v5 − keverék-prior": {k: v for k, v in V4.V5_OVERRIDES.items() if k != "theory_mix"},
}


def main(out_path, only=None):
    import os as _os
    rows = json.load(open(out_path)) if (only and _os.path.exists(out_path)) else {}
    for name, ov in VARIANTS.items():
        if only and name not in only:
            continue
        t0 = time.time()
        with V4.configured(ov) as cfg:
            rows[name] = V4.battery(cfg)
        rows[name]["_seconds"] = time.time() - t0
        print(name, json.dumps(rows[name], ensure_ascii=False, default=float), flush=True)
        json.dump(rows, open(out_path, "w"), ensure_ascii=False, indent=1, default=float)


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "..", "results", "kor-48", "battery.json")
    main(path, only=sys.argv[1:] or None)
