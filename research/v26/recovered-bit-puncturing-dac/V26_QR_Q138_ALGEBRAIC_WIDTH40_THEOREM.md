# V26 q138 Algebraically Compressed Exact QR Width-40 Theorem

## Purpose

This note combines two exact results:

1. the q138 width-41 bottleneck child has exact left-map rank `528`, not the topology-only interface dimension `3072`;
2. after replacing that 34-leaf child by an exact rank-528 factorization, the entire fixed-output q138 quarter-round Walsh network has a complete binary contraction tree whose largest message dimension is `2^40`.

Therefore the admitted exact structural progression for this q138 fixed-output one-QR object is

`44 -> 42 -> 41 -> 40`,

where the last step is algebraic rank compression rather than graph reordering alone.

## 1. Dependencies

The local exact Walsh representation is inherited from

- `V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`;
- `V26_MODADD_LOCAL_TT_RANK_THEOREM.md`.

The previous global exact baseline is

- `V26_QR_MINIMAL_CORE_WIDTH41_THEOREM.md`;
- `V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE.json`;
- `scripts/verify_v26_qr_minimal_core_width41.py`.

The algebraic replacement is certified by

- `V26_QR_Q138_LEFT_MAP_RANK528_THEOREM.md`;
- `scripts/verify_v26_qr_width41_left_rank528.py`.

That verifier uses exact rational arithmetic and proves the relevant 34-leaf map has rank exactly

`528`.

## 2. Exact rank replacement

The width-41 certificate contains a 34-leaf child map with

- 12 parent-external binary indices;
- a sibling interface of 10 binary plus 1 ternary index, dimension `3072`.

For the q138 fixed-output mask, the exact map rank is

`528`.

Hence it admits an exact factorization

`L(x,z) = sum_{r=1}^{528} X(x,r) Z(r,z)`.

Replace the original 34-leaf subnetwork by two exact factors:

- `X`, carrying the 12 original external binary indices plus the rank-528 index `r`;
- `Z`, carrying the original 10-binary-plus-1-ternary sibling interface plus `r`.

No approximation is introduced. This is simply a rank factorization of the exact rational map.

## 3. Modified exact network

After removing the 34 original tensor leaves and adding the two rank factors, the modified q138 network has

- `536` tensor vertices;
- `656` nontrivial indices;
- `513` binary indices;
- `142` ternary indices;
- one index of dimension `528`.

The exact replacement geometry is recorded in

`V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`.

In particular the certificate explicitly records

- the 34 removed original leaf IDs;
- the 12 external edges attached to `X`;
- the 11 original sibling-interface edges attached to `Z`;
- the new rank-528 bond connecting `X` and `Z`.

## 4. Complete width-40 tree

The certificate contains a full binary tree with

- `536` leaves;
- `535` internal nodes.

Every leaf occurs exactly once. For every non-root cluster, the verifier reconstructs the modified hypergraph and computes the exact message dimension

`D(S) = product(dim(e))`

over all indices crossing the cluster boundary.

The maximum over the complete tree is exactly

`D_max = 2^40 = 1,099,511,627,776`.

The maximizing cluster contains `171` tensor leaves and crosses exactly

`40` binary indices

with no ternary or rank-528 bond on that maximal cut.

Therefore the algebraically compressed q138 fixed-output one-QR network satisfies

`W <= 40`.

## 5. Independent structural verifier

The structural verifier is

`scripts/verify_v26_qr_q138_algebraic_width40.py`.

It does not trust the modified edge list blindly. It reconstructs the original 568-leaf minimal-core network from the same fixed local TT orders used by the width-41 certificate, removes the certified 34-leaf child, reconnects the recorded external/interface indices to `X` and `Z`, inserts the dimension-528 bond, and then verifies the complete tree.

Expected output includes

`PASS V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE`

and

`max_boundary_dimension=1099511627776=2^40`.

The verifier explicitly reports that the legitimacy of the dimension-528 replacement is a dependency on

`scripts/verify_v26_qr_width41_left_rank528.py`.

Thus the proof chain is separated cleanly:

`exact Fraction rank-528 proof -> exact structural width-40 tree proof`.

## 6. Structural improvement sequence

For the same q138 fixed-output one-quarter-round Walsh object, the exact representation results now read:

1. natural fused-site path frontier: `44` binary bits;
2. optimal fused-site carving tree: `42` binary bits;
3. minimal-rank local TT-core tree: `<=41` bits;
4. exact rank-528 separator compression plus new global tree: `<=40` bits.

Relative to the natural fused path, the largest formal dense message dimension is reduced by a factor

`2^(44-40) = 16`.

Relative to the previous minimal-core width-41 certificate, the global maximum dense message dimension is reduced by a factor 2.

The mechanism of the final step is qualitatively different: it uses actual exact tensor rank inside a certified separator, not merely another ordering of the same graph.

## 7. Why this matters mathematically

The result demonstrates a concrete hierarchy:

`explicit trail support`

is much larger than

`exact local MPO/TT state`

which is still larger than necessary if one uses only

`graph-topological separators`,

because the actual separator map can have substantial

`algebraic rank deficiency`.

For this q138 child, the topology-only 3072-dimensional interface collapses exactly to rank 528, a factor `64/11` reduction. Reinserting that exact low-rank map changes the global contraction certificate itself.

This is the first point in the V26 exact-QR line where local algebraic Schmidt compression has been shown to lower a complete global message-width certificate.

## 8. What width 40 means and does not mean

`W<=40` is an exact **message-dimension upper bound** for the stated fixed-output q138 one-QR representation.

It is not a claim that arithmetic work is `O(2^40)`. Contracting child tensors can involve products of several boundary dimensions, so operation count requires a separate certificate.

It is also not a practical-memory claim. A naive dense `2^40` scalar message is still enormous. The mathematical value is that an exact algebraic mechanism has been found that changes the certified global width rather than merely compressing one local table.

## 9. Scope

The rank-528 proof uses the q138 fixed-output structure, in particular

`w4 = 2^3`

and therefore zero T4 output-mask bits on the bottleneck segment `23..28`.

Accordingly the admitted theorem is scoped to the q138 fixed-output one-quarter-round Walsh network.

Do not silently generalize `W<=40` to arbitrary fixed input/output masks, an entire open spectrum, a double round, or a full ChaCha round family.

## 10. Optimality

No lower bound of 40 is claimed.

The current result is

`W <= 40`,

not

`W = 40` as a global optimum.

A representation or contraction tree below 40 may exist.

However the next useful research step should not be blind graph-order search. The successful mechanism was algebraic rank deficiency, so the first target is the actual rank/sector structure of the new certified 40-bit bottleneck message.

## 11. Next exact target

Take the 171-leaf cluster that realizes the `2^40` maximum and repeat the successful sequence:

1. identify a certificate child split or terminal interface;
2. derive its topology-only Schmidt bound;
3. expose semantic sigma/equality-class sectors;
4. compute exact rational rank of the smaller child map where feasible;
5. if a strict rank reduction exists, reinsert it and require another complete global tree certificate.

Only after exact algebraic rank compression stalls should certified epsilon-rank/tail approximation become the active mechanism.

## 12. Claims not admitted

This theorem does not establish practical exact QR evaluation, exact arithmetic-work reduction, full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, `alpha<1`, or full-round relevance.
