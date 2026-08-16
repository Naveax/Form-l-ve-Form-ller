# FDS_CONTINUE_HERE

**State:** V25 exponent track CLOSED; V26 first-difference/feed-forward-cancelled ANF `NO_GO`.  
**Active:** `V26_COUNTER_SECOND_DIFFERENCE_ANF_AUDIT`.

1. Use frozen plan under `research/v26/counter-second-difference-anf/`.
2. Counters exactly `[1,257,513]`, stride256, b=`8,10,12,14,16`, R4 control/R6 primary, all 512 bits.
3. Compute `D2 = Z513 - 2*Z257 + Z1 mod 2^32`; do not manually subtract feed-forward because the second difference cancels its linear counter term exactly.
4. Run exact packed ANF/Möbius metrics.
5. R6 PASS requires b16 median per-bit degree reduction >=2, median per-bit support-exponent reduction >=0.10, and >=16 stable sparse bits across b14/b16.
6. R4/first-difference diagnostics cannot rescue R6 failure.
7. Only PASS opens separately frozen polynomial-solving/TOTAL scaling.
8. On FAIL close this family; no stride/counter/order/output/threshold retuning.
