# FDS V25 — Output-Conditioned Feed-Forward Borrow Signature Audit

## Verdict
`NO_GO_BORROW_SIGNATURE`

Plan and pair-coordinate hash were committed before oracle results. 12 fresh b=10 targets reused the exact 32-pair carry pool. Fifteen inference-safe features summarized word4 feed-forward subtraction borrow masks over all 1,024 candidates; the true candidate was never singled out during descriptor construction.

All 6/6 gates failed: pooled Spearman **-0.11838**, median target **-0.12260**, median top8 enrichment **+0.00122**, positive **7/12**, gain vs public-carry **-0.04629**, permutation p **0.78210**. Public-carry control pooled Spearman **-0.07209**.

Accounting: total build wall **345.42 s**, median target **28.72 s**, max RSS **531.8 MiB**, plus 256 null permutations. Tests: borrow arithmetic 3/3, recovered regressions 23/23, combined 26/26 PASS.

Conclusion: stop adding aggregate summary descriptors. Next is non-aggregated algebraic candidate-trajectory consistency at an internal boundary.
