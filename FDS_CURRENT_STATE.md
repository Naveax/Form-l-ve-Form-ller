# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C branch is now active and Stage0 passed. Exact signed first-layer marginals onto all four second-layer column interfaces match explicit global materialization at cap2/cap3. At cap4, the global 222,660,480 Cartesian trails were avoided; packed exact separator supports are `[0,11846464,26912,0]`, total 24-byte compact estimate ~285 MB, measured peak RSS ~839 MiB.

Stage0 verdict: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

Important limit: these are exact signed marginals, not a complete joint second-layer distribution. Columns0/3 marginalize to zero but may remain coupled to other columns in the joint state.

## Next
Freeze and run a single-column inverse-QR transform falsifier. Validate it against explicit global propagation on cap2, then measure whether cap3 transformed column marginals remain practical. Only if that passes should joint cross-column contraction be attempted.

Still not admitted: full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, alpha<1, or full-round relevance.
