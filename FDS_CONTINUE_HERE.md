# FDS_CONTINUE_HERE

**State:** Issue #10 exact XOR 8+8 separability NO-GO; Issue #9 constant-factor PASS; alpha still 1.  
**Active:** `V25_BOUNDARY_SYNDROME_MODULAR_HALF_SEPARABILITY_AUDIT`.

1. Use frozen modular plan under `research/v25/modular-half-separability/`.
2. W5_SINGLE b16, logical 8+8, fresh targets `[50991,1272,39506,19952]` only.
3. Build exact 256×256 low16 syndrome table per target.
4. Test modular rectangle residual for m=`4,8,12,16`.
5. Select largest m exact on all four targets; PASS requires m>=8, true half-pair retained 4/4 and <=512 matches on every target.
6. Residual concentration/2-adic diagnostics cannot rescue exact FAIL.
7. Only on PASS open a separately frozen MITM TOTAL scaling stage.
8. On FAIL close this simple modular-additive family; no second target set.
9. Commit source/tests/results/decision/manifest + continuity.

No alpha<1/full-round claim from this structural audit alone.
