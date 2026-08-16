# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| Static quadratic selectors | fresh gates fail | NO-GO |
| P-only xor256 reliability | fresh gates fail | NO-GO |
| Synthetic descriptors | selector relevance fails | NO-GO |
| Public xor delta | 4/4 gates fail | NO-GO |
| Public additive distance | 4/4 gates fail | NO-GO |
| Public carry signature | 6/6 gates fail | NO-GO |
| Output-conditioned borrow summaries | 6/6 gates fail, 26/26 tests pass | `NO_GO_BORROW_SIGNATURE` |
| Internal boundary syndrome Stage0 | structural plan frozen | ACTIVE |
| End-to-end work reduction | not admitted | NOT ADMITTED |
| alpha<1 | — | NOT DEMONSTRATED |
