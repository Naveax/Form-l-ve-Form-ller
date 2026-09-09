# V26 q138 C916 e0 Gauss radical augmented separator

## Purpose

Continue the exact first-dyadic grouped-e0 carry program after the radical-control certificate.

For each of the 250 same-support C groups, lift the exact radical-sensitive Gauss support controls from the support-parameter quotient to the canonical 149 shared predecessor/right coordinates, prove that the lift ambiguity is already represented by the existing support state, then augment the established grouped-e0 support/frequency separator and remeasure its exact linear separator geometry.

## Gauge theorem

A radical control is initially a linear functional on the projected common-support tangent space. Any two 149-bit ambient representatives differ by a functional annihilating that projected tangent space.

For every one of the 250 support groups, the exact annihilator basis is contained in the group's pre-existing shared support basis. Therefore changing the ambient representative adds only rows already present in the canonical grouped-e0 state.

Consequently the extra rank obtained by adjoining radical-support controls to each group's existing `combined_basis` is gauge-independent.

The verifier also requires the lifted rows and the existing separator to use exactly the same canonical 149-coordinate order.

## Local augmentation

The per-group radical-control rank histogram is

`{1:29, 2:46, 3:68, 4:20, 5:48, 6:39}`.

After quotient-aware lifting and union with the existing support/frequency basis, the exact extra-rank histogram is

`{0:103, 1:3, 2:8, 3:36, 4:14, 5:47, 6:39}`.

Thus:

- 103 support groups need no additional linear state at all;
- maximum additional rank is 6;
- the refined local-rank histogram is
  `{12:3, 13:6, 14:8, 15:24, 16:25, 17:38, 18:40, 19:7, 20:14, 21:85}`.

The global union rank remains exactly 149.

This is consistent with the fact that the radical-support controls refine how the already-full shared domain is partitioned locally rather than creating new global shared coordinates.

## Recursive separator result

The unaugmented support/frequency target, under the deterministic multiplicity-then-rank tree constructed by the same oracle, has width 58 and depth 11.

After radical-support augmentation, exact recursive candidate widths are:

- `base_multiplicity_then_rank`: 67;
- `multiplicity_then_refined`: **61**;
- `radical_rank_ascending`: 65;
- `refined_rank_ascending`: 70;
- `refined_rank_descending`: 82.

The best displayed tree is therefore `multiplicity_then_refined` with

\[
\boxed{W_{\mathrm{rad-support}}=61}
\]

and depth 11.

Its two root children have equal separator coupling 40:

- size 166: rank 64, complement rank 125;
- size 84: rank 125, complement rank 64.

The best sampled balanced half cut is `radical_rank_ascending_half` with 125 groups on each side and coupling 52.

Decision:

`GAUSS_RADICAL_SUPPORT_AUGMENTED_SEPARATOR_WIDTH61`.

## Interpretation

The radical-sensitive zero/nonzero condition of the local Gauss transform can be integrated into the pre-existing grouped-e0 support/frequency state with a displayed recursive width only three bits above that target's width-58 baseline.

This is substantially smaller than carrying the raw 145-rank shared-to-local frequency-control family as an independent state. The distinction matters: local fiber elimination converts most of that raw frequency dependence into a Gauss problem whose support obstruction is controlled only by the local radicals.

However, width 61 is not a complete first-dyadic carry width. When the local Gauss sum is nonzero, its normalized sign/phase on the surviving shared support quotient and its power-of-two magnitude still have to be charged together with exact signed integer arithmetic.

The next exact task must treat that nonzero Gauss phase on the support quotient itself. A naive ambient 149-bit quadratic lift is not automatically gauge-invariant, because quadratic functions vanishing on an affine support are a larger object than the linear annihilator already absorbed above. The next probe should therefore work modulo the support ideal or use an exact support-conditioned evaluation-state/Gauss representation.

## Scope exclusions

No nonzero Gauss phase/amplitude theorem, no complete grouped-e0 first-dyadic carry theorem, no support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search, or full-round result is claimed.

`ALPHA_PASS=0`.
