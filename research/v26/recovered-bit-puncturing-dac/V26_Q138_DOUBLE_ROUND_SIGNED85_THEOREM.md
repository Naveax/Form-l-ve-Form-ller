# V26 q138 Exact Double-Round Signed Local-Rank Bound

## Statement

For the q138 fixed-output inverse-double-round five-QR star, exact dyadic local Walsh rank factorizations improve the nonlinear-support representation bound further to

`W_2_repr <= 79 + log2(87) = 85.44294349584872...`.

Equivalently the maximum message dimension on the frozen HT tree is at most

`87 * 2^79`.

This is an exact representation-existence theorem. The separately certified constructive ledger remains `W_2_construct<=95`.

## 1. Starting geometry

The frozen HT tree has two unique critical 11|21 central bipartitions:

`S1={0,1,2,3,4,5,12,13,14,15,16}`

and

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

The four fixed-input/single-output leaf vectors contribute the generic exact Hilbert exponent44 on either critical split.

For the central q138 QR, the fixed j4 output mask is `2^3`. Modular-addition MSB conservation therefore gives

`msb(u4)=msb(v4)=3`,

and the j3 rotation relation gives

`msb(u3)=msb(v3)=27`.

The previous support theorem used only the zero/nonzero consequences of these identities. The present theorem keeps the exact dyadic Walsh amplitudes and computes small local matrix ranks.

## 2. Exact local Walsh tensor

For an interior addition bit, use

`T(s,t,u,v,w) = 1[t=s xor u xor v xor w] * 1[s=1 or u=v=w] * (-1)^((u xor w)(v xor w)) * 2^(-s)`.

At bit0, sum out the absent previous-sigma leg, giving

`T0(s,u,v,w) = 1[s=1 or u=v=w] * (-1)^((u xor w)(v xor w)) * 2^(-s)`.

All local rank computations below are exact over `Q`; no floating tolerance or modular lower-bound inference is used.

## 3. S1 block 1: rank 16 on five physical row bits

Consider the physical S1 row variables

`A0,B0,C15,C16,D0`.

Every central occurrence of these five variables is included in the local subnetwork:

- j1 bit0 contains `A0,B0,D0`;
- j2 bit16 contains `C16,D0`;
- j2 bit15 contains `C15`.

Using the exact q138 MSB consequences

- `z2w_16=0`;
- `z2w_15=1`;
- `z2v_16=D0`,

the subnetwork is flattened from the five physical row bits to the interface variables

`(sigma2_16,z2v_15,sigma2_14,sigma1_0,u3_0,v3_12)`.

The resulting exact `32 x 64` rational matrix has rank

`16`.

Therefore these five physical row bits communicate with the rest of the central tensor through at most16 exact signed channels, rather than32 coordinate states.

## 4. S1 block 2: rank 2784 on thirteen physical row bits

Use the disjoint physical S1 row set

`A13..A16, B13..B16, D13..D16, C0`,

thirteen bits total.

All occurrences of the D bits are closed inside the block:

- D13..D16 occur in j1 bits13..16;
- D13,D14,D15 occur again in j2 bits29,30,31;
- D16 occurs again in j2 bit0.

For a fixed four-bit D sector:

1. the exact j1 bits13..16 row space on the eight A/B row bits has rank112;
2. j2 bits29..31 contribute an exact sector vector carrying the second occurrences of D13..15;
3. j2 bit0 contributes an exact rank-2 row space on C0 and closes the second occurrence of D16.

Taking exact Kronecker products of bases within each D sector and then exact rational union-rank over all16 D sectors gives

`rank = 2784`

for the full thirteen-row-bit block.

The verifier constructs 3584 exact sector-basis product vectors and reduces them over `Q`; their span dimension is2784.

## 5. S1 central rank

The two S1 blocks use disjoint physical row variables, so their exact rank channels may be multiplied safely. The remaining

`44 - 5 - 13 = 26`

physical S1 row bits are passed trivially.

Hence

`rank_center(S1) <= 16 * 2784 * 2^26`.

Since

`16 * 2784 = 87 * 2^9`,

this is

`rank_center(S1) <= 87 * 2^35`.

The complementary 21-site matricization has the same matrix rank bound.

This improves the earlier support-row bound `3*2^42`.

## 6. S2 signed top block

For S2, consider j1 bits31..27.

The fifteen physical row bits are

`A27..31, B27..31, D27..31`.

The D top pattern is kept as an explicit 32-sector label because those D bits also occur in j2 elsewhere. Within a fixed D sector, the exact j1 top tensor maps the ten A/B row bits to

- five internal `v3_7..11` bits;
- the outgoing sigma bit at26.

Exact rational ranks of the 32 D sectors are

- two sectors of rank32;
- thirty sectors of rank64.

Thus a valid exact sector-channel upper bound for all fifteen S2 row bits is

`2*32 + 30*64 = 1984 = 31*2^6`.

The other29 S2 physical row bits are passed trivially, so

`rank_center(S2) <= 1984 * 2^29 = 31 * 2^35`.

This is below the S1 central bound.

## 7. Complete HT-tree bound

At either critical 11|21 split the four leaf vectors retain the generic exponent44.

Therefore

- S1 message dimension `<= (87*2^35)*2^44 = 87*2^79`;
- S2 message dimension `<= (31*2^35)*2^44 = 31*2^79`.

Every noncritical node of the frozen HT tree already had generic-envelope exponent at most80.

Hence the complete maximum is

`87*2^79`,

so

`W_2_repr <= log2(87*2^79) = 79+log2(87) = 85.44294349584872...`.

## 8. Why the local products are globally valid

Each compressed S1 block either includes every central occurrence of its physical row variables, or, in the S2 top calculation, keeps the multiply-used D bits explicitly as sector labels. No physical row variable is silently mixed across a rank factor while also reappearing elsewhere in the network.

The two S1 blocks use disjoint physical row-variable sets. They may share internal interface variables; that does not invalidate the product upper bound, because after exact local rank factorization the row dependence enters the remainder only through the pair of rank-channel indices.

This occurrence accounting is essential. Local rank calculations that mix a physical row variable while forgetting a second occurrence elsewhere are not admissible.

## 9. Constructive ledger

This theorem proves existence of a lower-rank exact representation across the critical matricizations. It does not yet provide a complete factor-generation/contraction tree whose peak is bounded by `85.4429...`.

Retain separate ledgers:

- exact representation existence: `W_2_repr <= 79+log2(87)`;
- explicit constructive central-graph plus leaf-HT construction: `W_2_construct <=95`.

## 10. Verification

Authority verifier:

`scripts/verify_v26_q138_double_round_signed85.py`.

It uses exact `Fraction` arithmetic and sparse Gaussian elimination to verify

- S1 block1 rank16;
- S1 block2 rank2784;
- S2 D-sector rank distribution `{32:2,64:30}`;
- the resulting central bounds;
- every node of the frozen HT tree.

## 11. Scope

No approximation is used. No true optimality, arithmetic-work improvement, practical evaluator, ranking gain, `alpha<1`, or full-round cryptanalytic relevance is claimed.
