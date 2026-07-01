# Folder structure

```
rs-scpi-scopes/
├── SKILL.md                       # Thin orchestration (tool-wrapper pattern)
├── Folder_Structure.md            # This file
└── references/
    └── rs-scpi.snap.md            # MemNet wire snap inside a `memnet` fenced block; anchor TSK_rs_scpi
```

Primary pattern: **tool-wrapper**. Reference knowledge stored as a MemNet snap (wire format per `memnet-format`), loaded via `memnet query_warm(anchor="TSK_rs_scpi", depth=2)`; falls back to plain Read of the .snap file when MCP is unavailable.

Snap contents:

- `@TSK TSK_rs_scpi` — anchor
- `@RUL R01..R13` — normative rules (long-form, `RUNsingle`, error drain, format set, no `*RST` at connect, etc.)
- `@CLM CAP_S1..CAP_S13` + `@EDG next` — canonical capture sequence
- `@CLM HDR_F1..HDR_F4` — `DATA:HEADer?` field positions
- `@CLM PIT_01..PIT_13` + `@EDG correctedBy` / `violates` — common pitfalls and fixes
- `@SET family_modern` / `family_legacy` + `@CLM TRG_MODEL_*` + `@EDG usesTriggerModel`
- `@CLM` enums for `ACQ:TYPE`, `ACQ:INT`, `TRIG:MODE`, `FORM:DATA`, coupling
- `@ROU` transport matrix (R&S VISA, NI-VISA, pyvisa-py, RsInstrument)
- `@PRC DBG_1..DBG_5` + `@EDG next` — debugging playbook
- `@IDX rs_scpi_seeds` — retrieval keywords
