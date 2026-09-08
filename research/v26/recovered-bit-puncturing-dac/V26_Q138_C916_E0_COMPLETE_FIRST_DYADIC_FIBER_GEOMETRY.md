# V26 q138 C916 e0 complete first-dyadic fiber geometry

## Scope

PR #140 freezes the exact first grouped-e0 dyadic residual for C as 340 terms:

- 103 singleton `-q` terms,
- 237 selected pair-equality terms.

The present certificate asks where those terms live relative to the existing decomposition of the 160 external coordinates into 149 shared predecessor/right coordinates and 11 local-left coordinates.

For each common affine support, let its tangent space be parameterized by the deterministic support basis. Project that tangent space onto the 149 shared coordinates. The kernel of this projection is the local fiber. The probe then restricts each quadratic polar form and linear part to that fiber without choosing a special local coordinate basis.

## Exact support-projection geometry

Across support multiplicities `1,2,4`, the shared-projection rank histograms are:

- multiplicity 1: `{141:1, 142:49, 143:53}`
- multiplicity 2: `{141:2, 142:42, 143:13}`
- multiplicity 4: `{141:32, 142:46, 143:12}`

The corresponding local-fiber dimensions are:

- multiplicity 1: `{7:53, 8:49, 9:1}`
- multiplicity 2: `{7:13, 8:42, 9:2}`
- multiplicity 4: `{7:12, 8:44, 9:34}`

Thus every relevant support retains a nontrivial 7-, 8-, or 9-dimensional local fiber after projection to the 149 shared coordinates.

## Singleton regime

All 103 singleton residual terms are locally quadratic on that fiber.

Exact histograms:

- full restricted polar rank: `{142:74, 144:29}`
- local-to-all polar rank: `{7:53, 8:49, 9:1}`
- local-local polar rank: `{4:31, 6:72}`
- local linear restriction: `{1:103}`
- fiber category: `{local_quadratic:103}`
- terms descending to the shared quotient: `0`

Therefore none of the singleton residual terms can be represented as a function of the 149 shared quotient alone before eliminating or summing over the local fiber.

## Pair regime

The 237 selected pair differences all have total restricted polar rank two, but that rank-two structure is not shared-only.

Exact histograms:

- local-to-all polar rank: `{1:105, 2:132}`
- local-local polar rank: `{0:105, 2:132}`
- local linear restriction: `{0:6, 1:231}`
- fiber category: `{local_quadratic:132, shared_local_bilinear:105}`
- terms descending to the shared quotient: `0`

By support multiplicity:

- multiplicity 2: `{local_quadratic:42, shared_local_bilinear:15}`
- multiplicity 4: `{local_quadratic:90, shared_local_bilinear:90}`

For every multiplicity-4 support group, the deterministic selected matching therefore contributes exactly one local-quadratic pair term and one shared/local-bilinear pair term.

## Interpretation

Decision:

`FIRST_DYADIC_CARRY_IS_FIBER_COUPLED`

The low total polar rank of the pair layer is real, but it does not directly imply a two-bit state on the 149 shared separator domain. Every selected pair equality condition still depends on the local support fiber, either quadratically or through shared/local bilinear coupling. The singleton regime is even more strongly local-quadratic.

Consequently the next correct carry step is not to append 340 scalar bits, nor to label each pair by a shared-only rank-two state. Instead, derive exact local-fiber elimination/evaluation identities for the two categories:

1. local-quadratic terms,
2. shared/local-bilinear terms,

and only then measure the induced shared message state after the local-left variables have been contracted.

## Not included

This is geometry, not yet a grouped-e0 carry separator-width theorem. No support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`
