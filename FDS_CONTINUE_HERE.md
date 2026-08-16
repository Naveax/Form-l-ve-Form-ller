# FDS_CONTINUE_HERE

**State:** `NO_GO_BORROW_SIGNATURE`  
**Next:** `V25_INTERNAL_ROUND_BOUNDARY_CANDIDATE_TRAJECTORY_SYNDROME_AUDIT` Stage0.

1. Fresh main + authority.
2. Use frozen `research/v25/boundary-syndrome/V25_INTERNAL_ROUND_BOUNDARY_SYNDROME_CONE_PLAN.json`.
3. Enumerate exact word-level QR dependency cones for splits 1..5 and all 16 boundary words.
4. Select minimum total cone by structural cost only, tie smaller split then word.
5. Implement partial forward/inverse execution and compare target word exactly with full-state reference on random states.
6. If cone is not <24 QR or equivalence fails, close immediately.
7. If PASS, explicitly record constant-factor-only status; only then freeze Stage1 syndrome selectivity/cost targets.
8. Commit source/tests/results/decision/manifest and update continuity.

Stop: no target-output tuning in Stage0, no solver/ML rescue, no alpha claim from QR-count reduction.
