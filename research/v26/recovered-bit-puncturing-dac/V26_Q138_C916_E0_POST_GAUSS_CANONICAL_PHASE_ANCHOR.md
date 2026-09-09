# V26 Q138 C916 e0 post-Gauss canonical phase anchor

## Status

Exact diagnostic result for the C grouped-e0 local-Gauss phase geometry after the frozen first-dyadic pairing authority.

Decision:

`CANONICAL_SINGLETON_PHASE_ANCHOR_REQUIRES_REFINEMENT`

`ALPHA_PASS=0`

This note does **not** claim a complete grouped-e0 separator, complete C2, `W_repr`, arithmetic work, alpha improvement, ranking/search improvement, or full-round result.

## Motivation

The merged local-Gauss quotient result established that all 577 reachable C e0 sectors have nonzero exact Gauss transforms, but each individual normalized sign has high quotient polar rank 130-136.

The merged transformed-pair result then showed a strong cancellation of that high-rank body inside the frozen first-dyadic pairs: among 209 overlapping selected pairs, sign-difference polar ranks are `{0:203, 2:6}`.

The next question is whether one transformed sign can serve as a common phase anchor across distinct support groups.

## Gauge-free physical pullback

No arbitrary 149-bit ambient quadratic extension is introduced.

For each transformed sector:

1. reconstruct the exact common-support affine parametrization in the original 160-bit support coordinates;
2. split the support coefficient space into the shared projection and local fiber exactly as in the merged local-Gauss authority;
3. perform the same exact local Gauss elimination;
4. map the surviving radical-compatible shared quotient back to the physical 149 shared bits;
5. derive the exact affine constraints for that physical support;
6. retain the normalized sign only in its own physical-support coordinates.

For two transformed sectors, their physical affine supports are intersected exactly. The intersection basis is then solved separately in each side's own coordinates, and the two normalized signs are restricted to that common basis before taking their difference.

Thus every reported sign-difference polar rank is intrinsic to the true physical support intersection.

## Regressions

The pullback implementation first checks 576 ordered synthetic 5-bit affine-anchor pairs by explicit truth-table evaluation.

It then reproduces the merged transformed-pair authority for all 237 frozen selected pairs in physical coordinates.

Support relations reproduce exactly:

`{disjoint:28, equal:6, left_subset_right:4, overlap_incomparable:112, right_subset_left:87}`.

For the 209 overlapping frozen pairs, sign-difference polar ranks reproduce exactly:

`{0:203, 2:6}`.

This is the authority check that the cross-group physical coordinate machinery has not introduced a quadratic gauge artifact.

## Canonical root

The canonical root is the lexicographically first singleton transformed sector:

- group id: `1`
- sector index: `0`
- multiplicity: `1`
- physical support dimension: `140`
- physical support codimension: `9`
- normalized sign polar rank: `132`
- `log2(abs(G))`: `5`

There are 577 transformed sectors in total.

The frozen first-dyadic role split is:

- term anchors: `340`
  - 103 singleton anchors
  - 237 selected pair anchors
- selected pair mates: `237`

The canonical root itself is one of the 340 term anchors, so it is compared with 576 other transformed sectors and with 339 other term anchors.

## Root versus all transformed sectors

Physical support relations:

`{disjoint:222, left_subset_right:21, overlap_incomparable:333}`.

There are no equal-support or right-subset-root cases for this root.

For the 354 overlapping comparisons, physical intersection dimensions are:

`{136:62, 137:102, 138:147, 139:22, 140:21}`.

Equivalently, intersection codimensions inside the 149-bit shared domain are:

`{9:21, 10:22, 11:147, 12:102, 13:62}`.

Overlap sign-difference polar ranks are:

`{0:219, 2:120, 4:15}`.

Phase types are:

`{affine_nonconstant:219, quadratic_nonconstant:135}`.

No overlap has a constant sign difference.

Therefore the canonical root does expose a substantial common quadratic body, but it is not a global anchor: 222 transformed supports are disjoint from it, and 15 overlapping sectors still require rank-4 quadratic correction.

## Root versus the 340 first-dyadic term anchors

Excluding the root itself, 339 term anchors remain.

Support relations:

`{disjoint:139, left_subset_right:18, overlap_incomparable:182}`.

The 200 overlapping term anchors have sign-difference polar ranks:

`{0:149, 2:45, 4:6}`.

Thus one root covers only 200 of the other 339 term anchors, with six rank-4 exceptions even inside that overlap set.

This rules out the simple representation "one canonical phase anchor plus only affine/rank-2 corrections for every first-dyadic term".

## Root versus the 237 selected pair mates

Support relations:

`{disjoint:83, left_subset_right:3, overlap_incomparable:151}`.

The 154 overlapping mates have sign-difference polar ranks:

`{0:70, 2:75, 4:9}`.

Again, one root is insufficient.

## Interpretation

The result is still structurally useful.

The individual normalized signs have polar rank 130-136, while cross-group differences against this root never exceed rank 4 on an overlap. The high-rank part is therefore strongly shared across distinct support groups, not merely inside the frozen same-support pairs.

The obstruction is coverage, not a return to rank-130 complexity:

- many physical supports are disjoint from this particular root;
- a small number of overlaps need rank-4 correction.

The natural next object is therefore a low-rank overlap cover/forest on the 340 first-dyadic term anchors rather than a single global root.

## Next pass

Build a deterministic cover/forest over the 340 term anchors using exact physical support intersections.

Prefer edges lexicographically by:

1. non-disjoint physical overlap;
2. smaller intrinsic sign-difference polar rank;
3. lower intersection codimension / larger intersection dimension;
4. stable endpoint ordering.

Measure:

- number of connected components when only rank-0 edges are allowed;
- number of components when rank-0/2 edges are allowed;
- whether rank-4 edges are actually necessary for connectivity;
- maximum correction rank in a deterministic spanning forest;
- component/root counts needed to cover all 340 term anchors.

Only after that cover is understood should the common phase section be factored into a complete first-dyadic message-state representation.

## Scope exclusions

Not included:

- complete grouped-e0 carry separator;
- support/e1 carry;
- half cross;
- complete C2;
- `W_repr`;
- arithmetic-work bound;
- alpha bound;
- ranking/search claim;
- full-round claim.

`ALPHA_PASS=0`
