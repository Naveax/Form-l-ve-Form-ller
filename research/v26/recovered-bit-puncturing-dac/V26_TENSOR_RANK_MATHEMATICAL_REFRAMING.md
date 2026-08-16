# V26 Tensor-Rank Mathematical Reframing

## Purpose

This note records a mathematics-first interpretation of the recovered bit-puncturing / D&C line. It does not claim a new cap2/cap3 measurement and does not rewrite the already-frozen single-column QR-transform plan. Code is treated only as a calculator / falsifier for the mathematical objects below.

## 1. Exact first-layer factorization

Let the active initial column inverse-QR hull branches be indexed by `r`, with signed coefficient `a_r`. For each branch and each diagonal quarter-round `d in {0,1,2,3}`, let

`D_{r,d}(x_0,x_1,x_2,x_3)`

be the exact signed local hull tensor relative to the same bounded local sigma-cap family used by the recovered V25/V26 authority.

Conditioned on root branch `r`, the four diagonal quarter-rounds are independent. Therefore the full signed boundary tensor before the next column layer is

`F = sum_r a_r (D_{r,0} tensor D_{r,1} tensor D_{r,2} tensor D_{r,3})`,

with only a permutation needed to move between diagonal-local word order and global state-word order.

This is the mathematical content behind the recovered D&C memory reduction: the global Cartesian trail list is not the primitive object; the primitive object is a signed mixture of products.

## 2. ChaCha column/diagonal intersection lemma

The quarter-round layouts are

- columns: `(0,4,8,12)`, `(1,5,9,13)`, `(2,6,10,14)`, `(3,7,11,15)`;
- diagonals: `(0,5,10,15)`, `(1,6,11,12)`, `(2,7,8,13)`, `(3,4,9,14)`.

For diagonal index `d` and column index `c`, their unique intersection appears at local diagonal position

`p(d,c) = (c-d) mod 4`.

Thus every subset of columns corresponds, inside each diagonal tensor, to the same subset of local positions shifted cyclically by `d`.

## 3. General subset marginal theorem

For a column subset `S`, define the local marginal

`D^S_{r,d}`

by retaining exactly the positions `{p(d,c): c in S}` and summing all other local positions.

Then the exact signed boundary marginal on the columns in `S` is

`M_S = sum_r a_r tensor_{d=0}^3 D^S_{r,d}`.

This identity is purely algebraic. It explains the admitted single-column Stage0 and extends immediately to pairwise, triple-column, and full 2|2-flattening analysis without global Cartesian materialization.

## 4. Pairwise Kronecker theorem

For two columns `c,c'`, write the retained local two-word marginal of diagonal factor `d` as a matrix

`P^{cc'}_{r,d}`.

Arrange the complete state of column `c` as the row index and column `c'` as the column index. Up to fixed row/column permutations,

`M_{cc'} = sum_r a_r (P^{cc'}_{r,0} kron P^{cc'}_{r,1} kron P^{cc'}_{r,2} kron P^{cc'}_{r,3})`.

Hence

`rank(M_{cc'}) <= sum_r product_d rank(P^{cc'}_{r,d})`.

This is the first natural rank-based separator quantity. Sparse support can be large while this exact rank bound remains small.

The untransformed pairwise Frobenius energy also has a Gram contraction that avoids materializing `M_{cc'}`:

`||M_{cc'}||_F^2 = sum_{r,s} a_r a_s product_d <P^{cc'}_{r,d}, P^{cc'}_{s,d}>_F`.

Equivalently, if `G_d(r,s)=<P_{r,d},P_{s,d}>_F`, then the energy is the quadratic form in the Hadamard product `G_0 o G_1 o G_2 o G_3`.

## 5. Full four-column 2|2 flattening theorem

Let `A|B` be one of the three column bipartitions

- `01|23`,
- `02|13`,
- `03|12`.

For fixed `r,d`, flatten `D_{r,d}` according to the corresponding two local positions on side `A` versus the two on side `B`; call this matrix `Q^{A|B}_{r,d}`.

Then, up to fixed permutations,

`Flat_{A|B}(F) = sum_r a_r tensor_{d=0}^3 Q^{A|B}_{r,d}`,

so

`rank Flat_{A|B}(F) <= sum_r product_d rank(Q^{A|B}_{r,d})`.

This bound is a more intrinsic separator diagnostic than one-column support. The future computational task should therefore measure exact local matricization ranks first, not begin by constructing enormous pairwise sparse dictionaries.

