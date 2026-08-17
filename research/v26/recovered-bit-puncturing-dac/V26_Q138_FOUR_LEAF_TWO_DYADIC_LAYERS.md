# V26 Q1.38 four-leaf first two dyadic layers

## Scope

This theorem extends the clean four-leaf first dyadic layer by one exact lifting step. It uses the certified A/D second-residue bounds and only the generic 11|21 rank cap for the still-unresolved B/C second residues.

It constructs the first two exact dyadic layers of the four-predecessor-leaf product and of the complete S1 star. It is not a bound for the full residual hierarchy.

## Per-leaf lifts

Use the natural integer-scaled predecessor leaves

`M_A=2^92 L_A`, `M_D=2^92 L_D`,

`M_B=2^121 L_B`, `M_C=2^121 L_C`.

Choose first-layer integer lifts

`M_X = K_X +2 R_X`.

Certified first-layer ranks are

- `rank_Q(K_A)<=3`;
- `rank_Q(K_B)<=1052`;
- `rank_Q(K_C)<=1160`;
- `rank_Q(K_D)<=3`.

For A/D, the clean second-residue theorem gives

- `rank_F2(R_A mod2)<=309`;
- `rank_F2(R_D mod2)<=310`.

For B/C, no second-residue theorem is required here. Their 11|21 matrices have only `2^11=2048` rows, so universally

- `rank_F2(R_B mod2)<=2048`;
- `rank_F2(R_C mod2)<=2048`.

## Four-leaf product expansion

Let

`P=M_A tensor M_B tensor M_C tensor M_D`.

The first layer is

`P0=K_A tensor K_B tensor K_C tensor K_D`

with

`rank_Q(P0)<=3*1052*1160*3=10,982,880`.

Write

`P=P0+2Q`.

Modulo2, every term containing two or more residual factors vanishes. Therefore

`Q mod2`

is the sum of exactly four single-residual tensor terms. Subadditivity and tensor-product rank give

`rank_F2(Q mod2) <=`

`309*1052*1160*3`

`+3*2048*1160*3`

`+3*1052*2048*3`

`+3*1052*1160*310`

`=2,306,905,824`.

A GF(2) factorization of `Q mod2` can again be lifted to an integer matrix `K1` of rational rank at most the same number with `Q-K1` even. Hence

`P=P0+2 K1+4 Q2`

for an integer residual `Q2`, with

`rank_Q(K1)<=2,306,905,824`.

## Cumulative first-two-layer leaf rank budget

The sum of the two certified layer ranks is

`10,982,880 +2,306,905,824`

`=2,317,888,704`.

Its exponent is

`31.110164149389277...`.

The old generic four-leaf S1 Hilbert budget is `2^44`. Thus, before accounting for the remaining `4 Q2` hierarchy, the first two exact layers consume only

`2,317,888,704 /2^44`

of that generic channel budget. The remaining multiplicative headroom is

`2^44 /2,317,888,704 =7589.74579498...`,

or

`12.8898358506107...` bits.

This is headroom for the unresolved residual hierarchy, not an admitted full-rank gain.

## Attach the exact S1 center

The admitted central rank is

`R_center=3829*2^29=2,055,678,722,048`.

First layer:

`R_center*10,982,880`

`=22,577,272,722,806,538,240`,

exponent `64.2915050255997...`.

Second layer:

`R_center*2,306,905,824`

`=4,742,257,216,165,408,407,552`,

exponent `72.00606390817963...`.

Cumulative first two layers:

`R_center*2,317,888,704`

`=4,764,834,488,888,214,945,792`,

exponent `72.01291609423944...`.

These are layer-wise channel bounds, not `W_repr(1)<=72.01`: the exact `4 Q2` residual remains.

## Next sharp object

The highest-value next computation is no longer the first B/C parity layer; that is closed. It is the B/C second dyadic residue, because replacing the generic `2048,2048` terms in the second-layer formula can lower `2,306,905,824` directly and also provides the data needed for the third product layer.
