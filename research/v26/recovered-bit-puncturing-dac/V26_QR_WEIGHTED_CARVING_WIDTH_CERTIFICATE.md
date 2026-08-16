# V26 QR Weighted Carving-Width Certificate

## Purpose

The exact fixed-IO quarter-round site network has weighted path cutwidth 44. A general binary tensor-contraction tree can use non-prefix partitions, so path cutwidth is not the final topological obstruction.

This note computes the relevant general tree quantity for the reduced 32-site network: its weighted **carving width is exactly 42**.

Thus pure topological reordering/decomposition can improve the 44-bond path frontier by only two binary bonds. Any further reduction must exploit algebraic structure/rank of the tensors rather than graph topology alone.

## 1. Weighted site graph

Use the exact reduced site graph from `V26_QR_WEIGHTED_CUTWIDTH_CERTIFICATE.md`:

- vertices `0,...,31`;
- weight-4 path edges `(i,i+1)` for `i=0,...,30`, representing four sigma chains;
- weight-1 cyclic offset-8 edge family;
- weight-1 cyclic offset-12 edge family.

For a vertex subset S, define

`boundary(S) = sum_{edges crossing S | complement} weight(edge)`.

A contraction tree over site tensors associates an edge of the tree with a bipartition of the site set. The number of binary bond indices crossing that bipartition is exactly `boundary(S)` before any algebraic bond compression.

The weighted carving width is the minimum, over binary contraction trees, of the maximum such boundary weight.

## 2. Exact cardinality-cut profile

For every cardinality k=1,...,16, the minimum boundary over all k-site subsets was solved exactly as a 0-1 linear optimization problem.

By complement symmetry, values for `32-k` are identical.

The exact profile is:

| k | minimum boundary |
|---:|---:|
| 1 | 8 |
| 2 | 12 |
| 3 | 16 |
| 4 | 20 |
| 5 | 24 |
| 6 | 28 |
| 7 | 32 |
| 8 | 36 |
| 9 | 38 |
| 10 | 40 |
| 11 | 42 |
| 12 | 42 |
| 13 | 42 |
| 14 | 44 |
| 15 | 44 |
| 16 | 44 |

Each optimization terminated with HiGHS optimal status.

The formulation is the same exact cut MILP used for the 16|16 certificate:

- binary site-membership variables;
- linearized edge-crossing variables;
- exact cardinality constraint `sum x_i=k`;
- objective equal to weighted boundary.

## 3. Balanced-edge lemma for binary trees

Any binary/subcubic tree with 32 labeled leaves contains an edge whose removal separates the leaves into two sets each containing between one third and two thirds of the leaves.

Therefore every binary contraction tree has some induced site subset S with

`11 <= |S| <= 21`.

By the exact cardinality-cut profile and complement symmetry, every such subset satisfies

`boundary(S) >= 42`.

Hence

`carving_width(G) >= 42`.

This lower bound applies to every purely topological binary contraction tree on the site tensors.

## 4. Explicit width-42 recursive decomposition

A recursive exact cut search produced a full binary decomposition in which every proper cluster has global boundary at most 42.

The root split is:

`A = {0,1,2,3,4,5,6,7,8,12,13,14,15,16,17,24,25,26,27,28}`

with `boundary(A)=42`, and

`B = {9,10,11,18,19,20,21,22,23,29,30,31}`

with `boundary(B)=42`.

The larger side A is recursively split into

`{7,8,15,16,17,27,28}` with boundary 40

and

`{0,1,2,3,4,5,6,12,13,14,24,25,26}` with boundary 42.

The latter splits into

`{12,13,14,24,25,26}` with boundary 34

and

`{0,1,2,3,4,5,6}` with boundary 32.

The smaller root side B splits into

`{9,10,11,29,30,31}` with boundary 30

and

`{18,19,20,21,22,23}` with boundary 32.

Continuing by adjacent pairs/triples yields singletons while every cluster boundary stays at or below 42. The maximum over the full recursive decomposition is exactly 42.

Therefore

`carving_width(G) <= 42`.

## 5. Exact result

Combining lower and upper bounds:

`42 <= carving_width(G) <= 42`.

Hence

`carving_width(G)=42`.

For binary bond dimensions, the largest purely topological separator state space of an optimal contraction tree is therefore

`2^42 = 4,398,046,511,104`

basis states before exploiting numerical/algebraic rank structure.

At eight bytes per dense scalar this would still correspond to roughly 32 TiB, so the exact topology result is structural rather than practical.

## 6. Relation to path cutwidth

The exact path cutwidth is 44, while exact carving width is 42.

Thus allowing a general binary contraction tree instead of a linear bit sweep saves only

`2` binary frontier indices,

a factor of 4 in raw dense frontier dimension.

This is useful but nowhere near sufficient for a practical exact 32-bit contraction.

## 7. What is now exhausted

For the reduced fixed-IO site graph, the following purely graph-order questions are closed:

- arbitrary linear bit ordering: optimum frontier 44;
- arbitrary binary site-contraction tree: optimum topological frontier 42.

Therefore further attempts to rescue exact computation by merely permuting bits or choosing another ordinary contraction tree are not a genuinely new mechanism.

The remaining opportunity is algebraic.

## 8. The new sharp object: separator Schmidt structure

A cut with 42 binary network bonds has a formal bond space of dimension `2^42`. But the actual contracted tensor/message on those bonds may lie in a much smaller subspace.

The relevant quantities are now:

- exact Schmidt/matrix rank across subpartitions of the 42 boundary indices;
- singular-value decay / epsilon-rank if exact rank is large;
- symmetries or parity sectors that block-diagonalize the separator tensor;
- factorization of the separator message inherited from the four carry/sigma chains and rotation-offset structure.

If the exact message rank is small, topology overestimates the true contraction complexity. If the exact rank is essentially full, the exact-MPO route is structurally blocked at the quarter-round level for practical computation.

## 9. Important caveat

Carving width is a topology-only quantity. It assumes every crossing binary bond contributes its full dimension independently.

Therefore `carving_width=42` is **not** a lower bound on the actual numerical Schmidt rank of the tensor network and is not a mathematical NO-GO for algebraically compressed exact contraction.

It is the correct statement that topology alone cannot take us below 42.

## 10. Next mathematical falsifier

The next target is no longer another trail cap or another site ordering.

Choose one width-42 cut from the certified decomposition and derive the contracted-side boundary tensor in a factorized form. Then determine, without materializing `2^42` entries if possible:

1. parity/conservation constraints on the boundary indices;
2. exact rank bounds induced by those constraints;
3. Gram matrices of boundary slices;
4. small-word exact Schmidt spectra to identify a stable pattern;
5. a source-conditioned analytical rank or epsilon-rank bound.

That is the first mathematically distinct mechanism capable of beating the topology barrier.

## 11. Claims not admitted

This certificate does not prove that the separator tensor has full rank, does not establish practical exact QR computation, and does not imply a double-round/full-round result, ranking gain, or alpha<1.