# V26 QR Site-Fusion Refinement

## Purpose

The exact weighted cutwidth/carving-width certificates were computed on a reduced network in which all local factors at one bit position were fused into one site tensor after eliminating `u3_i,u4_i`.

That reduction is exact as a tensor value, but fusion can hide further factorization that is useful for contraction ordering. Therefore the site-graph carving width 42 is an exact optimum **for the fused-site representation**, not a universal lower bound for every factorization of the same QR tensor network.

This note records the finer exact local factorization and corrects the scope before the number 42 is overinterpreted.

## 1. Four local addition factors

At bit i, after fixed input/output mask transport, write the four exact modular-addition bit tensors as

- `T4_i`, depending on local `u4_i` and the addition-4 sigma pair;
- `T2_i`, depending on the same local `u4_i` and the addition-2 sigma pair;
- `T3_i`, depending on local `u3_i` and the addition-3 sigma pair;
- `T1_i`, depending on the same local `u3_i` and the addition-1 sigma pair.

The long-range mask variables are shared as follows:

- `v4_i`, `v4_{i+8}`;
- `v3_i`, `v3_{i+12}`.

No local variable is shared between the pair `(T4_i,T2_i)` and the pair `(T3_i,T1_i)` except those external v-mask indices.

## 2. Exact pair factorization

The local sum over `u4_i` and `u3_i` therefore factorizes exactly:

`S_i = sum_{u4_i,u3_i} T4_i T2_i T3_i T1_i`

`    = A_i * B_i`,

where

`A_i = sum_{u4_i} T4_i T2_i`,

`B_i = sum_{u3_i} T3_i T1_i`.

Thus one fused 12-leg-ish site tensor can be replaced exactly by two smaller factors.

A_i carries the sigma chains for additions 4 and 2 plus the relevant v-mask indices.

B_i carries the sigma chains for additions 3 and 1 plus the relevant v-mask indices.

This is an exact algebraic factorization, not an approximation.

## 3. Refined hypergraph

For n=32 the pair-factor representation has

- 64 factor vertices: `A_0..A_31`, `B_0..B_31`;
- 188 binary index hyperedges after local u elimination;
- 124 indices incident on two factors;
- 64 v-mask indices incident on three factors.

The degree-3 hyperedges appear because, for example, one `v4_j` participates in its local A factor and in both A/B factors eight sites away.

Therefore ordinary graph carving width of the 32 fused sites is not the exact same optimization problem as hypergraph contraction width of the 64 refined factors.

## 4. Concrete falsifier of a universal 42 lower bound

In the refined 64-factor hypergraph, a balanced 22|42 factor cut with only **41** crossing binary indices was found.

One 22-factor side is:

`{A18,A19,A20,A21,A22,A23,A28,A29,A30,A31,`

` B9,B10,B11,B18,B19,B20,B21,B22,B23,B29,B30,B31}`.

Its hyperedge boundary count is 41; the complement has the same boundary count.

A binary feasibility optimization with cardinality 22 and boundary limit 41 terminated feasible/optimal for the zero objective, confirming the stated cut exactly.

Therefore the statement

`every balanced factor-network cut has at least 42 bonds`

is false.

The previous 42 lower bound applies only after the A_i/B_i pair has been fused into one site vertex.

## 5. What is NOT yet established

A single 41-bond balanced cut does not prove a complete width-41 contraction tree.

Recursive heuristic splitting of the 42-factor complement currently encounters cuts around 42–44. No exact global hypergraph carving/branch-width value has yet been certified.

So the correct present inequalities are:

- fused-site path cutwidth = 44 exactly;
- fused-site carving width = 42 exactly;
- refined factor network has at least one balanced cut of size 41;
- refined global optimal contraction width remains unresolved, with an inherited explicit upper bound 42 by pairing A_i/B_i and using the fused-site width-42 decomposition.

Hence

`refined_width <= 42`,

but a matching lower bound is not yet known.

## 6. Local linear parity relations

Eliminating `u4_i` from the two sigma recurrences for additions 4 and 2 gives one exact GF(2) relation among their external variables:

`s4_{i-1} xor s2_{i-1}`

`= s4_i xor s2_i xor v4_i xor v4_{i+8} xor v3_{i+12} xor const_i^(42)`.

Similarly, eliminating `u3_i` from additions 3 and 1 gives

`s3_{i-1} xor s1_{i-1}`

`= s3_i xor s1_i xor v3_i xor v4_{i+8} xor v3_{i+12} xor const_i^(31)`.

The constants depend only on fixed boundary mask bits.

These relations explain algebraically why the local fused site has codimension at least two in its formal external binary index space.

However most such local relations are absorbed by internal variables when a large side of the network is projected onto a separator.

## 7. Width-42 root-cut parity check

For the previously certified fused-site root cut with 42 crossing binary indices:

- one side induces no independent GF(2) boundary parity after all internal linear variables are eliminated;
- the other side induces exactly one independent affine parity relation.

Thus pure linear recurrence parity reduces that particular formal boundary space from at most `2^42` to at most `2^41` on one side.

A search among several other width-42 balanced cuts found zero or one independent boundary parity, not a large linear collapse.

Therefore a dramatic algebraic reduction, if present, is unlikely to come from GF(2) linear recurrence constraints alone.

## 8. Correct next target

The factorization changes the next question from

`Can we reorder the 32 fused sites?`

to

`Can the 64-factor hypergraph and its actual tensor ranks be contracted below the fused-site width 42?`

The relevant mechanisms are:

1. refined hypergraph contraction trees that keep A_i/B_i split;
2. nonlinear support constraints from `sigma_i=0 => u_i=v_i=w_i`;
3. exact rank deficiency of A_i and B_i across useful index partitions;
4. algebraic compression of degree-3 v-mask hyperedges;
5. epsilon-rank if exact refinement remains too wide.

## 9. Canonical correction

Do not cite `carving_width=42` as a lower bound for the full exact QR factor network.

The accurate statement is:

> The fused-site network has exact weighted carving width 42. Exact local pair factorization refines that network, and a 41-bond balanced refined cut already exists; the global refined contraction width is still open but is at most 42.

This correction preserves all previous finite calculations while narrowing their scope correctly.

## 10. Claims not admitted

No width-41 full contraction tree is claimed. No practical exact QR computation, double-round contraction, ranking gain, alpha<1, or full-round result follows from the 41-bond cut.