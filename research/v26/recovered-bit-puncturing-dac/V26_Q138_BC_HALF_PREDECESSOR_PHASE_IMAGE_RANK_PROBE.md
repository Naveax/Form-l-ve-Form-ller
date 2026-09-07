# V26 Q1.38 B/C half predecessor phase-image rank probe

## Scope

The exact half-sector right21 witness calculation gives GF(2) ranks 128 for B and 136 for C at one explicit max-overlap predecessor per position. A separate sample probe tests several half-active predecessors. This rank-only probe asks a more structural question: how many predecessor degrees of freedom actually reach the exact half correction data?

For the common four half-sector support, solve the affine predecessor condition exactly. On its nullspace, build one joint linear feature map containing:

- the predecessor-induced shift of the common support right-hand-side syndrome;
- the predecessor-induced left-frequency shift for each of the four corrected quadratic phases;
- the predecessor-induced right-scalar linear term for each of the four corrected quadratic phases.

The probe reports the GF(2) rank of this joint map and the dimension of its kernel.

The remaining predecessor dependence can still enter through the quadratic predecessor constants of the four phases. Therefore, on the kernel of the joint linear feature map, the probe also measures each phase polar form against the full half-active predecessor nullspace and records the four-bit phase derivative patterns at an affine particular solution.

## Interpretation

If the joint linear feature rank is small and the quadratic action on its kernel is trivial, then the exact predecessor dependence factors through a small finite signature space. That would justify a complete exact predecessor-signature enumeration rather than sampling.

If the kernel has nontrivial quadratic action, then a simple linear-signature quotient is insufficient; the printed cross ranks identify the remaining obstruction.

This is a structural diagnostic only. It does not replace the admitted uniform B/C second-lift bounds and makes no complete-leaf, representation, arithmetic-work, alpha, ranking/search, or full-round claim.
