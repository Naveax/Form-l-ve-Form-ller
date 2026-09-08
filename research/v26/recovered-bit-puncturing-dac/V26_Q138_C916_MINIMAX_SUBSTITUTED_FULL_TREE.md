# V26 q138 C916 minimax-substituted full tree

## Result

PR #136 certifies that, within the fixed `multiplicity_then_function` order and contiguous binary-tree class inside parent `[166,250)`, the exact local minimax safe-evaluation width is 55 bits.

Substituting that exact witness into the complete 250-leaf C916 tree and re-evaluating all 498 non-root edges gives

\[
\boxed{W_{\mathrm{eval},C}\le 60}.
\]

This is an exact safe certificate for the displayed substituted tree. It improves the previous complete-tree ceiling from 65 bits to 60 bits.

## Exact tree data

- support groups: `250`
- non-root edges: `498`
- historical function-space tree width: `70`
- local minimax width inside `[166,250)`: `55`
- local root split: `167`
- minimax descendant edges inserted: `166`
- outside/local-parent-side safe width: `60`
- substituted full-tree safe width: `60`
- substituted full-tree function width: `70`
- substituted full-tree depth: `20`

The former unique 65-bit descendant edge `[166,199)` is absent from the substituted tree.

## New bottlenecks

Exactly two edges attain 60 bits.

### `[110,166)`

- size: `56`
- function lambda: `70`
- generic safe-evaluation bits: `60`
- exact safe bits: `60`
- quadratic residual dimension: `13`
- fiber residual becomes affine
- merged exact subset override is active

### `[55,110)`

- size: `55`
- function lambda: `64`
- generic safe-evaluation bits: `64`
- exact safe bits: `60`
- quadratic residual dimension: `12`
- residual remains genuinely quadratic on the affine kernel
- merged exact subset override is active

The next edge is `[0,110)` at 59 bits. The exact 55-bit local minimax witness contributes three 55-bit edges and therefore no longer controls the global ceiling.

## Interpretation

Local surgery succeeded. The historical 65-bit obstruction was a tree-shape artifact inside `[166,250)` for the displayed global order, not a persistent requirement of the remaining certified edge family.

The resulting complete displayed tree has safe evaluation width 60 while its degree-2 function-space width remains 70. This is not an unrestricted branchwidth optimum. It is, however, the strongest complete 498-edge C916 evaluation-state certificate currently in this chain.

Decision:

`FREEZE_COMPLETE_DISPLAYED_TREE_WIDTH60`

Further tree surgery below 60 would have to address the two independent 60-bit edges `[110,166)` and `[55,110)` rather than the right-side parent that has now been reduced to 55.

## Parallel carry result

The grouped-e0 carry program remains separate. The first dyadic pair-residual probe shows that all selected even-group pair equality conditions have restricted polar rank two. That structure should be lifted onto the shared/local coordinate decomposition before any carry cost is added to this 60-bit tree certificate.

## Scope

No unrestricted optimal branchwidth result, grouped-e0 carry completion, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
