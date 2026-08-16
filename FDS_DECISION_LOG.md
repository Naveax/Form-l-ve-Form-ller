# FDS_DECISION_LOG

## 2026-08-16 — Issue #8 strict scaling
Strict raw-survivor uniqueness family remains `NO_GO_STRICT_MULTI_LAYOUT_SCALING_GATE`. Do not reinterpret it.

## 2026-08-16 — Issue #9 collision-tolerant verified screening
Fresh protocol completed without retuning. Generated code matched generic reference for 696,320 full syndrome values and 696,320 direct predicates. True key survived 32/32 fresh cases; exact verification returned only the true key 32/32. Seven cases had raw syndrome collisions, all removed by the already-accounted verifier. All 32 wall cases showed positive speedup; all 8 layout×width gate cells passed.

Decision: `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`. This admits a reduced-model end-to-end constant-factor verified-screen optimization only. Leading enumeration remains `2^b`, alpha=1, and no full-round claim is made.

## Next
Stop accumulating constant-factor variants. Reopen only structural exponent-reduction hypotheses under fresh preregistration, beginning with half-key separability of the boundary-syndrome function.
