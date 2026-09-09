# V26 q138 C916 e0 transformed first-dyadic pair compatibility

## Purpose

Continue from the exact local-Gauss quotient geometry and evaluate the frozen 237 first-dyadic pair terms after local summation.

Each sector transform has the exact quotient form

\[
G_t(s)=2^{e_t}(-1)^{q_t(s)}\mathbf 1[A_t s=b_t].
\]

For every frozen pair `(i,j)` the actual first-dyadic residual is

\[
H(s)=\frac{G_i(s)+G_j(s)}2.
\]

The probe therefore compares affine supports, Gauss amplitudes and the sign-difference phase on the exact affine intersection. It does not reuse the pre-Gauss `±1` pair identity when transformed amplitudes differ.

## Regression

A synthetic three-shared-bit model exhaustively checks 2304 pair configurations covering:

- equal, subset, overlapping and disjoint affine supports;
- amplitudes `2^4` and `2^5`;
- constant, affine and quadratic signs.

For every case the symbolic support relation and minimum nonzero 2-adic valuation of `(G_i+G_j)/2` agree with explicit truth-table evaluation.

## Exact pair population

The frozen authority contains:

- 147 even-multiplicity support groups;
- 237 selected pair terms;
- 57 pairs from multiplicity-2 groups;
- 180 pairs from multiplicity-4 groups.

## Transformed support relations

Across all 237 pairs:

`{disjoint:28, equal:6, left_subset_right:4, overlap_incomparable:112, right_subset_left:87}`.

By multiplicity:

- multiplicity 2: `{disjoint:4, equal:4, left_subset_right:4, overlap_incomparable:35, right_subset_left:10}`;
- multiplicity 4: `{disjoint:24, equal:2, overlap_incomparable:77, right_subset_left:77}`.

Thus 209 pairs have nonempty transformed-support intersection and 28 are disjoint.

The intersection constraint-rank histogram for the 209 overlapping pairs is

`{1:4, 2:5, 3:89, 4:82, 5:29}`.

## Gauss amplitude compatibility

The exponent difference `|e_i-e_j|` is

`{0:132, 1:105}`.

By multiplicity:

- multiplicity 2: `{0:41, 1:16}`;
- multiplicity 4: `{0:91, 1:89}`.

Hence 105 pairs have unequal transformed amplitudes and cannot cancel pointwise on their overlap.

## Sign-difference collapse

The important contraction occurs after restricting `q_i xor q_j` to the exact transformed-support intersection.

Its polar-rank histogram is

`{0:203, 2:6}`.

The corresponding phase types are

`{affine_nonconstant:201, constant:2, quadratic_nonconstant:6}`.

By multiplicity, sign-difference polar ranks are

- multiplicity 2: `{0:49, 2:4}`;
- multiplicity 4: `{0:154, 2:2}`.

This is a sharp contrast with the individual nonzero Gauss signs, whose quotient-intrinsic polar ranks are 130-136. The high-rank quadratic bulk is overwhelmingly common inside the frozen pair structure and cancels in pair differences: only six overlapping pairs retain a quadratic difference, and each has rank exactly two.

The overlap arithmetic classes are

`{equal_amplitude_affine_switch:111, equal_amplitude_quadratic_switch:6, equal_amplitude_same_sign:1, no_overlap:28, unequal_amplitude_no_cancellation:91}`.

## Exact global pair classes

No transformed pair becomes a globally exact zero transform and no pair becomes a globally identical doubled transform.

The global classes are

`{disjoint_support_residual:28, genuine_residual:209}`.

By multiplicity:

- multiplicity 2: `{disjoint_support_residual:4, genuine_residual:53}`;
- multiplicity 4: `{disjoint_support_residual:24, genuine_residual:156}`.

Therefore the pair simplification is structural rather than wholesale deletion: the sign-difference phase becomes very small, but the support/amplitude pieces still leave a genuine residual.

## First-dyadic valuation

The minimum nonzero 2-adic valuation of the exact transformed residual `H` has histogram

`{3:21, 4:139, 5:77}`.

Relative to the naive `min(e_i,e_j)-1` bound, the valuation-gain histogram is

`{0:231, 1:6}`.

Exactly six pairs gain one extra dyadic level. These are the equal-support, equal-amplitude cases whose overlap arithmetic still switches with a nonconstant rank-2 phase; none vanishes globally.

Decision:

`TRANSFORMED_PAIR_SIGN_DIFFERENCE_POLAR_RANK0_2`.

## Interpretation

The previous local-Gauss result ruled out representing every sector sign independently with a few extra bits: each sign has polar rank 130-136. The transformed-pair result changes the useful representation target. Pair differences are almost entirely affine, with only six rank-2 exceptions.

A next first-dyadic message representation should therefore factor a common high-rank phase at the appropriate anchor level and encode pair corrections through:

- radical affine support relations;
- one-bit amplitude-exponent differences;
- affine sign switches for 201 overlapping pairs;
- six rank-2 quadratic switches;
- the 28 disjoint-support cases;
- the frozen first-dyadic valuation class.

The remaining hard part is the 103 singleton transforms and the choice of common phase anchors across support groups. No small separator width follows from this pair diagnostic alone.

## Scope exclusions

This is an exact transformed-pair compatibility theorem for the frozen 237 pair terms, not a complete grouped-e0 first-dyadic separator. It does not yet assemble these terms with the 103 singleton transforms. No support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search, or full-round claim is made.

`ALPHA_PASS=0`.
