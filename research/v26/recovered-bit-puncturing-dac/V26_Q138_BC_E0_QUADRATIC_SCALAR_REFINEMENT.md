# V26 Q138 B/C grouped-e0 quadratic scalar refinement

## Question

PR #112 and PR #113 establish a useful local linear-signature separator geometry for grouped-e0 factors on the shared 149-bit domain. The omitted piece is the scalar quadratic phase of each reachable e0 sector.

This note tests a deliberately strong exact route: extend each local support/frequency signature by the minimum additional **linear** information required to determine every sector scalar quadratic bit individually.

## Exact refinement theorem

Let `A_g` be the PR #112 local row space for support group `g`, and let `q_i` be the scalar Boolean quadratic of sector `i` restricted to the 128 predecessor plus 21 right-beta shared coordinates, with the 11 left-beta coordinates set to zero.

A hidden direction `h in ker(A_g)` preserves `q_i` on every fiber iff

`q_i(x+h) = q_i(x)` for all `x`.

For a Boolean quadratic this is equivalent to both:

1. `h` lies in the radical of the restricted polar bilinear form;
2. `q_i(h) = q_i(0)`.

Intersecting these exact conditions over every sector in the group gives the largest hidden subgroup `K_g` on which all sector scalar bits are invariant. Therefore `K_g^perp` is the minimum row space, among linear signatures extending `A_g`, that determines all sector scalar bits individually.

The implementation verifies the final hidden subgroup basis directly against every restricted polar row and every scalar delta.

## Clean run 34197928053

### B

Original local ranks were 20..28. After the minimum sectorwise scalar refinement:

- refined local ranks: `144:2, 145:46, 146:79, 147:67, 148:35, 149:22`
- extra rank over the PR #112 signature: `119:1, 121:11, 122:27, 123:34, 124:91, 125:80, 126:7`
- groups requiring zero extra rank: `0`
- groups refined all the way to rank 149: `22`
- best displayed deterministic balanced cut: `lambda = 147`
- every tested deterministic path ordering has maximum `lambda = 149`

### C

Original local ranks were 19..27. After sectorwise scalar refinement:

- refined local ranks: `145:43, 146:102, 147:52, 148:45, 149:8`
- extra rank: `120:1, 121:10, 122:37, 123:64, 124:52, 125:70, 126:14, 127:2`
- groups requiring zero extra rank: `0`
- groups refined to rank 149: `8`
- best displayed deterministic balanced cut: `lambda = 147`
- every tested deterministic path ordering has maximum `lambda = 149`

## Decision

`NO_SECTORWISE_LINEAR_SCALAR_SEPARATOR_GAIN`

The strong strategy of making each sector scalar quadratic individually a function of a refined local linear signature destroys essentially all of the PR #112/113 separator gain. A scalar-aware recursive tree over these sectorwise-refined row spaces is therefore not a useful next computation: the displayed path width already saturates at the full shared dimension 149.

## What this does not close

This is not a no-go theorem for the aggregate grouped-e0 factor. The sectorwise requirement is stronger than the actual grouped calculation may require. Sectors sharing the same affine support occur with multiplicities 1, 2, or 4 and may exhibit exact cancellation or collapse after they are combined.

The surviving route is therefore:

1. derive the exact same-support aggregate observable actually needed by grouped-e0;
2. combine/cancel sector scalar phases before asking for a local state representation;
3. measure the minimal dependence of the aggregate factor, not of each constituent sector separately;
4. only then re-run separator/tree analysis.

Existing exact same-support phase-combination machinery on the e1 side and the fixed-predecessor e0 aggregation code provide the canonical implementation starting points, but no aggregate-e0 theorem is claimed by this note.

## Frozen regression

`scripts/verify_v26_q138_bc_e0_quadratic_scalar_refinement_result.py` recomputes and freezes the clean-run result. The `pr` field returned by `full_corrected_phase` is recorded as `phase_internal_pr_histogram`; it is intentionally not relabeled as a polar-radical dimension.

## Not claimed

No claim is made about optimal branchwidth, aggregate grouped-e0 scalar dependence, grouped-e0 carry values, e0-half cross-carry, complete B2/C2, `W_repr`, `alpha < 1`, arithmetic-work reduction, ranking/search advantage, or full-round compression. `ALPHA_PASS=0` remains unchanged.
