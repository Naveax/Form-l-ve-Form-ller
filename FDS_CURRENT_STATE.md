# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains a scoped constant-factor screen; alpha=1. Simple exact half-key MITM is closed by Issues #10–#15. PNB/CPNB exponent work is closed as R6 constant-factor only. Issue #16 beam4096 quarter-round validation is a budget/quality NO-GO, not a semantic implementation failure.

Historical trail/D&C authority has now been recovered beyond Issue #16: DAC exact factorization, adaptive second-layer contraction, signed CP→C1, CERT90 signed contraction and one-word projected ranking were all already performed. CERT90 retains 4,395 C1 rows and 60,672 signed terms with certified fraction 0.9000132855 and exact signed energy 1.4649468239e-06. The full energy-selected trail family was not a robust q138 ranker (12-target median rank 704.5), and later selector families also failed robust holdout/confirm gates.

No branch currently demonstrates alpha<1 or end-to-end reduced-ChaCha key-search work below exhaustive scaling.

## Next
Open a V25 exponent-track closure audit before inventing another mechanism. Mechanically classify every tested family as exact NO-GO, constant-factor PASS, method-only PASS, or unresolved, verify no existing result satisfies the project's alpha<1 admission rule, and decide whether V25 should be formally closed or whether one genuinely untested structural family remains.