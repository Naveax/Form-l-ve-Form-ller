# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Closed NO-GO families now include static quadratic selectors, P-only xor256 reliability, synthetic score-shape/C1/public-counter descriptor learning, public xor-delta class, public additive-distance class, public carry-transition signature, and output-conditioned aggregate feed-forward borrow descriptors.

### Borrow result
12 fresh b=10 targets × reused 32 pairs; 15 candidate-ensemble borrow features. **6/6 gates failed**:
- pooled Spearman **-0.11838**;
- median target Spearman **-0.12260**;
- median top8 enrichment **+0.00122**;
- positive top8 targets **7/12**;
- gain vs public-carry control **-0.04629**;
- permutation p **0.78210**.
Carry control pooled Spearman: **-0.07209**.
Accounting: 345.42 s total, 28.72 s median/target, 531.8 MiB max RSS. Combined regression suite **26/26 PASS**.

### Structural boundary
The negative result now spans both public-static pair geometry and aggregate target-dependent candidate-ensemble descriptors. Stop adding summary-statistic descriptors under new names.

### Next
`V25_INTERNAL_ROUND_BOUNDARY_CANDIDATE_TRAJECTORY_SYNDROME_AUDIT`
Stage0 asks whether an exact partial internal-boundary word can be computed with materially fewer quarter-rounds than full 6-round verification. Even PASS is only a constant-factor opportunity, not alpha<1.

Still not admitted: true-key reliability mapping, end-to-end work reduction, alpha<1, full-round relevance.
