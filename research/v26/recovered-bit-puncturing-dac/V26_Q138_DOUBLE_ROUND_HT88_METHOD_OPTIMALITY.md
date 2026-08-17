# V26 q138 HT-88 Generic-Envelope Method Optimality

## Statement

The exact double-round structural representation bound `W_2_repr<=88` is optimal **inside the specific generic envelope method** that combines

1. the reduced central QR graph/physical-dimension rank bound; and
2. four arbitrary 32-bit leaf-vector Hilbert-rank bounds.

This is not a lower bound on the actual q138 double-round tensor. Any improvement below 88 must exploit coefficient-specific algebraic rank deficiency or a different representation mechanism.

## Cardinality-constrained central cuts

For the reduced central graph with four sigma path bonds and cyclic offsets 8, 12 and 16, exact HiGHS MILP solves the minimum weighted boundary among all site subsets of cardinality `k`.

For `k=11..16`:

| smaller side k | min central graph boundary |
|---:|---:|
| 11 | 51 |
| 12 | 52 |
| 13 | 55 |
| 14 | 54 |
| 15 | 55 |
| 16 | 56 |

Each returned MILP solution is independently recounted from the integer subset.

## Generic combined envelope

For a site subset of size `k<=16`, the central tensor also has physical matricization exponent at most `4k`. Four arbitrary 32-bit leaf vectors contribute at most `4k` in total. Hence this method assigns

`cost(k)=min(b_min(k),4k)+4k`.

The exact values are

- k=11: 88;
- k=12: 96;
- k=13: 104;
- k=14: 110;
- k=15: 115;
- k=16: 120.

Every binary tree with 32 leaves has an edge whose smaller side has 11..16 leaves by the standard balanced-edge lemma. Therefore every tree evaluated by this generic envelope has maximum at least 88.

The explicit HT88 tree attains 88, so 88 is exact for this method.

## Consequence

Further tree permutation or generic graph-cut search cannot lower the certified bound while retaining the same two generic ingredients.

To beat 88 one must obtain at least one of:

- actual central Schmidt rank below the generic physical-dimension cap on the critical 11|21 partitions;
- actual leaf Schmidt rank below the arbitrary-vector bound `2^11`;
- a joint central/leaf factorization that does not factor their rank envelopes independently;
- another exact representation outside this envelope.

## Verification

Authority:

`scripts/verify_v26_q138_double_round_ht88_method_optimal.py`.

Clean GitHub Actions run `32009470077`, job `95325735925`, passes all six MILPs and the balanced-edge lower-bound calculation.

## Scope

This is method-optimality only. It is not a tensor-rank lower bound, arithmetic-work lower bound, cryptanalytic lower bound, or full-round result.
