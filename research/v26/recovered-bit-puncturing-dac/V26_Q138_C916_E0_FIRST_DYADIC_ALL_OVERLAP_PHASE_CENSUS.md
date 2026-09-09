# V26 Q138 C916 C e0 Complete First-Dyadic Overlap Phase Census

## Status

Frozen exact result over every unordered pair of the 340 first-dyadic term anchors after exact local Gauss elimination.

Decision:

`FIRST_DYADIC_ALL_OVERLAP_SUPPORT_GRAPH_MULTIPLE_COMPONENTS`

`ALPHA_PASS=0`.

## Exact census

The 340 anchors give 57,630 unordered pairs.

- physical-overlap pairs: **29,996**
- physical-disjoint pairs: **27,634**

Support relations:

`{disjoint:27634, equal:378, left_subset_right:2269, overlap_incomparable:24026, right_subset_left:3323}`

Every one of the 29,996 physical-overlap pairs was phase-evaluated on its true intersection. Intrinsic normalized-sign difference polar ranks are:

`{0:13812, 2:9821, 4:4972, 6:1296, 8:95}`

Phase types:

`{affine_nonconstant:13808, constant:4, quadratic_nonconstant:16184}`

Intersection codimensions in the 149-bit physical shared space:

`{7:363, 8:376, 9:3826, 10:2624, 11:11250, 12:3096, 13:8131, 14:120, 15:210}`

## Exact component structure

Rank-0 edges give 9 components with sizes:

`[325,2,2,2,2,2,2,2,1]`

For every threshold 2, 4, 6 and 8 the component structure is already:

`[332,2,2,2,2]`

with stable roots:

`[(0,0),(158,0),(180,0),(236,0),(238,0)]`

The complete physical-support overlap graph itself has exactly the same five components. Therefore the four 2-anchor components are not separated from the dominant 332-anchor component by rank-6/rank-8 phase corrections. They are separated because there is **no physical support overlap at all**.

Exact cross-component physical-overlap count with respect to the rank<=4 components:

**0**.

The four 2-anchor components each contain one rank-0 internal edge. All rank-2/4/6/8 edges belong to the dominant 332-anchor component.

## Consequence for phase charts

Five physical phase charts are genuinely required at this support-cover level. They can be treated independently because no shared input activates anchors from different components.

Inside the dominant chart, however, direct pairwise sign-difference rank reaches 8. Thus connectivity by rank<=2 edges must not be confused with a rank<=2 residual representation. A common chart-local quadratic template whose residual polar rank is bounded by R must satisfy `2R >= 8`; consequently **R >= 4** is a necessary lower bound.

This is only a lower bound. Existence of a chart-local common template with residual rank <=4 is not implied by the pairwise census and must be tested as a separate gluing/extension problem.

## Next exact target

Solve the chart-local quadratic gluing problem:

- one independent common phase template for each of the five physical-support components;
- exact restriction to every anchor support;
- minimize the maximum residual polar rank;
- first test the now-sharp candidate bound `R=4` on the 332-anchor component;
- verify the four 2-anchor components separately, where their internal difference is already affine/rank 0.

Only after a valid common-template decomposition exists should residual phase information be attached to the merged 149-bit radical-support separator and recursive cut width be recomputed.

## Scope exclusions

No complete grouped-e0 separator theorem, quotient-aware first-dyadic message-state width, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work reduction, `alpha < 1`, ranking/search improvement, or full-round claim is made.
