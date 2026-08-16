# FDS_DECISION_LOG

## 2026-08-16 — Recovered bit-puncturing D&C separator Stage0
Exact signed factorized column marginals were validated against explicit first-layer global hulls at cap2 and cap3 for all four next columns. cap4 avoided 222.66M global Cartesian trails. Packed exact supports were 11,846,464 for column1 and 26,912 for column2, with columns0/3 cancelling exactly after marginalization. Compact estimate ~285 MB; peak RSS ~839 MiB, within frozen limits.

Decision: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

This does not preserve the full cross-column joint state and does not admit four-round energy/ranking/alpha. Next falsifier applies one next-column inverse QR to the exact marginal and checks whether even that local transform remains tractable before building a joint contraction.
