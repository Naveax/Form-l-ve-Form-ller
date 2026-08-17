# V26 q138 coefficient-blind constructive graph+leaf95 method optimality

Scope: only the frozen constructive method that combines the exact reduced central QR graph boundary with four generic predecessor-leaf Hilbert ranks. This is **not** a lower bound on the true q138 inverse-double-round tensor rank and does not constrain coefficient-aware signed factorizations.

For a bit-partition edge whose smaller side has cardinality `k`, this method has exact peak exponent envelope

`C(k,S)=gb(S)+4k`,

where `gb(S)` is the reduced central graph boundary and the `4k` term is the product of four generic leaf Hilbert dimensions.

The clean MILP cardinality theorem `scripts/verify_v26_q138_double_round_ht88_method_optimal.py` proves the exact central graph minima

- k=11: 51;
- k=12: 52;
- k=13: 55;
- k=14: 54;
- k=15: 55;
- k=16: 56.

Hence every such balanced edge has constructive graph+leaf cost at least

- k=11: 95;
- k=12: 100;
- k=13: 107;
- k=14: 110;
- k=15: 115;
- k=16: 120.

By the standard balanced-edge lemma for an unrooted/subcubic binary tree with32 leaves, every complete binary contraction tree has an edge whose smaller side lies in11..16. Therefore every contraction tree inside this coefficient-blind graph+leaf method has peak exponent at least95.

The existing constructive95 tree attains95, so

`W_construct,graph+leaf = 95`

is method-optimal.

This theorem closes **tree reordering alone** as a route below95. Any constructive bound `<95` must use additional coefficient-aware structure, e.g. explicit signed-rank factor insertion, non-generic leaf structure, or a different constructive representation.

Clean dependencies:

- `scripts/verify_v26_q138_double_round_ht88_method_optimal.py` and Actions run `32009470077`;
- `scripts/verify_v26_q138_double_round_constructive95.py`.

Verifier:

- `scripts/verify_v26_q138_constructive_graph_leaf95_optimal.py`.
