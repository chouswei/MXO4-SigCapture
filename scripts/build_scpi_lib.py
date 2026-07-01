"""Build MXO4 SCPI library JSON from user-manual text extract."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "docs" / "reference" / "_manual_extract.txt"
COMMAND_INDEX = ROOT / "docs" / "reference" / "_mxo4_scpi_commands.json"
OUT_DIR = ROOT / "src" / "mxo4_sigcapture" / "scpi" / "data"
MANIFEST_PATH = OUT_DIR / "manifest.json"
COMMANDS_PATH = OUT_DIR / "commands.json"

CH17_START = "===== PAGE 351 ====="
CH17_END = "===== PAGE 642 ====="


@dataclass
class CommandEntry:
    name: str
    page: int
    usage: str = "rw"
    summary: str = ""
    parameters: list[str] = field(default_factory=list)
    return_values: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    rst_default: str = ""
    scpi_confirmed: bool = False
    async_cmd: bool = False


def load_ch17_text() -> str:
    text = EXTRACT.read_text(encoding="utf-8")
    start = text.index(CH17_START)
    end = text.index(CH17_END)
    return text[start:end]


def _usage_from_block(block: str) -> str:
    m = re.search(r"Usage:\s*([^\n]+)", block)
    if not m:
        return "rw"
    u = m.group(1).strip().lower()
    if "query only" in u:
        return "query"
    if "setting only" in u:
        return "set"
    if "event" in u:
        return "event"
    if "asynchronous" in u:
        return "async"
    return "rw"


def _summary_from_block(block: str, cmd: str) -> str:
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith(cmd.split("[")[0][:12]) or cmd in line:
            for follow in lines[i + 1 : i + 6]:
                t = follow.strip()
                if not t or t.startswith("Suffix:") or t.startswith("Parameters:"):
                    continue
                if re.match(r"^[A-Za-z*][A-Za-z0-9<>:_\[\]?]+\s", t):
                    break
                return t[:400]
    return ""


def _collect_section(block: str, header: str) -> list[str]:
    items: list[str] = []
    if header not in block:
        return items
    part = block.split(header, 1)[1]
    for line in part.splitlines()[:16]:
        t = line.strip()
        if not t:
            continue
        if t.startswith("Usage:") or t.startswith("Manual operation:"):
            break
        if re.match(r"^[A-Za-z*][A-Za-z0-9<>:_\[\]?]+\s", t) and header not in t:
            break
        items.append(t[:200])
    return items


def _examples_from_block(block: str) -> list[str]:
    out: list[str] = []
    for m in re.finditer(r"Example:\s*([^\n]+)", block):
        ex = m.group(1).strip()
        if ex and not ex.startswith("See Chapter"):
            out.append(ex[:300])
    return out


def _rst_from_block(block: str) -> str:
    m = re.search(r"\*RST:\s*([^\n]+)", block)
    return m.group(1).strip()[:120] if m else ""


def _header_pattern(cmd: str) -> re.Pattern[str]:
    esc = re.escape(cmd)
    return re.compile(rf"^{esc}(?:\?)?(?:\s+[<[]|\?|\s*$)", re.MULTILINE)


def _find_all_headers(ch17: str, names: list[str]) -> dict[str, list[int]]:
    """All non-TOC header positions per command."""
    ordered = sorted(names, key=len, reverse=True)
    patterns = [(n, _header_pattern(n)) for n in ordered]
    hits: dict[str, list[int]] = {n: [] for n in names}
    for name, pat in patterns:
        for m in pat.finditer(ch17):
            hits[name].append(m.start())
    return hits


def _global_header_positions(ch17: str, names: list[str]) -> list[tuple[int, str]]:
    ordered = sorted(names, key=len, reverse=True)
    all_hits: list[tuple[int, str]] = []
    for name in ordered:
        for pos in _find_all_headers(ch17, [name]).get(name, []):
            all_hits.append((pos, name))
    all_hits.sort(key=lambda x: x[0])
    return all_hits


def _block_score(block: str, name: str) -> int:
    score = 0
    if "Usage:" in block:
        score += 50
    if "Parameters:" in block:
        score += 30
    if "Return values:" in block:
        score += 20
    if _summary_from_block(block, name):
        score += 10
    score += min(len(block) // 80, 25)
    return score


def parse_commands(ch17: str, names: list[dict]) -> list[CommandEntry]:
    name_list = [c["name"] for c in names]
    by_name = {c["name"]: c["page"] for c in names}
    all_positions = _global_header_positions(ch17, name_list)
    sorted_pos = [p for p, _ in all_positions]

    def block_end(start: int) -> int:
        for p in sorted_pos:
            if p > start:
                return p
        return len(ch17)

    blocks: dict[str, str] = {}
    for name in name_list:
        best = ""
        best_score = -1
        for pos in _find_all_headers(ch17, [name]).get(name, []):
            chunk = ch17[pos : block_end(pos)]
            sc = _block_score(chunk, name)
            if sc > best_score:
                best_score = sc
                best = chunk
        blocks[name] = best

    entries: list[CommandEntry] = []
    for name in name_list:
        page = by_name[name]
        block = blocks.get(name, "")
        if not block:
            entries.append(CommandEntry(name=name, page=page))
            continue
        entries.append(
            CommandEntry(
                name=name,
                page=page,
                usage=_usage_from_block(block),
                summary=_summary_from_block(block, name),
                parameters=_collect_section(block, "Parameters:"),
                return_values=_collect_section(block, "Return values:"),
                examples=_examples_from_block(block),
                rst_default=_rst_from_block(block),
                scpi_confirmed="SCPI confirmed" in block,
                async_cmd="Asynchronous command" in block,
            )
        )

    entries.sort(key=lambda e: e.name.upper())
    return entries


def build_manifest() -> dict:
    return {
        "instrument": "R&S MXO 4",
        "manual": "R&S_MXO_4-Series_Oscilloscope_UserManual_en_03.pdf",
        "conventions": {
            "default_usage": "set and query unless stated otherwise",
            "sync": "Use *OPC or *WAI after overlapping/async commands",
            "reset": "*RST restores defaults noted per command; does not reset waveform generator (use WGENerator<wg>:PRESet)",
            "short_form": "Manual examples use short headers (e.g. CHAN1:STAT); full form is CHANnel<ch>:STATe",
        },
        "connection": {
            "hislip": "TCPIP::<host>::hislip0[,<port>][::INSTR]",
            "vxi11": "TCPIP::<host>[::inst0][::INSTR]",
            "start_remote": "Send any command, or VXI-11 &GTR to leave local mode",
            "default_socket_port": 5025,
        },
        "parameters": {
            "waveform": {
                "C1": "channel 1 (CHAN1)",
                "C2": "channel 2",
                "C3": "channel 3",
                "C4": "channel 4",
                "M1-M8": "math waveforms",
                "R1-R4": "reference waveforms",
            },
            "slope": ["POSitive", "NEGative", "EITHer"],
            "polarity": ["POSitive", "NEGative", "EITHer"],
        },
        "recipes": {
            "identify": {
                "title": "Identify instrument",
                "steps": ["*IDN?"],
            },
            "reset": {
                "title": "Reset to defaults",
                "steps": ["*RST", "*OPC?"],
            },
            "continuous_acquire": {
                "title": "Start continuous acquisition",
                "steps": ["RUN"],
            },
            "single_acquire": {
                "title": "Single acquisition",
                "steps": ["ACQuire:COUNt 1", "RUNSingle", "*OPC?"],
            },
            "stop_acquire": {
                "title": "Stop acquisition",
                "steps": ["STOP"],
            },
            "enable_channel": {
                "title": "Enable analog channel n (1-4)",
                "steps": ["CHAN{n}:STAT 1"],
                "notes": "Short form; equivalent to CHANnel<ch>:STATe ON",
            },
            "vertical_setup": {
                "title": "Channel vertical scale and offset",
                "steps": [
                    "CHAN{n}:SCAL {volts_per_div}",
                    "CHAN{n}:OFFS {offset_v}",
                ],
            },
            "horizontal_setup": {
                "title": "Timebase scale and position",
                "steps": [
                    "TIM:SCAL {seconds_per_div}",
                    "TIM:HOR:POS {position_s}",
                ],
            },
            "ascii_waveform": {
                "title": "Configure ASCII waveform transfer",
                "steps": [
                    "FORM:DATA ASC,0",
                    "CHAN{n}:DATA:HEAD?",
                    "CHAN{n}:DATA?",
                ],
            },
            "binary_waveform": {
                "title": "Configure binary REAL32 waveform transfer",
                "steps": [
                    "FORM:DATA REAL,32",
                    "CHAN{n}:DATA:HEAD?",
                    "CHAN{n}:DATA?",
                ],
            },
            "autoscale": {
                "title": "Autoscale all enabled channels",
                "steps": ["AUToscale"],
            },
            "trigger_edge": {
                "title": "Edge trigger on channel n",
                "steps": [
                    "TRIG:MODE NORM",
                    "TRIG:EVEN1:SOUR C{n}",
                    "TRIG:EVEN1:TYPE EDGE",
                    "TRIG:EVEN1:LEV1 {level_v}",
                ],
            },
            "smartgrid_zoom": {
                "title": "SmartGrid layout with zoom (manual 17.4.1)",
                "steps": [
                    "CHAN1:STAT 1",
                    "CHAN2:STAT 1",
                    "CHAN3:STAT 1",
                    "LAY:DIAG2:ENAB 1",
                    "LAY:DIAG2:SOUR C2",
                    "LAY:DIAG3:ENAB 1",
                    "LAY:DIAG3:SOUR C3",
                    "LAY:NODE2:ENAB 1",
                    "LAY:NODE2:CHIL1:CONT:TYPE DIAG",
                    "LAY:NODE2:CHIL1:CONT:ID 2",
                    "LAY:NODE2:CHIL2:CONT:TYPE DIAG",
                    "LAY:NODE2:CHIL2:CONT:ID 3",
                    "LAY:NODE2:STYP VERT",
                    "LAY:NODE1:CHIL2:CONT:TYPE NODE",
                    "LAY:NODE1:CHIL2:CONT:ID 2",
                    "LAY:NODE1:STYP HOR",
                    "LAY:ZOOM:ENAB 1",
                    "LAY:ZOOM:SOUR 3",
                ],
            },
        },
        "subsystems": {
            "COMMON": "IEEE 488.2 common commands (*IDN?, *RST, *OPC, ...)",
            "ACQuire": "Acquisition mode, points, sample rate, history",
            "CHANnel<ch>": "Vertical channel setup (scale, offset, coupling)",
            "TIMebase": "Horizontal timebase",
            "TRIGger": "Trigger system and holdoff",
            "FORMat": "Waveform/result data encoding for remote transfer",
            "RUN": "Acquisition run/stop control",
            "CALCulate": "Math and spectrum analysis",
            "MEASurement<mg>": "Automatic measurements",
            "MMEMory": "File and settings storage on instrument",
            "STATus": "SCPI status reporting registers",
        },
    }


def main() -> None:
    if not EXTRACT.exists():
        raise SystemExit(f"Missing manual extract: {EXTRACT}")
    if not COMMAND_INDEX.exists():
        raise SystemExit(f"Missing command index: {COMMAND_INDEX}")

    index = json.loads(COMMAND_INDEX.read_text(encoding="utf-8"))
    ch17 = load_ch17_text()
    entries = parse_commands(ch17, index["commands"])
    manifest = build_manifest()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    COMMANDS_PATH.write_text(
        json.dumps(
            {
                "count": len(entries),
                "with_summary": sum(1 for e in entries if e.summary),
                "commands": [asdict(e) for e in entries],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"manifest -> {MANIFEST_PATH}")
    print(f"commands -> {COMMANDS_PATH} ({len(entries)} entries, {sum(1 for e in entries if e.summary)} with summary)")


if __name__ == "__main__":
    main()
