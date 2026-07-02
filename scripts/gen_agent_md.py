#!/usr/bin/env python3
"""Generate thin agent.md + MemNet skill matrix initial snap."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_SKILLS = Path.home() / ".cursor" / "skills"
CURSOR_SKILLS = Path.home() / ".cursor" / "skills-cursor"
OUT_AGENT = ROOT / "agent.md"
OUT_SNAP = ROOT / ".memnet" / "skill_matrix.snap.md"

REPO_SKILL = ("rs-scpi-scopes", "repo", ".cursor/skills/rs-scpi-scopes/SKILL.md", "rs-scpi")
MATRIX_ANCHOR = "TSK_mxo4_skill_matrix"

DOMAIN_PREFIXES = (
    ("sysml", ("sysml-",)),
    ("sysml-tool", ("mcp-sysml", "mcp-sysmledgraph")),
    ("pcba", ("pcba-", "polarfire-soc-setup", "sysml-eagle", "sysml-pcba")),
    ("doc", (
        "academic-", "adr-", "markdown-", "md-", "mdtohtml", "meeting-notes",
        "project-output", "project-planner", "rfc-", "system-design", "tech-report",
        "mermaid", "pretty-mermaid", "mmdc",
    )),
    ("reasoning", (
        "bayesian-", "causal-", "decision-", "empirical-", "entropy-",
        "falsification-", "first-principle", "game-theory", "incentive-",
        "inversion-", "knowledge-", "launch-readiness", "mcdm-", "optimization-",
        "paradox-", "risk-", "scientific-method", "reasoning-strategy",
        "control-theory", "pandas-expert",
    )),
    ("review", (
        "code-reviewer", "pr-reviewer", "security-reviewer", "architecture-reviewer",
        "skill-reviewer", "tech-report-reviewer", "incentive-alignment-reviewer",
        "pcba-design-reviewer", "sysml-part-reviewer", "sysml-requirements-audit",
        "review-", "launch-readiness",
    )),
    ("meta", (
        "memnet-", "mcp-memnet", "mcp-novel", "mcp-latex", "mcp-chrome",
        "toon-", "tron-", "skill-", "skillfish", "engineering-practices",
        "llm-model", "file-operations", "api-client", "traceability-footprint",
    )),
    ("cursor", ("automate", "babysit", "canvas", "create-", "loop", "migrate-",
                "onboard", "sdk", "shell", "split-to-prs", "statusline", "update-")),
)


def slug_id(name: str) -> str:
    return "SKL_" + name.replace("-", "_")


def classify_domain(name: str, pack: str) -> str:
    if pack == "cursor":
        return "cursor"
    for domain, prefixes in DOMAIN_PREFIXES:
        for p in prefixes:
            if name.startswith(p) or name == p.rstrip("-"):
                return domain
    if name.startswith("sysml-"):
        return "sysml"
    if "review" in name:
        return "review"
    if name == "commit-message-generator":
        return "git"
    return "coding"


def list_skill_dirs(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(
        p.name for p in root.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    )


def skl_row(name: str, pack_label: str, path: str) -> str:
    domain = classify_domain(name, pack_label)
    return (
        f"@SKL: {slug_id(name)}|{pack_label}|skill|{name}|{domain}|low|low|conceptual|"
        f"{path}|persistent"
    )


def clm_row(idx: int, name: str, pack_label: str, path: str) -> str:
    domain = classify_domain(name, pack_label)
    sid = slug_id(name)
    short_path = name if pack_label != "repo" else path
    return f"@CLM: CLM_mat_{idx:03d}|{domain}|{sid}|{pack_label}|{short_path}|on trigger|persistent"


def write_skill_matrix_snap(
    user_names: list[str],
    cursor_names: list[str],
) -> None:
    repo_name, _repo_pack, repo_path, _repo_domain = REPO_SKILL
    user_skl_ids = [slug_id(n) for n in user_names]
    cursor_skl_ids = [slug_id(n) for n in cursor_names]
    total = 1 + len(user_names) + len(cursor_names)

    lines: list[str] = []
    w = lines.append

    w("<!-- MemNet initial snap: MXO4 skill matrix (user + cursor + repo packs).")
    w(f"Anchor: {MATRIX_ANCHOR}. Wire format: memnet-format.")
    w("Load: memnet query_warm(anchor=\"" + MATRIX_ANCHOR + "\", depth=2)")
    w("Fallback: read @TAG rows inside the memnet fence. -->")
    w("")
    w("```memnet")
    w(f"@TSK: {MATRIX_ANCHOR}|MXO4 SigCapture skill routing matrix|active|persistent")
    w("@SKG: SKG_mxo4|v0.2|repo:MXO4-SigCapture|persistent")
    w(f"@EDG: E_sm_01|{MATRIX_ANCHOR}|owns|SKG_mxo4|skill_graph|persistent")
    w("")
    w("@CLM: CLM_mat_hdr|type=pipe|domain|skill_id|pack|path|when|persistent")
    w(f"@IDX: IDX_skill_matrix|{total}|skill routing index|persistent")
    w("@SET: SET_skills_repo|SKL_rs_scpi|persistent")
    w(f"@SET: SET_skills_user|{','.join(user_skl_ids)}|persistent")
    w(f"@SET: SET_skills_cursor|{','.join(cursor_skl_ids)}|persistent")
    w("@EDG: E_sm_02|IDX_skill_matrix|indexes|SET_skills_repo|repo|persistent")
    w("@EDG: E_sm_03|IDX_skill_matrix|indexes|SET_skills_user|user|persistent")
    w("@EDG: E_sm_04|IDX_skill_matrix|indexes|SET_skills_cursor|cursor|persistent")
    w("@EDG: E_sm_05|IDX_skill_matrix|documents|CLM_mat_hdr|columns|persistent")
    w("")
    w(
        "@SKL: SKL_rs_scpi|repo|tool-wrapper|rs-scpi-scopes|rs-scpi|high|high|structural|"
        ".cursor/skills/rs-scpi-scopes/SKILL.md|persistent"
    )
    w("@EDG: E_sm_06|SKG_mxo4|default_stack|SKL_rs_scpi|scpi_primary|persistent")
    w("@EDG: E_sm_07|SET_skills_repo|memberOf|SKL_rs_scpi|repo|persistent")

    idx = 1
    w(f"@CLM: CLM_mat_{idx:03d}|rs-scpi|SKL_rs_scpi|repo|{repo_path}|on trigger|persistent")
    idx += 1
    for name in user_names:
        w(skl_row(name, "user", f"~/.cursor/skills/{name}/SKILL.md"))
        w(clm_row(idx, name, "user", f"~/.cursor/skills/{name}/SKILL.md"))
        idx += 1
    for name in cursor_names:
        w(skl_row(name, "cursor", f"~/.cursor/skills-cursor/{name}/SKILL.md"))
        w(clm_row(idx, name, "cursor", f"~/.cursor/skills-cursor/{name}/SKILL.md"))
        idx += 1

    w("@EDG: E_sm_08|SET_skills_user|memberOf|SKG_mxo4|user_pack|persistent")
    w("@EDG: E_sm_09|SET_skills_cursor|memberOf|SKG_mxo4|cursor_pack|persistent")
    w("@ROU: ROU_skill_graph|global skill disambiguation|SKL_reasoning_strategy_selector|persistent")
    w("@EDG: E_sm_10|SKG_mxo4|routes|ROU_skill_graph|meta|persistent")
    w("```")

    OUT_SNAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_agent_md(user_count: int, cursor_count: int, total: int) -> None:
    lines: list[str] = []
    w = lines.append

    w("# MXO4 SigCapture — Agent context")
    w("")
    w("Cursor / coding-agent entry for [MXO4-SigCapture](https://github.com/chouswei/MXO4-SigCapture).")
    w("Project rules and modules here; **skill matrix** is a separate MemNet initial snap.")
    w("")
    w("## Quick facts")
    w("")
    w("| Item | Value |")
    w("|------|-------|")
    w("| Instrument | R&S **MXO4** (hardware only) |")
    w("| Transport | VISA / HiSLIP raw SCPI (`Mxo4Session`) |")
    w("| GUI | `mxo4-gui` |")
    w("| Capture | `CaptureService` → `data/captures/*.h5` |")
    w("| Tests | `python -m pytest tests/ -q` |")
    w("| Version | `0.2.0` |")
    w("")
    w("## MemNet load order")
    w("")
    w("1. `query_warm(anchor=\"TSK_mxo4_agent\", depth=2)` — project agent context (this file).")
    w(f"2. On skill routing need: `query_warm(anchor=\"{MATRIX_ANCHOR}\", depth=2)`.")
    w(f"3. **Initial snap** (warm_miss): [`.memnet/skill_matrix.snap.md`](.memnet/skill_matrix.snap.md)")
    w(f"   — **{total}** skills ({user_count} user + {cursor_count} cursor + 1 repo).")
    w("4. SCPI: `query_warm(anchor=\"TSK_rs_scpi\", depth=2)` → [rs-scpi.snap.md](.cursor/skills/rs-scpi-scopes/references/rs-scpi.snap.md).")
    w("5. Module graph: [`.memnet/lib_wire.txt`](.memnet/lib_wire.txt).")
    w("")
    w("Regenerate snap: `python scripts/gen_agent_md.py`")
    w("Ingest into MemNet: `python scripts/memnet_load_skill_matrix.py`")
    w("")
    w("## Docs")
    w("")
    w("- [README.md](README.md)")
    w("")
    w("---")
    w("")
    w("```memnet")
    w("@TSK: TSK_mxo4_agent|MXO4 SigCapture agent orchestration|active|persistent")
    w("@ENT: ENT_repo|MXO4-SigCapture|github.com/chouswei/MXO4-SigCapture|persistent")
    w(f"@EDG: E_ag_01|TSK_mxo4_agent|loads|{MATRIX_ANCHOR}|initial_snap|persistent")
    w("@EDG: E_ag_02|TSK_mxo4_agent|documents|ENT_repo|canonical|persistent")
    w("")
    w("@RUL: R_ag_01|MUST|hardware-only MXO4; no mock instrument|high|persistent")
    w("@RUL: R_ag_02|MUST|raw SCPI via Mxo4Session at runtime|high|persistent")
    w("@RUL: R_ag_03|MUST|long-form SCPI; drain SYST:ERR after critical blocks|high|persistent")
    w("@RUL: R_ag_04|MUST|minimize diff scope; match module style|high|persistent")
    w("@RUL: R_ag_05|SHOULD|pytest before commit or release|medium|persistent")
    w("@RUL: R_ag_06|SHOULD|British English in user-facing prose|medium|persistent")
    w("@RUL: R_ag_07|MUST|Windows shell: chain with ; not &&|medium|persistent")
    w("@EDG: E_ag_03|TSK_mxo4_agent|governed_by|R_ag_01|policy|persistent")
    w("@EDG: E_ag_04|TSK_mxo4_agent|governed_by|R_ag_02|policy|persistent")
    w("@EDG: E_ag_05|TSK_mxo4_agent|governed_by|R_ag_03|policy|persistent")
    w("")
    w("@MOD: MOD_scpi|src/mxo4_sigcapture/scpi|catalog session CLI|active|persistent")
    w("@MOD: MOD_capture|src/mxo4_sigcapture/capture|setup fetch service|active|persistent")
    w("@MOD: MOD_config|src/mxo4_sigcapture/config|AppConfig models|active|persistent")
    w("@MOD: MOD_storage|src/mxo4_sigcapture/storage|HDF5|active|persistent")
    w("@MOD: MOD_gui|src/mxo4_sigcapture/apps/gui|PySide6 GUI|active|persistent")
    w("@MOD: MOD_format|src/mxo4_sigcapture/formatting|SI units|active|persistent")
    w("@EDG: E_mod_01|MOD_gui|drives|MOD_capture|controller|persistent")
    w("@EDG: E_mod_02|MOD_capture|uses|MOD_config|setup|persistent")
    w("@EDG: E_mod_03|MOD_capture|uses|MOD_scpi|session|persistent")
    w("@EDG: E_mod_04|MOD_capture|writes|MOD_storage|hdf5|persistent")
    w("@EDG: E_mod_05|TSK_mxo4_agent|owns|MOD_scpi|codebase|persistent")
    w("@EDG: E_mod_06|TSK_mxo4_agent|owns|MOD_capture|codebase|persistent")
    w("@EDG: E_mod_07|TSK_mxo4_agent|owns|MOD_gui|codebase|persistent")
    w("")
    w("@ROU: ROU_scpi|SCPI work|SKL_rs_scpi|persistent")
    w("@ROU: ROU_gui|GUI work|MOD_gui|persistent")
    w("@ROU: ROU_capture|capture scripts|MOD_capture|persistent")
    w("@ROU: ROU_hdf5|HDF5 plot|MOD_storage|persistent")
    w("@ROU: ROU_skills|skill lookup|IDX_skill_matrix|persistent")
    w("@EDG: E_rou_01|ROU_skills|loads|TSK_mxo4_skill_matrix|snap|persistent")
    w("")
    w("@PRC: PRC_gui|1|read MOD_gui|persistent")
    w("@PRC: PRC_gui|2|scope-style widgets; smoke mxo4-gui|persistent")
    w("@PRC: PRC_scpi|1|warm TSK_rs_scpi|persistent")
    w("@PRC: PRC_scpi|2|edit MOD_scpi or MOD_capture|persistent")
    w("@PRC: PRC_release|1|pytest tests/ -q|persistent")
    w("")
    w("@SYM: SYM_mxo4_gui|mxo4_sigcapture.apps.gui.__main__:main|entry|persistent")
    w("@SYM: SYM_capture_svc|mxo4_sigcapture.capture.service:CaptureService|api|persistent")
    w("@SYM: SYM_session|mxo4_sigcapture.scpi.session:Mxo4Session|api|persistent")
    w("```")

    OUT_AGENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    user_names = list_skill_dirs(USER_SKILLS)
    cursor_names = list_skill_dirs(CURSOR_SKILLS)
    total = 1 + len(user_names) + len(cursor_names)
    write_skill_matrix_snap(user_names, cursor_names)
    write_agent_md(len(user_names), len(cursor_names), total)
    print(f"Wrote {OUT_AGENT} ({OUT_AGENT.read_text(encoding='utf-8').count(chr(10))} lines)")
    print(f"Wrote {OUT_SNAP} ({OUT_SNAP.read_text(encoding='utf-8').count(chr(10))} lines, {total} skills)")


if __name__ == "__main__":
    main()
