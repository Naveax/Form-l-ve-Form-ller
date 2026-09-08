# V26 q138 C916 e0 first dyadic pair residual

## Scope

PR #137 established that the 577 reachable C e0 sectors remain 577 distinct restricted nonconstant phase classes with unit signed coefficients. Therefore same-support/same-phase integer aggregation produces no carry gain.

For every even-multiplicity support group this certificate instead uses the exact pointwise identity

\[
\frac{(-1)^{q_i}+(-1)^{q_j}}{2}
=
(-1)^{q_i}\,\mathbf 1[q_i\oplus q_j=0].
\]

Multiplicity-2 groups have one forced pair. For multiplicity-4 groups all three perfect matchings are evaluated and a deterministic minimum-complexity matching is chosen using the restricted difference-polar ranks.

## Exact result

For C:

- reachable e0 sectors: `577`
- support groups: `250`
- support multiplicities: `{1:103, 2:57, 4:90}`
- even-multiplicity groups: `147`
- selected first-dyadic pair terms: `237`
- multi-sector support free dimensions: `{150:145, 151:2}`

Every selected equality condition is genuinely quadratic and has restricted polar rank exactly two:

- selected polar-rank histogram: `{2:237}`
- affine nonconstant selected differences: `0`
- genuinely quadratic selected differences: `237`
- maximum selected polar rank: `2`

For the 57 multiplicity-2 groups the forced pair rank histogram is `{2:57}`.

Across all multiplicity-4 matching candidates there are 540 pair occurrences with histogram

`{2:360, 4:180}`.

The deterministic lexicographic minimizer chooses matching index `0`, i.e. pairs `(0,1)` and `(2,3)`, in all 90 multiplicity-4 groups. The 180 selected multiplicity-4 pair terms therefore all have polar rank two. This does not assert uniqueness of that matching where ties may exist.

## Interpretation

The first cross-phase carry layer is not an arbitrary high-rank quadratic object. After exact pairing, all 237 selected equality supports are rank-2 quadratic conditions on their common affine supports.

This is materially stronger structure than the previous same-support integer-coefficient certificate, but it is not yet a separator-state theorem. The restricted support parameterizations have dimension 150 or 151 and include local left variables as well as the 149 shared predecessor/right coordinates.

Decision:

`RANK2_QUADRATIC_PAIR_EQUALITY_LAYER`

## Next target

Complete the first group-level dyadic residual by adding the 103 singleton terms, then decompose every selected rank-2 equality polynomial into the existing common-support coordinates: shared-only quadratic part, shared-to-left bilinear frequency part, and left-only quadratic part. Only after that decomposition should cut-local separator message complexity be measured.

## Not included

No separator width, grouped-e0 carry completion, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
