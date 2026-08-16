# V26 Modular-Addition Local TT-Rank Theorem

## Purpose

The exact modular-addition Walsh MPO has bond dimension 2 along the bit direction. This note studies the complementary question: how much can one **single interior addition-bit tensor** be factorized across its five local legs?

The result is an exact local rank characterization. The five-leg tensor is not bond-2 in every physical direction, but it admits an exact tensor train with maximum bond dimension **3**.

This gives a second, transverse compression mechanism in addition to the longitudinal carry/sigma bond dimension 2.

## 1. Interior bit tensor

For an interior bit `i>=1`, suppress the bit index and write the exact local tensor as

`T(s,t,u,v,w)`

where

- `s = sigma_i` is the current carry/sigma state;
- `t = sigma_{i-1}` is the next state in the downward recurrence;
- `u,v,w` are the three local Walsh mask bits.

The exact entries are

`T(s,t,u,v,w)`

`= 1[t = s xor u xor v xor w]`

`  * 1[s=1 or (u=v=w)]`

`  * (-1)^((u xor w)(v xor w))`

`  * 2^{-s}`.

All entries lie in `{0, ±1, ±1/2}`.

## 2. Mode ranks

Every single-leg flattening has rank 2. This is maximal for a binary leg.

Thus none of the five physical/state variables is redundant as a linear tensor mode.

## 3. Complete 2|3 rank table

For every pair of legs, flatten the tensor as a `4 x 8` matrix with that pair on the row side.

Exact rational Gaussian elimination gives:

- every pair containing the current sigma leg `s` has rank 4;
- every pair chosen entirely from `{t,u,v,w}` has rank 3.

Explicitly:

| pair | exact rank |
|---|---:|
| `(s,t)` | 4 |
| `(s,u)` | 4 |
| `(s,v)` | 4 |
| `(s,w)` | 4 |
| `(t,u)` | 3 |
| `(t,v)` | 3 |
| `(t,w)` | 3 |
| `(u,v)` | 3 |
| `(u,w)` | 3 |
| `(v,w)` | 3 |

The complementary 3|2 flattenings have the same ranks.

## 4. Representative exact matrices

For rows `(s,t)` and columns `(u,v,w)` in binary lexicographic order, one exact flattening is

`[[1,   0,   0,    0,    0,   0,   0,   0],`

` [0, 1/2, 1/2,    0, -1/2,   0,   0, 1/2],`

` [0,   0,   0,    0,    0,   0,   0,   1],`

` [1/2, 0,   0, -1/2,    0, 1/2, 1/2,   0]]`.

Its four rows are independent, so rank is 4.

For rows `(t,u)` and columns `(s,v,w)`, one exact flattening is

`[[1,   0, 0,  1/2, 0, -1/2, 0,   0],`

` [0, 1/2, 0,    0, 0,    0, 0, 1/2],`

` [0, 1/2, 0,    0, 0,    0, 0, 1/2],`

` [0,   0, 0, -1/2, 0,  1/2, 1,   0]]`.

Rows 2 and 3 are identical while the remaining three row directions are independent, so rank is exactly 3.

The other pair ranks follow by the corresponding exact rational calculations; no floating tolerance is involved.

## 5. Optimal tensor-train rank

For a five-leg tensor and a chosen leg order, the exact TT bond dimensions are the ranks of successive prefix-vs-suffix flattenings.

If the current sigma leg `s` appears in either two-leg prefix/suffix cut, the rank table forces a bond dimension 4.

To avoid this, place `s` in the central position.

For example the order

`(t, u, s, v, w)`

has exact TT rank profile

`[2, 3, 3, 2]`.

Therefore an exact TT representation exists with maximum bond dimension 3.

A maximum bond dimension 2 is impossible, because every possible leg ordering contains a two-leg cut not involving s, and every such pair flattening has rank 3; if s enters the two-leg cut the rank is even 4.

Hence the minimum possible maximum TT bond dimension over all 120 leg orders is exactly

`3`.

## 6. Longitudinal/transverse bi-factorization

The modular-addition Walsh tensor now has two complementary exact low-state descriptions:

1. **longitudinal bit direction:** the carry/sigma recurrence gives bond dimension 2 across adjacent bit positions;
2. **transverse local-leg direction:** each interior five-leg bit tensor has an exact TT with maximum bond dimension 3.

So the local building block is simultaneously low-rank in both directions.

This suggests representing the full QR not as a graph of dense five-leg factors but as a finer network of small bond-2 and bond-3 tensors.

## 7. Fixed-leg reductions

Fixing one of the ordinary mask legs `u`, `v`, or `w` to 0 or 1 gives a four-leg tensor whose optimal TT profile has maximum bond dimension 3.

Fixing the current sigma state `s` gives a four-leg tensor with maximum TT bond dimension 2.

This is consistent with the rank table: the rank-4 obstruction comes from mixing both sigma sectors across a 2|3 cut.

Thus conditioning or block-diagonalizing by the current sigma state can reduce local transverse rank further.

## 8. Implication for QR contraction

The earlier fused-site and pair-factor width calculations do not yet exploit this optimal local TT decomposition.

Therefore the next exact topology should be built from these minimal-rank local cores rather than treating `T_i` as one hyperfactor.

A successful global reduction would require arranging the local TT orders so that:

- bond-3 auxiliary indices remain mostly local;
- long-range rotation-mask legs attach near the ends of the local chains;
- sigma legs remain near the TT center where the rank-4 physical obstruction is avoided.

This is a genuine algebraic refinement, not another permutation of already-fused site tensors.

## 9. Computer-assisted scope

The local ranks were computed by exact rational Gaussian elimination on matrices of size at most `4 x 8`, and all 120 leg orderings were checked exactly.

This is a finite algebraic certificate. It does not depend on the missing historical project core or on any sigma cap.

## 10. Claims not admitted

The local bond-3 theorem does not by itself prove a lower global QR width or practical exact contraction. Auxiliary bond-3 edges can still accumulate across the composed network.

It does not establish a double-round/full-round result, ranking gain, alpha<1, or cryptanalytic improvement.