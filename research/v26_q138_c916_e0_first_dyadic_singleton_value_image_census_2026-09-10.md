# V26 Q138 C916 e0 first-dyadic singleton exact value-image census

Date: 2026-09-10

## Scope

This note freezes the exact nonlinear output image of the 103 multiplicity-1 C916 e0 support groups left outside the earlier even-multiplicity value-image census.

The relevant frozen arithmetic authority is the complete first-dyadic group residual identity

\[
R=\frac{\sum_i(-1)^{q_i}-(m\bmod 2)}{2}.
\]

For a singleton, `m=1`, so pointwise

\[
\frac{(-1)^q-1}{2}=-q.
\]

If the local fiber has dimension `k` and

\[
G(s)=\sum_t(-1)^{q(s,t)},
\]

then the exact singleton residual after local-fiber summation is

\[
R(s)=\frac{G(s)-2^k}{2}=-\sum_t q(s,t).
\]

This removes the earlier ambiguity between `G`, `G/2`, and a separate signed-unit convention. Neither `G` nor `G/2` alone is the singleton first-dyadic residual.

## Exact method

The probe reuses the existing exact local quadratic Gauss transform and never enumerates the full `2^149` physical shared domain.

For each singleton group:

1. Reconstruct the frozen 150-dimensional within-support phase space.
2. Split it into the shared projection and local fiber.
3. Apply the exact local Gauss elimination to obtain `G(s)` on the shared projection.
4. Map the transform through `R(s)=(G(s)-2^k)/2`.
5. Count the complete `value -> multiplicity` image over the physical 149-bit shared domain, with value zero outside the original shared projection.

The census implementation is independently checked by exhaustive pointwise enumeration on all 4096 quadratic forms in the synthetic four-variable `(2 shared, 2 local)` and `(1 shared, 3 local)` regression families.

## Frozen upstream geometry

```text
physical shared dimension       149
raw e0 sectors                  577
support groups                  250
singleton groups                103
support free dimension          150 for all singleton groups
shared projection rank          141: 1, 142: 49, 143: 53
local fiber dimension             7:53,   8:49,    9: 1
```

Every singleton local Gauss transform is nonzero as a transform. Its shared-support control rank is:

```text
rank 1   26 groups
rank 2   45 groups
rank 3   28 groups
rank 4    4 groups
```

The nonzero Gauss amplitude exponent is:

```text
log2 |G| = 4   26 groups
log2 |G| = 5   72 groups
log2 |G| = 6    5 groups
```

For all 103 groups the exact Gauss sign moment on its affine support is zero, so both signs occur equally often there.

## Exact singleton residual images

Every singleton group has exactly four residual values over the full physical shared domain:

```text
image size 4   103 groups
state bits 2   103 groups
nonzero values per image 3   103 groups
```

The zero value comes from states outside the original shared projection. Inside the projection, the residual has the baseline

\[
-2^{k-1}
\]

plus the two values obtained by adding or subtracting half of the nonzero Gauss amplitude.

Thus every individual singleton residual function has an exact isolated two-bit label. This is an isolated per-group statement, not a two-bit joint representation of the singleton family or of all 250 groups.

## 2-adic valuations and normalized alphabets

Minimum nonzero valuation:

```text
v2 = 3   26 groups
v2 = 4   72 groups
v2 = 5    5 groups
```

Exactly two normalized alphabets occur:

```text
[-9, -8, -7, 0]   72 groups
[-5, -4, -3, 0]   31 groups
```

Unlike the even-multiplicity pair-residual images, these singleton residual alphabets are not sign symmetric. That is expected: `R=-sum_t q` is nonpositive by construction. Treating singleton residuals as a signed copy of the even-group image would therefore be arithmetically wrong.

## Interpretation boundary

The result closes the previously unresolved singleton first-dyadic evaluation-state regime. Combined with the frozen even-multiplicity pass, all 250 C916 e0 support groups now have exact individual nonlinear value-image measurements:

- 103 singleton groups: exact image size 4, isolated width 2 bits;
- 57 multiplicity-2 groups: frozen even-group census;
- 90 multiplicity-4 groups: frozen even-group census.

This still does **not** establish a small joint separator state. All group functions depend on the same 149-bit physical input. Adding isolated bit widths, taking the maximum isolated width, or assuming independence would not prove the joint image.

No claim is made here about support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, ranking/search, full-round relevance, or `alpha < 1`.

## Next gate

The next valid step is dependency-aware joint-state analysis across the now-complete 250-group local image family. It must preserve the exact support controls, Gauss sign functions, and cross-group correlations rather than replace them with independent local labels.

A safe first pass is to classify exact equivalence/dependency among group output functions and shared affine controls before attempting any materialization of the all-250 joint image.

## Frozen decision

```text
SINGLETON_FIRST_DYADIC_EXACT_VALUE_IMAGE_CENSUS_COMPLETE
ALPHA_PASS=0
```
