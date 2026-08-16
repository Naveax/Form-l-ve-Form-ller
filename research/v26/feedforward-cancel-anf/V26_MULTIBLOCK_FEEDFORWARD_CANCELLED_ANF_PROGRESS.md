# V26 Multi-Block Feed-Forward-Cancelled ANF Audit

Frozen target-free Stage0 completed for b=8/10/12/14/16, counters 1/257, R4 control and R6 primary, all 512 output bits.

Exact vectorized ChaCha was checked against scalar reference; ANF Möbius transform passed known-polynomial and involution tests. Pytest: **3/3 PASS**.

R6 b16:
- single median degree: `16`;
- cancelled median degree: `15`, but median of the 512 per-bit degree reductions is **0**;
- median bitwise support-exponent reduction: `-5.6438e-05` (gate required >=0.10);
- sparse-useful bits: `0`;
- stable sparse bits across b14/b16: `0` (gate required >=16).

All **3/3 primary gates fail**. R4 also has zero stable sparse bits and cannot rescue the R6 result.

Decision: `NO_GO_FEEDFORWARD_CANCELLED_ANF`. No polynomial-solving stage opens. Counter pair, output set and thresholds are frozen/retired for this family.
