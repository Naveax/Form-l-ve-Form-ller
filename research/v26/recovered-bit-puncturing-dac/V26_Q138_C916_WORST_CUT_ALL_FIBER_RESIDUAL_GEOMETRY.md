# V26 q138 C916 worst-cut all-fiber residual geometry

## Scope

This note freezes the exact realizability geometry of the unique width-70 edge of the merged C916 degree-2 function-space separator tree. It is a shared-evaluation certificate for that one edge, not a complete grouped-e0 carry or complete C2 theorem.

`ALPHA_PASS=0`.

## Starting function-space certificate

The unique edge `[110,166)` has

- function-space intersection dimension: `70`,
- shared affine function dimension: `57`,
- varying affine-label rank: `56`,
- genuine quadratic residual dimension: `13`.

The shared affine kernel therefore has dimension `149-56 = 93`.

## Fiber restriction

On the 93-dimensional affine kernel K, every one of the 13 residual quadratic polar forms vanishes on `K x K`. Hence each residual becomes affine-linear on every affine separator fiber.

For the origin fiber, the 13 residual linear rows have rank `4`, giving exactly 16 residual outputs with `2^89` preimages each.

## Uniform all-fiber theorem

Moving the affine-fiber representative by a shared coordinate changes each residual row by the corresponding polar derivative restricted to K. Across all 13 residuals and all 149 shared-coordinate directions there are `13*149 = 1937` such translation-effect rows.

The exact GF(2) rank of

`span(origin residual rows, all translation-effect rows) subset K*`

is only `4`.

Therefore every affine fiber has residual rank at most 4. Since the origin fiber has rank 4, the maximum fiber residual rank is exactly 4.

## Exact all-fiber distribution

The 149 translation-effect matrices span a 4-dimensional matrix space. The translation map factors through the 56-dimensional affine-label quotient, so each of its 16 matrix-image states is attained by exactly `2^(56-4)=2^52` affine labels.

Enumerating those 16 matrix states gives the exact residual-rank histogram

- rank 1: 1 control state,
- rank 2: 2 control states,
- rank 3: 7 control states,
- rank 4: 6 control states.

Thus among all `2^56` affine fibers:

- rank 1 occurs on `1*2^52` fibers,
- rank 2 occurs on `2*2^52` fibers,
- rank 3 occurs on `7*2^52` fibers,
- rank 4 occurs on `6*2^52` fibers.

## Exact shared-evaluation tuple count

For a fiber with residual rank r, exactly `2^r` residual outputs are realized. Since the 56-bit affine label distinguishes fibers, the exact number of realizable shared evaluation tuples on this edge is

`2^52 * (1*2 + 2*4 + 7*8 + 6*16)`

`= 2^52 * 162`

`= 729583139634020352`.

This is 63.28125% of `2^60`. Its binary ceiling remains 60 bits, but unlike the earlier `2^60` envelope this is the exact tuple count for this edge.

## Interpretation

The degree-2 function-space width `70` substantially overstates the number of realizable evaluation states. On the worst function-space edge, 13 formally independent quadratic residual functions collapse fiberwise to a rank-at-most-4 affine-linear family.

This does **not** yet certify a full-tree width of 60 or lower. Other edges must undergo the same all-fiber realizability calculation. The next step is therefore an edge-by-edge evaluation-state certificate over all 498 non-root edges of the same tree.

Not included: aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, or full-round claims.
