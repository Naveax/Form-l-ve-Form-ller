# V26 q138 Full Physical Family Rank-27 + Support-216 Global Sub-39 Theorem

## Purpose

This note combines two exact physical-family facts:

1. every certified q138 fixed-output parent bottleneck has Schmidt rank at most 27 across the `16|24` partition;
2. the left parent factor inherits a uniform nine-bit support bound of at most 216 active assignments.

Reinserting both factorizations into the complete one-quarter-round network gives a complete exact global contraction-tree certificate below 39 for the **entire 4096-case physical fixed-mask family**.

The admitted structural bound is

`W <= log2(216 * 2^31) = 38.75488750216347... < 39`.

## 1. Algebraic construction

For each physical fixed mask `m`, write the certified 171-leaf parent message as

`M_m = X_m Z_m`

through a mask-conditioned Schmidt bond `RP` of dimension

`rho_m <= 27`.

Use dimension 27 as a safe uniform structural bond, padding smaller ranks with zeros.

By the left-I9 support theorem, the left factor may be chosen as `X_m=L_m B_m`, and its nine-bit support is contained in a set of size at most 216. Therefore `X_m` admits an exact further factorization

`X_m(I9,O7,RP) = sum_{a=1}^{r_m} XA_m(I9,a) XB_m(a,O7,RP)`

with

`r_m <= 216`.

Use dimension 216 as a safe all-mask bond `RL216`, again allowing zero padding.

No approximation is introduced. The excluded nine-bit assignments are exactly impossible in the Boolean support upper envelope, so this reduction has residual `epsilon=0`.

## 2. Global network

Start from the already certified rank-528-compressed width-40 network.

Remove its unique 171-leaf maximum cluster and replace it by three factors:

- `XA`, incident on the nine `I9` external bits and `RL216`;
- `XB`, incident on the remaining seven left-external bits, `RL216`, and `RP27`;
- `Z27`, incident on the 24 right-external bits and `RP27`.

The existing exact rank-528 replacement elsewhere in the network remains unchanged.

The resulting structural network has

- 368 tensor leaves;
- 468 nontrivial indices;
- 371 binary indices;
- 94 ternary indices;
- one dimension-528 bond;
- one dimension-27 parent Schmidt bond;
- one dimension-216 left-support bond.

## 3. Complete tree

Use the previously certified 367-leaf sub-40 tree only as a **topological source**. In its unique local pattern

`[[A229, X8], Z8]`

replace the old two-factor parent representation by

`[[A229, XA], [XB, Z27]]`.

All other tree structure is retained.

The rewritten tree contains

- 368 leaves;
- 367 internal nodes;
- every leaf exactly once.

Every non-root boundary is recomputed in the target rank-27/support-216 hypergraph.

The maximum exact message dimension is

`D_max = 216 * 2^31 = 463,856,467,968`.

Equivalently,

`log2(D_max) = 38.75488750216347...`.

The maximizing node contains only the two factors `XB` and `Z27`. Their internal `RP27` bond is contracted, so the boundary contains

- 31 binary indices;
- the dimension-216 `RL216` bond.

The parent-rank dimension 27 is therefore not present in the maximum boundary.

The next-largest certified messages have dimension

`528 * 2^29 = 283,467,841,536`

with log-width `38.04439411935845...`.

Thus the complete tree satisfies

`W < 39`.

## 4. Full-family scope

Unlike the earlier `u2_31=1` rank-8 result, this theorem uses the uniform physical parent bound `rho_m<=27` and the uniform left support bound `|S_m|<=216`.

It therefore applies to **all 4096 physical fixed-mask cases** covered by the physical rank-envelope theorem, including both `u2_31=0` and `u2_31=1`.

The exact global structural chain for the physical q138 fixed-output one-QR family is now

`44 -> 42 -> 41 -> 40 -> 38.754887502...`.

## 5. Mask-conditioned refinements

The 64 possible left fixed-mask choices produce support sizes

`117,120,144,174,177,180,216`

with 13 distinct support sets in total.

If a fixed mask belongs to a smaller support class, the same tree may replace 216 by that class size. The class-specific maximum is

`max(528*2^29, |S_m|*2^31)`.

Thus the 216 bound is only the all-mask envelope; many masks have smaller exact structural width.

The parent rank classes 5,6,7,8 within `u2_31=1` do not improve the 216-based maximum in this tree because the parent-rank bond is internal to the maximizing `XB-Z` pair.

## 6. Common support structure for later composition

The mask-conditioned support sets have

- 13 distinct classes;
- union size 384;
- intersection size 96;
- exact rational rank 12 for the `64 x 512` mask/support selector matrix.

Hence later joint-mask composition need not carry 64 unrelated support tables. A mask-independent coordinate envelope of size 384 is exact, while the selector dependence itself admits an exact rank-12 linear representation.

This is a bridge to subsequent-layer tensor analysis, not yet a full second-layer contraction theorem.

## 7. Machine authority

Compact certificate:

`research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json`

Structural verifier:

`scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`

Algebraic dependencies:

- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`;
- `scripts/verify_v26_qr_q138_left_i9_support216.py`.

The structural verifier reconstructs the target hypergraph from canonical certificates, applies the deterministic local tree rewrite, and recomputes every cluster boundary.

## 8. What is not proved

This result is a message-dimension/representation upper bound. It does not yet prove

- an arithmetic-work exponent reduction of the same magnitude;
- practical dense storage of the maximum message;
- optimality of width `38.754887502...`;
- a double-round or full second-layer contraction;
- four-inverse-round exact energy;
- ranking gain;
- `alpha<1`;
- full-round relevance.

Because the present gain is exact with `epsilon=0`, epsilon-rank approximation is not activated at this stage.