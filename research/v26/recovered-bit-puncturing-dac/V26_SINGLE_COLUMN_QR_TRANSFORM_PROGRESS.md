# V26 Single-Column QR Transform Falsifier — Progress

## Frozen authority

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` is frozen before measurement. No thresholds or caps have been changed.

## Implemented in this pass

- Added `fds_v26_single_column_qr_transform.py`.
- Added `test_fds_v26_single_column_qr_transform.py`.
- The cap2 reference path propagates each explicit first-layer global hull state through the corresponding exact bounded inverse QR **before** signed marginal merge, so it is not merely the factorized marginal path called twice.
- The test requires all four columns to match in support, every signed coefficient (`<=1e-12` absolute error), and signed energy (`<=1e-12`).
- The runner verifies the recovered bit-puncturing source SHA-256 before measurement.
- Added `scripts/rematerialize_v25_trail_dac.py`, which can search a snapshot ZIP, an outer raw ZIP, or a directory recursively for the exact frozen snapshot SHA-256 and restore runtime files only from that verified container.
- Added deterministic test-path wiring for `research/v25/bit-puncturing/recovered-runtime/`.

## Rematerialization-helper checks

- Python syntax compilation: PASS.
- Current `/mnt/data` mount: correctly returns `ok:false` because the exact recovered snapshot hash is absent.
- Synthetic nested-ZIP recovery path: PASS after substituting synthetic test hashes in-memory; nested snapshot discovery, core hash validation and runtime member discovery all succeeded.

These helper checks validate recovery mechanics only. They are **not** evidence for the cryptanalytic transform gate.

## Reproducibility blocker discovered before measurement

The current GitHub `main` tree does **not** contain `fds_v25_bit_puncturing.py`, although both the admitted Stage0 implementation and the new falsifier depend on it. The recovered authority identifies the expected core source SHA-256 as:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

The current conversation `/mnt/data` mount also does not contain the recovered snapshot or this source file. `archive/RAW_IMPORT_STATUS.md` explicitly records that the historical bulk ZIP bytes were not committed as Git objects; only manifests/authority records were retained. GitHub Actions currently has no retained artifacts for this repository either.

Therefore **no cap2/cap3 measurement is claimed in this pass**. This is a source-rematerialization/reproducibility blocker, not a mathematical NO-GO and not evidence against the frozen transform hypothesis.

## Required next execution step

1. Run `scripts/rematerialize_v25_trail_dac.py <candidate-path> --restore` when historical bytes are available.
2. Require snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6` and core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`.
3. Restore the recovered runtime dependencies and re-run the historical `19/19 PASS` baseline.
4. Run the new cap2 all-four-column exact regression.
5. Only after cap2 PASS implement/run the frozen packed cap3 measurement and enforce the existing 2 GiB RSS / 1 GiB compact gates.

Historical V25 second-layer/CERT90 records are provenance/context only and must not be substituted for the frozen V26 measurement.
