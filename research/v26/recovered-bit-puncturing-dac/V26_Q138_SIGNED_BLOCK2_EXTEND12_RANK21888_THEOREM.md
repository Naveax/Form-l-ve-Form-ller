# V26 q138 signed block2 site12 extension rank-21888 theorem

## Statement

Extend the clean d=1 S1 block2 by the three previously raw physical bits

`A12,B12,D12`.

All occurrences are closed: `D12` occurs in j1 bit12 and again in j2 bit28. The resulting exact sixteen-physical-row-bit block

`A12..16, B12..16, D12..16, C0`

has exact rational row rank

`21888`.

The old block2 rank2784 with three extra raw bits would cost

`2784*8=22272`.

Thus the exact gain is

`22272/21888 = 58/57`,

or `log2(58/57)=0.02509098096283...` bits.

## j1 sector structure

Fix a five-bit D sector `D12..16`.

The clean j1(13..16) row space has exact rank112. Add j1 bit12 and keep `A12,B12` as physical row bits. Treating those two new row bits trivially gives the exact upper bound `4*112=448`; exact rational basis construction in the verifier attains448 for every sector.

Now fix only `D12..15` and compare the `D16=0` and `D16=1` j1 subspaces. Each has dimension448. Exact rational union rank is472 for all16 choices of `D12..15`, so

`dim(J0 ∩ J1)=448+448-472=424`.

No modular inference is needed for this step; the verifier constructs exact Fraction bases.

## j2 high and bit0 sectors

The j2 bits28..31 tensor closes the second occurrences of `D12..15`. The sixteen exact high-sector vectors indexed by `D12..15` are linearly independent over Q, so the sixteen four-bit sectors form a direct sum.

`D16` closes separately through j2 bit0. For fixed `D16`, the two physical `C0` rows span a2-dimensional exact subspace. The union of the `D16=0` and `D16=1` bit0 subspaces has dimension3, hence their intersection has dimension1.

## Exact rank calculation

Within a fixed independent `D12..15` high sector, the two `D16` row spaces are

`J0 ⊗ K0`

and

`J1 ⊗ K1`,

with dimensions `448*2` each. For tensor-product subspaces,

`(J0⊗K0) ∩ (J1⊗K1) = (J0∩J1) ⊗ (K0∩K1)`.

Therefore the fixed-prefix union dimension is

`448*2 + 448*2 - 424*1 = 1368`.

The sixteen independent j2-high sectors give

`16*1368 = 21888`.

Hence the extended block rank is exactly21888.

## Consequence for d=1 representation

The rank16 block1 remains disjoint. The extended block2 now consumes16 physical S1 bits instead of the old13, leaving23 raw S1 physical bits. Therefore

`rank_center(S1) <= 16 * 21888 * 2^23`.

Relative to the clean signed85 central bound `16*2784*2^26`, this is exactly the factor

`57/58`.

With the four predecessor-leaf Hilbert exponent44,

`W_repr(1) <= 85.44294349584872... - log2(58/57)`

so

`W_repr(1) <= 85.4178525148859...`.

This is an exact representation upper bound, `epsilon=0`. The coefficient-aware materialized-factor generation ledger remains85.442943... until a separate explicit physical-row/factor-generation bridge for the extended rank21888 block is certified.

Verifier:

`scripts/verify_v26_q138_signed_block2_extend12_rank21888.py`.
