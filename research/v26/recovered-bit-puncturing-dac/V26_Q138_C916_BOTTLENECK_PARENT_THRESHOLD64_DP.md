# V26 Q138 C916 bottleneck-parent threshold-64 interval DP

## Scope

This note freezes the exact fixed-order contiguous-interval feasibility result for rebuilding the C916 parent `[166,250)` while constraining every new child and descendant safe-evaluation edge to at most 64 bits.

The parent edge itself is retained from the existing global tree and is not part of the new threshold test. No optimal branchwidth or complete C2 / full-round claim is made.

`ALPHA_PASS=0`.

## Authority

PR #134 established that, under the merged `multiplicity_then_function` group order, 36 of the 83 direct splits of `[166,250)` already have both child edges at most 64 bits. The present DP recursively tests whether those children can themselves be decomposed into threshold-compliant contiguous intervals down to all 84 leaves.

Each interval edge is evaluated with the merged refined C916 safe-evaluation oracle and subset-stable exact overrides.

## Exact result

The threshold-64 recursive feasibility problem is **feasible**.

- parent: `[166,250)`, 84 leaves
- direct root splits at most 64 bits: **36**
- witness root split: **167**
- witness non-root edge count: **166**
- witness maximum safe-evaluation width: **59 bits**
- witness maximum depth: **22**
- interval costs evaluated: **1534**
- feasibility states cached: **166**

The two worst witness edges are both 59 bits:

- `[179,250)`, function lambda 63, digest `95b3fcf51ed806d0`
- `[179,244)`, function lambda 63, digest `4809b3aae6e11ab7`

## Consequence

The old 65-bit edge `[166,199)` is not merely avoidable at the first split. A complete recursive replacement subtree exists in the same fixed group order, and every one of its 166 new non-root edges is at most 59 bits.

Therefore a 59-bit local certificate already follows from a search whose requested threshold was only 64. A threshold sweep restricted to 60 through 64 would add no information. The correct next step is an exact minimax interval DP that directly minimizes the maximum safe-evaluation edge width over all contiguous binary trees on `[166,250)` under this fixed order.

After the minimum local width is frozen, its witness subtree should be substituted into the 250-leaf global C916 tree and all 498 non-root edges re-evaluated exactly to obtain the new displayed full-tree safe width.

## Not included

This result does not include aggregate e0 carry completion, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work accounting, alpha, ranking/search, or a full-round compression claim.
