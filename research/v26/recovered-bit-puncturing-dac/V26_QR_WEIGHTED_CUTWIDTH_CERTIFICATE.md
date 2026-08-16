# V26 QR Weighted Cutwidth Certificate

## Purpose

`V26_EXACT_QR_PATHWIDTH_THEOREM.md` gives an explicit exact sequential contraction with at most 44 open binary bonds for a fixed-input/fixed-output 32-bit ChaCha quarter-round Walsh coefficient. This note asks whether a different **linear ordering of bit sites** can reduce that frontier.

For the reduced 32-site network, the answer is no: the weighted cutwidth is exactly **44**.

The lower-bound step is a finite computer-assisted exact optimization certificate. It is not a lower bound against arbitrary non-path contraction trees or algebraic low-rank compression.

## 1. Reduced weighted site graph

After exact local contraction of the `u3_i,u4_i` mask variables, the fixed-IO QR tensor network has one site tensor per bit position `i=0,...,31`.

Its binary bonds induce the following weighted graph on the 32 sites:

- path edge `(i,i+1)` of weight 4 for `i=0,...,30`, representing the four independent sigma/carry bonds;
- one weight-1 edge family with cyclic offset 8;
- one weight-1 edge family with cyclic offset 12.

The edge weight is `log2` of the fused bond dimension crossing that site pair. Thus the total weight of a cut is exactly the number of binary bond indices exposed by the corresponding prefix contraction.

## 2. Natural-order upper bound

For the order

`0,1,2,...,31`,

the exact frontier-weight profile after successive prefix contractions is

`8,12,16,20,24,28,32,36,38,40,42,44,44,44,44,44,44,44,44,44,42,40,38,36,32,28,24,20,16,12,8`.

Therefore

`cutwidth(G) <= 44`.

This is the same 44-bond upper bound derived analytically from

`4 + 2*8 + 2*12 = 44`.

## 3. Midpoint-bisection lower bound

Take any linear ordering of the 32 sites. After the first 16 sites, the ordering induces a 16|16 vertex bisection.

The frontier weight at that point is the weight of the bisection cut. Therefore

`cutwidth(G) >= b_16(G)`,

where `b_16(G)` is the minimum weighted cut among all 16-vertex subsets.

So an exact minimum-bisection result supplies a valid cutwidth lower bound.

## 4. Exact 0-1 optimization certificate

The 16|16 minimum bisection was solved as a binary linear optimization problem.

Variables:

- `x_i in {0,1}` for every site;
- `y_e in [0,1]` for every weighted graph edge.

Constraints:

`sum_i x_i = 16`,

`y_(i,j) >= x_i-x_j`,

`y_(i,j) >= x_j-x_i`.

Objective:

`min sum_e weight(e) y_e`.

Because all edge weights are positive, optimal `y_e` equals `|x_i-x_j|`, so the objective is exactly the bisection boundary weight.

The HiGHS mixed-integer solver terminated with **optimal status** and objective

`44`.

One optimal 16-site subset is

`{0,1,2,3,8,9,10,11,12,13,14,15,20,21,22,23}`.

Thus

`b_16(G)=44`.

The solver is used only as a finite exact combinatorial calculator. The reduction from minimum bisection to the cutwidth lower bound is elementary.

## 5. Exact weighted-cutwidth result

Combining the two inequalities,

`44 <= cutwidth(G) <= 44`.

Therefore

`cutwidth(G)=44`.

So the ordinary bit order is already optimal in maximum frontier weight among **all sequential one-site-at-a-time linear contraction orders** on this reduced site network.

A massive permutation search is therefore unnecessary; no reordering of the 32 bit sites can produce a path frontier below 44 binary bonds.

## 6. Independent heuristic consistency check

Before the exact bisection certificate, simulated-annealing / swap / segment-reversal searches over many site permutations repeatedly failed to find a cutwidth below 44.

This heuristic observation is not part of the proof. It is merely consistent with the exact certificate.

Likewise, tensor-hypergraph path search found a largest intermediate of `2^44`, matching the exact optimal path-cutwidth result.

## 7. What the certificate does NOT prove

This is crucial.

`cutwidth(G)=44` does **not** imply that every possible tensor contraction must create a `2^44` intermediate.

A general contraction tree is not restricted to a single linear prefix ordering. Its complexity is related to branch/tree decompositions rather than path cutwidth alone.

Also, the numerical bond dimension predicted by graph topology can be reduced if the actual intermediate tensor has exact algebraic rank deficiency.

Therefore 44 is a lower bound only for the chosen class:

**linear site-order / prefix contractions without algebraic bond recompression.**

It is not a mathematical NO-GO for exact QR contraction.

## 8. Consequence for the next search

Because linear site reordering is exhausted, the only meaningful ways to beat the 44 frontier are now structurally different:

1. use a non-path contraction tree / separator decomposition;
2. exploit exact low rank of the local/intermediate tensors across the large cut;
3. exploit symmetries or block diagonalization of the weighted site network;
4. use certified epsilon-rank compression if exact rank remains large.

Changing the bit permutation yet again would merely reopen a solved optimization problem under a new costume, a surprisingly popular research tradition best avoided here.

## 9. Relation to FDS

The result separates two facts cleanly:

- exact generative representation of modular addition is extremely compact (bond 2);
- composing the QR wiring creates an optimal linear frontier of 44 binary bonds.

Thus the next compression opportunity is no longer in local trail pruning or bit ordering. It lies in the **rank/structure of the 44-bond separator tensor itself**.

That is now the mathematically sharp next object.

## 10. Claims not admitted

The exact cutwidth certificate does not establish practical full QR contraction, does not determine general contraction-tree width, and does not imply a double-round/full-round result, ranking gain, or alpha<1.