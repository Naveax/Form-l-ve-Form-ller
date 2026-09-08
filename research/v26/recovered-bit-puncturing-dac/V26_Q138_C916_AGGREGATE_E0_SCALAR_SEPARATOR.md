# V26 q=138 C916 aggregate grouped-e0 scalar separator

## Status

Exact route-selection certificate for the right-only scalar omitted by the C grouped-e0 aggregate support/frequency separator.

The test is deliberately weaker than the historical sectorwise scalar refinement: sectors sharing one support are XOR-aggregated first, and only the resulting single aggregate scalar is required to be constant on refined local signature fibers.

## Construction

For each of the 250 C grouped-e0 support groups, start from the exact same-support aggregate linear signature used by the earlier separator theorem. Its shared-state inputs are the 149 predecessor/right coordinates and its linear observables encode affine support selection plus aggregate left frequency.

The full corrected phase of every constituent sector splits into:

- a left-only truth component;
- left/right cross-frequency terms;
- a right-only quadratic scalar.

XORing all sectors in one support group produces one aggregate right-only quadratic scalar `q_g(r)`.

For a hidden direction `h` in the kernel of the existing group signature, `q_g(x+h)=q_g(x)` for every shared state `x` iff:

1. `h` lies in the radical of the aggregate scalar polar form; and
2. the constant derivative `q_g(h)+q_g(0)` vanishes.

Intersecting these exact conditions gives the largest hidden subgroup preserving both the aggregate linear signature and aggregate scalar. Its annihilator is therefore the minimal linear refinement that makes that aggregate scalar constant on every refined signature fiber.

## Exact C result

The clean exploratory run gives:

- raw e0 sectors: `577`;
- support groups: `250`;
- global refined rank: `149`;
- no group requires zero extra rank;
- no individual group reaches rank 149;
- refined local ranks: `13..146`;
- maximum extra local rank: `127`;
- aggregate-scalar linear cut is needed in `220/250` groups.

Aggregate scalar polar ranks are sharply bimodal:

`{2:8, 4:53, 6:71, 8:11, 10:3, 12:1, 136:6, 138:50, 140:41, 142:6}`.

The refined local-rank histogram is:

`{13:18, 14:74, 15:46, 16:5, 17:4, 145:36, 146:67}`.

So many groups remain genuinely small after same-support cancellation, but a substantial family retains nearly full quadratic scalar dependence.

## Separator consequence

The unrefined same-support aggregate model had a displayed C recursive width `58`, with root-child separator dimensions `33/33`.

After the exact aggregate-scalar linear refinement:

- best deterministic balanced cut: `lambda=147`;
- path widths: `149 / 149 / 147 / 147` for the displayed orderings;
- every tested recursive ordering has width **`147`**;
- best recursive tree depth: `10`;
- best root children have `lambda=122` on both sides, with ranks `148|123` and `123|148`.

Thus same-support aggregation improves the historical sectorwise linear-refinement obstruction from width 149 to 147, but does not preserve the useful width-58 contraction geometry.

Verdict:

`AGGREGATE_SCALAR_LINEAR_REFINEMENT_NEAR_MONOLITHIC`.

## Interpretation

This closes only the strategy of forcing the aggregate quadratic scalar through an ordinary **linear signature refinement** before contraction. The failure does not prove that the scalar itself requires `2^147` work. A nonlinear contraction can carry the scalar polynomial directly rather than first making it constant on linear fibers.

That distinction is now important: the local aggregate scalar polar ranks show a mixed structure, with 147 groups at polar rank at most 12 and 103 groups at polar rank at least 136. A future route should exploit this heterogeneity or carry quadratic-form data directly through the factor tree, not flatten every scalar into additional linear coordinates.

This result also does not alter the current C916 second-lift authority, the half-induced third-carry span `636`, or the grouped-e0 own-carry span `1164`.

## Scope

Not included:

- nonlinear/quadratic scalar message contraction;
- exact all-group grouped-e0 aggregate carry;
- support/e1 carry or support-e0 cross carry;
- half cross carry;
- complete `C2`;
- `W_repr` / arithmetic-work;
- alpha/ranking/search/full-round claim.

Exploratory clean run: `34222984702`, job `102050248997`.

`ALPHA_PASS=0`.
