# V26 Q1.38 B/C half predecessor-signature rank probe

## Scope

The exact right21 half-sector probe gave much smaller fixed-predecessor second-bit correction spans, but only at explicit max-overlap predecessor witnesses. Before attempting any uniformization, this probe measures how many predecessor degrees of freedom actually affect the exact half construction.

For the common half-sector affine support, project onto predecessor128 and restrict all predecessor dependence to that reachable affine space. Measure the GF(2) rank of the predecessor variation seen by:

- support right-hand-side syndromes;
- the four left phase-frequency maps;
- the four right linear-phase maps.

The four predecessor-only sector phase constants are quadratic Boolean functions. Independently of their internal quadratic rank, together they add at most four output bits. Therefore `full_linear_signature_rank + 4` is a safe log2 state-count envelope for a complete predecessor signature that retains every quantity used by the exact half right21 construction.

The script also prints the restricted polar rank of each of the four predecessor-only quadratic phase constants. This is diagnostic information for deciding whether a later exact finite-state enumeration can quotient the quadratic kernel further.

## Claim discipline

This probe proves no new uniform rank bound. Its only purpose is to decide whether exact predecessor-signature enumeration is tractable and structurally justified. A small signature rank would support a complete uniform half analysis; a large rank would rule out naive enumeration and redirect the route toward affine-equivalence or transfer arguments.
