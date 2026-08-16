# V26 q138 Width-41 Left-Map Rank-528 Theorem

## Purpose

`V26_QR_WIDTH41_SEPARATOR_TOPOLOGICAL_RANK_BOUND.md` bounded the certified 34-leaf child map

`L : 2^12 -> 3*2^10`

by the topological interface dimension `3072`.

This note evaluates the actual exact rational algebra of that left map for the q138 fixed-output wiring and proves

`rank(L)=528`.

Thus the first algebraic separator pass succeeds by a large margin: the 3072-dimensional topological interface contains only 528 independent directions for this q138 child map.

## 1. Why the q138 T4 segment has fixed zero w-bits

The local q138 output mask has only word B bit 10 active.

Backward transport through the final ChaCha rotation by 7 moves that mask to bit 3 on the C2/addition-4 output mask. Therefore the fourth modular addition is driven by

`w4 = 2^3`.

The certified 34-leaf bottleneck child uses the T4 carry segment around bits 23..29. In particular,

`w4_i = 0` for every `i=23,...,28`.

Those are precisely the fixed output-mask bits used in the rank calculation below.

## 2. Certified 34-leaf child geometry

Relative to the width-41 parent message, the 34-leaf child has

- 12 parent-external binary indices;
- an interface to the 306-leaf child containing 10 binary plus 1 ternary index.

Therefore its raw matrix dimensions are

`4096 x 3072`.

The exact child network separates further through the interface bit

`q = v3_6`.

After internal exact contraction it is the entrywise/tensor product of

- a small T1 piece `F1_q`;
- a larger T4/T3/T2/P26 piece `F2_q`.

The two q values occupy separate interface-column sectors.

## 3. Small T1 sector

For the relevant fixed-u T1 bit tensor, view the matrix with

- rows `(w,t)`;
- columns `(q=v,s)`.

For either possible fixed input bit `u`, the two q-sector column ranks are

`{2,1}`.

Which q value receives rank 2 is swapped when the fixed u bit flips, but the multiset is unchanged.

Moreover the two q-sector column spaces have zero intersection: their concatenated rank is

`2+1=3`.

Hence no rank is lost when the two q blocks are later combined.

## 4. Large piece and the r=v4_28 split

The larger piece has a second binary internal sector

`r = v4_28`.

For fixed q and r, it factorizes as a Kronecker product

`A_{q,r} tensor B_r`,

where

- `A` is the q138 T4 carry-segment plus P26 piece;
- `B` is the local T3/T2 piece.

The r bit is summed, so

`F2_q = A_{q,0} tensor B_0 + A_{q,1} tensor B_1`.

## 5. Exact q138 T4 ranks

Using the exact Fraction TT cores for the fixed q138 pattern

`w4_23=...=w4_28=0`,

the two r-sector ranks are

- `rank(A_{q,0}) = 18`;
- `rank(A_{q,1}) = 17`.

For both q values, the concatenated column-space rank is only 18. Therefore

`Col(A_{q,1}) subset Col(A_{q,0})`.

The q bit enters this T4/P26 piece only through an affine parity relabeling, so the same dimensions hold for q=0 and q=1.

## 6. Exact local T3/T2 ranks

For the T3/T2 piece, each r sector has

`rank(B_0)=rank(B_1)=6`.

Their concatenated column-space rank is

`10`.

Therefore

`dim(Col(B_0) intersection Col(B_1)) = 6+6-10 = 2`.

This statement was checked exactly for

- both possible fixed T2 input bits;
- both affine relabelings of the r bit on the T2 side;
- both affine relabelings of the r bit on the T3 side.

So the rank statement does not depend on those fixed-mask/XOR conventions.

## 7. 176-dimensional large-sector bound

Choose a direct-sum decomposition

`Col(B_0)=I direct_sum E_0`,

`Col(B_1)=I direct_sum E_1`,

where

- `dim(I)=2`;
- `dim(E_0)=dim(E_1)=4`.

Because `Col(A_{q,1})` is contained in `Col(A_{q,0})`, the column space of

`F2_q = A_{q,0} tensor B_0 + A_{q,1} tensor B_1`

is contained in the sum of three subspaces:

1. `Col(A_{q,0}) tensor I`, dimension at most `18*2 = 36`;
2. `Col(A_{q,0}) tensor E_0`, dimension at most `18*4 = 72`;
3. `Col(A_{q,1}) tensor E_1`, dimension at most `17*4 = 68`.

Therefore

`rank(F2_q) <= 36+72+68 = 176`.

Independent exact sparse Fraction Gaussian elimination attains 176 for both q sectors, so

`rank(F2_0)=rank(F2_1)=176`.

This is an exact rational rank equality, not a floating tolerance result and not a finite-field-only witness.

## 8. Exact left-map rank

For each q sector,

`rank(F1_q tensor F2_q) = rank(F1_q) * rank(F2_q)`.

The F1 q-sector column spaces are disjoint. Therefore the two q blocks add their ranks exactly:

`rank(L)`

`= 2*176 + 1*176`

`= 528`.

Hence

`rank(L)=528`.

## 9. Compression factor

The previous topology-only interface dimension was

`3072`.

The actual exact q138 left-map rank is

`528`.

Thus the algebraic compression factor is

`3072/528 = 64/11 ~= 5.81818`.

The effective Schmidt width is

`log2(528) ~= 9.0443941` bits.

Relative to the 12-bit smaller external side, the exact rank saves

`12-log2(528) ~= 2.9556059` bits.

Relative to the topology-only interface width `log2(3072)=11.5849625`, algebra removes about

`2.5405684` effective bits.

## 10. Machine verifier

The independent verifier is

`scripts/verify_v26_qr_width41_left_rank528.py`.

It uses only exact `Fraction` arithmetic. It reconstructs

- the q138 fixed-zero T4 segment through exact TT factorization;
- the sparse 34-child subfactors required for the rank proof;
- both T1 fixed-u cases;
- every T2 fixed-u / T2-r-shift / T3-r-shift combination.

Expected output is

`PASS V26_QR_WIDTH41_LEFT_MAP_RANK528`

followed by the exact rank summary

`A_sector_ranks=18,17 ... F2_rank=176 ... L_rank=528`.

## 11. Consequence for the global QR representation

The 34-leaf child map admits an exact rank factorization

`L(x_12,z_3072) = sum_{r=1}^{528} X(x_12,r) Z(r,z_3072)`.

Therefore the original 3072-dimensional child interface can be replaced, for this q138 fixed-output structure, by an exact internal bond of dimension 528 before it is connected to the 306-leaf sibling.

This is the first certified algebraic bond compression beyond the graph/min-cut limit of the width-41 certificate.

It does **not** by itself prove a new global contraction width. The compressed bond must be reinserted into the whole QR network and a complete contraction/representation certificate must be constructed.

## 12. Next exact target

Replace the certified 34-leaf subnetwork by its exact rank-528 factorization and recompute the whole fixed-output q138 QR contraction geometry.

The immediate question is whether the previous 41-bit dense-message bottleneck can be reduced below 41 when the 528-dimensional algebraic bond is kept factorized rather than materializing the 340-leaf parent message.

A complete global certificate is required before changing the admitted global width.

## 13. Claims not admitted

This theorem does not yet prove a global width below 41, practical exact QR evaluation, a full second-layer contraction, a double-round/full-round result, ranking gain, or `alpha<1`.
