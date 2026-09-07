# V26 Q1.38 B uniform second-residue binary-basis gauge probe

## Scope

The admitted uniform B second-residue certificate is

`668 + 144 = 812`,

where 668 is the support-only Walsh space and 144 is the exact rational rank of the projected Walsh images of one chosen 0/1 GF(2) basis for the 348-dimensional sign-dependent residual span.

Recent fixed-predecessor diagnostics show that the exact rational quotient is **binary-basis gauge dependent** even when the GF(2) correction space and its dimension are unchanged. Therefore the canonical 144 quotient need not be minimal over all valid binary bases of the already-admitted uniform sign span.

This probe searches only for a better certificate; it does not alter the residual space.

It constructs several deterministic bases of the same admitted 348-dimensional uniform B GF(2) span by changing component insertion order, vector order, weight/pivot ordering, and deterministic shuffles. For each basis it computes projected Walsh rank modulo two large primes. Modular rank is a lower bound on the exact rational rank, so any candidate whose modular rank is already at least144 cannot improve the admitted certificate.

Only a candidate with modular lower bound below144 is sent to an exact `ZZ` rank computation. If exact quotient rank `r<144` is found, then the same already-admitted support lift gives a valid improved **uniform** bound

`B_second <= 668 + r`.

## Claim discipline

The search is heuristic and not an optimality theorem. Failure to find a better gauge does not prove144 minimal. A printed exact improvement, however, is a valid alternative binary-lift certificate because every tested basis spans exactly the already-admitted uniform GF(2) residual space.

No complete-leaf Schmidt-rank, representation, arithmetic-work, alpha, search/ranking, or full-round claim follows by itself.
