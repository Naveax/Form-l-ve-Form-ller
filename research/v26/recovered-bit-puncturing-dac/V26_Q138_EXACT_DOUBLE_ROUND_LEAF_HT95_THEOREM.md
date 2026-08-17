# V26 q138 Exact Double-Round Leaf-HT Width-95 Theorem

## Statement

For the q138 fixed-output inverse-double-round dependency cone consisting of one central column QR and four diagonal leaf QRs, there exists an exact structural representation with peak message exponent

`W_2_repr <= 95`.

This improves the clean open-boundary topology path bound 236 by exactly factorizing each one-output-word leaf as a hierarchical tensor over its 32 open output-mask bits.

## Five-QR star

The active final column QR is `(0,4,8,12)`. Its four open input-word masks are supplied independently by four diagonal leaf QRs, one for each local A/B/C/D position.

The central reduced fixed-output/open-four-input QR has the exact site graph

- four parallel sigma path bonds;
- cyclic offset-8 bonds;
- cyclic offset-12 bonds;
- cyclic offset-16 bonds.

For any bit-site subset `S`, let `b_center(S)` denote the number of these binary central edges crossing `S | Sbar`.

## Exact leaf rank envelope

Each leaf QR has fixed input masks and only one 32-bit output-word mask open. After contracting its internal QR factors, it is therefore an exact vector

`v : {0,1}^32 -> Q`.

For any subset `S` of the 32 bit positions, the matricization rank of an arbitrary 32-bit vector across `S | Sbar` is bounded by

`2^min(|S|,32-|S|)`.

Hence any chosen binary partition tree on the 32 bit positions admits an exact hierarchical Tucker representation of each leaf with edge-rank exponent at most

`min(|S|,32-|S|)`

on the tree edge associated with cluster `S`.

The four independent leaves multiply their exact rank bounds, giving total leaf exponent

`4*min(|S|,32-|S|)`.

Combining the leaf hierarchical bonds with the central QR graph therefore gives the exact cluster message bound

`w(S) = b_center(S) + 4*min(|S|,32-|S|)`.

## Explicit 32-bit partition tree

A verified binary tree is

`[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]`.

For every non-root cluster in this tree,

`w(S) <= 95`.

The maximum 95 occurs on three clusters with smaller side 11 bits. Each has

- central boundary exponent 51;
- four-leaf hierarchical rank exponent 44;
- total 95.

The next significant cluster has total 94; all others are smaller.

Thus

`W_2_repr <= 95`.

## Factor generation

This is a representation/message-width statement. It does not assume the leaf factorization is magically free.

However factor generation itself does not violate the 95-bit peak-message bound:

- each original reduced leaf QR has path topology <=44;
- materializing a complete 32-bit leaf vector requires at most `2^32` coefficients;
- exact hierarchical rank factorizations of that vector can therefore be generated below the final `2^95` representation peak.

This does not imply favorable arithmetic work.

## Verification

Authority:

`scripts/verify_v26_q138_double_round_leaf_ht95.py`.

Clean GitHub Actions run `32008540992`, job `95322970930`, passes and recomputes every cluster boundary from the explicit tree.

Historical intermediate bounds:

- raw/reduced common-prefix star topology: 236;
- natural common-prefix leaf TT bound: 124;
- explicit hierarchical leaf/tree bound: 95.

## Scope

The theorem proves an exact structural two-layer representation upper bound. It does not prove

- optimality of 95;
- arithmetic-work reduction;
- sparse-work reduction;
- a practical evaluator at `2^95` scale;
- a recurrence for further rounds;
- ranking gain;
- `alpha<1`;
- full-round relevance.

The natural next target is the actual Schmidt/sector structure of the central and leaf kernels on the three 95-bit maximizing partitions, since the generic leaf rank envelope may be far from saturated for the q138 coefficient instance.
