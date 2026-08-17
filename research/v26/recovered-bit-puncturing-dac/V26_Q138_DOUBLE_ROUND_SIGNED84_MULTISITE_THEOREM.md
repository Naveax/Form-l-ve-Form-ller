# V26 q138 exact d=1 four-site signed-rank theorem

## Statement

For the q138 fixed-output inverse-double-round five-QR star, the d=1 S1 central matricization admits the exact bound

`rank_center(S1) <= 261 * 2^32`,

and therefore the frozen complete HT tree satisfies

`W_repr(1) <= 76 + log2(261) = 84.02790599656988...`.

This improves the previous signed85 bound by

`log2(8/3)=1.415037499278844...` bits.

All arithmetic is exact and `epsilon=0`.

## Starting point

The previous exact S1 factorization used

- block1 rank16 on five physical row bits;
- block2 rank2784 on thirteen disjoint physical row bits;
- twenty-six remaining physical row bits passed raw.

Among those raw bits, take all eight physical input-mask bits on sites2 and3:

`A2,B2,C2,D2,A3,B3,C3,D3`.

They are disjoint from block1 and block2.

## Occurrence-closed four-site block

The physical D bits occur twice in the fused exact central QR representation:

- `D2` occurs as `d0` at site2 and as `d1` at site18;
- `D3` occurs as `d0` at site3 and as `d1` at site19.

Therefore use the four fused sites

`{2,3,18,19}`

as one local block. This includes every central occurrence of the eight physical row variables.

The exact q138 output has `b0=Bout[i+7]=1` only at site3; it is0 at sites2,18,19.

Within each adjacent pair `(2,3)` and `(18,19)`, contract the four longitudinal modular-addition carry channels exactly. Retain the pair-boundary carries as column/interface variables. The long-range fused K/z channels are deliberately relaxed as independent retained columns. This relaxation can only enlarge row rank; re-identifying/contracting those columns in the true network is a linear map on the column side and cannot increase the row rank.

The complement physical bits `D18,D19` are retained/summed as column variables while their two occurrences are identified between the main and complement pairs.

## Exact rank96

The resulting relaxed coefficient map has256 physical rows. Rather than materializing its enormous column space, the verifier constructs the exact integer Gram matrix after a common scale.

Its row structure is exceptionally simple:

-64 Gram rows are exactly zero;
- the other192 rows form96 equality/sign pairs;
- therefore `rank_Q(Gram)<=96`;
- rank modulo the odd prime1000003 is96, so a96x96 integer minor is nonzero and `rank_Q(Gram)>=96`.

Hence

`rank_Q(Gram)=96`.

For a real/rational coefficient matrix M,

`rank(M M^T)=rank(M)`,

so the relaxed four-site coefficient map itself has exact rational rank96.

The signed-class structure also makes the factor explicit: each nonzero physical row is exactly `+1` or `-1` times one of96 physical-row basis directions;64 physical rows vanish.

## New S1 rank

Replace eight raw row bits, formerly dimension256, by the exact96-channel block. The other eighteen formerly-raw bits remain trivial. Thus

`rank_center(S1) <= 16 * 2784 * 96 * 2^18`.

Since

`16*2784*96*2^18 = 261*2^32`,

this is exactly a factor `3/8` of the previous `87*2^35` bound.

With four generic predecessor-leaf Hilbert exponents44,

`dim_message(S1) <= 261*2^76`,

hence

`W_S1 <= 76+log2(261)=84.02790599656988...`.

The previous S2 exact message remains

`31*2^79`, exponent `83.95419631038688...`,

and all noncritical frozen-tree nodes remain at most80. Therefore S1 still wins, but only by about0.07371 bits.

## Scope

This is an exact representation upper bound. It is not a lower bound or optimality statement. The long-range-channel relaxation is safe only in the direction used here: it may lose additional compression, never create a falsely small rank.

The associated materialized-factor constructivity is certified separately because the rank96 signed classes have an explicit physical-row basis.

Verifier:

`scripts/verify_v26_q138_double_round_signed84_multisite.py`.
