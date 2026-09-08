# V26 q138 C916 aggregate scalar Gauss classes

## Result

For the 250 same-support grouped-e0 factors at position C, classify the exact right-only aggregate quadratic scalar over the full 149-bit predecessor/right shared domain.

The classifier uses polynomial-time hyperbolic-pair elimination for Boolean quadratics and is regression-checked against brute-force evaluation for every Boolean quadratic on `n=1..4`, totaling `2196` forms.

Exact result:

- aggregate scalar groups: `250`;
- Gauss sum zero: `248`;
- Gauss sum nonzero: `2`;
- both nonzero groups have multiplicity `1`;
- one has signed magnitude `+2^78`;
- one has signed magnitude `-2^79`.

Polar-rank histogram:

`{2:8, 4:53, 6:71, 8:11, 10:3, 12:1, 136:6, 138:50, 140:41, 142:6}`.

The `248` zero cases are exact radical-linear obstructions after hyperbolic elimination. No `2^149` enumeration is used.

## Interpretation

This is a useful nonlinear primitive, not a separator-state or complete carry theorem. In particular, the fact that an individual global scalar Gauss sum is zero does **not** mean that the scalar can be discarded inside support-conditioned or cut-conditioned grouped-e0 contractions. Conditioning changes the relevant affine domain and can remove a global cancellation.

The important operational consequence is that cut-restricted Gauss sums and evaluation images can now be computed algebraically rather than by shared-state enumeration.

## Next use

Combine this primitive with the quadratic function-space separator certificate. For the worst separator cuts, restrict the relevant quadratic residual family to the affine fiber fixed by the ordinary linear separator coordinates, then compute exact/bounded evaluation-image sizes or character sums.

## Scope exclusions

No cut-restricted Gauss sums, aggregate grouped-e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, or full-round claim.

`ALPHA_PASS=0`.