## 6. Full exact QR layers are local basis changes

For a full, untruncated linear-correlation operator of an invertible quarter-round, the correlation matrix is an orthogonal change of Walsh basis. If `T_c` denotes that full exact operator on column `c`, then the next column layer acts as

`T_0 tensor T_1 tensor T_2 tensor T_3`.

For every column bipartition `A|B`,

`Flat_{A|B}(T F) = (tensor_{c in A} T_c) Flat_{A|B}(F) (tensor_{c in B} T_c)^T`.

Therefore, for the full exact operator,

- bipartition matrix rank is invariant;
- Frobenius energy is invariant.

So the intrinsic tensor-rank question can be studied before the next QR layer. The QR layer changes coordinates/sparsity, not the exact Schmidt ranks across column bipartitions.

Important caveat: the current V26 transform plan is exact only relative to a bounded local sigma-cap trail family. That capped operator need not be orthogonal/invertible. Its cap2/cap3 test remains useful as a capped-model implementation/representation check, but it is not the primary mathematical mechanism.

## 7. Stage0 cap4 singleton structure mapped back to diagonal-local positions

The admitted cap4 column-word union supports are

- `C0 = [1,0,122,8]`,
- `C1 = [394,1,16,3792]`,
- `C2 = [44,58,1,16]`,
- `C3 = [0,1,58,1]`.

Using `p(d,c)=(c-d) mod 4`, these map to local one-word marginal union supports by diagonal factor:

- `D0 = [1,1,1,1]`,
- `D1 = [394,58,58,8]`,
- `D2 = [44,1,122,3792]`,
- `D3 = [0,0,16,16]`.

Thus the exact single-column cancellations of `C0` and `C3` are not diffuse accidents: both are caused by the same diagonal factor `D3`.

`C0` uses local `D3` position 1, whose one-word signed marginal is identically zero across the factorized branches.

`C3` uses local `D3` position 0, whose one-word signed marginal is also identically zero.

This identifies a sharply targeted hidden-correlation question.

## 8. First mathematical falsifier: the D3 (positions 0,1) joint marginal

Define, for each root branch `r`,

`P^{03}_{r,3}(u,v) = sum_{x_2,x_3} D_{r,3}(v,u,x_2,x_3)`

(up to the fixed choice of row/column orientation).

Because both corresponding one-word marginals vanish,

- every row sum of `P^{03}_{r,3}` is zero;
- every column sum is zero.

But this does not force the matrix itself to be zero.

Therefore the smallest meaningful cross-column question is:

`Does any exact capped local D3 branch have P^{03}_{r,3} != 0?`

If all such matrices are zero, the specific hidden `C0-C3` correlation route dies locally before any large contraction.

If at least one is nonzero, then the single-column zeros hide genuine two-column signed structure and pairwise/joint contraction is mathematically justified.

The next test after that is whether the root-branch mixture

`M_{03} = sum_r a_r tensor_d P^{03}_{r,d}`

remains nonzero after signed cancellation.

## 9. Rank-first execution order

The mathematics-first order is now:

1. Preserve the existing frozen QR plan as historical/capped-model authority; do not retune it.
2. When canonical runtime bytes are restored, compute only the local `D3` `(0,1)` two-word marginals first.
3. Test exact nonzero structure plus exact row/column-sum-zero identities.
4. Compute exact local `2|2` matricization ranks for every `D_{r,d}` under the three column bipartitions.
5. Form the rigorous global rank upper bounds `B_{A|B}=sum_r product_d rank(Q^{A|B}_{r,d})`.
6. Prefer the bipartition with the smallest rigorous bound / observed exact rank profile.
7. Only if rank structure is favorable should a larger pairwise or junction-tree sparse materialization be attempted.
8. Use Gram contractions for energy wherever possible before constructing explicit joint supports.

Exact rank should be evaluated over the exact coefficient field. Since the local Walsh/trail coefficients are dyadic in the full formulation, integer scaling / rational arithmetic is the authority; floating SVD may be used only as an exploratory diagnostic.

## 10. Claims not admitted

This note does not demonstrate:

- a nonzero `C0-C3` pair tensor;
- a low exact separator rank;
- full second-layer contraction;
- four-inverse-round exact energy;
- ranking gain;
- `alpha < 1`;
- full-round relevance.

It identifies the mathematically smallest and most informative next objects to test once the exact historical runtime is restored.