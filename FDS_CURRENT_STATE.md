# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted. Exact signed first-layer marginals onto all four second-layer column interfaces matched explicit global materialization at cap2/cap3. At cap4, the global 222,660,480 Cartesian trails were avoided; packed exact separator supports were `[0,11846464,26912,0]`, total 24-byte compact estimate ~285 MB, measured peak RSS ~839 MiB.

Stage0 verdict: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

Important limit: these are exact signed marginals, not a complete joint second-layer distribution. Columns0/3 marginalize to zero but may remain coupled to other columns in the joint state.

## Active QR-transform falsifier

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` is frozen. The cap2 factorized path, independent explicit-global-before-marginalization reference path, and all-four-column `1e-12` regression have been committed.

A reproducibility blocker was found before new measurement: current Git `main` does not contain the recovered `fds_v25_bit_puncturing.py` source required by both the admitted Stage0 source and the active falsifier. The expected recovered core SHA-256 is `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`. The current conversation mount also lacks the recovered snapshot/source, while `archive/RAW_IMPORT_STATUS.md` records that historical bulk ZIP bytes were not Git objects.

This is a source-rematerialization blocker, not a mathematical NO-GO. No cap2/cap3 transform measurement is claimed until the exact source is restored, its SHA is verified, and the historical 19/19 baseline is re-run.

## Next

Re-materialize the exact recovered core, verify provenance, restore runtime dependencies, re-run 19/19, then execute the frozen cap2 all-column transform regression. Only cap2 PASS opens the packed cap3 measurement under the existing 2 GiB RSS / 1 GiB compact gates.

Still not admitted: full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, alpha<1, or full-round relevance.
