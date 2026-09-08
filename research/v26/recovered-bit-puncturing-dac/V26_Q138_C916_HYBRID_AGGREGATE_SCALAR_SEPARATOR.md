# V26 q=138 C916 hybrid aggregate-scalar separator

## Status

Exact diagnostic of the multiplicity/polar-rank split in the C same-support aggregate scalar family, together with a hybrid linear separator skeleton.

This is not a complete separator or carry theorem because the high-rank singleton quadratic labels are deliberately left nonlinear.

## Exact split

The 250 C grouped-e0 factors divide exactly as follows.

### Singleton groups

There are `103` multiplicity-1 groups. Their aggregate scalar polar ranks are all high:

- rank 136: `6` groups;
- rank 138: `50` groups;
- rank 140: `41` groups;
- rank 142: `6` groups.

### Multi-sector groups

There are `147` multiplicity-2/4 groups. Their same-support XOR-aggregate scalar polar ranks are all low:

- rank 2: `8` groups;
- rank 4: `53` groups;
- rank 6: `71` groups;
- rank 8: `11` groups;
- rank 10: `3` groups;
- rank 12: `1` group.

Thus the observed high/low split is exactly the singleton/multi-sector split, not an approximate correlation.

## Hybrid linear skeleton

The probe keeps the 103 singleton groups on their original aggregate support/frequency signatures and does **not** linearly refine their high-rank quadratic scalars. For the 147 multi-sector groups it applies the exact aggregate-scalar refinement certified by PR #124.

The resulting linear route still has global rank 149. Exact displayed separator results are:

- original unrefined aggregate recursive width: `58`;
- hybrid best recursive width: **`83`**;
- best order: `multiplicity_then_hybrid`;
- depth: `11`;
- best balanced cut: `lambda=61`, ranks `61 | 149` across `125/125` groups;
- root children: `lambda=45/45`, sizes `166/84`, ranks `71/123`.

For comparison, linearly refining all 250 aggregate scalars gives width `147`. Therefore retaining singleton scalars nonlinearly preserves a substantial part of the useful separator geometry:

`58 -> 83` rather than `58 -> 147`.

The width `83` is **not** a complete interface cost because it excludes representation/evaluation of the 103 nonlinear singleton scalar labels.

## Singleton quadratic-family dimension

The singleton high-rank quadratic forms do not collapse to a tiny shared global family:

- singleton polar-form span rank: `94`;
- singleton polar affine-difference rank: `93`;
- singleton full quadratic-polynomial span rank: **`100`**;
- singleton full quadratic-polynomial affine-difference rank: `99`.

With 103 singleton groups, a global basis therefore removes only three full-polynomial dimensions. The naive strategy of replacing 103 singleton scalar bits by a very small common quadratic basis is not available.

For reference, the 147 multi-sector forms have polar span rank `88` and full quadratic-polynomial span rank `102`.

## Decision

The surviving nonlinear route is cut-local rather than global. The next useful diagnostic should combine each group's aggregate linear signature coordinates and its aggregate scalar quadratic polynomial in one GF(2) function space and measure exact cut intersections

`lambda_F(S) = dim(F_S) + dim(F_Sbar) - dim(F_all)`

on deterministic/recursive trees.

This does not by itself prove an exact contraction-state count, because nonlinear evaluation compatibility can impose additional structure. It does, however, measure how much quadratic scalar information is genuinely shared across a factor cut without forcing every scalar to become a linear function of the original 149 state bits.

## Authority

Exploratory clean run: `34225140693`, job `102057301987`.

## Scope

Not included:

- exact nonlinear singleton contraction cost;
- all-group aggregate e0 carry;
- support/e1 carry;
- half/e0 cross carry;
- complete `C2`;
- complete leaf theorem;
- `W_repr`;
- arithmetic-work factor;
- alpha/ranking/search/full-round claim.

`ALPHA_PASS=0`.
