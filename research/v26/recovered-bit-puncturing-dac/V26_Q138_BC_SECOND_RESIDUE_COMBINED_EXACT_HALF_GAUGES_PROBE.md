# V26 Q1.38 B/C combined exact-half gauge probe

## Scope

This probe combines the two strongest fixed-predecessor second-residue diagnostics now available:

- the specialized e0 correction space, with both the original specialized binary basis and the exact support/cross joint-enumeration binary basis;
- the exact half-sector correction span obtained by traversing all `2^21` right-beta assignments with the four right-only scalar signs kept exact.

The two e0 constructions have the same GF(2) dimension and are asserted to span the same fixed-predecessor GF(2) e0 correction space. They nevertheless define different 0/1 integer-lift bases, and the exact rational Walsh quotient is basis-gauge sensitive. Therefore this probe evaluates both e0 gauges and both component insertion orders against the exact half basis.

For each explicit max-overlap predecessor witness it evaluates:

1. `oldE -> exactH`;
2. `exactH -> oldE`;
3. `jointE -> exactH`;
4. `exactH -> jointE`.

Each candidate is a valid binary lift of the same fixed-predecessor residual family. The support-only `U120` space remains the existing global exact lift.

## Claim discipline

The minimum exact ZZ quotient over these four certified gauges gives an upper bound only at the explicit predecessor witness. It is **not** a uniform B/C second-lift theorem and does not replace canonical `B<=812`, `C<=972` unless a separate uniform predecessor argument is proved.

No complete-leaf Schmidt-rank, representation, arithmetic-work, alpha, ranking/search, or full-round claim follows.
