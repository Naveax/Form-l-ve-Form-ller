# V26 Q1.38 predecessor-leaf A/D second dyadic residue

## Scope

This is an exact coefficient-arithmetic statement for the predecessor one-QR leaf at output positions A and D, across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split. It is not a rational Schmidt-rank bound and not an arithmetic-work win.

The previous clean theorem proved

`L_A,L_D in 2^-92 Z`

and the first residue bound

`rank_F2((2^92 L_A) mod2)<=3`,

`rank_F2((2^92 L_D) mod2)<=3`.

## Exact second lift

Write

`M=2^92 L`.

Choose the integer first-layer lift `M0` as the sum of the three affine indicators that survive modulo2:

1. weight92 zero carry `(j1,bit0)`;
2. weight92 zero carry `(j3,bit0)`;
3. weight93 top two-point fiber with equal signs.

Then `M-M0` is even entrywise, so

`M1=(M-M0)/2`

is an integer coefficient tensor.

Only carry weights93,92,91 can affect `M1 mod2`.

### Affine rank-one sectors

For A/D, among the weight91 two-zero sectors the internal rank128 sectors are exactly the183 pairs containing `(j1,bit0)` or `(j3,bit0)`.

After full affine consistency:

- A:181 are reachable; the two impossible sectors are `((j1,bit0),(j2,bit15))` and `((j2,bit15),(j3,bit0))`;
- D: all183 are reachable.

Every reachable weight91 support has zero intersection between the S1 and complement beta-column images, hence communication rank1.

For weight92 nullity-one sectors, the contribution to `M1 mod2` is the equal-sign derivative-zero indicator.

- A:90 reachable; `(j2,bit15)` is impossible;
- D:91 reachable.

Every reachable derivative-zero support again has zero S1/complement beta-image intersection, hence communication rank1.

### Three signed quadratic sectors

The remaining terms are the two weight92 unique-solution sectors and the weight93 equal-sign top sector. On their rank-one affine support, the sign phase is a quadratic Boolean form.

After exact internal elimination, the cross-S1/complement bilinear ranks of that quadratic form are:

- A:11,10,11;
- D:10,10,10.

A quadratic form with cross bilinear rank `r`, gated by a rank-one affine support, has communication rank at most `r+2`: one term for the left-only part, one for the right-only/constant part, and `r` separable bilinear terms.

Therefore

A:

`rank_F2(M1 mod2) <= 181 + 90 + (11+2)+(10+2)+(11+2) =309`.

D:

`rank_F2(M1 mod2) <= 183 + 91 + 3*(10+2) =310`.

So the exact dyadic beginning is

`2^92 L = M0 + 2 M1`,

with

`rank_F2(M0)<=3`,

`rank_F2(M1_A mod2)<=309`,

`rank_F2(M1_D mod2)<=310`.

## Interpretation

The first two 2-adic layers are dramatically smaller than the generic single-leaf 11|21 dimension2048, but this does not by itself imply a rational leaf rank below2048. Higher dyadic residues can still accumulate new channels.

The next exact A/D object is the third residue after choosing a low-rank integer lift of `M1 mod2`. In parallel, the B/C natural scale `2^121` first parity layer remains open.
