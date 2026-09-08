# V26 q=138 C916 refined evaluation-aware recursive tree

## Result

The expanded deterministic evaluation-aware tree search does not beat the merged C916 safe evaluation width.

The exact candidate safe widths are

- `multiplicity_then_function`: 65,
- `multiplicity_then_linear`: 65,
- `function_then_multiplicity`: 72,
- `linear_then_multiplicity`: 72,
- `function_descending`: 77,
- `linear_descending`: 77.

The best displayed width therefore remains

\[
\boxed{65}.
\]

Verdict:

`NO_REFINED_EVALUATION_AWARE_TREE_GAIN`.

## Search refinements

Relative to the earlier no-gain search, this probe expands the deterministic search in three ways.

First, recursive split candidates are widened to approximately `1/4`, `1/3`, `2/5`, `1/2`, `3/5`, `2/3`, and `3/4`, with all possible splits used for intervals of size at most six.

Second, six deterministic group orders are tested rather than two.

Third, merged exact edge refinements are injected by the actual group-ID subset and its complement rather than by interval position. The exact override metadata is:

- former width-70 subset `[110,166)`: 60 bits, digest `ddddf643ea96032a`,
- former width-64 quadratic subset `[55,110)`: 60 bits, digest `c72f29e8fe2266ec`,
- exact current bottleneck `[166,199)`: 65 bits, digest `50a4b970f7f85916`.

This subset-keyed representation makes the overrides invariant under alternative orderings whenever the same cut reappears.

## Persistent bottleneck

The best two orders remain the multiplicity-first orders. Their worst edge is still the exact certified subset `[166,199)`:

- group count 33,
- function lambda 68,
- residual dimension 5,
- fiber-affine residual geometry,
- safe evaluation width 65.

The wider split search changes some surrounding right-side substructure, for example exposing `[199,237)` at 61 bits, but does not remove the 65-bit cut.

The rank-first orders are strictly worse at 72 bits, and descending rank orders are worse again at 77 bits. Therefore continuing to add similar global rank-based orderings is poorly motivated.

## Interpretation

The current 65-bit obstruction is not an artifact of using function-space lambda as the split objective, of the original narrow split ratios, or of failing to feed the two merged 60-bit exact edge refinements back into the search. All three cheap explanations have now been tested.

The next useful search should be local. In the multiplicity-first order, enumerate every split of the parent interval containing `[166,199)`, then use thresholded local interval dynamic programming or local reordering only where necessary. This directly tests whether the 65-bit child can be avoided while keeping the remainder of the certified tree at 64 bits or below.

## Scope

This is an exact safe certificate for the displayed heuristic trees, not an optimal branchwidth proof. It does not establish aggregate e0 carry completion, support/e1 carry, half cross-carry, complete C2, `W_repr`, arithmetic work, alpha, ranking/search, or full-round cost.

`ALPHA_PASS=0`.
