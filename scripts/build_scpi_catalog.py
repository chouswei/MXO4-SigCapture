"""Build enriched SCPI catalog from MXO4 user manual chapter 17."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL_EXTRACT = ROOT / "docs" / "reference" / "_manual_extract.txt"
COMMAND_INDEX = ROOT / "docs" / "reference" / "_mxo4_scpi_commands.json"
OUT_CATALOG = ROOT / "src" / "mxo4_sigcapture" / "scpi" / "data" / "catalog.json"

CH17_START = "===== PAGE 351 ====="
CH17_END = "===== PAGE 642 ====="


def subsystem(name: str) -> str:
    if name.startswith("*"):
        return "COMMON"
    match = re.match(r"^([A-Za-z][A-Za-z0-9<>]*(?:\[[^\]]*\])?)", name)
    return match.group(1) if match else name.split(":")[0]


def match_header(line: str, names: list[str]) -> str | None:
    stripped = line.strip()
    if not stripped or "...." in stripped:
        return None
    for name in names:
        if not stripped.startswith(name):
            continue
        rest = stripped[len(name) :]
        if rest == "" or rest[0] in " ?<[":
            return name
    return None


def parse_block(raw: str, name: str) -> dict:
    lines = [line.rstrip() for line in raw.splitlines()]
    syntax: list[str] = []
    body: list[str] = []
    for line in lines:
        if line.startswith(name) and (not syntax or line == lines[0]):
            syntax.append(line.strip())
        else:
            body.append(line)

    text = "\n".join(body).strip()
    usage = ""
    examples: list[str] = []
    manual_op = ""
    description_lines: list[str] = []

    for line in body:
        if line.startswith("Usage:"):
            usage = line[len("Usage:") :].strip()
        elif line.startswith("Example:"):
            examples.append(line[len("Example:") :].strip())
        elif line.startswith("Manual operation:"):
            manual_op = line[len("Manual operation:") :].strip()
        elif line.startswith(
            ("Suffix:", "Parameters:", "Setting parameters:", "Return values:", "Query parameters:")
        ):
            break
        elif line.strip():
            description_lines.append(line.strip())

    description = " ".join(description_lines)
    if len(description) > 500:
        description = description[:497] + "..."

    params_match = re.search(
        r"(?:Setting parameters:|Parameters:|Query parameters:|Return values:)(.*)",
        text,
        flags=re.S,
    )
    params = ""
    if params_match:
        params = params_match.group(1).strip()
        params = re.sub(r"\n{3,}", "\n\n", params)
        if len(params) > 1200:
            params = params[:1197] + "..."

    return {
        "name": name,
        "syntax": syntax,
        "description": description,
        "usage": usage,
        "examples": examples,
        "manual_operation": manual_op,
        "parameters": params,
    }


def extract_ch17_blocks(text: str, names: list[str]) -> dict[str, str]:
    start = text.find(CH17_START)
    end = text.find(CH17_END)
    if start < 0 or end < 0:
        raise SystemExit("chapter 17 bounds not found in manual extract")

    lines = text[start:end].splitlines()
    blocks: dict[str, str] = {}
    i = 0
    while i < len(lines):
        name = match_header(lines[i], names)
        if not name:
            i += 1
            continue
        start_i = i
        i += 1
        while i < len(lines):
            if match_header(lines[i], names) and i > start_i:
                break
            i += 1
        raw = "\n".join(lines[start_i:i]).strip()
        if name not in blocks or len(raw) > len(blocks[name]):
            blocks[name] = raw
    return blocks


def main() -> None:
    manual = MANUAL_EXTRACT.read_text(encoding="utf-8")
    index = json.loads(COMMAND_INDEX.read_text(encoding="utf-8"))
    commands = index["commands"]
    names = sorted({c["name"] for c in commands}, key=len, reverse=True)

    blocks = extract_ch17_blocks(manual, names)
    missing = [c["name"] for c in commands if c["name"] not in blocks]
    if missing:
        raise SystemExit(f"missing usage blocks for {len(missing)} commands")

    remote_setup = {
        "interfaces": [
            {
                "name": "HiSLIP",
                "visa": "TCPIP::<host>::hislip0[,<port>][::INSTR]",
                "example": "TCPIP::192.1.2.3::hislip0",
            },
            {
                "name": "VXI-11",
                "visa": "TCPIP::<host>[::inst0][::INSTR]",
                "example": "TCPIP::192.1.2.3",
            },
        ],
        "start_session": "Send a command from the controller, or &GTR for VXI-11",
        "sync": ["*OPC?", "*WAI"],
        "reset": "*RST",
        "identify": "*IDN?",
    }

    entries = []
    for cmd in commands:
        name = cmd["name"]
        parsed = parse_block(blocks[name], name)
        entries.append(
            {
                **parsed,
                "page": cmd["page"],
                "subsystem": subsystem(name),
                "is_query": name.endswith("?"),
            }
        )

    catalog = {
        "instrument": "R&S MXO 4",
        "source": "R&S_MXO_4-Series_Oscilloscope_UserManual_en_03.pdf",
        "chapter": "17 Remote control commands",
        "command_count": len(entries),
        "remote_setup": remote_setup,
        "commands": entries,
    }

    OUT_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    OUT_CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT_CATALOG} ({len(entries)} commands)")


if __name__ == "__main__":
    main()
