# V26 q138 C916 left-parent threshold59 DP

## Question

The current complete displayed C916 tree has safe-evaluation width 60, attained by two left-side descendants `[55,110)` and `[110,166)`. Their common baseline parent is `[0,166)`.

This certificate asks whether the descendants of `[0,166)` can be rebuilt, while preserving the fixed `multiplicity_then_function` leaf order, so that every new non-root descendant interval has safe-evaluation cost at most 59 bits.

The parent edge itself is retained.

## Exact parent data

The interval `[0,166)` is an actual node of the baseline tree.

Its exact evaluator data are:

- size: `166`
- safe-evaluation bits: `40`
- generic safe-evaluation bits: `40`
- function lambda: `44`
- quadratic residual dimension: `6`
- residual becomes affine on the evaluator fiber
- no exact subset override
- digest: `9e28f443b9a32e2e`

Thus the parent edge is not the obstruction.

## Exact threshold-59 result

All contiguous root splits and recursively reachable fixed-order intervals were tested with the same merged safe-evaluation oracle.

- direct root splits whose two immediate children are both `<=59`: `29`
- interval costs evaluated: `6270`
- feasibility states cached: `291`
- complete threshold-59 witness: **none**

Therefore

`THRESHOLD59_FIXED_ORDER_CONTIGUOUS_NO_GO`.

The no-go is recursive rather than first-level: many direct splits pass the 59-bit threshold, but every such branch eventually encounters a descendant interval that prevents a complete contiguous binary-tree decomposition under this fixed order.

## Consequence

The existing 60-bit complete displayed-tree certificate cannot be improved to 59 merely by another fixed-order contiguous rebuild of the `[0,166)` parent.

This does not prove unrestricted branchwidth 60. It only closes the threshold-59 class for this exact parent and leaf order.

The next precise tree question is the exact minimax width of `[0,166)` over all contiguous binary trees on this fixed order. Since the current displayed tree already supplies a 60-bit construction while threshold 59 is impossible, that minimax value is expected to be 60; an exact minimax DP should freeze that statement rather than infer it informally.

## Not included

Grouped-e0 carry remains separate. No unrestricted branchwidth theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`
