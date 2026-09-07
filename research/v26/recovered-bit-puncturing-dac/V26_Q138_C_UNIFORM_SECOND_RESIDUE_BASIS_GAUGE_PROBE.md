# V26 Q1.38 C uniform second-residue binary-basis gauge probe

## Scope

The admitted uniform C second-residue certificate is `788 + 184 = 972`, where 788 is the support-only Walsh space and 184 is the exact rational rank of the projected Walsh images of one chosen 0/1 GF(2) basis for the 432-dimensional sign-dependent residual span.

Fixed-predecessor diagnostics show that this rational quotient can depend on the chosen binary basis gauge even when the GF(2) correction space is unchanged. This probe therefore searches only for a better certificate inside the already-admitted uniform C sign span.

It constructs deterministic alternative GF(2) bases by changing component insertion order, vector weight/pivot ordering, reversal, and seeded shuffles. Every candidate is screened modulo two large primes. A modular rank is a lower bound on the exact rational rank, so candidates with lower bound at least184 cannot improve the admitted certificate.

Every candidate with modular lower bound below184 is checked by exact `ZZ` rank. If any exact quotient `r<184` is found, the unchanged support lift gives the valid improved uniform bound `C_second <= 788 + r`.

Failure to find a better basis is heuristic only and does not prove184 minimal. No complete-leaf Schmidt-rank, representation, arithmetic-work, alpha, ranking/search, or full-round claim follows by itself.
