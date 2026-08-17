# V26 q138 coefficient-aware constructive double-round width-94 theorem

## Statement

For the q138 fixed-output inverse-double-round five-QR star there is an explicit exact factor-generation/contraction construction with peak structural message exponent

`W_2_construct <= 94`.

This improves the previous constructive95 ledger by using the exact signed S1 row factorization during factor generation. It remains much weaker than a practical evaluator claim: the arithmetic work of the construction may be enormous.

## Ingredients

Use the frozen constructive partition tree. Its root split is

`S1={0,1,2,3,4,5,12,13,14,15,16}`

versus its21-site complement.

The signed S1 central rank is

`R = 16 * 2784 * 2^26 = 87 * 2^35`.

The block1 rank16 factor is explicit. The block2 physical-row bridge proves that its rank2784 retained-column basis can be generated from actual physical block2 rows: every normalized basis slice is an exact combination of at most64 physical block2 rows. The remaining26 S1 row bits are identity channels. Therefore every global signed right-basis slice is an exact combination of at most64 ordinary central-QR slices with the44 S1 physical input-mask bits fixed.

## Left factor

Let `alpha` denote the four predecessor-leaf mask bits on S1, hence `2^44` possibilities. The signed left factor `U(alpha,r)` has at most

`2^44 * R = 87 * 2^79`

entries, exponent

`79+log2(87)=85.44294349584872... <94`.

Its local rank factors are explicitly generated below `2^30` scalars by the block1/block2 explicit-factor theorems.

## Right factor generation

For each signed rank index `r` and each `alpha`, generate the scalar right entry

`N(r,alpha)`

as follows.

1. Expand the block2 basis slice into at most64 actual physical block2 rows. Block1 contributes one scaled physical row and the26 raw S1 row bits are fixed, so each term is an ordinary physical S1 central-row assignment.
2. For one such physical assignment, fix all44 S1 central input-mask bits. Contract the S1 part of the exact reduced central QR graph. On the frozen left subtree the internal central-only graph boundary never exceeds34, and the completed S1 side leaves the exact 51-bit central graph boundary to the complement.
3. The four predecessor leaf vectors are exact 32-bit vectors and can be generated with peak at most44 by the previous constructive95 dependency. Fix their11 S1 bit positions to `alpha`; each becomes an arbitrary exact vector on the remaining21 complement positions. Factor each restricted vector hierarchically on the complement subtree. For a complement cluster T of size k, four leaves contribute at most `4*min(k,21-k)` Hilbert bits.
4. Contract the complement central graph plus those four restricted leaf vectors on the frozen complement subtree. Exact recount gives

`gb(T)+4*min(|T|,21-|T|) <=94`

for every internal cluster. The unique 94 cluster is

`{17,18,19,20,21,22,23,24,25,26}`.

The complement root carries only the51 central boundary bits; closing it against the fixed-row S1 boundary factor yields the scalar physical-slice contribution. Sum at most64 such contributions to obtain `N(r,alpha)`.

The complete dense right table has the same size as the left table,

`R*2^44 = 87*2^79`,

well below `2^94`.

Finally contract the two tables over `(r,alpha)`; this can be streamed without a larger structural message.

Therefore the maximum structural message/factor dimension in this explicit exact construction is `2^94`.

## What changed relative to constructive95

The old coefficient-blind graph+four-leaf method is method-optimal at95: the clean cardinality MILP theorem plus the balanced-edge lemma proves no tree reordering inside that method can do better. Constructive94 escapes that lower bound because it is coefficient-aware and replaces the S1 51-bit graph boundary by the exact signed rank basis during factor generation.

## Scope

This theorem claims only an exact constructive structural-message upper bound. It does **not** claim useful arithmetic work. The procedure repeats complement contractions over a very large signed-rank/alpha index set; work can be vastly worse than the previous method. No ranking gain, alpha<1, practical evaluator, or full-round relevance follows.

Dependencies:

- `V26_Q138_CONSTRUCTIVE_GRAPH_LEAF95_METHOD_OPTIMAL_THEOREM.md`;
- `V26_Q138_SIGNED_BLOCK1_EXPLICIT_FACTOR_THEOREM.md`;
- `V26_Q138_SIGNED_BLOCK2_EXPLICIT_FACTOR_THEOREM.md`;
- `V26_Q138_SIGNED_BLOCK2_PHYSICAL_ROW_BRIDGE_THEOREM.md`;
- existing exact reduced central graph and leaf constructive95 representation.

Verifier:

`scripts/verify_v26_q138_double_round_constructive94.py`.
