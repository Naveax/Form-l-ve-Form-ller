# V26 q138 C916 e0 first-dyadic common-left block spans

## Common coordinates

Use one exact 160-coordinate representation split as 149 shared predecessor/right variables plus 11 common local-left variables. Each first-dyadic phase is decomposed into a local linear block, a local quadratic block, and a shared-to-local bilinear block.

The local quadratic ambient space has 55 coefficients and the shared/local bilinear ambient space has 1639 coefficients.

## Exact result

### All 340 anchor phases

- local quadratic span rank: `11`
- local linear span rank: `11`
- local polynomial span rank: `23`
- cross-matrix coefficient span rank: `237`
- joint shared-to-local frequency control rank: `145`
- per-term cross-rank histogram: `{10:8, 11:332}`

Thus the common local quadratic content occupies only 11 dimensions of the 55-dimensional ambient local quadratic space. This does not by itself imply an 11-bit separator state, because the shared input controls the term-specific local frequencies with rank 145.

### Singleton anchors

For the 103 singleton terms:

- local quadratic span rank: `7`
- local linear span rank: `9`
- local polynomial span rank: `16`
- cross-matrix coefficient span rank: `86`
- joint shared-to-local frequency control rank: `45`
- per-term cross rank: `{10:7, 11:96}`

### Pair anchors

For the 237 signed pair anchors:

- local quadratic span rank: `11`
- local linear span rank: `11`
- local polynomial span rank: `23`
- cross-matrix coefficient span rank: `169`
- joint shared-to-local frequency control rank: `144`
- per-term cross rank: `{10:1, 11:236}`

By multiplicity, the joint shared-control ranks are `53` for multiplicity 2 and `118` for multiplicity 4.

### Pair equality differences

For the 237 equality differences:

- local quadratic span rank: `9`
- local linear span rank: `11`
- local polynomial span rank: `21`
- cross-matrix coefficient span rank: `98`
- joint shared-to-local frequency control rank: `87`
- per-term cross rank: `{1:46, 2:88, 3:73, 4:24, 5:6}`

## Interpretation

Decision:

`COMMON_LEFT_QUADRATIC_SPAN_11_SHARED_CONTROL_145`

The shared local-left variables create a compact common quadratic block, but the shared-to-local bilinear control remains high-dimensional. The correct next representation must combine this block structure with support/frequency constraints and signed first-dyadic arithmetic instead of independently charging one local state per support group.

The full-coordinate representative is valid but not proven gauge-minimal modulo the support constraints. Further support-gauge reductions may therefore exist.

## Scope

This is an exact representation diagnostic, not a minimal separator-state theorem. No grouped-e0 carry width, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`
