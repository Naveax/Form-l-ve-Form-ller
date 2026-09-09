# V26 q138 C916 e0 first-dyadic Gauss radical control

## Scope

For each of the 577 exact C grouped-e0 sector characters, restrict its quadratic polar form to the local fiber of the common-support projection from the 160 external coordinates onto the 149 shared predecessor/right coordinates.

If the local-fiber polar form has radical `R`, then for every `r in R`, the polar derivative `B(r,.)` annihilates the local projection kernel and therefore descends to a linear functional on the shared support projection. These descended functionals are exactly the shared controls that move the Gauss cancellation/support coset after local-fiber elimination.

This certificate measures only those radical-sensitive support controls. It does not yet charge the nonzero Gauss phase/amplitude, signed integer carry arithmetic, or a complete separator state.

## Exact sector geometry

Across all 577 sectors, local-fiber dimensions are

`{7:127, 8:309, 9:141}`.

The restricted local polar-rank histogram is

`{4:209, 6:329, 8:39}`.

Hence the local radical-dimension histogram is

`{0:3, 1:88, 2:172, 3:180, 4:134}`.

The exact shared-projection radical-control-rank histogram is identical:

`{0:3, 1:88, 2:172, 3:180, 4:134}`.

Therefore, sector by sector, the map

`r in radical -> B(r,.) on the shared support projection`

has full rank equal to the radical dimension. Equivalently, the descended control map is injective on every local radical.

Only three sectors have zero radical and therefore need no radical-support control. The maximum sector control rank is 4. The sum of the 577 sector control ranks is 1508, but this sum is not a separator width because controls overlap strongly across sectors and support groups.

## Exact support-group unions

Within each of the 250 same-support groups, union the radical-control rows from all sectors in that group. The exact group-rank histogram is

`{1:29, 2:46, 3:68, 4:20, 5:48, 6:39}`.

Thus every support group requires at most six independent radical-sensitive shared controls.

By support multiplicity:

- multiplicity 1: `{1:26, 2:45, 3:28, 4:4}`;
- multiplicity 2: `{1:3, 2:1, 3:39, 4:12, 5:2}`;
- multiplicity 4: `{3:1, 4:4, 5:46, 6:39}`.

Decision:

`GAUSS_RADICAL_CONTROL_MAX6_PER_SUPPORT_GROUP`.

## Interpretation

The previously measured shared-to-local frequency-control family has global rank 145, so carrying all raw local-frequency shifts is expensive. The Gauss support/cancellation condition is much smaller locally: no individual sector needs more than four descended radical controls, and no same-support group needs more than six after union.

This does not mean the entire first-dyadic carry costs six bits. A nonzero local Gauss sum still has a sign/phase and magnitude determined by the nondegenerate quotient, and the controls must be represented consistently in the 149-bit shared coordinate system before separator widths can be measured.

The next exact step is therefore:

1. choose deterministic 149-bit shared representatives for every descended radical-control functional modulo the support-projection gauge;
2. combine those rows with each group's existing support/frequency `combined_basis`;
3. measure global union rank and recursive cut widths on the same 250 support groups;
4. only then add the remaining Gauss phase/amplitude and signed first-dyadic arithmetic.

## Scope exclusions

No complete grouped-e0 carry separator-width theorem, no Gauss phase/amplitude charge, no support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`.
