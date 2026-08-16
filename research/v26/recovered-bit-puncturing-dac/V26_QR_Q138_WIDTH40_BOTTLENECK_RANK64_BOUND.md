# V26 q138 Width-40 Bottleneck Rank-64 Bound

## Purpose

`V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md` gives a complete exact q138 fixed-output one-QR contraction tree with maximum formal message dimension `2^40`.

This note analyzes the unique 171-leaf cluster that realizes that maximum and shows that the corresponding 40-bit boundary tensor is strongly rank-deficient across its certificate child partition:

`rank <= 64`.

This is an exact topology-induced Schmidt bound. It does not yet lower the complete global width below 40, but it proves the new bottleneck need not be represented as a dense `2^40` array.

## 1. Certified maximum cluster

The width-40 certificate contains exactly one non-root cluster with boundary dimension

`2^40`.

It has

- `171` tensor leaves;
- exactly `40` binary boundary indices;
- no ternary, rank-528, or other nonbinary index on the maximum cut.

Its two certificate children contain

- `64` leaves;
- `107` leaves.

Call them `A` and `B`.

## 2. Parent boundary partition

Of the parent cluster's 40 external binary indices,

- `A` touches `16`;
- `B` touches the remaining `24`;
- no parent-external boundary index is shared by both children.

Therefore the parent message can be viewed as a matrix

`M(x_A,x_B)`

with formal dimensions

`2^16 x 2^24`.

A generic matrix of this shape could have rank as large as `2^16`.

## 3. Six-bit child interface

The only indices connecting `A` and `B` internally are six binary indices:

- `aux_j2_i8_k0`;
- `aux_j4_i11_k0`;
- `aux_j4_i16_k0`;
- `sig1_7`;
- `sig3_7`;
- `sig4_7`.

Thus the exact child interface dimension is

`2^6 = 64`.

After contracting internal tensors on the two sides separately,

`M(x_A,x_B) = sum_{z in {0,1}^6} L(x_A,z) R(z,x_B)`.

Hence

`rank(M) <= 64`.

Equivalently the Schmidt width of this 40-bit parent tensor across the 16|24 boundary partition is at most six bits.

## 4. Exact construction cost of the 64-leaf side

The existing certified subtree for child `A` was rescanned against the full rank-528-compressed hypergraph.

Every intermediate cluster in that 64-leaf subtree has message dimension at most

`2^22`.

The maximum occurs at the complete 64-leaf child itself, whose boundary consists of

- 16 parent-external binary indices;
- the 6 child-interface bits.

Thus the left factor `L(x_A,z)` can itself be produced exactly without exceeding a `2^22` message in the already-certified construction.

This matters because the rank-64 factorization is not hiding a need to first materialize the `2^40` parent message.

## 5. Interpretation

The width-40 certificate measures the size of a dense parent message if the two certificate children are fully combined at that node.

The rank bound shows that this dense materialization is algebraically unnecessary:

`2^40` formal entries

can be left factorized through only

`64`

Schmidt channels across the certificate child split.

This is the same structural pattern that previously turned the width-41 bottleneck's 3072-dimensional interface into an exact rank-528 bond. Here the first bound is already available from the six-bit graph interface itself.

## 6. Why this does not yet prove W < 40

A low-rank factorization of one maximum message must be reinserted into the **whole** hypergraph and followed by a complete global contraction tree before changing the admitted global width.

Replacing the 64-leaf child by an exact rank-64 factorization changes the global geometry because its 16 parent-external edges connect to multiple outside regions.

A preliminary exact separator search on one natural continuation did not immediately close a complete `W<=39` tree. That exploratory search is not a lower bound and is not admitted as a NO-GO.

Therefore the current canonical global result remains

`W <= 40`.

## 7. Next exact target

Use the six-bit factorization explicitly:

1. compile the 64-leaf child to a factor `X_64(x_16,r_64)`;
2. connect `r_64` to a second factor carrying the six original child-interface bits;
3. rebuild the full q138 rank-528-compressed network;
4. search for and verify a complete global tree below width 40;
5. if topology stalls, compute the **actual rational rank** of the `2^16 x 64` child map. A rank below 64 would supply genuine algebraic compression beyond the graph interface.

## 8. Claims not admitted

This note does not prove `W<=39`, does not prove the child-map rank is exactly 64, does not establish practical exact QR evaluation or arithmetic-work reduction, and does not imply a double-round/full-round result, ranking gain, or `alpha<1`.
