# V26 q=138 C916 width-64 quadratic edge: exact all-fiber image

## Result

The fiber-quadratic edge `[55,110)` of the C916 separator tree has conservative safe evaluation width 64, but its exact shared-evaluation geometry is much smaller.

Its exact all-fiber shared-evaluation tuple count is

\[
\boxed{900719925474099200},
\]

with binary ceiling

\[
\boxed{60\text{ bits}}.
\]

This does not change the already certified full-tree width 65 because the exact `[166,199)` edge remains the unique 65-bit bottleneck.

## Origin affine fiber

The edge has:

- function lambda 64,
- shared affine dimension/rank 52,
- affine-kernel dimension 97,
- genuine quadratic residual dimension 12.

Exactly one residual basis element has nonzero polar form on the affine kernel. The restricted polar space therefore has rank 1.

Evaluating all `2^12 = 4096` residual Fourier characters by exact quadratic Gauss elimination gives:

- polar-rank histogram `{0:2048, 88:2048}`,
- 4080 zero Gauss characters,
- 16 nonzero characters,
- every nonzero character has absolute value `2^97`,
- residual image size 256,
- 3840 missing residual outputs,
- every realized output has exactly `2^89` preimages.

Thus the origin-fiber residual map uses only 8 effective output bits rather than the 12-dimensional function-space quotient.

## All-fiber structure

Choose the 12 residual coordinates so that 11 have zero polar form on the affine kernel and one carries the unique nonzero polar direction. Write these as the affine residual map `L` and one quadratic coordinate `q`.

The fixed restricted polar form of `q` has rank 88 on the 97-dimensional kernel, hence radical dimension 9. A maximal totally isotropic subspace therefore has dimension

\[
9+88/2=53.
\]

For any value of the 11 affine residual coordinates, the corresponding `L`-fiber kernel has dimension at least

\[
97-11=86>53.
\]

Consequently the rank-88 polar form cannot vanish on an `L`-fiber kernel. Therefore `q` cannot be constant on any `L` fiber and always doubles the image of `L`.

Across affine separator labels, the translation matrices controlling `L` span only a 3-dimensional matrix space. Its eight exact control states have affine-residual rank histogram

`{5:1, 6:2, 7:5}`.

Each control state represents `2^49` affine labels. Hence the exact number of shared evaluation tuples is

\[
2^{49}\left(1\cdot2^{6}+2\cdot2^{7}+5\cdot2^{8}\right)
=900719925474099200.
\]

The maximum residual image size on every affine fiber is exactly 256, so this edge has exact 60-bit ceiling after combining the 52 affine-label bits with the all-fiber residual distribution.

## Interpretation

The edge was classified as fiber-quadratic by the generic safe evaluator because one residual polar survives on the affine kernel. That classification is correct but conservative. The one-dimensional polar structure is sufficiently rigid that the residual family decomposes into an affine map plus one fixed high-rank quadratic coordinate, making an exact all-fiber calculation possible without enumerating `2^52` separator labels.

This suggests a reusable refinement for other fiber-quadratic edges whose restricted polar space has rank 1: isolate the unique polar coordinate, control the affine residual rows by the translation-matrix image, and use the maximal-totally-isotropic dimension of the fixed polar form to decide whether the quadratic coordinate doubles every affine residual fiber.

## Scope

This is an exact certificate for one edge. It does not reduce the already-certified full-tree 65-bit ceiling, which is attained exactly by `[166,199)`. It does not establish aggregate e0 carry completion, support/e1 carry, half cross-carry, complete C2, `W_repr`, arithmetic work, alpha, ranking/search, or full-round cost.

`ALPHA_PASS=0`.
