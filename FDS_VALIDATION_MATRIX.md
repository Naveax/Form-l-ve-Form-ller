# FDS_VALIDATION_MATRIX

| Family | Result | Validation | Verdict |
|---|---|---|---|
| Static quadratic selectors | fresh gates failed | closed | NO-GO |
| P-only xor256 reliability | fresh gates failed | closed | NO-GO |
| Synthetic score-shape/C1 descriptors | 24-target grouped audit failed selector relevance | closed | `NO_GO_CURRENT_DESCRIPTOR_FAMILY` |
| Public xor delta | 4/4 gates failed | closed | `NO_GO_PUBLIC_DELTA_CLASS` |
| Public additive distance | 4/4 gates failed | closed | `NO_GO_PUBLIC_ADDITIVE_DISTANCE` |
| Public carry-transition | **6/6 gates failed** | no fresh validation | `NO_GO_PUBLIC_CARRY_SIGNATURE` |
| Output-conditioned feed-forward borrow | plan frozen | LOCKED | ACTIVE NEXT |
| End-to-end work reduction | — | — | NOT ADMITTED |
| alpha<1 | — | — | NOT DEMONSTRATED |
| Full-round relevance | — | — | NO CLAIM |
