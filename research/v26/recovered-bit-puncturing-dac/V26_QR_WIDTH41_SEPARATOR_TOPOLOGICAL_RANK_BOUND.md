# V26 QR Width-41 Separator Topological Rank Bound

## Purpose

`V26_QR_MINIMAL_CORE_WIDTH41_THEOREM.md` gives a complete exact contraction tree whose largest formal message boundary has dimension `2^41`.

This note asks a different question about that **specific certified bottleneck message**:

> if its 41 boundary indices are partitioned according to the two children already present in the certificate tree, what exact Schmidt/matrix-rank upper bound follows before using any numerical tensor values?

The answer is a strict reduction from the smaller formal boundary side `2^12=4096` to an interface dimension `3072`.

## 1. Certified bottleneck cluster

The unique maximum-dimension cluster in the width-41 certificate contains `340` tensor leaves and crosses

- `41` binary indices;
- no ternary boundary index.

Hence its formal dense message space has dimension

`2^41`.

The certificate tree splits this 340-leaf cluster into children of sizes

- `34` leaves;
- `306` leaves.

Call the corresponding child subnetworks `A` and `B`.

## 2. External-boundary partition

Relative to the 340-leaf parent boundary:

- child `A` touches `12` of the parent's 41 binary boundary indices;
- child `B` touches the remaining `29` parent boundary indices;
- no parent-external index is shared by both children.

Therefore the parent message can be viewed as a matrix

`M(x_A,x_B)`

with

- `x_A in {0,1}^12`, dimension `4096`;
- `x_B in {0,1}^29`, dimension `2^29`.

Without further structure the matrix rank could be as large as `4096`.

## 3. Child interface

The only indices connecting `A` and `B` internally are

- `10` binary indices;
- `1` ternary index.

Thus the exact child interface space has dimension

`D_AB = 2^10 * 3 = 3072`.

Contracting the internal tensors on each side separately gives exact maps

`L(x_A,z)`

and

`R(z,x_B)`

with `z` ranging over those 3072 interface states. Therefore

`M(x_A,x_B) = sum_z L(x_A,z) R(z,x_B)`.

This is an exact factorization, not an approximation.

## 4. Schmidt-rank consequence

Any matrix factorization through a 3072-dimensional interface obeys

`rank(M) <= 3072`.

Therefore the certified width-41 bottleneck message satisfies, across this 12|29 boundary partition,

`rank(M) <= 3072 < 4096`.

Equivalently,

`log2 rank(M) <= log2(3072)`

`= 10 + log2(3)`

`= 11.584962500721...`.

Compared with the formal smaller-side dimension `2^12`, this is an exact rank reduction by a factor

`4096/3072 = 4/3`.

In bit units the reduction is

`12 - log2(3072) = log2(4/3) ~= 0.4150375`.

This is modest, but it is the first strict exact Schmidt-rank reduction recorded for the machine-certified width-41 message.

## 5. Topological min-cut check inside the 34-leaf child

The 34-leaf child itself was analyzed as a terminal cut problem between

- its 12 parent-external boundary bits; and
- the `10 binary + 1 ternary` interface to the 306-leaf child.

Using edge capacities `log2(dim(index))`, the exact minimum terminal cut has capacity

`10 + log2(3)`.

That equals the full interface dimension bound above.

Therefore ordinary graph/min-cut structure inside the 34-leaf child does **not** improve the rank bound below 3072.

Any stricter rank reduction for this 12|29 flattening must exploit actual tensor algebra:

- equality-class sectors;
- sigma/class-parity selection rules;
- sign cancellation;
- exact linear dependence of interface slices.

Another topology-only separator inside this child cannot supply the missing reduction.

## 6. Relation to the ternary class core

The one ternary interface index has exact semantic meaning after the class-core factorization:

`00`, `11`, `unequal`.

Its state space is the direct sum

`E direct_sum U`

with dimensions `2+1`, and the local class-parity theorem gives the sector-flip rule

`e(c) xor e(d)=s`.

Thus the 3072-dimensional topological interface should not be treated as an anonymous dense `3 * 2^10` state in the next pass.

The correct next question is whether the 12 external boundary bits populate all three class sectors independently, or whether projected class-parity/support rules make some interface slices dependent or impossible.

## 7. Scope of the result

This note proves a rank upper bound for one specific flattening of the certified width-41 parent message.

It does **not** reduce the global contraction-tree message-width certificate from 41, because a matrix rank bound across one 12|29 partition is not the same object as a complete width-40 contraction tree.

Nor does it prove that rank 3072 is attained. The actual tensor rank may be smaller.

## 8. Next algebraic falsifier

Freeze the 34|306 split and replace the anonymous ternary interface basis by the semantic equality-class basis.

Then:

1. gauge the rank-2 endpoint TT bonds to their physical/sigma binary legs;
2. write every surviving class-parity segment law from `V26_MODADD_CLASS_PARITY_CONSERVATION.md`;
3. project out internal variables exactly;
4. count independent boundary/interface sectors;
5. derive the exact rank of the 4096-by-3072 left map `L`, or a strict upper bound below 3072;
6. only if `L` is full column rank should the 306-leaf side become the next target.

A strict bound `rank(L)<3072` would be a genuinely algebraic compression beyond graph topology.

## 9. Claims not admitted

This note does not prove `W<=40`, practical exact QR evaluation, a double-round/full-round contraction, ranking gain, or `alpha<1`.
