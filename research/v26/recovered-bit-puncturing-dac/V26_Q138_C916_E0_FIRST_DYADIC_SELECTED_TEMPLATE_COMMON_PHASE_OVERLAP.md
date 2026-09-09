# V26 q138 C916 e0 selected-template common-phase overlap

## Purpose

Test whether the exact deterministic phase-template selections from the R2/R4/R6/R8 Pareto authorities are merely restrictions of one common phase, up to one constant bit per selected template.

This is a deliberately cheap gate before any ambient 149-bit quadratic extension solve. If two selected templates have overlapping physical supports and their normalized sign difference is nonconstant on that overlap, then no single phase on the union can restrict to both templates modulo constants.

## Exact gate

For every selected-template pair, intersect the two physical supports and restrict the sign difference to that intersection. Classify the result as:

- constant;
- affine nonconstant;
- quadratic nonconstant.

If all overlap differences were constant, the constant difference bits would have to form a consistent GF(2) cocycle, equivalent to choosing one constant offset per template. This pass checks that condition too.

In the actual C916 selections, the stronger obstruction occurs first: **there are no constant physical-overlap edges at all** for R2, R4, R6 or R8.

## R2 / 39-template result

There are 741 template pairs:

- 284 disjoint;
- 123 equal-support;
- 334 overlap-incomparable.

Thus there are 457 physical-overlap edges. Their sign-difference polar-rank histogram is

`{0:34, 2:139, 4:111, 6:136, 8:37}`.

Type histogram:

`{affine_nonconstant:34, quadratic_nonconstant:423}`.

Constant overlap edges: **0**.

The physical-overlap graph has component sizes `[35,1,1,1,1]`.

## R4 / 22-template result

There are 231 template pairs:

- 95 disjoint;
- 6 equal-support;
- 130 overlap-incomparable.

There are 136 physical-overlap edges, with polar-rank histogram

`{0:18, 2:66, 4:23, 6:29}`

and type histogram

`{affine_nonconstant:18, quadratic_nonconstant:118}`.

Constant overlap edges: **0**.

Physical-overlap component sizes: `[18,1,1,1,1]`.

## R6 / 18-template result

The structural-minimum 18-template selection has 153 template pairs:

- 71 disjoint;
- 82 overlap-incomparable.

There are no equal-support pairs because exactly one template is selected per maximal support class.

All 82 physical overlaps are nonconstant. Polar-rank histogram:

`{0:14, 2:56, 4:12}`.

Type histogram:

`{affine_nonconstant:14, quadratic_nonconstant:68}`.

Constant overlap edges: **0**.

Physical-overlap component sizes: `[14,1,1,1,1]`.

## R8 / 18-template result

Again there are 153 pairs, 71 disjoint and 82 overlap-incomparable.

All 82 physical overlaps are nonconstant. Polar-rank histogram:

`{0:16, 2:46, 4:12, 6:8}`.

Type histogram:

`{affine_nonconstant:16, quadratic_nonconstant:66}`.

Constant overlap edges: **0**.

Physical-overlap component sizes: `[14,1,1,1,1]`.

## Decision

For all four frozen Pareto selections,

\[
\boxed{\text{no common phase on the selected-support union modulo template constants}}
\]

because every physical overlap already has a nonconstant sign difference.

Decision:

`SELECTED_TEMPLATE_COMMON_PHASE_ON_UNION_REFUTED_FOR_R2_R4_R6_R8`.

The constant-edge cocycle is vacuously consistent because it has no edges; each template is an isolated vertex in that compatibility graph. This is not evidence for gluing. The physical-overlap graph itself contains many edges, and every one of them violates constant compatibility.

## Consequence

There is no reason to build the much larger ambient quadratic-extension system for these selected templates: an ambient common phase would restrict to a common phase on every physical overlap, which is already contradicted.

This closes the strongest single-common-template-phase interpretation of the 18-template R6/R8 structure. It does **not** refute phase aggregation more generally. In particular, exact grouped first-dyadic integer/Gauss arithmetic can still have smaller evaluation-state complexity than independently carrying each template/residual phase.

The next useful target should therefore act on the **actual grouped arithmetic function**, not try to identify all selected templates with one common quadratic phase.

## Scope exclusions

No aggregate grouped-function stabilizer or evaluation-state count, no complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search or full-round result is claimed.

`ALPHA_PASS=0`.
