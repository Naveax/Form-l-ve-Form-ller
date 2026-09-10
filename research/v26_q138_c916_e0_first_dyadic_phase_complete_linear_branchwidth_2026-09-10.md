# V26 Q138 C916 e0 phase-complete linear branchwidth: dual-kernel coverage

## Scope

This note freezes the exact dual-kernel overlap geometry of the 250 minimal GF(2) linear-factorization spaces from PR #168.

For a group space V_i in the 149-bit physical shared domain, let K_i = V_i^perp. Since the exact group ranks are 142..147, the kernel dimensions are only 2..7. A set of groups has union row rank below 149 iff the corresponding kernels have a common nonzero direction. Therefore the maximum number of groups covered by one nonzero kernel direction is exactly the maximum cardinality of a non-full-rank group subset.

## Exact result

- global union rank: 149
- kernel dimension histogram: `{2:16, 3:12, 4:72, 5:60, 6:16, 7:74}`
- unordered pairs: 31,125
- pair union-rank histogram: `{142:5, 143:194, 144:2359, 145:7774, 146:6117, 147:11195, 148:3110, 149:371}`
- non-full pairs: 30,754
- unique nonzero kernel directions: 3,607
- maximum common-direction coverage: 217 groups
- exactly one direction attains coverage 217; digest `4a6fb6925a8f5418ab88`
- maximum non-full group subset size: exactly 217
- every subset of size at least 218 has full union rank 149

The complete coverage histogram is frozen in the verifier.

## Branchwidth consequence

The balanced-edge lemma for a subcubic tree with 250 leaves guarantees an edge with at least `ceil(250/3)=84` leaves on each side. The dual-coverage threshold is 218, not 84, so this argument does not force both sides of that balanced edge to have rank 149.

Thus this pass does **not** prove branchwidth 149. From PR #168, individual group ranks reach 147, while the ambient dimension is 149, so the exact phase-complete linear branchwidth remains in the narrow interval `[147,149]`.

Decision: `PHASE_COMPLETE_LINEAR_BRANCHWIDTH_DUAL_COVERAGE_INCONCLUSIVE`.

## Next gate

The dominant kernel direction shared by 217 groups gives strong structure for an explicit width-148 construction attempt. A sufficient width-148 decomposition can be built if the groups can be organized recursively so every proper cluster or its complement retains a nonzero common kernel direction. The first target is to exploit the 217/33 split induced by the dominant annihilator and test whether the 33 exceptional groups admit a compatible non-full hierarchy.

This remains a linear-factorization statement. It does not rule out nonlinear compression and does not include the exact all-250 nonlinear joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic work, ranking/search, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`
