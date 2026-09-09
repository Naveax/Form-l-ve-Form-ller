# V26 q138 C916 left-parent exact minimax width 60

## Fixed class

Consider the baseline parent interval `[0,166)` under the fixed `multiplicity_then_function` leaf order. The admissible class is every contiguous binary contraction tree on those 166 leaves. This certificate does not address unrestricted branchwidth.

## Exact lower bound

The frozen threshold-59 dynamic program exhausts the fixed-order contiguous class and finds no complete tree whose every non-root descendant edge has safe evaluation cost at most 59 bits.

Therefore

\[
W_{\min}\ge 60.
\]

The no-go search evaluates 6270 interval costs and still has 29 first-level splits whose two direct children are individually at most 59 bits. The obstruction is therefore recursive rather than a root-split artifact.

## Explicit upper witness

The existing baseline function-tree subtree on `[0,166)` is re-evaluated with the merged safe-evaluation oracle.

Exact witness data:

- leaves: `166`
- descendant edges: `330`
- maximum depth: `9`
- maximum safe edge width: `60`
- number of 60-bit edges: `2`
- number of 59-bit edges: `1`

The two 60-bit bottlenecks are `[110,166)` and `[55,110)`. The next edge is `[0,110)` at 59 bits.

Thus

\[
W_{\min}\le 60.
\]

Combining the lower and upper bounds gives

\[
\boxed{W_{\min}=60}.
\]

Decision:

`EXACT_FIXED_ORDER_CONTIGUOUS_MINIMAX_WIDTH_60`.

## Consequence

No further fixed-order contiguous surgery inside `[0,166)` can lower the complete displayed-tree ceiling below 60 bits. Any improvement below 60 must change the leaf order, leave the contiguous-tree class, or improve the edge-state representation itself.

## Scope

This is not an unrestricted branchwidth lower bound. Grouped-e0 carry remains separate. No support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
