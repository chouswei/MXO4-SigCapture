---
name: rs-scpi-scopes
description: >-
  Author, review, and debug SCPI for Rohde & Schwarz oscilloscopes
  (MXO4/5, RTO/RTO6, RTP, RTM/RTA). Enforces long-form command style,
  canonical waveform capture sequence, correct trigger and acquire enums,
  binary transfer format discipline, and error-queue drain. Reference
  knowledge is a MemNet snap loaded via query_warm. Use when writing
  SCPI, integrating RsInstrument or raw VISA, porting between R&S scope
  families, or diagnosing failing scope automation.
  Triggers: R&S SCPI, Rohde & Schwarz oscilloscope, MXO4, MXO5, RTO,
  RTO6, RTP, RTM, RTA, RsInstrument, HiSLIP, VISA scope, DATA:HEADer,
  waveform binary block.
metadata:
  pattern: tool-wrapper
  domain: rs-oscilloscope-scpi
  version: 1.1-rs-scpi-scopes
---

# R&S Oscilloscope SCPI

Reference lives in a MemNet snap: [references/rs-scpi.snap.md](references/rs-scpi.snap.md) — anchor `TSK_rs_scpi`. Wire rows are inside the `memnet` fenced block; ignore the surrounding markdown wrapper. Wire format per [memnet-format](../../../../../.cursor/skills/memnet-format/SKILL.md).

## Load knowledge

1. Prefer MCP: `memnet query_warm(anchor="TSK_rs_scpi", depth=2)`.
2. Fallback (no MCP): Read `references/rs-scpi.snap` directly.

The snap contains: rules `R01..R13`, capture sequence `CAP_S1..CAP_S13` (`@EDG next` chain), header fields `HDR_F1..HDR_F4`, pitfalls `PIT_01..PIT_13` (`@EDG correctedBy`, `@EDG violates`), family sets and trigger models, enums, transport routes, debugging procedure `DBG_1..DBG_5`.

## When writing SCPI

1. Warm the snap.
2. Emit long-form commands (`R01`) via canonical sequence `CAP_S1 -> CAP_S13`.
3. Set `FORMat:DATA` / `FORMat:BORDer` before every binary read (`R07`).
4. Drain error queue after each critical block (`R05`).

## When reviewing SCPI

1. Warm the snap.
2. For each suspect line, look up matching `PIT_*`; cite `violates` rule id and apply `FIX_*`.
3. Confirm capture order matches `CAP_S*` chain and `vals_per_sample` handled (`R09`).

## When porting between families

1. Warm the snap.
2. Detect family from `*IDN?`; classify against `@SET family_modern` vs `@SET family_legacy`.
3. Pick trigger model via `@EDG usesTriggerModel` (`TRG_MODEL_MOD` or `TRG_MODEL_LEG`). Do not mix (`R11`).

## When debugging

Follow `DBG_1 -> DBG_5` chain in the snap.

## Persistence

Snap rows are `persistent` recycle. Update rules or pitfalls by editing `references/rs-scpi.snap` and re-warming; bump `metadata.version` on publish.

## Non-goals

- Not a general SCPI tutorial; assumes IEEE 488.2 basics.
- Not a substitute for the family manual on enum drift — echo the instrument's value.
- Does not cover R&S signal generators, spectrum analysers, or PSUs.

## Pairing

- [memnet-format](../../../../../.cursor/skills/memnet-format/SKILL.md) — wire grammar.
- [mcp-memnet](../../../../../.cursor/skills/mcp-memnet/SKILL.md) — `query_warm` / `add` / `update` tools.
- **RsInstrument** examples ([Rohde-Schwarz/Examples](https://github.com/Rohde-Schwarz/Examples/tree/main/Oscilloscopes/Python)) — ground truth for binary transfer.
- MXO4-specific work in this repo: `src/mxo4_sigcapture/scpi/`.
