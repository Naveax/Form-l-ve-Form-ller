# V26 Q138 C916 e0 first-dyadic group-output pair dependency

Date: 2026-09-10

## Scope

This pass is the first dependency-aware step after completing exact nonlinear value-image censuses for all 250 C916 e0 first-dyadic support groups.

It asks one deliberately narrow exact question: can two distinct group-output functions be equal, negatives of one another, or any other exact real scalar multiples on the full 149-bit physical shared domain?

The result is a pairwise statement only. It does not exclude higher-order linear relations among three or more outputs, and it does not establish the size of the nonlinear joint image.

## Exact function model

The frozen even-multiplicity authority supplies 147 group outputs with multiplicity 2 or 4. The frozen singleton authority supplies the remaining 103 outputs.

Each physical group function is reconstructed from the post-Gauss physical affine-support/sign representation:

- every Gauss sector contributes its exact half-amplitude times its quadratic sign on its physical affine support;
- every singleton additionally contains the exact projection baseline from

\[
R(s)=\frac{G(s)-2^k}{2}.
\]

Thus the 577 Gauss sector terms plus 103 singleton projection-baseline terms give exactly 680 physical terms.

Before any pairwise conclusion is accepted, the reconstructed physical function norm for every group is checked against the independently frozen exact `value -> multiplicity` census:

\[
\langle f_g,f_g\rangle
 = \sum_v v^2\,N_g(v).
\]

All 250 norm cross-checks pass.

## Pair filter

There are

```text
250 choose 2 = 31125
```

unordered group pairs.

Exact scalar proportionality forces the two full-domain value distributions to agree after one global nonzero scalar rescaling, up to sign. A primitive scale-invariant distribution signature therefore gives an exact necessary filter before expensive physical inner products.

The 250 outputs form 19 such signature classes, with class-size histogram

```text
1:6, 2:2, 4:2, 6:1, 8:1, 11:1,
14:1, 26:1, 27:1, 36:1, 45:1, 59:1
```

This rejects 26915 of the 31125 pairs immediately and leaves 4210 scale-compatible candidates.

A notable fact is that all 4210 surviving candidates actually have the same exact unscaled value distribution. Therefore matching marginal output histograms are common and by themselves reveal essentially nothing about equality of the underlying functions.

## Exact proportionality test

For every scale-compatible pair `f,g`, the probe computes the exact physical inner product by intersecting the corresponding affine supports and evaluating the resulting quadratic sign moments exactly.

For nonzero real functions, Cauchy-Schwarz equality is exact and decisive:

\[
\langle f,g\rangle^2
 = \langle f,f\rangle\langle g,g\rangle
\]

if and only if `g` is a real scalar multiple of `f`.

Among the 4210 candidates:

```text
exact scalar proportional pairs   0
exact equal function pairs        0
exact negated function pairs      0
other exact scaled pairs          0
exact zero-inner-product pairs 2536
```

Hence every scale-compatible pair fails Cauchy equality. The proportional-dependency graph on all 250 group outputs therefore has 250 singleton connected components.

## Interpretation

This closes the simplest possible cross-group reuse mechanism. No two distinct exact first-dyadic group outputs can be represented by storing one function plus a scalar label.

It also gives a useful warning about marginal-state reasoning: 4210 pairs have identical exact value distributions, yet none are equal as functions. Small isolated alphabets or matching histograms do not imply shared state.

The 2536 zero-inner-product pairs show that a substantial fraction of the scale-compatible candidates are exactly orthogonal in the full physical function space. Orthogonality does not itself prove global independence, but it is strong evidence that the remaining compression problem is genuinely about higher-order structure rather than pairwise duplication.

## Next gate

The next exact dependency question is higher-order linear dependence among the 250 integer-valued output functions.

A computationally cheaper rigorous first pass than forming the complete exact Gram matrix is to search for an explicit full-rank physical evaluation witness. Choose deterministic physical input points, evaluate the 250 exact integer functions, and row-reduce the resulting matrix modulo an odd prime. If rank 250 is reached modulo the prime, some integer 250x250 minor is nonzero and the 250 functions are therefore linearly independent over Q.

Failure to reach rank 250 at a chosen sample budget would be inconclusive and must not be reported as a dependence theorem.

## Boundary

No claim is made here about a complete all-250 nonlinear joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, ranking/search, full-round relevance, or `alpha < 1`.

## Frozen decision

```text
NO_PAIRWISE_EXACT_SCALAR_DEPENDENCY_ACROSS_250_GROUP_OUTPUTS
ALPHA_PASS=0
```
