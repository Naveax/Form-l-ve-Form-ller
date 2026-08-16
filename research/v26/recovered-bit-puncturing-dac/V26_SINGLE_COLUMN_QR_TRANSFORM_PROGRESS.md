# V26 Single-Column QR Transform Falsifier — Progress

## Frozen authority

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` is frozen before measurement. No thresholds or caps have been changed.

## Implemented in this pass

- Added `fds_v26_single_column_qr_transform.py`.
- Added `test_fds_v26_single_column_qr_transform.py`.
- The cap2 reference path propagates each explicit first-layer global hull state through the corresponding exact bounded inverse QR **before** signed marginal merge, so it is not merely the factorized marginal path called twice.
- The test requires all four columns to match in support, every signed coefficient (`<=1e-12` absolute error), and signed energy (`<=1e-12`).
- The runner verifies the recovered bit-puncturing source SHA-256 before measurement.

## Reproducibility blocker discovered before measurement

The current GitHub `main` tree does **not** contain `fds_v25_bit_puncturing.py`, although both the admitted Stage0 implementation and the new falsifier depend on it. The recovered authority identifies the expected core source SHA-256 as:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

The current conversation `/mnt/data` mount also does not contain the recovered snapshot or this source file. `archive/RAW_IMPORT_STATUS.md` explicitly records that the historical bulk ZIP bytes were not committed as Git objects; only manifests/authority records were retained.

Therefore **no cap2/cap3 measurement is claimed in this pass**. This is a source-rematerialization/reproducibility blocker, not a mathematical NO-GO and not evidence against the frozen transform hypothesis.

## Required next execution step

1. Re-materialize the exact recovered `fds_v25_bit_puncturing.py` source.
2. Verify SHA-256 equals `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`.
3. Restore the recovered runtime dependencies and re-run the historical `19/19 PASS` baseline.
4. Run the new cap2 all-four-column exact regression.
5. Only after cap2 PASS implement/run the frozen packed cap3 measurement and enforce the existing 2 GiB RSS / 1 GiB compact gates.

Historical V25 second-layer/CERT90 records are provenance/context only and must not be substituted for the frozen V26 measurement.
