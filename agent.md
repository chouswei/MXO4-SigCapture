# MXO4 SigCapture — Agent context

Cursor / coding-agent entry for [MXO4-SigCapture](https://github.com/chouswei/MXO4-SigCapture).
Project rules and modules here; **skill matrix** is a separate MemNet initial snap.

## Quick facts

| Item | Value |
|------|-------|
| Instrument | R&S **MXO4** (hardware only) |
| Transport | VISA / HiSLIP raw SCPI (`Mxo4Session`) |
| GUI | `mxo4-gui` |
| Capture | `CaptureService` → `data/captures/*.h5` |
| Tests | `python -m pytest tests/ -q` |
| Version | `0.2.0` |

## MemNet load order

1. `query_warm(anchor="TSK_mxo4_agent", depth=2)` — project agent context (this file).
2. On skill routing need: `query_warm(anchor="TSK_mxo4_skill_matrix", depth=2)`.
3. **Initial snap** (warm_miss): [`.memnet/skill_matrix.snap.md`](.memnet/skill_matrix.snap.md)
   — **116** skills (96 user + 19 cursor + 1 repo).
4. SCPI: `query_warm(anchor="TSK_rs_scpi", depth=2)` → [rs-scpi.snap.md](.cursor/skills/rs-scpi-scopes/references/rs-scpi.snap.md).
5. Module graph: [`.memnet/lib_wire.txt`](.memnet/lib_wire.txt).

Regenerate snap: `python scripts/gen_agent_md.py`
Ingest into MemNet: `python scripts/memnet_load_skill_matrix.py`

## Docs

- [README.md](README.md)

---

```memnet
@TSK: TSK_mxo4_agent|MXO4 SigCapture agent orchestration|active|persistent
@ENT: ENT_repo|MXO4-SigCapture|github.com/chouswei/MXO4-SigCapture|persistent
@EDG: E_ag_01|TSK_mxo4_agent|loads|TSK_mxo4_skill_matrix|initial_snap|persistent
@EDG: E_ag_02|TSK_mxo4_agent|documents|ENT_repo|canonical|persistent

@RUL: R_ag_01|MUST|hardware-only MXO4; no mock instrument|high|persistent
@RUL: R_ag_02|MUST|raw SCPI via Mxo4Session at runtime|high|persistent
@RUL: R_ag_03|MUST|long-form SCPI; drain SYST:ERR after critical blocks|high|persistent
@RUL: R_ag_04|MUST|minimize diff scope; match module style|high|persistent
@RUL: R_ag_05|SHOULD|pytest before commit or release|medium|persistent
@RUL: R_ag_06|SHOULD|British English in user-facing prose|medium|persistent
@RUL: R_ag_07|MUST|Windows shell: chain with ; not &&|medium|persistent
@EDG: E_ag_03|TSK_mxo4_agent|governed_by|R_ag_01|policy|persistent
@EDG: E_ag_04|TSK_mxo4_agent|governed_by|R_ag_02|policy|persistent
@EDG: E_ag_05|TSK_mxo4_agent|governed_by|R_ag_03|policy|persistent

@MOD: MOD_scpi|src/mxo4_sigcapture/scpi|catalog session CLI|active|persistent
@MOD: MOD_capture|src/mxo4_sigcapture/capture|setup fetch service|active|persistent
@MOD: MOD_config|src/mxo4_sigcapture/config|AppConfig models|active|persistent
@MOD: MOD_storage|src/mxo4_sigcapture/storage|HDF5|active|persistent
@MOD: MOD_gui|src/mxo4_sigcapture/apps/gui|PySide6 GUI|active|persistent
@MOD: MOD_format|src/mxo4_sigcapture/formatting|SI units|active|persistent
@EDG: E_mod_01|MOD_gui|drives|MOD_capture|controller|persistent
@EDG: E_mod_02|MOD_capture|uses|MOD_config|setup|persistent
@EDG: E_mod_03|MOD_capture|uses|MOD_scpi|session|persistent
@EDG: E_mod_04|MOD_capture|writes|MOD_storage|hdf5|persistent
@EDG: E_mod_05|TSK_mxo4_agent|owns|MOD_scpi|codebase|persistent
@EDG: E_mod_06|TSK_mxo4_agent|owns|MOD_capture|codebase|persistent
@EDG: E_mod_07|TSK_mxo4_agent|owns|MOD_gui|codebase|persistent

@ROU: ROU_scpi|SCPI work|SKL_rs_scpi|persistent
@ROU: ROU_gui|GUI work|MOD_gui|persistent
@ROU: ROU_capture|capture scripts|MOD_capture|persistent
@ROU: ROU_hdf5|HDF5 plot|MOD_storage|persistent
@ROU: ROU_skills|skill lookup|IDX_skill_matrix|persistent
@EDG: E_rou_01|ROU_skills|loads|TSK_mxo4_skill_matrix|snap|persistent

@PRC: PRC_gui|1|read MOD_gui|persistent
@PRC: PRC_gui|2|scope-style widgets; smoke mxo4-gui|persistent
@PRC: PRC_scpi|1|warm TSK_rs_scpi|persistent
@PRC: PRC_scpi|2|edit MOD_scpi or MOD_capture|persistent
@PRC: PRC_release|1|pytest tests/ -q|persistent

@SYM: SYM_mxo4_gui|mxo4_sigcapture.apps.gui.__main__:main|entry|persistent
@SYM: SYM_capture_svc|mxo4_sigcapture.capture.service:CaptureService|api|persistent
@SYM: SYM_session|mxo4_sigcapture.scpi.session:Mxo4Session|api|persistent
```
