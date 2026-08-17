# V26 q138 block1 x block2 shared-v3_12 no-gain theorem

## Statement

The current d=1 S1 central upper bound multiplies two disjoint physical-row blocks:

- block1 exact rank16;
- extended block2 exact rank21888.

Although the physical row variables are disjoint, the retained-column descriptions are not completely independent: block1 and the block2 j2-bit0 factor both contain the same internal column variable `v3_12`.

Merging this shared coordinate exactly does **not** reduce the product rank. The exact joint row-space rank of this smallest shared-column merge is

`16*21888 = 350208`.

Therefore the shared `v3_12` coordinate alone does not improve the canonical d=1 bound.

## 1. Block1 interface

The exact rank16 block1 uses physical rows

`A0,B0,C15,C16,D0`

and retained columns

`(sigma2_16, z2v_15, sigma2_14, sigma1_0, u3_0, v3_12)`.

Its exact row rank is16.

## 2. Block2 D16 bit0 interface

For fixed `D16`, the extended block2 bit0 factor uses physical row `C0` and retained columns

`(sigma2_0,u4_0,v3_12)`.

Each fixed-D16 bit0 row space has exact rank2. The two D16 spaces have union rank3 and hence intersection dimension1 in the standalone block2 theorem.

The coordinate `v3_12` is the common retained variable with block1 and must be identified, not duplicated.

## 3. Exact shared-coordinate merge

For fixed D16, form the joint row vectors by multiplying a block1 row with a bit0 row only when their `v3_12` coordinates agree, retaining one shared `v3_12` output coordinate.

The exact rational ranks are

- `rank(K'_0)=32`;
- `rank(K'_1)=32`;
- `rank(K'_0+K'_1)=48`.

Therefore

`dim(K'_0 ∩ K'_1)=32+32-48=16`.

So the standalone bit0 geometry

`2,2, intersection1`

has become exactly

`32,32, intersection16`,

which is simply the old geometry scaled by the block1 rank16. No extra overlap appears from identifying `v3_12`.

## 4. Recombine with the extended block2 D16 geometry

For every fixed independent high prefix `D12..15`, the previously certified extended-block2 j1 spaces satisfy

- `dim(J0)=dim(J1)=448`;
- `dim(J0 ∩ J1)=424`.

The j1 retained columns are disjoint from the merged `K'_D16` retained columns. Hence

`(J0 tensor K'_0) ∩ (J1 tensor K'_1)`

has dimension

`424*16`.

The fixed-prefix union rank is therefore

`448*32 + 448*32 - 424*16`

`= 21888`.

The sixteen `D12..15` j2-high sector vectors are exact independent, so the complete merged block1 x extended-block2 rank is

`16*21888 = 350208`.

This equals the existing product upper bound

`rank(block1)*rank(extended block2)=16*21888`.

Thus the shared-v3_12 coupling gives no rank reduction.

## Consequence

The canonical central S1 bound remains

`16*21888*2^23 = 171*2^34`,

and with the four predecessor-leaf exponent44,

`W_repr(1) <= W_factor-gen <= 78+log2(171)=85.4178525148859...`.

A future d=1 gain must use a coupling not captured by this single shared coordinate, for example a genuine multi-site j2 carry bridge between the block1 C12..16 region and the extended block2 sectors.

## Scope

This theorem closes only the smallest direct joint-channel overlap caused by the common retained coordinate `v3_12`. It does not prove the full central tensor rank is the product, and it does not exclude larger merged block1/block2 factors involving additional carry structure.

All ranks are exact over Q and `epsilon=0`.

Verifier:

`scripts/verify_v26_q138_block1_block2_shared_v312_no_gain.py`.
