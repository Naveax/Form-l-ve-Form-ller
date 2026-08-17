# V26 Q1.38 predecessor-leaf B/C Fourier-aligned first dyadic lift

## Scope

Let

`M_B=2^121 L_B`, `M_C=2^121 L_C`.

The previous clean first-residue theorem represented `M mod2` as

1. the XOR of103 odd affine-support indicators; and
2. one four-sector signed Boolean term on a common affine support.

Summing the 103 support ranks independently gave the valid but loose GF(2) bounds1052/1160.

This theorem constructs much smaller **integer** first-layer lifts directly from the same coefficient sectors. It is uniform over every fixed128-bit predecessor input mask.

## Affine part in Walsh coordinates

Fix one predecessor input mask. Each surviving affine support is an affine subset of the32 beta bits. Across the frozen S1|complement split, write beta as `(x,y)` with11 left and21 right bits.

For an affine system

`H_L x + H_R y = b`,

the indicator has Walsh expansion supported, on the left side, only on characters in the projection of the dual row space to the11 left coordinates. Equivalently its possible left frequencies lie in the F2 row span of the rows of `H_L`.

Changing the predecessor input changes only the affine offset `b`. It changes Walsh coefficients/signs but not the homogeneous frequency set.

Canonicalizing the103 odd affine supports from the clean B/C first-residue theorem and taking the union of all their left frequency sets gives exactly

- B:16 distinct left Walsh frequencies;
- C:64 distinct left Walsh frequencies.

Therefore the integer sum of all103 odd affine-support indicators has rational matrix rank at most

`rank_Q(A_B)<=16`,

`rank_Q(A_C)<=64`.

This replaces the old independent affine-sum bounds1036/1144 for the purpose of constructing an integer dyadic lift.

## Four-sector signed Boolean term

The four weight122 unique-solution sectors share one affine support. The support has exact S1/complement intersection dimension2, hence it decomposes into at most `2^2=4` rank-one affine rectangles.

On each rectangle the parity contributed by the four sectors is the Boolean quadratic function

`q=q1 xor q2 xor q3 xor q4`.

Its S1/complement cross-bilinear rank is exactly2.

For a Boolean quadratic matrix with cross rank r, the sign matrix `(-1)^q` has rational rank at most `2^r`; therefore the 0/1 Boolean matrix `q=(1-(-1)^q)/2` has rational rank at most `2^r+1`.

With r=2, each rectangle contributes rank at most5. Across at most4 support rectangles,

`rank_Q(S)<=4*5=20`.

## Explicit integer dyadic lift

Let

`K_B=A_B+S_B`,

`K_C=A_C+S_C`,

where the affine terms are taken as ordinary integer0/1 support indicators and S is the ordinary integer0/1 signed-parity function.

By construction

`K_B = M_B (mod2)`,

`K_C = M_C (mod2)`.

Hence there exist integer residual matrices R_B,R_C with

`M_B = K_B +2 R_B`,

`M_C = K_C +2 R_C`.

The rational ranks of the explicit first-layer lifts satisfy

`rank_Q(K_B)<=16+20=36`,

`rank_Q(K_C)<=64+20=84`.

Consequently the first GF(2) residue ranks are also at most36 and84, but the stronger point for the dyadic program is that the low-rank lifts are explicit coefficient-aligned integer matrices rather than opaque Gaussian factorizations.

These bounds strictly supersede1052/1160 as first-layer rank envelopes for the dyadic convolution.

## What this does not prove

It does not bound the full rational Schmidt rank of L_B or L_C. The residual matrices R_B,R_C remain unresolved. It also does not by itself lower the complete d=1 representation or arithmetic-work ledgers.
