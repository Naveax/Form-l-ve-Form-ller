# V26 Q138 C916 e0 first-dyadic group-output minimal linear factorization

## Scope

This note freezes the exact minimal GF(2) linear factorization row space of each of the 250 integer-valued C916 e0 first-dyadic group residual functions.

For a function on GF(2)^149, the minimal linear factorization row space is exactly the span of its nonzero Walsh frequencies. The computation uses the exact 680-term physical representation frozen upstream: 577 post-Gauss sector terms plus 103 singleton projection-baseline terms.

Each affine-supported quadratic term has an exact affine Walsh-support set. The first pass derives this support from radical consistency. The overlap-closure pass independently constructs the symbolic Walsh transform by quadratic Gauss elimination, requires the two support descriptions to agree, and then evaluates exact group Walsh coefficients on candidate frequencies. Candidate discovery is deterministic; every accepted frequency has an exact nonzero coefficient, so sampling affects discovery only, never validity.

## Regression and cross-checks

- physical shared dimension: 149
- support groups: 250
- multiplicities: `{1:103, 2:57, 4:90}`
- physical terms: 680
- synthetic exact Fourier-transform regression: 28 affine-supported quadratic terms over GF(2)^5, 896 brute-force frequency checks
- symbolic per-term Walsh support is independently cross-checked against radical-consistency support

## Exact result

All 250 groups close exactly. The exact minimal-rank histogram is:

`{142:74, 143:16, 144:60, 145:72, 146:12, 147:16}`.

By multiplicity:

- multiplicity 1: `{142:74, 144:29}`
- multiplicity 2: `{143:16, 144:29, 145:12}`
- multiplicity 4: `{144:2, 145:60, 146:12, 147:16}`

Closure method:

- 140 groups close using certified unique-term Walsh-support frequencies alone
- 110 additional groups close after exact overlap-cancellation evaluation
- unresolved groups: 0

The exact overlap pass uses 4,245 exact candidate-frequency evaluations: 1,835 nonzero and 2,410 zero. Rank-increasing exact witnesses comprise 96 support origins, 547 support-basis single toggles, and 1,192 deterministic support-hash points.

Relative to the PR #148 refined support/frequency/radical-control local row spaces, the exact minimal rank requires an additional 121 to 133 dimensions, with histogram:

`{121:60, 122:10, 123:29, 124:4, 126:2, 127:34, 128:51, 129:29, 130:18, 131:9, 132:3, 133:1}`.

Decision:

`EXACT_MINIMAL_LINEAR_FACTORIZATION_RANKS_CLOSED_FOR_250_GROUPS`

## Interpretation

The PR #148 width-61 separator remains exact for the support/frequency/radical-control target it measured. It cannot be promoted unchanged to the exact first-dyadic integer outputs. PR #167 already gives direct translation counterexamples for every group; this result quantifies the missing phase information exactly.

Every exact group residual depends, in the minimal linear-factorization sense, on between 142 and 147 independent linear forms of the 149 physical shared bits. Thus any phase-complete linear separator analysis must be rebuilt from these exact minimal row spaces rather than by adding a handful of correction bits to the width-61 state.

This result does not rule out nonlinear compression and does not itself give an optimal or displayed phase-complete separator width. It does not include the exact all-250 joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic work, ranking/search, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`
