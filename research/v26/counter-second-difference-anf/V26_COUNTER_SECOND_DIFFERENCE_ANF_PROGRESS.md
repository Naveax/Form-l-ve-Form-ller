# V26 Counter Second-Difference ANF Audit

Frozen Issue #18 target-free protocol completed for b8/10/12/14/16, R4/R6, counters `[1,257,513]`, all 512 bits.

Second finite difference: `D2 = Z513 - 2*Z257 + Z1 mod 2^32`; the linear counter feed-forward term cancels exactly.

R6 b16:
- median per-bit degree reduction vs single: **0** (gate >=2);
- median per-bit support-exponent reduction: **-3.4348e-05** (gate >=0.10);
- sparse-useful bits: **0**;
- stable sparse b14/b16 bits: **0** (gate >=16).

All 3/3 gates fail. R4 also has zero stable sparse bits. Decision: `NO_GO_COUNTER_SECOND_DIFFERENCE_ANF`.

Do not continue derivative-order or stride tuning inside this family.
