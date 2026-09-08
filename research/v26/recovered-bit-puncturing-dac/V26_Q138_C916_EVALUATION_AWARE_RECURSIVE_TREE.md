# V26 q=138 C916 evaluation-aware recursive tree

## Result

A first deterministic recursive-tree search that chooses splits by the merged safe evaluation-state edge cost does **not** improve the certified C916 tree width.

Both tested orders give

\[
\boxed{W_{\mathrm{safe}}=65}.
\]

The verdict is

`NO_GENERIC_EVALUATION_AWARE_TREE_GAIN`.

## Search

The probe uses the same group family and safe edge evaluator as the merged full-tree certificate. For every recursive interval it evaluates the bounded candidate splits at approximately `1/3`, `2/5`, `1/2`, `3/5`, and `2/3`, then minimizes child safe-evaluation cost before function-space cost and balance.

Two deterministic orders were tested:

- `multiplicity_then_function`,
- `multiplicity_then_linear`.

For both:

- safe evaluation width = 65,
- function-space width on the selected tree = 70,
- maximum depth = 10,
- fiber-quadratic edge count = 126.

The persistent worst edge is `[166,199)` with:

- size 33,
- function lambda 68,
- residual dimension 5,
- fiber-affine residual geometry,
- safe evaluation width 65.

That is the same exact 65-bit bottleneck already certified in the baseline tree.

## Interpretation

Changing the greedy split objective from function-space lambda to the generic safe evaluation-state cost is not sufficient when the order family and split candidates remain narrow. The negative result is useful because it rules out a cheap tree-selection fix.

The next search should therefore change the search space rather than repeat the same heuristic: add wider deterministic orders and split offsets, and incorporate merged exact edge refinements by the actual group-ID subset rather than by interval coordinates.

## Scope

This is an exact certificate for the displayed heuristic trees, not an optimal branchwidth result. It does not establish aggregate e0 carry completion, support/e1 carry, half cross-carry, complete C2, `W_repr`, arithmetic work, alpha, ranking/search, or full-round cost.

`ALPHA_PASS=0`.
