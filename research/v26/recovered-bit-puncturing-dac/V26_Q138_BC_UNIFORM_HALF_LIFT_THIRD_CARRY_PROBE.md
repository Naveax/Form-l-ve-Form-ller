# V26 Q1.38 B/C uniform half-lift third-carry probe

## Scope

PR104 clean authority proves a uniform relaxed half-correction span of dimension144 for both B and C, and that this span is contained in grouped-e0:

- B relaxed half144 inside grouped-e0 dimension272;
- C relaxed half144 inside grouped-e0 dimension388.

This work studies the inherited third-bit carry of that half family in two complementary gauges:

1. the reconstructed144-vector half basis itself, useful as a compact alternate-gauge diagnostic;
2. the **canonical PR104 grouped-e0 basis**, which is the primary authority-compatible route.

The distinction matters because exact ZZ quotient rank is basis-gauge sensitive. GF(2) containment alone does not prove that a new 0/1 basis preserves the admitted748/936 integer-lift bound.

Only the **half correction** is covered. Grouped-e0's own family carry, the support-only lift carry, and cross-carries among the components remain outside scope. Therefore no result here alone is a complete B2/C2 theorem.

## Self-contained reconstruction of the 144-dimensional half span

The PR104 combined predecessor/right state image has rank18. On a fixed support-syndrome fiber and fixed four-bit scalar pattern, the2048-bit half correction is a degree-at-most-two Boolean polynomial in the fiber coordinates.

Therefore every value on that fiber is spanned by:

- the value at zero;
- every first difference along one fiber basis direction;
- every mixed second difference along a pair of directions.

The probe rebuilds the relaxed half span by this degree-two interpolation rather than by scanning all2,097,152 state/scalar pairs. It asserts exact dimension144 and solves every reconstructed basis vector in grouped-e0, revalidating `half subset grouped-e0` on the current checkout.

## Canonical PR104 integer gauge

PR104 forms its sign basis by inserting grouped-e0 **before** the relaxed half span. Since the new half span is contained in grouped-e0, the later half insertions add no pivots. Thus the canonical PR104 sign lift uses the existing grouped-e0 pivot basis itself.

The verifier rechecks its exact quotient against the unchanged support-only Walsh space:

- B support-only668 plus canonical ZZ quotient80 gives748;
- C support-only788 plus canonical ZZ quotient148 gives936.

This makes the canonical grouped-e0 basis the preferred gauge for deciding whether half structure genuinely propagates from the admitted748/936 second lift.

## Canonical half carry has degree at most four on each fiber

Fix one support-syndrome fiber and one scalar pattern. Let `t` denote the fiber coordinates and let

`y(t)`

be the half-correction truth vector. By the degree-two reconstruction above, `y(t)` has degree at most2.

Coordinates of `y(t)` in the fixed canonical grouped-e0 basis are GF(2)-linear functions of `y`, so every coordinate bit also has degree at most2 in `t`.

For an explicit parity lift with basis vectors `v_i`, if

`y = XOR_i a_i v_i`

and

`K(y)=SUM_i a_i v_i`,

then pointwise

`(K-y)/2 mod2 = C(n,2) mod2`

where `n` is the number of active basis terms equal to1. Hence

`carry(y)=XOR_{i<j, a_i=a_j=1}(v_i AND v_j)`.

The carry is quadratic in the coordinate bits `a_i`. Since each `a_i(t)` has degree at most2, canonical half carry has degree at most4 on the fiber.

Therefore the entire relaxed canonical half-carry span is recovered exactly from the vector-valued ANF coefficients through degree4. The new certificate evaluates only subsets of at most four fiber directions, extracts the Möbius coefficients, inserts those coefficients into a GF(2) span, and regresses the interpolation on deterministic higher-weight fiber points.

This replaces a possible2,097,152-state fallback by an exact low-degree certificate when the cheap canonical pairwise hull itself has already saturated.

## Canonical pairwise-hull precheck

Before degree-four interpolation, the canonical certificate forms

`H_can = span_GF2 { v_i AND v_j : i<j }`

for the actual grouped-e0 basis.

Every canonical half carry lies in this hull. Thus if `dim H_can<2048`, the hull alone is an immediate authority-compatible uniform half-only carry upper span.

If `H_can` saturates2048, that is not a lower bound on realized half carry. The exact degree-four fiber interpolation is then used to determine the span actually attained by the relaxed half family.

## Compact 144-basis alternate gauge

The companion diagnostic also uses the reconstructed144 half vectors themselves as an explicit parity-lift basis. Its pairwise-intersection hull is

`H_half = span_GF2 { h_i AND h_j : i<j }`.

If this hull is subgeneric, it is an immediate upper span for half-only inherited carry in that compact gauge. If it saturates, the companion probe may scan the complete relaxed family with coordinate/carry caching.

Because this is an alternate integer basis, the verifier separately builds a deterministic **half-first extension** to the full grouped-e0 GF(2) space:

1. insert the144 half basis vectors first;
2. extend with grouped-e0 vectors until dimension272 for B or388 for C;
3. compute the exact ZZ quotient against the same support-only Walsh space.

It reports

`half_first_preserves_or_improves_PR104_total`.

A compact-gauge carry gain with a false compatibility flag is still a valid alternate-gauge diagnostic, but it does not propagate the current748/936 authority. A compatible compact gauge is potentially useful, although complete B2/C2 still requires the omitted carry pieces.

## Uniform relaxation semantics

Both routes use the same PR104 relaxed family:

- predecessor restricted to the exact half-active affine space;
- predecessor-null and right21 variables combined;
- exact linear image rank18;
- `2^18` linear states;
-131072 support-feasible states;
- all16 scalar phase patterns safely allowed per feasible state.

The true scalar-feasible family is a subset. Therefore a subgeneric span computed for the full relaxation is a valid uniform upper span for the true half-only carry in the stated gauge.

Conversely, saturation of a relaxed route is only a NO-GAIN result for that gauge/relaxation. It is not an invariant lower bound on the true third-residue rank.

## Claim discipline

Not included:

- grouped-e0 family own lift carry;
- support-only lift carry;
- cross-carry between support/e0/half contributions;
- complete B2/C2;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work, alpha, ranking/search, or full-round claims.

The primary useful outcome is a subgeneric **canonical grouped-e0-gauge** half-carry span, because that attaches directly to the admitted748/936 second lift. The compact144-basis result is secondary gauge geometry and helps diagnose whether a poor canonical result is intrinsic to the relaxed half family or merely basis-induced.
