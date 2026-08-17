# V26 Q138 predecessor-leaf B/C second dyadic residue: rank 1016 / 1220

## Scope

Let

`M_B = 2^121 L_B = K_B,0 + 2 R_B`,

`M_C = 2^121 L_C = K_C,0 + 2 R_C`,

with the already admitted first integer lifts

`rank_Q(K_B,0) <= 36`,

`rank_Q(K_C,0) <= 84`.

This theorem constructs second integer lifts for `R_B mod 2` and `R_C mod 2`. It is not a full rational Schmidt-rank theorem for either complete predecessor leaf.

## 1. Support-only second-residue part

The clean support-frequency nesting theorem decomposes the support-indicator contribution into the weight-120 unique-solution frequency space. The e1 support corrections and raw-e0 support indicators add no new left Walsh frequencies.

Therefore integer support-only lifts exist with

`rank_Q(S_B^lift) <= 668`,

`rank_Q(S_C^lift) <= 788`.

This is the existing clean authority `V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_SUPPORT_FREQUENCY_NESTING`.

## 2. Exact e0 Gauss-sign correction

The raw e0 carry sectors have class counts

- one `(124,4,2)` sector;
- fourteen `(125,3,2)` sectors;
- eight `(126,2,0)` sectors;
- seventy-four `(127,1,0)` sectors;
- 484 `(128,0,0)` sectors before external consistency filtering.

For polar-rank-zero fibers, the nonzero-Gauss support kills all residual linear fiber terms and the sign equals the section phase.

Only the polar-rank-two sectors require completion of squares. Their nullspaces have dimension 3 or 4. For each such sector, the exact Gauss sum over the small nullspace is enumerated and its sign is interpolated as a quadratic ANF in the nullspace linear-term bits. Direct external-support witnesses are then summed over the entire internal fiber and compared to the completed sign formula.

For the actual nullspace bases used by the verifier the required sign correction is represented by the quadratic monomial selected by the exact ANF solve; no assumed closed form is used by the theorem.

After this exact correction, raw e0 sectors sharing one canonical external support are XOR-aggregated before rank accounting. This is mandatory because the second residue is over `F_2`.

The raw sectors collapse to

- B: 581 sectors -> 251 canonical-support groups, multiplicities `1^103, 2^57, 4^91`;
- C: 577 sectors -> 250 groups, multiplicities `1^103, 2^57, 4^90`.

Uniformly over every fixed 128-bit predecessor input and every right assignment, the grouped e0 correction left-function spans have dimensions

`rank_F2(E_B) <= 272`,

`rank_F2(E_C) <= 388`.

## 3. Four half-integral sectors

The four weight-122 half-integral sectors share one support. Their exact second-bit Boolean correction is

`h(q_1,q_2,q_3,q_4) = 1 + sum_i q_i + sum_{i<j} q_i q_j`

over `F_2`.

The uniform supported left-function spans are

`rank_F2(H_B) <= 252`,

`rank_F2(H_C) <= 280`.

## 4. Sign-dependent overlap

The e0 and half-correction spans are not disjoint. Exact GF(2) union ranks are

`rank_F2(E_B + H_B) <= 348`,

`rank_F2(E_C + H_C) <= 432`.

Thus the overlaps have dimensions at least 176 for B and 236 for C relative to the separate envelopes.

Any binary matrix of GF(2) rank `r` has an integer lift congruent modulo 2 with rational rank at most `r`, by lifting an `F_2` rank factorization to integer 0/1 factors. Hence integer sign-dependent second lifts exist with ranks at most 348 and 432.

## 5. Complete second-residue lifts

Write the complete second residue as support-only plus sign-dependent parts. Adding the two integer lifts gives

`rank_Q(K_B,1) <= 668 + 348 = 1016`,

`rank_Q(K_C,1) <= 788 + 432 = 1220`,

with

`R_B = K_B,1 + 2 R_B,2`,

`R_C = K_C,1 + 2 R_C,2`.

Therefore the current predecessor-leaf dyadic envelopes become

A: `[3,219,2048,...]`,

B: `[36,1016,2048,...]`,

C: `[84,1220,2048,...]`,

D: `[3,207,2048,...]`.

No claim is made about the complete rational rank of a B or C leaf, nor about arithmetic-work reduction. The unresolved higher residues remain bounded only by the universal row cap 2048.
