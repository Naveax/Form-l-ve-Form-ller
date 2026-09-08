# V26 Q1.38 B/C grouped-e0 shared-state rank diagnostic

## Motivation

PR109 proves that the half-only inherited third carry remains subgeneric in the exact canonical PR104 grouped-e0 gauge: B <=1312 and C <=1834. The missing pieces for a complete third-bit lift still include grouped-e0's own carry and e0-half cross-carry.

A direct per-support-group relaxation would destroy the shared predecessor/right coupling and can spuriously inflate the state space. This diagnostic therefore asks a narrower question first: how many independent linear state bits are jointly visible to every grouped-e0 support syndrome and every sector left-frequency map at once?

## Diagnostic

For each reachable grouped-e0 support group, the probe packs:

- the support-syndrome delta induced by predecessor and right-beta changes;
- the left-frequency deltas for every sector in that support group.

It concatenates those signatures across all groups into one GF(2) linear map driven by the same 128 predecessor bits and 21 right-beta coordinates. The resulting joint rank is the exact dimension of this shared linear signature map.

The probe also records predecessor-only rank, right-only rank, cumulative rank checkpoints, support-group multiplicities, and support-syndrome widths. Existing exact counts are asserted: B has 581 raw e0 sectors in 251 support groups; C has 577 in 250 groups.

## Interpretation

If the joint rank is small, complete shared-state enumeration may be practical and can feed an exact grouped-e0 carry probe without relaxing support groups independently. If it is close to the ambient 149 input bits, direct enumeration is the wrong route and the next step should use quotient/degree factorization instead.

Scalar phase bits and all quadratic carry evaluation are deliberately excluded here. This is a rank-only route-selection diagnostic, not a B2/C2 theorem.

## Claim discipline

Not included: grouped-e0 carry rank, e0-half cross-carry, support-only lift carry, complete B2/C2, complete leaf Schmidt rank, W_repr, alpha, arithmetic-work, ranking/search, or full-round claims.
