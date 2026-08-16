# FDS_DECISION_LOG

## 2026-08-16 — Output-conditioned borrow descriptors
`NO_GO_BORROW_SIGNATURE`; 6/6 gates failed.

## 2026-08-16 — Aggregate descriptor stop boundary
Static public pair geometry and target-dependent candidate-ensemble summary descriptors are closed. Do not resurrect them by renaming statistics.

## 2026-08-16 — Internal boundary syndrome
Stage0 found an exact 18-QR split1/word0 boundary cone vs 24 full-state and 21 direct-word pre-cache baseline; 10,240 equality checks passed. Stage1 froze width16. Stage2 untouched b=10 retained the unique true candidate on 12/12. Candidate-ensemble common-subexpression caching reduced the fair constants to `15*2^b + 6 + 17*N` vs `18*2^b + 3`. Stage3 b=10..16 passed every QR/wall/correctness gate.

**Decision:** `ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN` for the tested one-word reduced-key layout. QR speedup ~1.20x and measured wall speedup ~1.12–1.16x. Leading term remains `15*2^b`; alpha is 1.0. No exponent/full-round/general-layout claim.

## Next
Run reduced-key layout transfer falsifier before broadening the claim.
