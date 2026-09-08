# V26 Q1.38 B/C grouped-e0 local linear separator diagnostic

## Authority

This note continues the PR111 conclusion that the global grouped-e0 support signature is already injective on the full

`128 predecessor + 21 right-beta = 149`

bit shared state. Therefore a global lossless linear quotient cannot reduce the state dimension.

Clean pull-request run:

- PR: `#112`;
- workflow: `B-C e0 local-group separator diagnostic`;
- run: `34193133033`;
- job: `101955119716`;
- result: `PASS V26_Q138_BC_E0_LOCAL_GROUP_SEPARATOR`.

All ranks below are exact over `GF(2)`.

## Local factor model

For each grouped-e0 support group `g`, the probe constructs the exact local linear map from the same 149 shared input bits to that group's:

1. support-syndrome deltas;
2. per-sector left-frequency deltas.

Let `R_g` be the row space of this local map. For a set of groups `S`, define

`r(S) = dim span(R_g : g in S)`.

The complete family has `r(all)=149` for B and C.

For a split `S | Sbar`, define

`lambda(S) = r(S) + r(Sbar) - r(all)`.

Because

`dim(U intersect W) = dim(U) + dim(W) - dim(U + W)`,

`lambda(S)` is exactly the dimension of linear information seen by both sides of the split.

For arbitrary factor functions that depend only on the displayed local linear projections, a change of basis can separate left-only, shared, and right-only coordinates. Hence the two sides need communicate only the `lambda(S)` shared binary coordinates. This is the exact linear-separator quantity relevant to contraction of the PR110/PR111 signature family.

This theorem does **not** yet include the omitted quadratic scalar phase. That phase must be incorporated separately before claiming an exact grouped-e0 carry contraction.

## B result

- raw e0 sectors: `581`;
- support groups: `251`;
- global support rank: `149`;
- global frequency rank: `149`;
- global combined rank: `149`.

Local combined ranks are only `20..28`:

`{20:4, 21:104, 22:35, 23:18, 24:8, 25:67, 26:14, 28:1}`.

The largest exact pairwise row-space intersection is:

`24` dimensions.

A deterministic multiplicity/local-rank balanced split gives:

- left groups: `125`;
- right groups: `126`;
- left rank: `61`;
- right rank: `149`;
- exact separator: `lambda = 61`.

The best verified deterministic path order in this probe is local-rank ascending / multiplicity-then-rank:

`max lambda = 85`.

For comparison:

- canonical order: `124`;
- local-rank descending: `96`.

Thus the displayed linear signature family already has a certified path-contraction upper bound of `2^85` shared states, rather than a monolithic `2^149` state.

That is a mathematical separator gain of `64` binary dimensions for this linear family. It is still much too large to call practical enumeration.

## C result

- raw e0 sectors: `577`;
- support groups: `250`;
- global support rank: `149`;
- global frequency rank: `147`;
- global combined rank: `149`.

Local combined ranks are only `19..27`:

`{19:4, 20:14, 21:87, 22:16, 23:36, 24:10, 25:71, 26:11, 27:1}`.

The largest exact pairwise row-space intersection is:

`24` dimensions.

A deterministic multiplicity/local-rank balanced split gives:

- left groups: `125`;
- right groups: `125`;
- left rank: `57`;
- right rank: `149`;
- exact separator: `lambda = 57`.

The best verified deterministic path order in this probe is local-rank descending:

`max lambda = 89`.

For comparison:

- canonical order: `114`;
- local-rank ascending: `92`;
- multiplicity-then-rank: `92`.

Thus the displayed C linear signature family has a certified path-contraction upper bound of `2^89` shared states instead of the monolithic `2^149` state.

This is a `60`-dimension separator gain for the linear family, again not yet a practical enumeration result.

## Why the balanced cut matters

PR111 showed that support alone globally remembers all 149 shared input bits. That could have suggested that all large subsets of factors must remain globally entangled.

The new result disproves that inference.

For B, 125 groups together see only a 61-dimensional linear subspace while the complementary 126 groups already span all 149 dimensions. For C, the analogous half sees only 57 dimensions.

So global injectivity is produced by a highly nonuniform accumulation of local information. The state is not linearly quotientable as one block, but it **is separator-structured as a factor family**.

Renaming a 149-bit state was not compression. Splitting the factor family across a 57/61-dimensional exact shared subspace actually is.

## Decision

The local-linear separator route survives strongly:

`PASS_LOCAL_LINEAR_SEPARATOR_STRUCTURE_DETECTED`.

The next canonical task is to replace the path-only upper bound by a complete recursive contraction-tree certificate. The tree must record every internal group cluster and verify

`lambda(cluster) = r(cluster) + r(complement) - 149`

at every message edge.

Useful targets from the present result are:

- B: beat the path bound `85`, with the `61` balanced split as the first root candidate;
- C: beat the path bound `89`, with the `57` balanced split as the first root candidate.

Only after a recursive linear tree is frozen should the omitted quadratic scalar phase be lifted onto the same decomposition. If the scalar phase destroys the low separator, the linear result remains correct but insufficient for grouped-e0 carry.

## Claim discipline

Not included:

- optimal branchwidth/minimum separator proof;
- quadratic scalar phase;
- grouped-e0 own carry rank;
- e0-half cross-carry;
- support-only lift carry;
- complete `B2/C2`;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work reduction;
- `alpha < 1`;
- ranking/search gain;
- full-round security claim.

The fixed-seed random balanced cuts in the probe are route diagnostics only. Their sampled minimum is not used as an optimality claim.

`ALPHA_PASS=0` remains unchanged.
