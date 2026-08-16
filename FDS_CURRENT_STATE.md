# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains a scoped collision-tolerant constant-factor PASS; alpha=1.

Exact structural exponent hypotheses closed NO-GO:
- Issue #10 XOR 8+8 output separability;
- Issue #11 modular-additive 8+8 output separability;
- Issue #12 single-boundary W4_W6 disjoint-half dependency MITM.

Issue #12 enumerated all 80 internal cones. **0/80** had exact nonempty disjoint active supports `{4}` vs `{6}`. Forty-eight cones were fully mixed on both sides.

No alpha<1 result exists.

## Next
Before abandoning dependency-separated MITM entirely, run one target-free exhaustive layout falsifier over every unordered pair of active key/state words 4..11 (28 layouts × 80 cones). If none has an exact disjoint-half cone, close the whole simple two-word single-boundary family.
