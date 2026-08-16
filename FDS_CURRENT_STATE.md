# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted. Exact signed first-layer marginals onto all four second-layer column interfaces matched explicit global materialization at cap2/cap3. At cap4, the global 222,660,480 Cartesian trails were avoided; packed exact separator supports were `[0,11846464,26912,0]`, total 24-byte compact estimate ~285 MB, measured peak RSS ~839 MiB.

Stage0 verdict: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

Important limit: these are exact signed marginals, not a complete joint second-layer distribution. Columns0/3 marginalize to zero but may remain coupled to other columns in the joint state.

## Active QR-transform falsifier

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` is frozen. The cap2 factorized path, independent explicit-global-before-marginalization reference path, and all-four-column `1e-12` regression have been committed.

Recovery tooling now accepts either the exact canonical snapshot or an exact SHA-locked core hit from a direct file/directory/nested ZIP. A `core_only` restore is explicitly marked `snapshot_verified=false` and `runtime_complete=false`; it does not open measurement until dependencies and the historical baseline are verified.

## Current blocker — exact historical runtime bytes

The exact recovered `fds_v25_bit_puncturing.py` source required by the admitted Stage0 source and active falsifier is not present in current Git `main` or the current conversation mount.

Canonical recovery authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Required identities:

- snapshot `FDS_V25_TRAIL_ENUMERATION_DAC_SNAPSHOT.zip` SHA-256: `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- core `fds_v25_bit_puncturing.py` SHA-256: `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

Search status as of the latest 2026-08-16 audit:

- current conversation `/mnt/data`, including nested ZIP contents: `0 matches`;
- broader `/mnt` + `/home/oai` + `/tmp`: 812 files / 130,949,394 bytes SHA-256 scanned; canonical snapshot/core/test/cert: `0 hits`;
- historical recovery commit `2a94d1e...` records prior snapshot verification and `19/19 PASS`, but its Git tree does not contain the canonical core blob;
- bootstrap raw ZIP was locally verified but was not committed as a Git object;
- connected-account global GitHub code search and public web search produced no canonical byte source.

Historical transcript text records the hashes and recovered result lineage but does not provide a verified byte-identical core.

This is a source-rematerialization/provenance blocker, **not a mathematical NO-GO**. Do not substitute a rewritten core silently.

## Next

1. Obtain historical backup ZIP/source bytes.
2. Run `scripts/rematerialize_v25_trail_dac.py <candidate-path> --restore`.
3. Require exact snapshot SHA, or exact core SHA with explicitly incomplete snapshot/runtime provenance.
4. Restore/verify dependencies and reproduce historical `19/19 PASS`.
5. Execute frozen cap2 all-column transform regression.
6. Only cap2 PASS opens packed cap3 measurement under 2 GiB RSS / 1 GiB compact gates.

Still not admitted: full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, alpha<1, or full-round relevance.
