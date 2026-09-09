# V26 Q138 C916 C e0 Maximal-Support Phase Template Cover

## Status

Frozen constructive post-Gauss phase-template result.

Precise frozen decision:

`MAXIMAL_SUPPORT_ANCHOR_TEMPLATE_COVER_RESIDUAL_POLAR_RANK2`

`ALPHA_PASS=0`.

## Construction

The 340 frozen first-dyadic term anchors are represented on exact physical affine supports in the 149-bit shared domain. A template is allowed to cover an anchor only when the anchor support is contained in the template support. Therefore the template sign is defined on every point where the covered anchor is active; no ambient quadratic extension and no path-only overlap argument is used.

The candidate template set is the set of actual support-maximal anchors.

## Exact support structure

- anchors: 340
- physical support components: 5
- component sizes: `[332,2,2,2,2]`
- support-maximal anchors: **52**
- maximal support dimensions: `{140:4, 142:48}`
- maximal support equal classes: **15**
- equal-class sizes: `{1:13, 18:1, 21:1}`
- maximal anchors by physical component: `{0:48, 1:1, 2:1, 3:1, 4:1}`

Every anchor has either 1, 18 or 21 containing maximal-anchor candidates:

`{1:24, 18:201, 21:115}`.

## Exact residual result

For every anchor, choose the containing maximal anchor minimizing the intrinsic direct sign-difference polar rank on the **entire child support**.

Minimum direct residual polar ranks:

`{0:222, 2:118}`

Thus:

- rank 0 covers 222/340 anchors;
- rank <=2 covers **340/340** anchors;
- maximum minimum residual polar rank is exactly **2**.

By role:

- pair anchors: `{0:144, 2:93}`
- singleton anchors: `{0:78, 2:25}`

Residual phase types:

`{affine_nonconstant:170, constant:52, quadratic_nonconstant:118}`.

The direct construction initially uses all 52 support-maximal anchors as templates because each maximal anchor trivially selects itself at rank 0. This is not a minimum-template claim.

## Why this is stronger than the previous R>=4 observation

The complete overlap census showed direct pairwise differences up to rank 8, which forces residual rank at least 4 **if a single common template is required for an entire physical chart**. This pass allows multiple support-maximal templates inside a chart and proves a strictly stronger constructive result: every anchor has a containing real-anchor template with residual rank at most 2.

So the previous `R>=4` lower bound applied only to the single-template-per-chart model. It does not apply to this multi-template containment cover.

## Next exact target

The 52-template construction is deliberately unoptimized. Because maximal supports form only 15 equality classes, the next pass should solve an exact set-cover problem separately in the five physical support components:

- candidate roots: the 52 support-maximal anchors;
- a root covers an anchor iff support containment holds and direct residual polar rank is <=R;
- solve minimum template count for `R=0`, `R=2`, and `R=4`;
- freeze exact root sets and assignment certificates;
- in particular determine the minimum root count for the now-proven sufficient threshold `R=2`.

Only after template-count minimization should the residual rank-0/2 functions be converted into minimal linear signatures and attached to the merged radical-support separator. Pair-mate corrections must be charged separately. The high-rank common template signs are still an explicit signed-arithmetic blocker and are not declared free.

## Scope exclusions

No complete grouped-e0 separator theorem, optimized template count, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work reduction, `alpha < 1`, ranking/search improvement, or full-round claim.
