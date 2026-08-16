# FDS V25 — Public Counter Carry-Transition Signature Audit

## Verdict
`NO_GO_PUBLIC_CARRY_SIGNATURE`

The family was preregistered on GitHub before oracle results were inspected. It used 32 public source-counter pairs and 12 fresh b=10 targets in three grouped folds.

All 6/6 frozen gates failed: pooled Spearman **-0.07541**; median target Spearman **-0.03423**; median top-8 enrichment **-0.03994**; positive top-8 targets **5/12**; gain vs distance-only **-0.06990**; shuffle p **0.78988**. Distance-only pooled Spearman was **-0.00551**.

Accounting: 12x32 pairs, 39 unique counters/target; total target build wall **349.87 s**, median **29.12 s**, max peak RSS **527.2 MiB**, plus 256 shuffle null replicates.

Conclusion: public-static xor delta, additive distance and carry-transition signature all fail robust transfer. Next must be target/output-dependent.
