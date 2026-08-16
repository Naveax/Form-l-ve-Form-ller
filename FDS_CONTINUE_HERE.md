# FDS_CONTINUE_HERE

**State:** Issue #9 `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`; Issue #8 remains NO-GO.  
**Active:** `V25_BOUNDARY_SYNDROME_KEY_HALF_SEPARABILITY_AUDIT`.

1. Use frozen plan `research/v25/half-key-separability/V25_BOUNDARY_SYNDROME_KEY_HALF_SEPARABILITY_PLAN.json`.
2. W5_SINGLE b16 only; logical split 8+8; targets `[43051,21863,31754,45567]` only.
3. Build exact 256x256 low16 syndrome table for each target.
4. Compute exact rectangle residual and stable exact XOR-separable bit positions.
5. Primary PASS requires >=8 identical exact bit positions across all four targets, true half pair retained 4/4, and <=512 signature matches per target.
6. GF(2) ranks/residual density/SVD are diagnostics only and cannot rescue primary FAIL.
7. Only on primary PASS freeze a separate MITM scaling/TOTAL protocol.
8. On FAIL close simple half-key XOR-separability immediately; no second target set.
9. Commit source/tests/results/decision/manifest and continuity.

No alpha<1 or full-round claim from this Stage0 structural audit.
