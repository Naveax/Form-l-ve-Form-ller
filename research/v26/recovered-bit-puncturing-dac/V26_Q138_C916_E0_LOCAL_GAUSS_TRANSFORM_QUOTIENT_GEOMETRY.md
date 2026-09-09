# V26 q138 C916 e0 local Gauss transform quotient geometry

## Purpose

Continue the exact C grouped-e0 first-dyadic program after the radical-support separator certificate without introducing an arbitrary quadratic lift on the 149 shared coordinates.

For each of all 577 reachable C e0 sector characters, the common affine support is parameterized and split into a complement of the shared projection plus its 7-9 dimensional local fiber. The local quadratic is then eliminated exactly by hyperbolic-pair Gauss identities. The surviving normalized sign is measured only after restricting to the radical-compatible affine quotient.

This makes the reported sign geometry intrinsic to the actual support quotient rather than to a chosen ambient quadratic representative.

## Exact symbolic elimination

For a quadratic form split into shared variables `s` and local variables `x`, repeated local hyperbolic-pair elimination uses

\[
\sum_{x_i,x_j}(-1)^{x_i x_j+a x_i+b x_j}=2(-1)^{ab}.
\]

After all nondegenerate local pairs are eliminated, each remaining local radical variable contributes an affine shared constraint. If those constraints are inconsistent, the local Gauss transform is identically zero. Otherwise the transform has the form

\[
G(s)=2^e(-1)^{q_{\rm surv}(s)}\mathbf 1[A s=b]
\]

on the shared support quotient.

The implementation treats the inconsistent-radical case as an exact zero transform rather than as an elimination failure.

## Exhaustive regression

The partial symbolic Gauss eliminator is checked against direct local summation for every Boolean quadratic on four variables under two different splits:

- 2 shared + 2 local: 2048 forms, including 336 identically-zero transforms;
- 1 shared + 3 local: 2048 forms, including 644 identically-zero transforms.

All 4096 forms match brute-force local summation exactly.

These synthetic zero cases are important because they verify the affine-radical edge case even though none of the 577 actual C e0 sector transforms is identically zero.

## Exact C e0 geometry

There are exactly 577 reachable sector characters in 250 support groups with multiplicities

`{1:103, 2:57, 4:90}`.

Shared-projection ranks are

`{141:133, 142:317, 143:127}`.

Local-fiber dimensions are

`{7:127, 8:309, 9:141}`.

The local-fiber polar-rank histogram is

`{4:209, 6:329, 8:39}`,

so the corresponding radical dimensions are

`{0:3, 1:88, 2:172, 3:180, 4:134}`.

The descended radical-control coefficient ranks reproduce the merged authority exactly:

`{0:3, 1:88, 2:172, 3:180, 4:134}`.

All 577 actual transforms have a nonempty radical-compatible shared support:

- identically-zero Gauss sectors: 0;
- nonzero Gauss sectors: 577.

## Nonzero amplitude

The exact nonzero Gauss magnitude is always a power of two with

`log2(abs(G))` histogram

`{4:55, 5:283, 6:239}`.

By support-group multiplicity:

- multiplicity 1: `{4:26, 5:72, 6:5}`;
- multiplicity 2: `{4:12, 5:88, 6:14}`;
- multiplicity 4: `{4:17, 5:123, 6:220}`.

## Quotient-intrinsic normalized sign

After imposing the radical affine constraints, the surviving shared-support free dimensions are

`{138:233, 139:6, 140:281, 141:2, 142:55}`.

The normalized sign remains a genuinely high-rank quadratic on every one of the 577 surviving quotients. Its polar-rank histogram is

`{130:162, 132:275, 134:125, 136:15}`.

Thus:

- minimum observed normalized-sign polar rank: 130;
- maximum observed normalized-sign polar rank: 136;
- affine normalized-sign sectors: 0;
- constant normalized-sign sectors: 0.

By support multiplicity the polar-rank histograms are:

- multiplicity 1: `{130:4, 132:53, 134:38, 136:8}`;
- multiplicity 2: `{130:7, 132:59, 134:43, 136:5}`;
- multiplicity 4: `{130:151, 132:163, 134:44, 136:2}`.

Decision:

`LOCAL_GAUSS_QUOTIENT_SIGN_POLAR_RANK130_136`.

## Interpretation

The previous radical-support result is genuinely small: the zero/nonzero support obstruction requires only low-dimensional radical controls. That does **not** imply that the nonzero Gauss sign is small.

After exact local elimination and after quotienting by the radical constraints, the surviving sign is still a 130-136 rank quadratic. Therefore a complete first-dyadic carry separator cannot simply append a handful of sign bits to the width-61 radical-support state.

The next useful contraction must exploit the frozen signed-pair arithmetic itself. For each of the 237 selected first-dyadic pairs, the exact transformed supports, powers-of-two amplitudes, and normalized quadratic signs should be compared on their common affine intersection. This can reveal exact disjointness, cancellation, doubling, valuation gain, or a genuinely phase-dependent residual before any separator-state assembly.

## Scope exclusions

This is quotient geometry, not a complete grouped-e0 carry separator theorem. It does not yet combine the 577 transforms using the frozen singleton/pair signed arithmetic. No support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search, or full-round claim is made.

`ALPHA_PASS=0`.
