# FDS_CONTINUE_HERE

**State:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Active:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing from Git `main` and the current conversation mount.

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue `#22 — Restore exact recovered V25 trail-DAC runtime bytes`

1. Use the frozen plan in `research/v26/recovered-bit-puncturing-dac/V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json`.
2. Preserve all prior NO-GO/inapplicable results and Stage0 separator evidence.
3. First re-materialize the recovered runtime with `scripts/rematerialize_v25_trail_dac.py <candidate-path> --restore`.
4. Provenance gate requires snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6` and core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130` exactly. Do not substitute a rewritten core silently.
5. Current 2026-08-16 conversation files, including nested ZIP contents, were SHA-scanned and contain **0 matches** for both canonical hashes. Historical transcript text records the hashes but does not restore byte-identical provenance.
6. Restore runtime dependencies and re-run the historical `19/19 PASS` baseline before any new transform measurement.
7. The cap2 factorized/reference implementation and all-four-column regression are committed. Run them only after the provenance gate passes.
8. cap2 equality requires exact support plus every signed coefficient and energy within `1e-12`.
9. cap3: no global joint materialization; construct all four transformed marginals with cached local QR hulls and packed signed merge.
10. PASS requires all cap2 exact checks plus complete cap3 transforms under 2 GiB peak RSS and 1 GiB total 24-byte compact representation.
11. Zero input marginals stay zero by linearity but are not evidence of absent joint correlations.
12. Only PASS opens a separately frozen pairwise/junction-tree cross-column contraction stage. No AI prompt or alpha/full-round claim at this gate.

**First unfinished canonical pass:** obtain historical backup bytes → SHA-locked rematerialization → historical 19/19 baseline → cap2 ×4 exact QR-transform gate.
