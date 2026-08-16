# V26 q138 Physical Right/Parent Rank-Envelope Theorem

## Purpose

The certified width-40 q138 one-QR representation contains a unique 171-leaf bottleneck with a `64|107` child split through six binary interface bits. Previous work proved the left 64-leaf child has uniform exact rank 48 and that the 107-leaf right rank is input-mask conditioned.

This note closes the physical fixed-mask rank envelope exactly.

For every physical fixed input mask compatible with the q138 fixed-output right-map geometry:

- the 107-leaf right map has exact rank between 11 and 38;
- the full 171-leaf parent flattening has exact rank between 5 and 27.

Thus the formal `2^40` bottleneck admits, for every physical fixed-mask coefficient instance, an exact Schmidt factorization with at most 27 channels across the certified `16|24` external partition.

## 1. Physical control bits

The actual parity factor is

`u4_i xor v3_{i+12} xor w2_i = 0`.

Therefore the generalized affine parity controls `p_i` are not physical source-mask parameters. Fix `p_i=0`.

The 107-leaf right map depends on twelve physical fixed input-mask bits:

- `u1_3,...,u1_7` (5 bits);
- `u2_3,...,u2_8,u2_31` (7 bits).

Hence the complete physical fixed-mask family has exactly

`2^12 = 4096`

cases.

The bit `u2_8` is shared with the left child but is rank-inert on the right map: flipping it never changes the exact right rank.

## 2. Transfer calculation

Use the exact five-site transfer chain and the physical reachable hull from

`V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`.

The calculation is finite-state exact algebra, not 4096 independent 107-leaf contractions:

1. build the four site-3 doubled boundary vectors for each physical `(u1_3,u2_3)` choice;
2. propagate them through the exact site-4,5,6 transfer operators selected by `(u1_i,u2_i,p=0)`;
3. close with the site-7 tensor, keeping `u2_8` and the T2 bit-31 control `u2_31` as their actual boundary controls;
4. assemble the exact `64 x 64` right Gram matrix in the canonical six-interface-bit order;
5. compute exact rational rank.

All arithmetic is dyadic/rational. No floating rank tolerance, sigma cap or approximation is used.

## 3. Exact right-map envelope

Over all 4096 physical fixed-mask cases,

`11 <= rank(R_m) <= 38`.

The exact rank distribution is:

| rank | cases |
|---:|---:|
| 11 | 172 |
| 12 | 34 |
| 13 | 130 |
| 15 | 4 |
| 16 | 4 |
| 17 | 1024 |
| 18 | 396 |
| 19 | 284 |
| 22 | 86 |
| 23 | 28 |
| 24 | 188 |
| 25 | 92 |
| 26 | 64 |
| 27 | 184 |
| 28 | 228 |
| 29 | 168 |
| 30 | 322 |
| 33 | 4 |
| 34 | 4 |
| 37 | 428 |
| 38 | 252 |

The T2 bit-31 boundary control creates a particularly strong split:

- if `u2_31=0`, right rank lies in `22..38`;
- if `u2_31=1`, right rank lies in `11..19`.

Thus the raw six-bit interface dimension 64 is never attained by a physical right map.

## 4. Left row-space collapse

The left 64-leaf map has rank 48 for all 64 combinations of its six fixed T1/T2 input bits, as already proved.

A stronger fact holds: its exact 48-dimensional row space has only two classes, selected solely by the shared bit `u2_8`.

Within either value of `u2_8`, changing the other five left fixed bits does not change the exact row space. This is verified by exact union-rank tests: the representative row space and every same-`u2_8` row space have combined rank 48.

Therefore the full parent-rank classification does not require multiplying 64 unrelated left maps by every right map. Only the two exact left row-space representatives are needed.

## 5. Canonical interface order

The six interface bits are ordered canonically as

1. `aux_j2_i8_k0`;
2. `aux_j4_i11_k0`;
3. `aux_j4_i16_k0`;
4. `sig1_7`;
5. `sig3_7`;
6. `sig4_7`.

The second entry is the site-3/start interface bit. The verifier assembles the Gram matrix in this canonical order before multiplying by the left map.

This ordering matters for the parent product even though it does not affect the right-map rank itself.

## 6. Exact parent envelope

Let

`M_m = L_m R_m`

be the certified 171-leaf parent flattening across its `16|24` external partition.

Using the exact left row-space representative selected by the shared `u2_8` bit and the exact right Gram matrix for each of the 4096 physical right controls gives

`5 <= rank(M_m) <= 27`.

The exact parent-rank distribution is:

| rank | cases |
|---:|---:|
| 5 | 240 |
| 6 | 100 |
| 7 | 1028 |
| 8 | 680 |
| 16 | 120 |
| 17 | 338 |
| 18 | 410 |
| 19 | 42 |
| 20 | 450 |
| 23 | 8 |
| 26 | 428 |
| 27 | 252 |

Again the bit-31 boundary control is decisive:

- if `u2_31=0`, parent rank lies in `16..27`;
- if `u2_31=1`, parent rank lies in `5..8`.

The shared `u2_8` bit does not change the parent rank after the corresponding left row-space class is used.

## 7. Cross-checks

The exact transfer calculation reproduces the previously admitted fixed-mask examples:

- zero representative: right rank 34, parent rank 23;
- all-one representative: right rank 19, parent rank 8;
- previous high representative: right rank 37, parent rank 26.

These matches are useful because they compare the finite-state transfer route against the earlier full doubled-network Gram contractions.

## 8. Algebraic consequence

For every physical fixed-input/fixed-output q138 coefficient instance, the 171-leaf bottleneck tensor satisfies

`rank(M_m) <= 27`

across the certified `16|24` split.

Therefore it admits an exact factorization

`M_m(x_A,x_B) = sum_{r=1}^{rho_m} X_m(x_A,r) Z_m(r,x_B)`

with

`rho_m <= 27`.

This is a much stronger statement than the topology-only six-bit interface bound `<=64` and the uniform left-child bound 48.

The rank basis may depend on the fixed mask `m`; the theorem is a uniform dimension envelope, not a claim that one mask-independent 27-dimensional basis works for all masks simultaneously.

## 9. Global-width caveat

A low Schmidt rank at the bottleneck must still be reinserted into the whole network and followed by a complete contraction-tree/work certificate before changing the admitted global `W<=40` bound.

Exploratory rank-27 reinsertion gives very small top-level separators, but one natural recursive geometry still encounters a subproblem that does not split below 40. That is a scoped geometry result, not a lower bound or NO-GO for `W<40`.

## 10. Machine verifier

Authority verifier:

`scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

It uses exact rational transfer algebra, enumerates the finite physical 4096-control family on the transfer chain, verifies both distributions, verifies the two left row-space classes, and checks the previous three full-network reference ranks.

## 11. Claims not admitted

This theorem does not prove global `W<=39`, practical exact QR evaluation, an arithmetic-work exponent reduction, full second-layer contraction, ranking gain, `alpha<1`, or full-round relevance.