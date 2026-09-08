# V26 q138 C916 bottleneck-parent exact minimax interval DP

## Scope

This certificate replaces threshold-feasibility search inside the C916 bottleneck parent `[166,250)` with an exact dynamic program over **every contiguous binary tree** on the fixed `multiplicity_then_function` group order.

For a non-root interval `I`, let `c(I)` be its exact safe-evaluation edge cost under the merged evaluator. The recurrence is

`M(I) = max(c(I), min_s max(M(I_left), M(I_right)))`.

The parent `[166,250)` already exists as an edge in the global tree, so its own cost is excluded from the replacement-subtree objective. At the retained root the objective is therefore

`M_root = min_s max(M(left), M(right))`.

This is an exact minimax calculation for the stated fixed-order/contiguous-tree class, not a sampled or heuristic tree search.

## Exact result

- position: `C`
- order: `multiplicity_then_function`
- parent interval: `[166,250)`
- parent size: `84`
- retained parent safe-evaluation edge cost: `40` bits
- retained parent function lambda: `44`
- exact local minimax safe width: **`55` bits**
- root split: `167`
- root child subtree widths: `[12,55]`
- witness non-root edges: `166`
- witness maximum depth: `19`
- intervals evaluated: `3570`
- DP states: `3569`
- split comparisons: `98770`
- oracle cache entries: `3570`

The witness edge-width histogram is:

`{11:1, 12:24, 13:58, 14:5, 15:13, 16:15, 17:4, 18:5, 19:2, 20:6, 21:1, 22:1, 23:3, 24:2, 25:2, 29:2, 31:3, 32:1, 36:1, 40:1, 41:1, 42:1, 44:1, 46:1, 47:1, 48:2, 49:1, 51:1, 52:1, 53:1, 54:2, 55:3}`.

The three edges attaining the optimum are:

1. `[173,243)`, size `70`, safe width `55`, function lambda `59`, quadratic residual dimension `6`, digest `666736852e0e2036`.
2. `[173,241)`, size `68`, safe width `55`, function lambda `59`, quadratic residual dimension `6`, digest `9883979cefaaef27`.
3. `[173,201)`, size `28`, safe width `55`, function lambda `57`, quadratic residual dimension `4`, digest `f1ab5bee99739b49`.

## Interpretation

The previous threshold-64 DP certified a complete local witness whose actual maximum edge cost was `59` bits, but that algorithm returned the first feasible recursive decomposition rather than optimizing the subtree maximum. The exact minimax DP lowers the fixed-order local optimum from `59` to `55` bits.

Relative to the historical exact `65`-bit bottleneck edge `[166,199)`, the local replacement-tree bottleneck has therefore fallen by `10` bits. Relative to the previous complete 59-bit witness, it falls by `4` bits.

The exact statement is:

`FIXED_ORDER_CONTIGUOUS_LOCAL_OPTIMUM = 55`.

This does **not** prove unrestricted branchwidth `55`. Reordering the 84 leaves or permitting a non-contiguous decomposition could in principle do better.

## Next target

Substitute this exact minimax witness for the `[166,250)` subtree in the full 250-leaf C916 tree and re-evaluate all `498` non-root edges with the same exact/safe evaluation oracle. That determines the displayed global tree width after local surgery and exposes the next real bottleneck, instead of continuing the traditional sport of optimizing a bottleneck that no longer exists.

## Not included

No unrestricted branchwidth theorem, aggregate grouped-e0 carry completion, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
