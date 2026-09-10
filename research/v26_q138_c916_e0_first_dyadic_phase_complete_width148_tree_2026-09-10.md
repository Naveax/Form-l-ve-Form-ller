# V26 Q138 C916 e0 first-dyadic phase-complete width-148 tree

## Scope

This note freezes an explicit exact width-148 branch-decomposition certificate for the 250 phase-complete minimal GF(2) linear-factorization spaces from PR #168, using the dual-kernel geometry measured in PR #169.

The 149-bit physical shared domain is used throughout. PR #169 found a unique nonzero annihilator direction shared by 217 groups. Every subset of those 217 groups therefore has union rank at most 148. The remaining 33 groups are partitioned by two additional exact annihilator directions, into blocks of sizes 21 and 12. Every subset inside each block is likewise non-full.

The resulting rooted binary tree is not accepted from the construction heuristic alone. Every non-root edge is independently recomputed using exact common-kernel intersections on both sides of the cut.

## Exact certificate

- support groups: 250
- physical shared dimension: 149
- minimal group-rank histogram: `{142:74, 143:16, 144:60, 145:72, 146:12, 147:16}`
- dominant annihilator digest: `4a6fb6925a8f5418ab88`
- dominant coverage: 217 groups
- exceptional groups: 33
- exceptional cover size: 2 directions
- exceptional direction digests: `0913d6a8787377491d4d`, `d249413823c65dd43a21`
- exceptional partition sizes: 21 and 12
- tree nodes: 499
- independently checked non-root edges: 498
- certified tree width: 148
- edges with lambda above 148: 0
- edge lambda histogram: `{142:74, 143:17, 144:81, 145:124, 146:78, 147:79, 148:45}`

Decision:

`PHASE_COMPLETE_LINEAR_BRANCHWIDTH_IN_147_148_WITH_WIDTH148_CERTIFICATE`

## Lower bound

A rank-147 group gives a universal lower bound of 147. The frozen witness is group 5. Its 249-group complement has full union rank 149, so the corresponding leaf edge has

`lambda = 147 + 149 - 149 = 147`.

Therefore the exact phase-complete linear branchwidth is rigorously confined to `[147,148]`.

## Interpretation and next gate

The previous ambient upper bound 149 is no longer needed: an explicit exact width-148 tree exists. The remaining linear question is now one bit wide: determine whether a width-147 branch decomposition exists or prove that every branch decomposition contains an edge of lambda at least 148.

A width-147 edge requires `rank(S) + rank(S^c) <= 296`. In dual terms, if `k(S)` and `k(S^c)` are common-kernel dimensions, then `lambda = 149 - k(S) - k(S^c)`, so width 147 requires `k(S) + k(S^c) >= 2` on every edge. The next pass should exploit this exact criterion rather than merely asking whether either side has one common annihilator.

This remains a linear-factorization statement only. It does not rule out nonlinear compression and does not include the exact all-250 nonlinear joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic work, ranking/search, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`
