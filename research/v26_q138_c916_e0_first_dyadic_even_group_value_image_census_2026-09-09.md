# V26 Q138 C916 e0 first-dyadic even-group exact nonlinear value-image census

Date: 2026-09-09

## Scope

This note freezes the exact nonlinear output image of the 147 C916 e0 support groups already covered by the frozen even-multiplicity pair-residual authority:

- 57 groups of multiplicity 2;
- 90 groups of multiplicity 4.

The 103 multiplicity-1 support groups are deliberately deferred. Existing authority leaves their signed-unit 2-adic lift outside scope, so this pass does not invent a singleton rule.

For each measured group,

\[
F_g(s)=\frac{1}{2}\sum_{i=0}^{m-1}G_i(s),\qquad m\in\{2,4\}.
\]

For `m=4`, this is exactly the sum of the two frozen pair residual functions. The direct four-transform sum is algebraically independent of which perfect matching is used to represent the group.

This is a group-local evaluation-state measurement. It is **not** a joint separator width across the 147 groups and does not establish `alpha < 1`.

## Exact method

No `2^149` physical-domain enumeration is used.

For a group of at most four transformed terms:

1. Exact affine support intersections are solved for every nonempty support mask.
2. Exact support-membership cells are isolated by inclusion-exclusion.
3. On each realized membership cell, all joint sign populations are recovered by Walsh inversion.
4. Every Walsh character moment is evaluated by exact quadratic Gauss elimination on the corresponding affine intersection.
5. The signed amplitudes are summed and divided by two to obtain the exact `value -> multiplicity` map over the full 149-bit physical domain.

The analytic implementation is checked against direct pointwise enumeration on 650 synthetic four-bit cases:

```text
2 transforms   25 cases
4 transforms  625 cases
total          650 cases
```

## Frozen upstream compatibility

The pass reproduces the frozen support structure:

```text
physical shared dimension 149
raw e0 sectors             577
support groups              250
multiplicity 1              103
multiplicity 2               57
multiplicity 4               90
even-multiplicity groups    147
```

All 57 multiplicity-2 groups reproduce the frozen pair census exactly, including the complete `value -> multiplicity` map.

All 90 multiplicity-4 frozen matchings partition the four transforms exactly once. The measured function itself uses the direct four-term sum, so its value image does not depend on the selected matching representation.

## Exact even-group images

The exact value-image size histogram is:

```text
image size 3    6 groups
image size 5   51 groups
image size 7   88 groups
image size 9    2 groups
```

Therefore the minimum isolated state-label width is:

```text
2 bits    6 groups
3 bits  139 groups
4 bits    2 groups
```

The maximum exact group-local image is 9 values, requiring 4 bits as an isolated label.

This is substantially tighter than treating the constituent pair states as an unconstrained Cartesian product. In particular, among the 90 multiplicity-4 groups, 88 realize only 7 output values and only 2 realize 9 values.

## Nonzero values and valuations

Exact nonzero-value counts:

```text
2 nonzero values    6 groups
4 nonzero values   51 groups
6 nonzero values   88 groups
8 nonzero values    2 groups
```

Minimum nonzero 2-adic valuation:

```text
v2 = 3   21 groups
v2 = 4  123 groups
v2 = 5    3 groups
```

By support-group multiplicity:

```text
m = 2: v2=3 ->  6, v2=4 -> 48, v2=5 -> 3
m = 4: v2=3 -> 15, v2=4 -> 75
```

## Normalized alphabets

After shifting each group's values by its minimum nonzero valuation, exactly six normalized alphabets occur:

```text
[-1, 0, 1]                        6 groups
[-2, -1, 0, 1, 2]               37 groups
[-3, -1, 0, 1, 3]               14 groups
[-3, -2, -1, 0, 1, 2, 3]        12 groups
[-4, -3, -2, -1, 0, 1, 2, 3, 4] 2 groups
[-5, -3, -1, 0, 1, 3, 5]        76 groups
```

All 147 alphabets are sign symmetric, and all 147 exact value-multiplicity maps are also sign symmetric.

## Multiplicity breakdown

Exact image-size breakdown:

```text
m = 2: image 3 ->  6, image 5 -> 51
m = 4: image 7 -> 88, image 9 ->  2
```

Exact state-bit breakdown:

```text
m = 2: 2 bits ->  6, 3 bits -> 51
m = 4: 3 bits -> 88, 4 bits ->  2
```

Exact support-membership cell counts:

```text
m = 2: 2 cells -> 4, 3 -> 18, 4 -> 35
m = 4: 3 cells -> 1, 5 -> 12, 7 -> 75, 8 -> 1, 10 -> 1
```

Combined realized-cell histogram:

```text
2 ->  4
3 -> 19
4 -> 35
5 -> 12
7 -> 75
8 ->  1
10 -> 1
```

Cached quadratic-character moment count histogram:

```text
7 ->  4
8 -> 18
9 -> 35
38 -> 1
48 -> 12
56 -> 75
63 -> 1
66 -> 1
```

## Interpretation boundary

The result establishes a very small exact nonlinear image **for each even-multiplicity group independently**. It does not imply a four-bit global representation.

All 147 group functions depend on the same 149-bit physical input. Their joint image can only be established by a separate dependency-aware joint-state analysis. Concatenating local state labels, adding their bit widths, or taking the largest local width would not prove a global separator.

The singleton groups also remain unresolved. In particular, this pass makes no assumption that a multiplicity-1 group's first-dyadic contribution is simply `G0`. The signed-unit 2-adic lift must be derived from upstream arithmetic authority before singleton output images are measured.

## Next gate

1. Freeze this even-multiplicity group authority with an exact verifier.
2. Derive the exact signed-unit 2-adic lift semantics for the 103 singleton groups from existing first-dyadic/integer-coefficient authority.
3. Measure the singleton nonlinear output images under that proven lift.
4. Only then attempt an all-250-group or cross-group joint-state analysis.

## Frozen decision

```text
EVEN_MULTIPLICITY_GROUP_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE
```

Not included: singleton signed-unit lift, joint state across groups, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round claims.

```text
ALPHA_PASS=0
```
