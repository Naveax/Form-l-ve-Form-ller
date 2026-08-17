# V26 q138 exact d=1 signed83 two-factor theorem

## Statement

For the q138 fixed-output inverse-double-round five-QR star, an exact S1-root two-factor representation exists with factor dimension

`3393 * 2^72`,

hence

`W_repr(1) <= 72 + log2(3393) = 83.72834571471098...`.

The same representation is coefficient-aware materialized-factor generable at the same maximum single-factor dimension, with right-entry contraction peak80. Arithmetic work is not reduced by this theorem.

## First multisite block

The previously certified occurrence-closed four-site block

`{2,3,18,19}`

acts on the eight S1 physical row bits at sites2,3 and has exact rational rank96 instead of256. It is disjoint from the earlier rank16 and rank2784 S1 blocks.

## Second disjoint multisite block

Use the eight physical S1 row bits on sites4,5:

`A4,B4,C4,D4,A5,B5,C5,D5`.

Close the second occurrences of D4,D5 by including complement sites20,21. Thus the local occurrence-closed subnetwork is

`{4,5,20,21}`.

The exact q138 fixed output has `b0=0` on all four of these sites. Contract the four adjacent carry channels exactly within `(4,5)` and `(20,21)`. Retain pair-boundary carries as columns. Long-range K/z channels are relaxed as independent retained columns; later identifying/contracting them is a linear column-side map and cannot increase row rank.

Construct the exact integer Gram matrix of the resulting256-row relaxed map. Exact rational Gaussian elimination gives

`rank_Q(Gram)=208`.

Odd-prime rank is also208.

Moreover the rank basis is physically constructive:

-208 actual physical rows can be selected as a basis;
- the remaining48 physical rows are each an exact combination of exactly three basis rows;
- every nonzero coordinate coefficient is `+1` or `-1`.

Therefore the coefficient map itself has exact rational rank208 and an explicit physical-row basis.

## Combined S1 rank

The four S1 row-variable groups are pairwise disjoint:

- block1:5 physical bits, rank16;
- block2:13 physical bits, rank2784;
- special four-site block on sites2,3:8 physical bits, rank96;
- generic four-site block on sites4,5:8 physical bits, rank208.

Only ten S1 physical row bits remain raw. Hence

`rank_center(S1) <= 16*2784*96*208*2^10`.

This equals

`3393*2^28`,

with central exponent

`28+log2(3393)=39.72834571471098...`.

Four predecessor leaves contribute44 S1 mask bits. Therefore an S1-root exact factor has

`3393*2^72`

entries, exponent

`83.72834571471098...`.

## Why the old S2 HT bottleneck no longer controls

On the old frozen HT tree, the S2 internal node would remain at

`31*2^79`, exponent `83.95419631038688...`,

slightly above the new S1 message. That is a property of that particular hierarchical tree, not a lower bound on the full tensor representation.

The coefficient-aware construction instead uses the S1 cut as the root and generates the complement factor with the explicit21-site complement tree whose entry-generation peak is80. It never materializes the old S2 HT node. Therefore the complete two-factor representation/factor-generation bound is controlled by the S1 factor itself at83.7283, not by the historical S2 node.

## Constructivity

- rank16 block1 is physical-row explicit;
- rank2784 block2 has the clean physical-row bridge with at most64 ordinary physical rows per normalized retained-column basis slice;
- rank96 block uses actual physical signed row classes;
- rank208 block uses208 actual physical basis rows and ±1 three-term dependencies;
- the ten residual bits are identity channels.

Hence every complete signed right-basis direction is still an exact combination of at most64 ordinary physical S1 central rows. Reuse the exact complement tree from the factor-generation85 theorem; its right-entry contraction peak remains80, below83.7283.

Thus both the representation and the coefficient-aware materialized-factor generation upper bounds are

`83.72834571471098...`.

## Scope

This is exact, `epsilon=0`. No lower bound, optimality, practical evaluator, arithmetic-work reduction, ranking gain, alpha<1 or full-round relevance is claimed.

Verifier:

`scripts/verify_v26_q138_double_round_signed83_twofactor.py`.
