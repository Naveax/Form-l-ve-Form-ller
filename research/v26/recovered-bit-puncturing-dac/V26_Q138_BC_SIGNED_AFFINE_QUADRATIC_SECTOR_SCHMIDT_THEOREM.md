# V26 Q1.38 signed affine-quadratic sector Schmidt theorem

## Scope

Consider one predecessor-leaf sector across the frozen 11|21 split, after the 128-bit predecessor input is fixed. Its exact signed matrix has the form

`M(x,y) = 1_A(x,y) (-1)^q(x,y)`,

where `A` is an affine support in `F2^11 x F2^21` and `q` is a quadratic Boolean phase. All statements below are exact over `Q`; `epsilon=0`.

## Affine rectangle decomposition

Write the homogeneous support equations as

`H_L x + H_R y = b`.

Let

`d = dim(im H_L intersect im H_R)`

be the usual support cut-intersection dimension. Equivalently, the affine support decomposes into exactly `2^d` nonempty disjoint row/column rectangles

`X_t x Y_t`.

Within each rectangle the row differences lie in

`K_X = ker H_L`,

and the column differences lie in

`K_Y = ker H_R`.

The rectangles have pairwise disjoint row sets and pairwise disjoint column sets, so the full matrix is block diagonal after row/column permutations.

## Restricted quadratic cross rank

On one rectangle, affine substitution writes the phase as

`q(x,y) = q_L(x) + q_R(y) + B(x,y) + ell_L(x) + ell_R(y) + c`,

where `B` is the bilinear cross part. The row-only and column-only phases multiply rows and columns by nonzero signs, so they do not change rational rank.

Restrict `B` to `K_X x K_Y` and let its exact GF(2) bilinear rank be `r`.

The character matrix

`(-1)^{B(x,y)}`

has exactly `2^r` distinct independent Walsh-character rows. Therefore its rational rank is exactly

`2^r`.

Every support rectangle has the same homogeneous kernels and the same restricted cross rank. Since the `2^d` rectangles are row/column disjoint, their ranks add exactly.

Hence

`rank_Q M = 2^(d+r)`.

This is an equality, not merely an upper bound.

## B/C direct valuation-e1 consequence

Apply the formula to the reachable direct-e1 B/C sectors from the current dyadic decomposition.

A clean exhaustive-until-witness verifier finds:

- B: after five reachable sectors, the sector with zero set `{(1,5)}` and internal class `(124,4,2)` has `d=5`, restricted cross rank `r=6`, hence exact rank `2^11=2048`;
- C: the first reachable witness, zero set `{(1,1)}` with the same internal class `(124,4,2)`, already has `d=5`, `r=6`, hence exact rank `2048`.

Thus an individual direct-e1 signed sector is already full row rank for both B and C.

## Method-scope closure

Consequently any universal K1 argument based only on sectorwise rational-rank subadditivity,

`rank(sum M_nu) <= sum rank(M_nu)`,

is generic as soon as it includes the full-rank witness and cannot prove a subgeneric `<2048` bound.

Likewise, the previously observed rapid saturation of global left-Fourier frequency envelopes is structural rather than a predecessor-shift artifact.

This does **not** prove that the complete signed direct-e1 aggregate has rank2048. Different sectors may cancel exactly. Therefore the remaining mathematically meaningful routes are:

1. cross-sector signed cancellation in the complete aggregate;
2. blocked multi-bit integer lifts that avoid residue-by-residue rank sums;
3. a direct complete-leaf Schmidt/Gram/transfer theorem.

No complete B/C K1 lower bound, no complete leaf rank, no lower d=1 representation bound, no arithmetic-work reduction, and no alpha/full-round claim is made.

## Verifier

Authority verifier:

`scripts/probe_v26_q138_bc_direct_e1_signed_sector_exact_schmidt.py`

Clean pull-request run:

`32228201480`.
