# V26 Q138 C916 e0 first-dyadic frozen-pair exact nonlinear value-image census

Date: 2026-09-09

## Scope

This note freezes the exact local output-image geometry of the 237 transformed pairs selected by the existing C916 e0 first-dyadic pair-residual authority.

For a frozen pair, the measured function is

\[
H(s)=\frac{G_i(s)+G_j(s)}{2}
\]

over the full 149-bit physical shared domain.

This is an evaluation-state measurement of each pair function independently. It is **not** a joint separator width and does not establish a complete grouped-e0 representation or `alpha < 1`.

## Exact method

Each transformed term is zero outside an affine support and is a signed power of two on its support. The census avoids all `2^149` enumeration.

For the intersection of two supports, let

\[
N=|S_i\cap S_j|,
\quad
A=\sum(-1)^{q_i},
\quad
B=\sum(-1)^{q_j},
\quad
C=\sum(-1)^{q_i+q_j}.
\]

The four joint sign populations are obtained exactly by the two-bit Walsh inverse:

\[
N_{++}=\frac{N+A+B+C}{4},
\quad
N_{+-}=\frac{N+A-B-C}{4},
\]

\[
N_{-+}=\frac{N-A+B-C}{4},
\quad
N_{--}=\frac{N-A-B+C}{4}.
\]

Total left/right sign moments and intersection moments are computed by exact quadratic Gauss elimination. Subtracting the intersection contribution gives left-only and right-only populations; the complement of the support union gives the exact zero mass. Therefore the final `value -> multiplicity` map is exact over all `2^149` shared inputs without enumerating them.

The analytic method is additionally checked against direct enumeration on 2,304 synthetic 4-bit affine/quadratic pair cases.

## Frozen upstream compatibility

Before accepting the new image census, the probe reproduces the existing transformed-pair authority:

- frozen transformed pairs: 237;
- raw e0 sectors: 577;
- support groups: 250;
- group multiplicities: `{1:103, 2:57, 4:90}`;
- even-multiplicity support groups: 147.

Support-relation histogram:

```text
disjoint             28
equal                 6
left_subset_right     4
overlap_incomparable 112
right_subset_left    87
```

Amplitude-delta histogram:

```text
0 132
1 105
```

Overlap sign-difference type:

```text
affine_nonconstant    201
constant                2
quadratic_nonconstant   6
```

Overlap sign-difference polar rank:

```text
0 203
2   6
```

## Exact nonlinear pair images

Every one of the 237 frozen pairs has only 3 or 5 realized output values:

```text
image size 3   20 pairs
image size 5  217 pairs
```

Hence the minimum local state-label width is:

```text
2 bits   20 pairs
3 bits  217 pairs
```

The corresponding nonzero-value counts are 2 and 4 respectively:

```text
2 nonzero values   20 pairs
4 nonzero values  217 pairs
```

No frozen pair realizes the loose seven-value upper bound. The exact maximum local pair image is therefore 5 values, requiring at most 3 bits as an isolated state label.

Minimum nonzero 2-adic valuation:

```text
v2 = 3   21 pairs
v2 = 4  139 pairs
v2 = 5   77 pairs
```

After shifting by the pair's minimum nonzero valuation, exactly three normalized alphabets occur:

```text
[-1, 0, 1]             20 pairs
[-2, -1, 0, 1, 2]     126 pairs
[-3, -1, 0, 1, 3]      91 pairs
```

All 237 alphabets are sign symmetric, and all 237 exact value multiplicity maps are also sign symmetric.

## Breakdowns

By support-group multiplicity:

```text
m = 2: image 3 ->  6, image 5 ->  51
m = 4: image 3 -> 14, image 5 -> 166
```

By amplitude delta:

```text
delta = 0: image 3 -> 20, image 5 -> 112
delta = 1: image 5 -> 105
```

By support relation:

```text
disjoint:             image 3 -> 14, image 5 -> 14
equal:                image 3 ->  6
left_subset_right:    image 5 ->  4
overlap_incomparable: image 5 -> 112
right_subset_left:    image 5 -> 87
```

## Interpretation

The earlier template/residual passes measured how many **linear input signature bits** are sufficient to determine residual phase behavior. Those widths remained around 100 bits even after template optimization.

The present result measures something different: the actual nonlinear pair function output. At this level every frozen pair has only 3 or 5 values. This confirms that carrying a large linear signature can be vastly more expensive than representing the realized nonlinear evaluation state.

However, the local 2/3-bit labels cannot be summed or concatenated and called a global separator. The 237 pair functions share the same 149-bit physical input and can have substantial dependencies. The next question is therefore the exact grouped and then joint image geometry, not `237 * 3` or any similarly decorative bit count.

## Next gate

Compute exact first-dyadic grouped arithmetic images for all 250 support groups:

- 103 multiplicity-1 singleton groups;
- 57 multiplicity-2 groups, which must reproduce this frozen pair census exactly;
- 90 multiplicity-4 groups, evaluating the exact combined function `H1 + H2 = (G0+G1+G2+G3)/2` under the frozen decomposition and checking pairing independence where applicable.

The intended exact mechanism for multiplicity 4 is affine support membership inclusion-exclusion plus joint quadratic Walsh moments. No `2^149` enumeration is required.

## Frozen decision

```text
FROZEN_PAIR_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE
```

Not included: joint state across groups, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round claims.

```text
ALPHA_PASS=0
```
