# FDS_VALIDATION_MATRIX

| Family / claim | Frozen train/dev | Fresh/grouped eval | Validation | Verdict |
|---|---:|---:|---:|---|
| Static quadratic selectors | done | done | limited as gated | NO-GO |
| P-only xor-256 reliability | done | done | not opened after failures | NO-GO |
| Synthetic descriptor→oracle reliability | 24 targets / 6 folds | grouped CV + shuffle null | selector gate failed | `NO_GO_CURRENT_DESCRIPTOR_FAMILY` |
| Public xor delta j6/j7/j8/j9 | 12 targets / 3 folds | done | not opened | `NO_GO_PUBLIC_DELTA_CLASS` |
| Public additive distance d1/d64/d256/d512 | 12 targets / 3 folds | done | not opened | `NO_GO_PUBLIC_ADDITIVE_DISTANCE` |
| Public carry-transition signature | plan frozen | NOT STARTED | LOCKED | ACTIVE NEXT |
| End-to-end work reduction | — | — | — | NOT ADMITTED |
| `alpha < 1` | — | — | — | NOT DEMONSTRATED |
| Full-round relevance | — | — | — | NO CLAIM |

## Active carry gate
Every requirement in `research/v25/carry-transition/V25_PUBLIC_COUNTER_CARRY_TRANSITION_SIGNATURE_PLAN.json` must pass. Failure means no validation and no second development set.
