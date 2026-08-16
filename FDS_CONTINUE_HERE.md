# FDS_CONTINUE_HERE

**State:** `NO_GO_PUBLIC_CARRY_SIGNATURE`  
**Next:** `V25_OUTPUT_CONDITIONED_FEEDFORWARD_BORROW_SIGNATURE_AUDIT`  
**Backlog:** GitHub Issue #4 after creation.

## Continuation
1. Fresh main + mandatory authority reading.
2. Use frozen borrow plan under `research/v25/borrow-transition/`.
3. Build exactly 12 fresh targets over the reused 32-pair pool.
4. Compute word4 feed-forward subtraction borrow descriptors over all 1,024 candidates without singling out the true key.
5. Fixed Ridge(alpha=1) grouped CV vs fresh-target public-carry control.
6. Run 256 within-target label-permutation null; all six gates must pass.
7. PASS -> untouched descriptor-only ranking validation. FAIL -> stop summary-statistic descriptor search and pivot to non-aggregated algebraic self-consistency across trajectories/round boundaries.
8. TOTAL accounting + source/tests/results/manifest + continuity closure to GitHub.

## Stop rules
No second development set; no score-shape/RMS/tail/C1 features added to rescue borrow; no feature threshold retuning after oracle inspection; no alpha/full-round claim.
