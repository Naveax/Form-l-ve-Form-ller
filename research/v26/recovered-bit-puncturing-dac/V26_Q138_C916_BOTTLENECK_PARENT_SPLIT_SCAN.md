# V26 Q138 C916 bottleneck-parent split scan

## Scope

This note freezes the exact contiguous split scan of the persistent C916 safe-evaluation bottleneck parent under the merged `multiplicity_then_function` group order. It is a local tree-surgery certificate only. It does not claim optimal branchwidth or complete C2 / full-round compression.

`ALPHA_PASS=0`.

## Authority

The parent interval is `[166,250)`, containing 84 grouped-e0 support groups. Its merged safe-evaluation edge width is 40 bits. The previously selected child cut `[166,199)` is the exact 65-bit bottleneck, with complement child `[199,250)` at 63 bits.

All 83 possible contiguous binary splits of `[166,250)` were evaluated with the same exact safe edge evaluator and subset-stable merged overrides used by the refined C916 tree work.

## Exact result

- splits scanned: **83 / 83**
- splits with both direct children at most 64 bits: **36**
- splits with max child width below 65: **36**
- best direct split: **167**
  - `[166,167)`: 12 bits
  - `[167,250)`: 41 bits
  - max child width: **41**
- previous split: **199**
  - `[166,199)`: 65 bits
  - `[199,250)`: 63 bits
  - max child width: **65**

The exact histogram of the maximum child safe width over the 83 splits is frozen by `verify_v26_q138_c916_bottleneck_parent_split_scan_result.py`.

## Consequence

The old 65-bit bottleneck is not forced by the parent cut or by the fixed local group order. There are 36 first-level splits whose two child edges already satisfy the target `<=64` condition.

Therefore local reordering is not yet necessary. The correct next test is an exact recursive interval-feasibility search on `[166,250)`: for every non-root descendant interval used in the rebuilt local subtree, require `safe_evaluation_bits <= 64`, and require an internal interval to admit a split into two recursively feasible children.

If such a recursive tree exists, substituting it for the old `[166,250)` subtree removes the displayed 65-bit local bottleneck while preserving the rest of the contraction tree. If no such tree exists, direct-child feasibility alone was insufficient and local reordering becomes the next route.

## Not included

This result does not include aggregate e0 carry completion, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work accounting, alpha, ranking/search, or a full-round compression claim.
