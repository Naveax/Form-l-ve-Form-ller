# FDS_CONTINUE_HERE

**State:** V26 counter first/second finite-difference ANF families NO-GO.  
**Active:** `V26_CROSS_WORD_XOR_PROJECTION_ANF_AUDIT`.

1. Use frozen plan under `research/v26/cross-word-xor-anf/`.
2. Counter1 only; b=`8,10,12,14,16`; R4 control/R6 primary.
3. Exhaustively evaluate all 120 unordered output-word XOR pairs and all 32 bits, not a selected subset.
4. Exact ANF via packed Möbius; compute component-word baseline metrics too.
5. Stable-useful projected bit: degree<=6 and support-exp<=0.75 at both b14/b16.
6. R6 PASS requires >=16 stable projected bits, >=4 distinct pairs, and b16 median component degree/support gains >=2 / >=0.10.
7. R4 cannot rescue R6 failure.
8. Only PASS opens separately frozen algebraic-system/TOTAL scaling.
9. On FAIL close XOR projection family; no pair/threshold/output retuning.
