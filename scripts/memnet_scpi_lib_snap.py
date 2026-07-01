"""Add SCPI lib layer (recipes, conventions) to MemNet snap."""

from __future__ import annotations

import json
from pathlib import Path

from memnet.serve import send_command

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / ".memnet" / "mxo4_scpi.snap"
MANIFEST = ROOT / "src" / "mxo4_sigcapture" / "scpi" / "data" / "manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    resp = send_command(["session_load", "--file", str(SNAP)])
    if int(resp.get("exit_code", 1)) != 0:
        raise SystemExit(resp.get("stderr"))

    session = "mn_loaded"
    for line in (resp.get("stderr") or "").splitlines():
        if line.startswith("MEMNET_SESSION="):
            session = line.split("=", 1)[1].strip()

    lines = [
        "@MOD: MOD_scpi_lib|src/mxo4_sigcapture/scpi|MXO4 SCPI catalog session recipes|active|persistent",
        "@EDG: E_lib_01|TSK_mxo4_scpi_snap|owns|MOD_scpi_lib|python_lib|persistent",
        "@EDG: E_lib_02|MOD_scpi_lib|implements|IDX_mxo4_scpi_all|catalog|persistent",
        "@USR: USR_scpi_sync|convention|*OPC? or *WAI after async commands|active|persistent",
        "@USR: USR_scpi_short|convention|CHAN1:STAT short form for CHANnel<ch>:STATe|active|persistent",
    ]

    edge = 10
    for key, rec in manifest["recipes"].items():
        prc_id = f"PRC_scpi_{key}"
        title = rec["title"][:80]
        steps = "|".join(rec["steps"])
        if len(steps) > 3500:
            steps = steps[:3500]
        lines.append(f"@PRC: {prc_id}|{title}|{steps}|persistent")
        lines.append(f"@EDG: E_lib_{edge:02d}|MOD_scpi_lib|documents|{prc_id}|recipe|persistent")
        edge += 1

    for topic, text in manifest["conventions"].items():
        lines.append(f"@USR: USR_scpi_conv_{topic}|convention|{text[:200]}|active|persistent")

    for i in range(0, len(lines), 80):
        batch = lines[i : i + 80]
        resp = send_command(
            ["add", "--stdin", "--session", session, "--allow-new-relation"],
            stdin="\n".join(batch),
        )
        if "@ERR:" in (resp.get("stderr") or ""):
            raise SystemExit(resp.get("stderr"))

    send_command(
        ["update", "--stdin", "--session", session],
        stdin="@TSK: TSK_mxo4_scpi_snap|MXO4 SCPI index + usage lib|MOD_scpi_lib|done|persistent",
    )
    send_command(["session_save", "--session", session, "--file", str(SNAP)])
    print(f"updated {SNAP} with {len(lines)} lib rows")


if __name__ == "__main__":
    main()
