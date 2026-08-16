# V26 Cross-Word XOR Projection ANF Audit

Frozen exhaustive target-free audit completed.

For every b in 8/10/12/14/16 and both R4/R6, all 120 unordered output-word XOR projections and all 32 bit positions were transformed exactly to ANF: 3,840 projected bits per width/round.

Sparse-useful rule: degree<=6 and support exponent<=0.75.

Result: **0 sparse-useful projected bits at every tested width in both R4 and R6**. Therefore the R6 b14/b16 stable set is empty and all 4 primary gates fail.

Decision: `NO_GO_CROSS_WORD_XOR_PROJECTION_ANF`. Per the frozen rule, no pair cherry-picking, threshold change, modular-sum reinterpretation or second development set is allowed inside this family.
