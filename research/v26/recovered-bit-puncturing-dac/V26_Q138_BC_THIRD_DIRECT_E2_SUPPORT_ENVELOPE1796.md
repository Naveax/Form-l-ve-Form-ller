# V26 Q1.38 B/C third-residue direct-e2 support envelope

## Scope

This theorem assembles the **leading support-indicator parity** of every direct dyadic-exponent `e=2` B/C carry family across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

It is not the complete B/C third residue. Corrections inherited from lower dyadic exponents and the chosen explicit36/812 and84/972 integer lifts remain separate.

## Exact e=2 carry classes

Use the four-dimensional B/C top-nullspace quotient and the restricted quadratic polar form. For a carry pattern with `k` zero sites, nullity `n` and restricted polar rank `pr`, the nonzero Gauss amplitude starts at scaled dyadic exponent

`e = k-3+n-pr/2`.

Exact quotient-matroid counting gives the direct `e=2` classes:

### k=2, weight122

- `(internal rank124, n4, pr2)`:4465 patterns;
- `(internal rank125, n3, pr0)`:686 patterns.

Total `5151`.

### k=3, weight121

- `(125,3,2)`:66570 patterns;
- `(126,2,0)`:63174 patterns.

Total `129744`.

### k=4, weight120

- `(127,1,0)`:450840 patterns.

### k=5, weight119

- `(128,0,0)`:1,152,040 patterns.

The counts for k<=3 reproduce the earlier exact dyadic class authorities. The k4/k5 counts follow from the same29-active /95-inert quotient matroid.

## Fast exact Gauss-support row space

For a non-full-rank e=2 class, the support of the nonzero Gauss sum is obtained by adding derivative-zero equations for a basis of the radical of the restricted polar form.

The verifier performs the following exact homogeneous elimination:

1. eliminate the124-dimensional top internal row space once;
2. add the two quotient restrictions for each zero carry;
3. compute the surviving four-dimensional quotient kernel and its polar radical;
4. add the corresponding exact sign-derivative rows;
5. eliminate the remaining top-null internal coordinates;
6. project the residual external row space to the11 S1 beta coordinates.

Representative patterns from every e=2 nullity/polar class are cross-checked against the full canonical Gauss-support construction before the large finite enumeration.

## B lower-family nesting

The exact left Walsh-frequency unions are

`|U_B,k2|=1712`,

`|U_B,k3|=1712`,

`|U_B,k4|=1712`.

More strongly,

`U_B,k2 = U_B,k3 = U_B,k4 =: U_B,low`.

The exact full-rank weight119 candidate envelope is

`|U_B,k5|=1796`.

And

`U_B,low subset U_B,k5`,

with

`|U_B,k5 \ U_B,low|=84`.

Therefore every direct-e2 B support indicator, including every externally reachable member of all four carry families, has its left Walsh factors in the fixed1796-dimensional character space

`W_B,e2 = span_Q{chi_u : u in U_B,k5}`.

Hence the complete **direct-e2 support-only parity contribution** for B admits an integer lift with left-factor rank at most

`1796`.

This is a strict subgeneric structural bound.

## C method scope

For C, the internally-full-rank weight119 candidate homogeneous envelope already saturates all2048 left Walsh frequencies. Thus the same candidate-envelope route cannot yield a subgeneric C direct-e2 bound.

This does not prove that the externally reachable C direct-e2 support union has rank2048. External consistency, predecessor-condition regrouping, correction overlap or another nonlocal representation may still reduce it.

## What remains

The current B third residue cannot yet be recorded as `b2<=1796`. The explicit second lift `K_B,1` of rank<=812 was chosen to represent the complete second residue, and its induced third-bit correction must be assembled with the direct-e2 support parity. The same issue is open for C.

No complete `b2/c2`, complete leaf Schmidt-rank, complete-factor, arithmetic-work or `alpha` improvement is claimed.
