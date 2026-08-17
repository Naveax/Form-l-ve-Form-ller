# V26 q138 Exact Double-Round HT-88 Representation Theorem

## Statement

The q138 five-QR inverse-double-round star admits an exact hierarchical structural representation with

`W_2_repr <= 88`.

This supersedes the intermediate leaf-HT bound 95.

## Construction

Use the same verified 32-bit partition tree as the HT95 construction:

`[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]`.

For a cluster `S`, two independent exact upper bounds hold for the central fixed-output/open-four-input QR tensor:

1. factor-graph separator exponent `b_center(S)`;
2. physical matricization exponent `4*min(|S|,32-|S|)`, because there are only four open binary input-word coordinates per bit site.

Hence its exact Schmidt exponent obeys

`c(S) <= min(b_center(S), 4*min(|S|,32-|S|))`.

Each of the four diagonal leaf QRs contracts to a 32-bit vector. Exact hierarchical factorization on the same partition tree gives each leaf exponent at most `min(|S|,32-|S|)`, so four leaves contribute

`4*min(|S|,32-|S|)`.

Thus the composed cluster exponent is bounded by

`w(S) = min(b_center(S),4m) + 4m`,

where `m=min(|S|,32-|S|)`.

## Explicit maximum

The complete verifier recomputes every cluster in the explicit tree. The maximum is 88 on three 11|21 partitions.

For each maximizing cluster:

- central graph boundary: 51;
- central physical-dimension Schmidt bound: 44;
- four-leaf hierarchical rank exponent: 44;
- total: `44+44=88`.

Therefore

`W_2_repr <= 88`.

## Relation to factor generation

This is an exact representation theorem, not an arithmetic-work theorem.

The leaf factors can be generated below this peak: each leaf reduced QR has topology path at most 44 and a dense 32-bit leaf vector has exponent 32.

The central `min(graph,physical-dimension)` rank replacement is an existence/Schmidt statement. A separately certified factor-generation procedure achieving peak 88 has not been proved. Keeping the central graph representation avoids this issue but gives the constructive intermediate bound 95.

Thus retain two ledgers:

- exact representation existence: `W_2_repr <= 88`;
- currently explicit graph-plus-leaf-factor construction: `W_2_construct <= 95`.

## Verification

Authority:

`scripts/verify_v26_q138_double_round_leaf_ht95.py`

(the historical filename is retained; its current milestone output is `V26_Q138_EXACT_DOUBLE_ROUND_LEAF_HT88`).

Clean GitHub Actions run `32008738204` passes.

## Scope

No optimality, arithmetic-work reduction, practical evaluator, multi-double-round recurrence, ranking gain, `alpha<1`, or full-round relevance is claimed.

The next algebraic target is the actual central Schmidt rank on the three 11|21 maximizing partitions, followed by actual leaf ranks when the fixed leaf input masks are made explicit. Any deficiency immediately lowers 88.
