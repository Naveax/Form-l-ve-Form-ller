# V26 q138 Central Critical-Boundary GF(2) No-Constraint Falsifier

## Statement

The HT88 tree has three maximizing clusters but only two distinct 11|21 bipartitions; one maximizing cluster pair are complements.

On both unique critical bipartitions, the linear support equations coming from

- all four modular-addition sigma recurrences;
- exact XOR mask propagation;
- exact ChaCha rotation wiring;
- the fixed q138 output mask (affine constants ignored only because they do not change projected dimension)

impose **zero** pure GF(2) parity constraints on the 44 physical central input-mask bits on the smaller side.

Thus the projected linear boundary codimension is

`0,0`.

## Method

Write all sigma recurrence and XOR/rotation equations as an affine GF(2) system. For a critical 44-bit physical boundary `X` and all remaining variables `Y`, the codimension of the projected feasible subspace on `X` is

`rank([A_X A_Y]) - rank(A_Y)`.

Exact bit-matrix Gaussian elimination gives zero on both unique critical bipartitions.

## Consequence

There is no free linear-parity reduction of the central generic exponent44 on the HT88 bottlenecks.

This is consistent with the refined terminal-cut result44 and narrows the remaining exact mechanisms to

- nonlinear sigma-support restrictions;
- signed coefficient cancellation;
- actual coefficient Schmidt deficiency;
- joint central/leaf algebra.

The test deliberately does not encode the conditional nonlinear rule `sigma_i=0 => u_i=v_i=w_i`, so it is not a complete support-rank theorem.

## Verification

Authority:

`scripts/verify_v26_q138_central_boundary_gf2_constraints.py`.

Clean GitHub Actions run `32011914166` passes.

## Scope

Linear-support falsifier only; no tensor-rank lower bound, arithmetic-work lower bound, or attack claim.
