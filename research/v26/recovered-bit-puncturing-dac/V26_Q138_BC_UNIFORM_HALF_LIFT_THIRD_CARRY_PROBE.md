# V26 Q1.38 B/C uniform half-lift third-carry probe

## Scope

PR104 clean authority proves a uniform relaxed half-correction span of dimension144 for both B and C, and the combined sign span has the same GF(2) dimension as grouped-e0 alone:

- B relaxed half144 inside grouped-e0 dimension272;
- C relaxed half144 inside grouped-e0 dimension388.

This probe reconstructs that 144-dimensional relaxed half span self-containedly and uses the **half basis itself** as an explicit integer parity-lift gauge. Because every half basis vector is reverified to lie in grouped-e0, this gauge does not enlarge the admitted PR104 ambient sign left-factor space.

It covers the **half correction only**. It does not include grouped-e0's own lift carry, the support-only lift carry, or cross-carries among those components. Therefore it cannot by itself prove a complete B2/C2 bound.

## Self-contained reconstruction of the 144-dimensional half basis

The PR104 combined predecessor/right state image has rank18. On a fixed support-syndrome fiber and fixed four-bit scalar pattern, the 2048-bit half correction is a degree-at-most-two Boolean polynomial in the fiber coordinates.

Therefore every value on that fiber is spanned by:

- the value at zero;
- every first difference along one fiber basis direction;
- every mixed second difference along a pair of directions.

The probe rebuilds the relaxed half span with this degree-two interpolation rather than scanning all 2,097,152 state/scalar pairs. It asserts exact dimension144 and then solves every reconstructed half-basis vector in the grouped-e0 basis, certifying the containment required by the lift gauge.

## Explicit parity lift

Let `v_i`, `i=1..144`, be the reconstructed relaxed half basis. For every half-correction truth vector `y`, solve exactly over GF(2)

`y = XOR_i a_i v_i`.

Choose the integer lift

`K(y) = SUM_i a_i v_i`.

This is congruent to `y mod2` by construction and all left factors stay inside the admitted grouped-e0 ambient space.

Pointwise, if `n` active basis terms equal one, then

`(K-y)/2 mod2 = floor(n/2) mod2 = C(n,2) mod2`.

Hence the induced third-bit carry is exactly

`carry(y) = XOR_{i<j, a_i=a_j=1} (v_i AND v_j)`.

## Pairwise-intersection hull precheck

Before enumerating the full relaxed state family, the verifier builds

`H = span_GF2 { v_i AND v_j : i<j }`

using the 144-vector half basis.

Every carry produced by this explicit parity lift lies in `H`. Therefore

`dim carry_span <= dim H`.

If `dim H < 2048`, that value is immediately a valid uniform upper span for the half-only inherited carry and the expensive full relaxed scan is unnecessary.

If `dim H = 2048`, the hull gives no subgeneric gain but does not imply that the actually realized carry family spans2048. The verifier then scans the exact PR104 relaxed family, with coordinate/carry caching, to measure the realized carry span.

## Uniform relaxed state family

If the hull saturates, the fallback scan uses the same PR104 state reduction:

- predecessor restricted to the exact half-active affine space;
- predecessor-null and right21 variables combined;
- exact linear image rank18;
- 2^18 linear states;
- 131072 support-feasible states;
- all16 scalar phase patterns safely allowed per feasible state.

The complete relaxed family has2,097,152 state/scalar pairs. The true scalar-feasible family is a subset.

If the complete relaxed scan finishes with carry dimension below2048, the result is a valid uniform upper span for the true half-only inherited carry of this explicit 144-vector gauge.

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

The purpose is to determine whether the new uniform 748/936 construction propagates useful structure into the third dyadic bit and, if not, to isolate the failure specifically to this half-lift gauge rather than to the invariant object.
