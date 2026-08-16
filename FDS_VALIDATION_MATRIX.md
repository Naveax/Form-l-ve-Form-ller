# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| Static quadratic selectors | fresh gates fail | NO-GO |
| P-only xor256 reliability | fresh gates fail | NO-GO |
| Synthetic descriptors | selector relevance fails | NO-GO |
| Public xor delta | 4/4 gates fail | NO-GO |
| Public additive distance | 4/4 gates fail | NO-GO |
| Public carry signature | 6/6 gates fail | NO-GO |
| Output-conditioned borrow summaries | 6/6 gates fail | NO-GO |
| Boundary syndrome Stage0 | 18 vs24 QR; 10,240 exact checks | PASS CONSTANT FACTOR |
| Boundary syndrome Stage2 | untouched 12/12 true retained | PASS |
| Boundary syndrome cached wall | wall win 12/12 | PASS |
| Boundary syndrome Stage3 b10..16 | every correctness/QR/wall gate passes | `ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN` |
| Layout transfer | not yet measured | ACTIVE NEXT |
| alpha<1 | leading term 15*2^b | NOT DEMONSTRATED; alpha=1 |
| Full-round relevance | — | NO CLAIM |
