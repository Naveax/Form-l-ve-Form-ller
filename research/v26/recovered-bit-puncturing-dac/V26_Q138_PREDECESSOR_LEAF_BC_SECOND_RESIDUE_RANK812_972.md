# V26 Q138 predecessor-leaf B/C second dyadic residue: Walsh-quotient rank 812 / 972

## Scope

This theorem sharpens the complete B/C second integer-lift envelopes. It supersedes the component-sum bounds 1016/1220 before those bounds are used as current authority.

Write

`2^121 L_B = K_B,0 + 2 R_B`,

`2^121 L_C = K_C,0 + 2 R_C`,

with first lifts `rank_Q(K_B,0)<=36`, `rank_Q(K_C,0)<=84`.

The second residue `R mod2` is decomposed into

- a support-only part, and
- the combined sign-dependent part consisting of grouped e0 Gauss-sign corrections plus the four half-sector corrections.

## Support-only left factor space

The clean support-frequency nesting theorem gives exact left Walsh frequency sets

`|U_B|=668`,

`|U_C|=788`.

The support-only binary residue admits an integer lift whose left factors are Walsh characters indexed by these sets. Hence its rational left-factor space is contained in

`W_B = span_Q{chi_u : u in U_B}`,

`W_C = span_Q{chi_u : u in U_C}`.

## Sign-dependent integer lift

The exact Gauss-completed sign-span theorem gives GF(2) column-space dimensions

`r_sign,B <=348`,

`r_sign,C <=432`.

Choose an `F_2` column basis of the sign-dependent binary matrix and lift that factorization entrywise to integers. This produces an integer matrix congruent to the sign residue modulo2 whose left factors are the corresponding 0/1 truth vectors.

Let `F_B` and `F_C` be those left-factor families.

## Walsh quotient

The 2048-point Walsh transform is invertible over Q. Under this transform, the Walsh-character spaces `W_B,W_C` become coordinate subspaces supported exactly on `U_B,U_C`.

Therefore

`dim_Q(W + span_Q F)`

is exactly

`|U| + rank_Q( Walsh(F) restricted to U^c )`.

The verifier constructs the exact sign GF(2) bases, computes their integer Walsh transforms, deletes the support-only coordinates, and computes exact rank over `ZZ`.

The quotient ranks are

`rank_Q(Walsh(F_B)|U_B^c)=144`,

`rank_Q(Walsh(F_C)|U_C^c)=184`.

Hence the complete second-residue integer lifts may share one left factor space of dimensions

`668+144 = 812` for B,

`788+184 = 972` for C.

Thus integer second lifts exist with

`R_B = K_B,1 + 2 R_B,2`, `rank_Q(K_B,1)<=812`,

`R_C = K_C,1 + 2 R_C,2`, `rank_Q(K_C,1)<=972`.

Equivalently,

`2^121 L_B = K_B,0 + 2 K_B,1 + 4 R_B,2`,

`2^121 L_C = K_C,0 + 2 K_C,1 + 4 R_C,2`.

## Current dyadic envelopes

Use

A: `[3,219,2048,...]`,

B: `[36,812,2048,...]`,

C: `[84,972,2048,...]`,

D: `[3,207,2048,...]`.

This remains a dyadic-lift statement only. It does not imply complete rational leaf Schmidt ranks 812/972 and does not by itself establish arithmetic-work reduction.
