# FDS_DECISION_LOG

## V26 counter derivatives
First and second finite-difference exact ANF families failed all primary gates and are retired.

## 2026-08-16 — Cross-word XOR projection
Frozen exhaustive class covered all 120 unordered output-word pairs and all 32 bits for b8→b16, R4/R6. Sparse-useful projected bits were 0 at every width/round; stable R6 b14/b16 set = 0.

Decision: `NO_GO_CROSS_WORD_XOR_PROJECTION_ANF`. Do not rescue with pair cherry-picking, threshold changes or modular-sum reinterpretation inside this family.

Next mechanism selection must be literature-grounded and structurally distinct.
