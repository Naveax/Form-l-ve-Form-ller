# V26 Q1.38 B/C uniform half-lift third-carry probe

## Scope

PR104 clean authority proves a uniform relaxed half-correction span of dimension144 for both B and C, contained in grouped-e0:

- B relaxed half144 inside grouped-e0 dimension272;
- C relaxed half144 inside grouped-e0 dimension388.

This work studies the inherited third-bit carry of that half family in two gauges:

1. the reconstructed144-vector half basis, a compact alternate-gauge diagnostic;
2. the **canonical PR104 grouped-e0 basis**, the primary authority-compatible route.

The distinction matters because exact integer/ZZ quotient rank is basis-gauge sensitive. GF(2) containment alone does not prove that a new 0/1 basis preserves the admitted748/936 lift.

Only the half correction is covered. Grouped-e0's own family carry, support-only lift carry, and cross-carries remain outside scope, so this cannot by itself prove complete B2/C2.

## Self-contained 144-dimensional half reconstruction

The PR104 combined predecessor/right state image has rank18. On a fixed support-syndrome fiber and fixed four-bit scalar pattern, the2048-bit half correction is a degree-at-most-two Boolean polynomial in the fiber coordinates.

Therefore every value on that fiber is spanned by the value at zero, first differences, and mixed second differences. The compact probe rebuilds the relaxed half span by this interpolation instead of scanning all2,097,152 state/scalar pairs, asserts exact dimension144, and verifies every reconstructed basis vector lies in grouped-e0.

## Compact 144-basis parity-lift diagnostic

For the reconstructed basis `h_i`, write

`y = XOR_i a_i h_i`

and choose integer lift

`K_half(y)=SUM_i a_i h_i`.

Then

`carry_half(y)=XOR_{i<j, a_i=a_j=1}(h_i AND h_j)`.

The probe first measures

`span_GF2{h_i AND h_j : i<j}`.

A subgeneric hull is an immediate uniform half-only carry upper span for this compact gauge. If that hull saturates2048, the probe falls back to the full PR104 relaxed state/scalar family with coordinate and carry caching.

This compact gauge is diagnostic only unless separately connected to an authority-compatible full integer lift.

## Canonical PR104 grouped-e0 gauge

PR104 inserts grouped-e0 before the relaxed half span. Because the latter is contained in grouped-e0, the half insertions add no GF(2) pivots. Thus the canonical sign lift uses the grouped-e0 pivot basis itself.

The canonical certificate rechecks the exact quotient against the unchanged support-only Walsh space:

- B: support-only668, canonical exact ZZ quotient80, total748;
- C: support-only788, canonical exact ZZ quotient148, total936.

It then solves every relaxed half vector in this exact canonical basis and studies the inherited carry of those canonical coordinates.

## Degree-four canonical carry certificate

Fix a support-syndrome fiber and scalar pattern, with fiber coordinates `t`.

The half vector `y(t)` has degree at most2. Coordinates in a fixed GF(2) basis are linear functions of `y`, so every canonical grouped-e0 coordinate bit also has degree at most2 in `t`.

For basis vectors `v_i`, canonical parity-lift carry is

`carry(y)=XOR_{i<j, a_i=a_j=1}(v_i AND v_j)`.

This is quadratic in the coordinate bits `a_i`, hence degree at most4 in `t`.

Therefore the complete relaxed canonical half-carry span on each fiber is recovered exactly from vector-valued ANF coefficients through degree4. The certificate evaluates fiber subsets of size at most4, performs the GF(2) Möbius transform, inserts every coefficient into the carry span, and regresses the reconstructed polynomial at deterministic higher-weight fiber points.

Before this interpolation it also measures the canonical all-coordinate pairwise hull

`span_GF2{v_i AND v_j : i<j}`.

If that hull is already subgeneric, it is an immediate authority-compatible half-only carry upper span. If it saturates2048, the degree-four interpolation determines the smaller span, if any, actually realized by the relaxed half family.

## Uniform relaxation semantics

Both gauges use the PR104 relaxed family:

- predecessor restricted to the exact half-active affine space;
- predecessor-null and right21 variables combined;
- exact linear image rank18;
- `2^18` linear states;
-131072 support-feasible states;
- all16 scalar phase patterns safely allowed per feasible state.

The true scalar-feasible family is a subset. Hence a subgeneric span for the full relaxation is a valid uniform upper span for the true half-only inherited carry in the stated gauge.

Conversely, saturation is only a NO-GAIN result for that gauge/relaxation, not an invariant lower bound on the true third-residue rank.

## Claim discipline

Not included:

- grouped-e0 family own lift carry;
- support-only lift carry;
- coordinate-level cross-carries between the omitted pieces and half;
- complete B2/C2;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work, alpha, ranking/search, or full-round claims.

The primary useful outcome is a subgeneric **canonical grouped-e0-gauge** half-carry span because that attaches directly to the admitted748/936 second lift. The compact144-basis result is secondary gauge geometry and helps separate basis-induced carry growth from structure intrinsic to the relaxed half family.
