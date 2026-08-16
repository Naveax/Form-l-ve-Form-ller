# FDS GitHub Bootstrap Certificate — 2026-08-16

## Repository

`Naveax/Form-l-ve-Form-ller`

## Bootstrap authority chain

Initial authority commit:
`13d618d3d63241d81b21b8365f749e830e34c0d6`

Continuity/vision/disciplined-roadmap commit:
`80dfbc1f5be8b2bd8a472c854d23807547fcbd55`

Latest HEAD observed before this certificate commit:
`7254e24986b8a9aac6c765ac1d9d8d04e79525bb`

## Authority files established

- `README.md`
- `AGENTS.md`
- `FDS_CONTINUE_HERE.md`
- `FDS_CURRENT_STATE.md`
- `FDS_VISION.md`
- `FDS_RESEARCH_DISCIPLINE.md`
- `FDS_COMPUTE_POLICY.md`
- `FDS_KNOWLEDGE_GRAPH.md`
- `FDS_SOURCE_REGISTRY.md`
- `FDS_VALIDATION_MATRIX.md`
- `FDS_CHECKLIST.md`
- `FDS_DECISION_LOG.md`
- `FDS_REPO_LAYOUT.md`
- `archive/RAW_IMPORT_MANIFEST.json`
- `archive/RAW_IMPORT_FULL_MANIFEST.json`
- `archive/RAW_IMPORT_STATUS.md`
- `scripts/continuity_check.py`
- `scripts/verify_raw_import.py`

## Executable backlog

GitHub Issue #1: `V25 — Synthetic Reliability Learnability Audit`.

## Raw-source provenance

Current conversation mount captured:
- 94 files
- 4,341,402 bytes
- locally verified compressed snapshot size: 1,566,535 bytes
- snapshot SHA-256: `b21a45f80d7af4fdf745d490daf8c100d620e40b89dc6b49a158a8c0f4263863`

All 94 filename/byte/SHA-256 records are committed in `archive/RAW_IMPORT_FULL_MANIFEST.json`.

The bulk ZIP itself is **not** falsely certified as a Git object: current GitHub connector has no local binary file-parameter bridge and the container has no authenticated `gh` credential. See `archive/RAW_IMPORT_STATUS.md`.

## Verification observations

- GitHub connector confirmed repository write access and reads current root contents.
- Local clean-clone verification could not run because the container's outbound DNS could not resolve `github.com`; this is classified as a transport limitation, not a repository test failure.
- Raw import verifier was changed to support manifest-only self-check plus explicit `--source-dir` / `--archive` verification when raw bytes are materialized.

## Continuation guarantee

A future agent can begin from fresh `main`, read `AGENTS.md` + `FDS_CONTINUE_HERE.md`, follow the mandatory reading order, resolve Issue #1, and continue without relying on chat-memory as the sole authority.
