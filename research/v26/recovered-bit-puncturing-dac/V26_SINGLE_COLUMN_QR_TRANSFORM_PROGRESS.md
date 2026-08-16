# V26 Single-Column QR Transform Falsifier — Progress

## Frozen authority

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` is frozen before measurement. No thresholds or caps have been changed.

## Implemented in this pass

- Added `fds_v26_single_column_qr_transform.py`.
- Added `test_fds_v26_single_column_qr_transform.py`.
- The cap2 reference path propagates each explicit first-layer global hull state through the corresponding exact bounded inverse QR **before** signed marginal merge, so it is not merely the factorized marginal path called twice.
- The test requires all four columns to match in support, every signed coefficient (`<=1e-12` absolute error), and signed energy (`<=1e-12`).
- The runner verifies the recovered bit-puncturing source SHA-256 before measurement.
- Added `scripts/rematerialize_v25_trail_dac.py`, which searches a snapshot/core file, an outer ZIP, or a directory recursively, including nested ZIPs.
- Snapshot recovery still requires exact snapshot SHA-256 before restoring runtime files and independently verifies the core source SHA-256.
- Exact core-only recovery is now also supported by the frozen core SHA-256. This mode explicitly records `snapshot_verified=false` and `runtime_complete=false`; it cannot by itself open the transform measurement gate.
- Added deterministic test-path wiring for `research/v25/bit-puncturing/recovered-runtime/`.
- Added `scripts/test_rematerialize_v25_trail_dac.py` regression coverage for nested snapshot recovery and nested filename-independent core-only recovery.

## Rematerialization-helper checks

- Python syntax compilation: PASS.
- Current accessible mount: correctly returns `ok:false` because neither exact recovered snapshot nor exact core hash is present.
- Synthetic nested-snapshot recovery + restore: PASS.
- Synthetic nested core-only SHA recovery + explicit incomplete-provenance restore: PASS.
- Local regression: `2 passed`.

These helper checks validate recovery mechanics only. They are **not** evidence for the cryptanalytic transform gate.

## Extended provenance search

A broader recovery audit was completed before any new measurement:

- `/mnt`, `/home/oai`, and `/tmp`: 812 files / 130,949,394 bytes SHA-256 scanned; snapshot/core/test/cert canonical hashes all `0 hits`.
- Historical commit `2a94d1ea06c6f167b6f2e64ba71ae8bd0a5e9a1e` records the earlier snapshot verification and `19/19 PASS`, but the canonical core is not a Git blob in that commit tree; direct historical path lookups return 404.
- `archive/raw-import-2026-08-16.zip` was locally verified during bootstrap but was never committed as a Git object. Stale wording in `RAW_IMPORT_MANIFEST.json` was corrected.
- Global code search across the connected GitHub account for the core filename, core SHA and snapshot filename returned no matches.
- Public web search for the exact snapshot/core hashes and filenames returned no matches.

Canonical detail lives in `V26_MISSING_CANONICAL_BYTES.md` and GitHub Issue #22.

## Reproducibility blocker remains

The current GitHub `main` tree still does **not** contain the canonical `fds_v25_bit_puncturing.py` bytes required by both the admitted Stage0 implementation and the new falsifier.

Expected core source SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

Therefore **no cap2/cap3 measurement is claimed in this pass**. This is a source-rematerialization/reproducibility blocker, not a mathematical NO-GO and not evidence against the frozen transform hypothesis.

## Required next execution step

1. Run `scripts/rematerialize_v25_trail_dac.py <candidate-path> --restore` when historical bytes are available.
2. Prefer and require snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`; if only the exact canonical core is recovered, require core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130` and keep snapshot/runtime provenance explicitly incomplete until dependencies are separately verified.
3. Restore/verify the recovered runtime dependencies and re-run the historical `19/19 PASS` baseline.
4. Run the new cap2 all-four-column exact regression.
5. Only after cap2 PASS implement/run the frozen packed cap3 measurement and enforce the existing 2 GiB RSS / 1 GiB compact gates.

Historical V25 second-layer/CERT90 records are provenance/context only and must not be substituted for the frozen V26 measurement.
