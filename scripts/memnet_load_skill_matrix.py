#!/usr/bin/env python3
"""Load skill matrix wire rows into MemNet (initial snap ingest)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / ".memnet" / "skill_matrix.snap.md"
ANCHOR = "TSK_mxo4_skill_matrix"


def extract_wire(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```memnet\n(.*?)```", text, re.DOTALL)
    if not match:
        raise SystemExit(f"No memnet fence in {path}")
    return match.group(1).strip()


def main() -> int:
    try:
        from memnet.serve import send_command
    except ImportError:
        print(
            "memnet package not installed; read wire from "
            f"{SNAP} or use MCP query_warm(anchor={ANCHOR!r})",
            file=sys.stderr,
        )
        return 1

    wire = extract_wire(SNAP)
    lines = [ln for ln in wire.splitlines() if ln.strip() and not ln.strip().startswith("#")]

    resp = send_command(["session_new"])
    if int(resp.get("exit_code", 1)) != 0:
        print(resp.get("stderr", ""), file=sys.stderr)
        return 1

    session = "default"
    for line in (resp.get("stderr") or "").splitlines():
        if line.startswith("MEMNET_SESSION="):
            session = line.split("=", 1)[1].strip()

    batch_size = 80
    for i in range(0, len(lines), batch_size):
        batch = lines[i : i + batch_size]
        resp = send_command(
            ["add", "--stdin", "--session", session, "--allow-new-relation"],
            stdin="\n".join(batch),
        )
        if int(resp.get("exit_code", 1)) != 0 or "@ERR:" in (resp.get("stderr") or ""):
            print(resp.get("stderr", ""), file=sys.stderr)
            return 1

    out_snap = ROOT / ".memnet" / "skill_matrix.snap"
    send_command(
        ["update", "--stdin", "--session", session],
        stdin=f"@TSK: {ANCHOR}|MXO4 skill matrix loaded|active|persistent",
    )
    send_command(["session_save", "--session", session, "--file", str(out_snap)])
    print(f"Loaded {len(lines)} wire rows into MemNet session {session!r}")
    print(f"Saved {out_snap}")
    print(f"MEMNET_SESSION={session}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
