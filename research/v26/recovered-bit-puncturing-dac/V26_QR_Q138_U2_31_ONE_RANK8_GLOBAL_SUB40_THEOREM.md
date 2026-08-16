# V26 q138 `u2_31=1` Rank-8 Global Sub-40 Theorem

## Purpose

The physical q138 rank-envelope theorem proves that, on the fixed-input-mask subclass

`u2_31 = 1`,

the certified 171-leaf width-40 bottleneck has exact Schmidt rank between 5 and 8 across its `16|24` external partition. This note reinserts that algebraic fact into the complete q138 fixed-output one-quarter-round Walsh network and proves a new complete structural message-width upper bound strictly below 40 for this subclass.

The admitted result is

`W <= log2(528 * 2^30) = 39.04439411935845... < 40`.

This is the first complete global sub-40 contraction-tree certificate in the exact q138 line, but it is source/input-mask conditioned: it requires `u2_31=1`.

## 1. Algebraic dependency

`V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md` proves, by exact rational transfer algebra over every physical fixed-mask case, that

- `u2_31=0` gives parent rank `16..27`;
- `u2_31=1` gives parent rank `5..8`.

Therefore every `u2_31=1` instance admits an exact factorization of the certified 171-leaf parent message

`M_m(x_A,x_B) = sum_r X_m(x_A,r) Z_m(r,x_B)`

with `rho_m <= 8`.

For a uniform structural certificate, smaller ranks 5, 6 or 7 may be embedded in an 8-dimensional bond by zero padding. No approximation is introduced.

## 2. Global replacement

Start from the already certified rank-528-compressed width-40 network.

Remove the unique 171-leaf maximum cluster. Its 40 external binary indices are partitioned exactly as in the width-40 certificate:

- 16 indices on the left external side;
- 24 indices on the right external side.

Replace the removed cluster by two exact factors:

- `X8`, incident on the 16 left external binary indices and a new rank-8 bond;
- `Z8`, incident on the 24 right external binary indices and the same rank-8 bond.

The pre-existing rank-528 compression elsewhere in the network is retained unchanged.

The resulting structural network has

- 367 tensor leaves;
- 365 surviving leaves from the width-40 network;
- 2 new rank factors;
- 467 nontrivial indices;
- 371 binary indices;
- 94 ternary indices;
- one dimension-528 index;
- one dimension-8 Schmidt index.

## 3. Complete contraction tree

The machine certificate contains a complete binary tree with

- 367 leaves;
- 366 internal nodes;
- every leaf used exactly once.

Every non-root cluster boundary is recomputed from the reconstructed hypergraph.

The maximum exact message dimension is

`D_max = 528 * 2^30 = 566,935,683,072`.

Equivalently,

`log2(D_max) = 39.04439411935845...`.

The maximizing cluster contains 230 leaves and crosses

- 27 binary indices;
- the existing rank-528 bond;
- the new rank-8 Schmidt bond.

Thus

`D_max < 2^40`

and the complete conditioned network satisfies

`W < 40`.

## 4. Relation to the previous chain

For the unconditional physical fixed-mask family, the admitted complete global chain remains

`44 -> 42 -> 41 -> 40`.

For the `u2_31=1` subclass, exact source-conditioned algebra extends the chain to

`44 -> 42 -> 41 -> 40 -> 39.044394119...`.

The last step is not merely a graph-order improvement. It uses the exact rank-8 envelope of the physical bottleneck and then verifies a complete global tree after reinsertion.

## 5. What has and has not been proved

Proved:

- exact rank `<=8` for the 171-leaf bottleneck on every physical `u2_31=1` fixed-mask instance, by the rank-envelope dependency;
- an exact rank-8 structural replacement, allowing zero padding when the actual rank is lower;
- a complete 367-leaf contraction tree whose maximum formal message dimension is exactly `528*2^30`;
- therefore a strict global message-width improvement below 40 for this subclass.

Not proved:

- a sub-40 certificate for the general `u2_31=0` / rank-27 family;
- `W<=39` or optimality of `39.044394119...`;
- an arithmetic-work bound of the same exponent;
- practical dense memory at the certified maximum;
- a mask-independent rank-8 basis;
- a double-round/full-round result, ranking gain or `alpha<1`.

## 6. Machine authority

Certificate:

`research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE.json`

Structural verifier:

`scripts/verify_v26_qr_q138_u2_31_one_rank8_global_sub40.py`

Algebraic dependency verifier:

`scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

The structural verifier reconstructs the width-40 network from its canonical certificate, removes the certified 171-leaf cluster, inserts the two rank-8 factors, rebuilds all nontrivial indices, and recomputes every cluster boundary in the new complete tree.

## 7. Next exact target

There are now two distinct next directions:

1. **General physical family:** use the uniform parent-rank envelope `rho_m <=27` and find a complete sub-40 global tree, or isolate the exact residual algebraic separator that prevents one in the current geometry.
2. **Strong `u2_31=1` subclass:** analyze the certified `528 * 2^30` maximum cluster and ask whether its rank-528/binary boundary admits another exact algebraic compression, with `W<=39` as the next clean threshold.

Do not replace either task with blind ordering search. The successful reductions in this line have come from identifying the algebraic rank structure of the actual boundary message and then reinserting it globally.
