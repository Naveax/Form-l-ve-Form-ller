# FDS_CONTINUE_HERE

**State:** simple exact MITM branch closed; PNB exponent track recovered as closed; bit-puncturing core reproduced.  
**Active:** `V25_REDUCED_QUARTER_ROUND_WALSH_TRAIL_VALIDATION`.

1. Use frozen n=5 reduced-quarter-round plan under `research/v25/bit-puncturing/`.
2. First pass the n=2 full-enumeration coefficient-wise regression.
3. Exact n=5 references use the complete 2^20 input truth table/FWT for A0,B1,C2,D3.
4. Trail engine must use exact addition coefficients, exact XOR/rotation mask transport, merge duplicates before pruning, and beam caps 64/256/1024/4096 only.
5. Primary PASS requires beam4096 spectral cosine^2 >=0.90 and exact-support energy >=0.90 on all four masks, <=4096 final coefficients, and >=256x truth-table/coefficient count ratio.
6. No mask or beam retuning after spectrum inspection.
7. Only PASS opens q138/source-orbit ranking integration with full offline/TOTAL accounting.
8. No alpha<1 or full-round claim from method validation.
