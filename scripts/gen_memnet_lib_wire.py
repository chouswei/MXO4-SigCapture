"""Generate MemNet lib wire lines."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src" / "mxo4_sigcapture" / "scpi" / "data" / "manifest.json"
OUT = ROOT / ".memnet" / "lib_wire.txt"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lines = [
        "@MOD: MOD_scpi_lib|src/mxo4_sigcapture/scpi|MXO4 SCPI catalog session recipes|active|persistent",
        "@EDG: E_lib_01|TSK_mxo4_scpi_snap|owns|MOD_scpi_lib|python_lib|persistent",
        "@EDG: E_lib_02|MOD_scpi_lib|implements|IDX_mxo4_scpi_all|catalog|persistent",
    ]
    i = 3
    for topic, text in manifest["conventions"].items():
        lines.append(f"@USR: USR_scpi_conv_{topic}|convention|{text[:180]}|active|persistent")
    for key, rec in manifest["recipes"].items():
        steps = "; ".join(rec["steps"])[:3500]
        content = f"{rec['title']}: {steps}"
        lines.append(f"@USR: USR_recipe_{key}|recipe|{content[:3800]}|active|persistent")
        lines.append(f"@EDG: E_lib_{i:02d}|MOD_scpi_lib|documents|USR_recipe_{key}|howto|persistent")
        i += 1
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT, len(lines))


if __name__ == "__main__":
    main()
