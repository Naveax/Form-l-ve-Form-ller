# V26 Q1.38 B/C second-residue joint-image rank probe

## Scope

This is a rank-only planning diagnostic for the explicit max-overlap predecessor witnesses used by the fixed-predecessor specialization probe.

The previous specialization still span-relaxes the support-syndrome image and phase cross-frequency image independently even though both are driven by the same 21 right-beta bits. This probe measures the exact rank of their common linear image before any expensive state enumeration is attempted.

For each reachable e0 support group it records

- support-syndrome rank `s`,
- assembled phase cross-frequency rank `c`,
- exact joint rank `j` of `right21 -> syndrome x frequency`,
- Cartesian excess `s+c-j`.

For the four half sectors it measures the common image of the support syndrome together with all four phase cross-frequency families.

A strict positive Cartesian excess certifies that the earlier independent span construction contains unreachable support/frequency combinations. A small joint rank can justify exact joint-image enumeration. A joint rank near 21 is a warning against naive per-group `2^j` enumeration.

This probe makes no second-lift rank, uniform predecessor, representation, arithmetic-work, alpha, or full-round claim.
