# V26 Q1.38 four-leaf first dyadic star layer

## Scope

This theorem combines the certified first dyadic predecessor-leaf residues across all four output positions with the existing exact S1 central rank.

It constructs one exact low-rank dyadic layer of the complete five-QR star. It is not a rank bound for the complete star because higher dyadic residuals remain.

## Per-leaf exact dyadic lifts

The certified coefficient lattices are

`L_A,L_D in 2^-92 Z`,

`L_B,L_C in 2^-121 Z`.

Define integer-scaled leaves

`M_A=2^92 L_A`,
`M_D=2^92 L_D`,
`M_B=2^121 L_B`,
`M_C=2^121 L_C`.

The first residue theorems give

`rank_F2(M_A mod2)<=3`,
`rank_F2(M_D mod2)<=3`,
`rank_F2(M_B mod2)<=1052`,
`rank_F2(M_C mod2)<=1160`.

A GF(2) rank-r factorization `M mod2 = U V` can be lifted entrywise to integer binary matrices. The ordinary integer product `K=UV` then has rational rank at most r and satisfies

`M-K =0 mod2`.

Hence

`M = K +2R`

for an integer residual R. Therefore every certified parity-rank bound produces an exact first dyadic low-rank lift over Q, without claiming anything about the rank of the residual.

## Four-leaf product

Use the natural common scaling

`2^(92+121+121+92)=2^426`.

The scaled predecessor product is

`P=M_A tensor M_B tensor M_C tensor M_D`.

Choose the four first-layer lifts `K_A,K_B,K_C,K_D`. Expanding the product gives

`P = K_A tensor K_B tensor K_C tensor K_D +2 P1`

for an integer residual `P1`.

The first-layer rational Schmidt rank is at most

`3*1052*1160*3`

`=10,982,880`.

Its exponent is

`log2(10,982,880)=23.38875308074955...`.

The generic four-leaf Hilbert accounting at S1 was `2^44`; the new number applies only to the first dyadic layer, not the complete leaf product.

## Attach the exact S1 center

The admitted central rank is

`R_center<=3829*2^29=2,055,678,722,048`.

Using the same frozen-star channel product accounting, the first dyadic complete-S1 layer has at most

`(3829*2^29)*10,982,880`

`=22,577,272,722,806,538,240`

channels.

The exponent is

`64.2915050255997...`.

Again, this is not `W_repr(1)<=64.29`: the exact full factor is the first layer plus dyadically weighted residual layers. No full-factor storage or arithmetic-work reduction is admitted from this theorem alone.

## Consequence for the next search

The previous 84.90275 materialization barrier is not present in the first dyadic coefficient layer. The remaining question is whether the residual hierarchy can be represented and contracted with a controlled sum of layer ranks.

The next sharp objects are therefore:

1. B/C second dyadic residues;
2. higher A/D residues after the certified 309/310 second layer;
3. a total layer-rank/work summation fused into the central D16 common/private decomposition.
