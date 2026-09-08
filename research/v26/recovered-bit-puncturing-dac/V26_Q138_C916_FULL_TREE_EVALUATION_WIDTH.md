# V26 q=138 C916 full-tree realizable evaluation width

## Result

Starting from the exact C aggregate grouped-e0 degree-2 function-space tree with function-space width 70, evaluate every one of its 498 non-root edges using the shared affine fiber geometry.

The resulting safe full-tree realizable evaluation-state upper bound is

\[
\boxed{W_{\mathrm{eval},C}\le 65}.
\]

This is strictly below the function-space width 70. It is still an upper bound because edges whose residual remains genuinely quadratic on the affine kernel are intentionally left at the conservative residual-dimension envelope.

## Edge classification

Across all 498 non-root edges:

- residual-zero edges: 175,
- fiber-affine residual edges: 372,
- fiber-quadratic residual edges: 126.

For a fiber-affine edge the genuine quadratic quotient becomes affine-linear after conditioning on the shared affine separator label. Its residual rows on the affine kernel are therefore controlled by the exact span of the origin rows and all 149 coordinate translation effects. The rank of this common kernel-dual row space is a uniform all-fiber residual-rank upper bound.

For a fiber-quadratic edge no such reduction is assumed; the conservative affine-label-rank plus residual-dimension envelope is retained.

## Former width-70 edge

The unique function-space-width-70 edge is `[110,166)`.

It has:

- function lambda 70,
- shared affine dimension 57,
- varying affine-label rank 56,
- genuine quadratic residual dimension 13,
- affine-kernel dimension 93,
- common kernel-dual residual-row rank 4,
- translation-matrix control rank 4.

Thus its safe evaluation width is only 60 bits. The separate exact all-fiber certificate gives 729583139634020352 realizable shared evaluation tuples on this edge.

## Unique 65-bit edge

After the edge-by-edge reduction, the unique remaining 65-bit edge is `[166,199)`.

Its geometry is:

- function lambda 68,
- shared affine function dimension 63,
- varying affine-label rank 62,
- affine-kernel dimension 87,
- genuine quadratic residual dimension 5,
- common kernel-dual residual-row rank 3,
- translation-matrix control rank 3.

The exact 3-dimensional control image contains 8 states. Their residual-rank histogram is

`{1:1, 2:2, 3:5}`.

Each control state represents exactly `2^59` affine labels. Therefore the exact number of realizable shared-evaluation tuples on this edge is

\[
2^{59}(1\cdot 2+2\cdot 4+5\cdot 8)
=28823037615171174400.
\]

Its binary ceiling is still 65 bits. Every other tree edge has a certified safe upper bound of at most 64 bits, so exact enumeration of this edge does not reduce the full-tree ceiling below 65.

## Interpretation

This certificate separates three notions that were previously easy to conflate:

1. degree-2 function-space width: 70;
2. safe realizable evaluation width: 65;
3. exact tuple counts on selected fiber-affine edges, which can be substantially below the corresponding power-of-two envelope without changing the bit ceiling.

The result shows that treating every genuinely quadratic shared function as an independent separator state bit is unnecessarily strong. It does **not** yet establish an exact contraction-state count for every edge because 126 edges retain genuine quadratic behavior on their affine kernels.

## Next target

The next useful edge is the 64-bit fiber-quadratic edge `[55,110)`:

- function lambda 64,
- shared affine dimension/rank 52,
- affine-kernel dimension 97,
- quadratic residual dimension 12,
- at least one residual basis element retains nonzero polar form on the kernel.

Use the exact quadratic Gauss primitive to analyze the residual image on its affine fibers. This can determine whether its conservative 64-bit envelope is actually tight or can be reduced, after which the remaining 63-bit and lower edges can be ranked by necessity rather than processed indiscriminately.

## Scope exclusions

No claim is made here for aggregate e0 carry completion, support/e1 carry, half cross-carry, complete C2, `W_repr`, arithmetic work, alpha, ranking/search, or full-round cost.

`ALPHA_PASS=0`.
