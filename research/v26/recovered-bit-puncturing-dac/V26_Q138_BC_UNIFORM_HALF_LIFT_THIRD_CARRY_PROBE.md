# V26 Q1.38 B/C uniform half-lift third-carry probe

## Scope

PR104 clean authority proves a uniform relaxed half-correction span of dimension144 for both B and C, and the combined sign span has the same GF(2) dimension as grouped-e0 alone:

- B relaxed half144 inside grouped-e0 dimension272;
- C relaxed half144 inside grouped-e0 dimension388.

This probe reconstructs that 144-dimensional relaxed half span self-containedly and uses the **half basis itself** as an explicit integer parity-lift gauge for the half-only family.

GF(2) containment is not enough to say that a new 0/1 basis preserves the exact PR104 quotient: exact ZZ quotient rank is basis-gauge sensitive. Therefore the verifier also measures a deterministic **half-first extended gauge** obtained by inserting the144 half basis first and then extending it to the full grouped-e0 span. It separately rechecks the canonical grouped-e0 quotient and reports whether the half-first extension preserves or improves the admitted748/936 second-lift total.

It covers the **half correction only**. It does not include grouped-e0's own lift carry, the support-only lift carry, or cross-carries among those components. Therefore it cannot by itself prove a complete B2/C2 bound.

## Self-contained reconstruction of the 144-dimensional half basis

The PR104 combined predecessor/right state image has rank18. On a fixed support-syndrome fiber and fixed four-bit scalar pattern, the2048-bit half correction is a degree-at-most-two Boolean polynomial in the fiber coordinates.

Therefore every value on that fiber is spanned by:

- the value at zero;
- every first difference along one fiber basis direction;
- every mixed second difference along a pair of directions.

The probe rebuilds the relaxed half span with this degree-two interpolation rather than scanning all2,097,152 state/scalar pairs. It asserts exact dimension144 and then solves every reconstructed half-basis vector in the grouped-e0 basis, certifying GF(2) containment.

## Integer-gauge compatibility check

For each position the verifier first rechecks the admitted canonical grouped-e0 exact quotient against the unchanged support-only Walsh space:

- B support-only668 plus canonical quotient80 gives748;
- C support-only788 plus canonical quotient148 gives936.

It then builds a deterministic half-first basis of the same grouped-e0 GF(2) space:

1. insert the144 reconstructed half basis vectors;
2. extend with grouped-e0 vectors until the full272-dimensional B or388-dimensional C space is recovered;
3. compute the exact ZZ quotient of that half-first basis against the same support-only space.

The reported boolean

`half_first_preserves_or_improves_PR104_total`

is true exactly when the resulting total is no worse than748 for B or936 for C.

This check is important because two binary bases spanning the same GF(2) space may define different integer lifts and therefore different exact rational quotient ranks.

A subgeneric half-carry result with a **false** compatibility flag remains a valid diagnostic for that alternate half-first gauge, but it is not yet a propagation theorem for the current748/936 authority. A subgeneric carry with a **true** compatibility flag is much more directly useful for the current k9 program, though complete B2/C2 still requires the omitted carry pieces below.

## Explicit parity lift

Let `v_i`, `i=1..144`, be the reconstructed relaxed half basis. For every half-correction truth vector `y`, solve exactly over GF(2)

`y = XOR_i a_i v_i`.

Choose the integer half lift

`K(y) = SUM_i a_i v_i`.

This is congruent to `y mod2` by construction.

Pointwise, if `n` active basis terms equal one, then

`(K-y)/2 mod2 = floor(n/2) mod2 = C(n,2) mod2`.

Hence the induced third-bit carry is exactly

`carry(y) = XOR_{i<j, a_i=a_j=1} (v_i AND v_j)`.

## Pairwise-intersection hull precheck

Before enumerating the full relaxed state family, the verifier builds

`H = span_GF2 { v_i AND v_j : i<j }`

using the144-vector half basis.

Every carry produced by this explicit parity lift lies in `H`. Therefore

`dim carry_span <= dim H`.

If `dim H < 2048`, that value is immediately a valid uniform upper span for the half-only inherited carry and the expensive full relaxed scan is unnecessary.

If `dim H = 2048`, the hull gives no subgeneric gain but does not imply that the actually realized carry family spans2048. The verifier then scans the exact PR104 relaxed family, with coordinate/carry caching, to measure the realized carry span.

## Uniform relaxed state family

If the hull saturates, the fallback scan uses the same PR104 state reduction:

- predecessor restricted to the exact half-active affine space;
- predecessor-null and right21 variables combined;
- exact linear image rank18;
- `2^18` linear states;
-131072 support-feasible states;
- all16 scalar phase patterns safely allowed per feasible state.

The complete relaxed family has2,097,152 state/scalar pairs. The true scalar-feasible family is a subset.

If the complete relaxed scan finishes with carry dimension below2048, the result is a valid uniform upper span for the true half-only inherited carry of this explicit144-vector gauge.

If the relaxed carry span reaches2048, that is NO-GAIN only for this relaxed gauge/global-span route. It is not a lower bound on the true carry rank and does not exclude another integer-lift basis from giving a smaller carry hull.

## Claim discipline

Not included:

- grouped-e0 own lift carry;
- support-only lift carry;
- cross-carry between support/e0/half lifts;
- complete B2/C2;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work, alpha, ranking/search, or full-round claims.

The purpose is to determine whether the new uniform half construction propagates useful structure into the third dyadic bit and to separate two logically different failure modes:

1. the half-only carry hull/span is already generic for this gauge; or
2. the half-only carry is structured, but the half-first integer gauge does not preserve the current748/936 quotient budget.

Either outcome narrows the next lift-design step without being mistaken for an invariant lower bound.
