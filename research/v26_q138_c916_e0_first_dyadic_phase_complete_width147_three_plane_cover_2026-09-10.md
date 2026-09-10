# V26 Q138 C916 e0 first-dyadic width147 three-plane cover obstruction

## Scope

This note freezes an exact obstruction to one strong sufficient construction for phase-complete linear branchwidth 147.

For any edge cut `S | S^c`, let `k(S)` be the common-kernel dimension of the exact minimal group row spaces on side `S`. Since the ambient shared dimension is 149,

`lambda(S) = 149 - k(S) - k(S^c)`.

Thus width 147 requires `k(S)+k(S^c) >= 2` on every edge. A sufficient construction would cover all 250 groups by at most three blocks, each sharing a common 2D kernel plane, and arrange those blocks under a binary root. Every descendant subset inside a block then retains kernel dimension at least 2.

## Exact forced-plane obstruction

PR #168 gives 16 groups of exact minimal row rank 147. Each such group has kernel dimension exactly 2, so it contains exactly one 2D kernel plane. Therefore any cover of those groups by common-2D-kernel blocks must include every distinct plane forced by the rank-147 groups.

The 16 rank-147 groups are:

`[5, 8, 24, 62, 113, 154, 155, 156, 158, 179, 182, 186, 234, 239, 241, 244]`.

They force **five** distinct 2D kernel planes. Their digests and total group coverages are:

- `35078c9c78e4ea8a77dd`: 191 groups
- `648c2d0942437f963696`: 10 groups
- `3d38bd58df28dcc428a3`: 7 groups
- `3fddb3d36da3e8c82c5f`: 73 groups
- `6cd96f38e42b56e8ff91`: 8 groups

Because all five planes are mandatory, no cover of all 250 groups by at most three common-2D-kernel planes can exist.

Decision:

`THREE_COMMON_2D_KERNEL_COVER_IMPOSSIBLE_WIDTH147_OPEN`

## Boundary

This result does **not** prove that width147 is impossible. A more general width147 tree may contain cuts with kernel split `(1,1)`, may use more than three 2D-kernel regions, and need not arise from a global three-block cover.

The exact phase-complete linear branchwidth therefore remains in `[147,148]`, with the width148 upper bound certified by PR #170 and the width147 lower bound witnessed by group 5 with full-rank 249-group complement.

## Next gate

Search directly in the space of admissible cluster merges. Starting from singleton groups, merge two current clusters only when the exact global cut for their union satisfies `k(U)+k(U^c) >= 2`. Any completed binary tree found this way can be independently rechecked on all 498 non-root edges. Failure of a bounded heuristic search must not be promoted to an impossibility theorem.

This remains a linear-factorization statement only. It does not rule out nonlinear compression and does not include the exact all-250 nonlinear joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic work, ranking/search, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`
