# V26 Q1.38 C uniform second-residue basis-gauge fast probe

## Scope

This is a byte-semantics-preserving acceleration of the deterministic C uniform binary-basis gauge search. The admitted support-only space remains 788 and the admitted exact Walsh-complement quotient rank remains 184.

For each deterministic 432-dimensional GF(2) basis gauge, the previous probe forms the 0/1 integer lift, computes its Walsh rows outside the 788-dimensional support space, and asks whether the exact rational quotient can fall below 184.

The expensive part is repeatedly ranking the complete dense projected matrix. This fast version first selects several deterministic sets of exactly184 Walsh-complement coordinates. If any resulting 432x184 matrix has rank184 over `F_65521`, then the complete matrix has modular rank at least184, hence rational rank at least184, so that gauge cannot improve the admitted quotient. This is a rigorous minor certificate.

If none of the deterministic minors reaches184, the script falls back to the complete modular matrix. Only a complete modular rank below184 is eligible for exact `ZZ` rank.

Thus no mathematical conclusion is drawn from a failed projection minor; it is only a cheap positive certificate when full rank184 is observed.

## Claim discipline

Any exact quotient rank `r<184` printed by the probe yields a valid alternative uniform C second-lift upper bound `788+r`. Failure to find such a gauge is scoped only to the deterministic basis family tested and is not an optimality theorem.

No third-residue, complete-leaf, representation, arithmetic-work, alpha, ranking/search, or full-round claim follows.
