# V26 q138 C916 e0 first-dyadic signed-pair anchor geometry

## Exact signed residual

For every selected pair in the first grouped-e0 dyadic residual, the exact term is

\[
(-1)^{q_i}\,\mathbf 1[q_i\oplus q_j=0].
\]

The rank-two equality difference `q_i xor q_j` is therefore only one factor. This certificate measures the missing anchor phase `q_i` on the same common-support local fiber used by the complete first-dyadic fiber certificate.

## Exact result

There are 237 signed pair terms across 147 even-multiplicity support groups.

The anchor restricted polar-rank histogram is

`{142:163, 144:74}`.

By support multiplicity:

- multiplicity 2: `{142:33, 144:24}`
- multiplicity 4: `{142:130, 144:50}`

For multiplicity 4, the two selected pair slots have identical histograms `{142:65, 144:25}`.

Relative to the local fiber, the anchor geometry is:

- local-to-all polar rank: `{7:37, 8:130, 9:70}`
- local-local polar rank: `{4:60, 6:138, 8:39}`
- local linear restriction: `{1:237}`
- fiber category: `{local_quadratic:237}`
- anchors descending to the shared quotient: `0`

The equality-difference categories remain `{local_quadratic:132, shared_local_bilinear:105}`. Jointly:

- `132` terms are `local_quadratic|local_quadratic`
- `105` terms are `local_quadratic|shared_local_bilinear`

## Interpretation

Decision:

`SIGNED_PAIR_ANCHOR_IS_ALWAYS_LOCAL_QUADRATIC`

The low rank of the equality condition does not make the complete signed pair residual low-rank on the shared separator domain. Every selected pair carries a high-rank, local-quadratic anchor phase in addition to the rank-two equality condition.

Consequently a valid grouped-e0 carry representation must preserve both the anchor and equality geometries over the common local-left variables before separator-state counting.

## Scope

This is exact common-support fiber geometry only. It is not a carry separator-width theorem. No support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`
