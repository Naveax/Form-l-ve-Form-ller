# V26 Q1.38 B/C uniform half fiber-quadratic span probe

## Purpose

The fixed-predecessor exact-right21 half correction has rank128 for B and136 for C, and four deterministic predecessor samples reproduce those ranks. The predecessor-signature diagnostic nevertheless shows that naive complete predecessor enumeration is impossible: full predecessor linear signature ranks are38/36 and the four predecessor-only scalar quadratic forms have restricted polar rank112.

This probe avoids both exponential obstacles.

## Key observation

For the four common-support half sectors, after fixing a support-syndrome fiber, the only non-scalar predecessor/right-beta dependence entering the 2048-bit left correction is through four left phase frequencies. Those frequencies are linear functions of the combined predecessor-null and right-beta variables.

The half correction

`f = 1 xor q1 xor q2 xor q3 xor q4 xor sum_{i<j} qi qj`

has degree two in the four sector sign bits. Consequently, on any fixed support-syndrome fiber and fixed four-bit scalar pattern, the resulting 2048-bit left correction is a **degree-at-most-two Boolean polynomial** in coordinates of the fiber's linear state space.

A degree-two vector-valued Boolean polynomial is completely spanned by its coefficient vectors:

- the value at zero;
- every first difference along one basis direction;
- every second mixed difference along a pair of basis directions.

Therefore a fiber of dimension `r` requires only

`1 + r + binom(r,2)`

vector evaluations, not `2^r` evaluations.

## Uniformity and safe scalar relaxation

The probe constructs the exact combined linear image of:

- half-active predecessor null directions;
- the21 right-beta directions;
- common support syndrome;
- four left phase frequencies.

It then splits that image into exact support-syndrome fibers. For each nonzero left-support fiber, it allows **all16 scalar phase patterns**. The true four quadratic scalar phases realize only a subset, so this is a safe overapproximation. Every exact half correction for every predecessor is included.

For each relaxed scalar pattern the probe inserts the degree-two coefficient vectors into a GF(2) basis. Deterministic random fiber values are checked to lie in the reconstructed coefficient span. The final uniform half basis is also required to lie inside the previously admitted uniform half basis.

## Second-lift consequence

The new uniform half upper span is combined with the unchanged admitted grouped-e0 uniform span and the unchanged support-only Walsh space. The projected Walsh quotient is then computed exactly over `ZZ`.

Any printed total

`support_only + exact_ZZ_quotient`

is therefore a valid uniform B/C second-residue lift bound. It can replace812/972 if smaller.

The all16 scalar relaxation is intentionally non-optimal. Failure to improve does not prove the existing bounds minimal; success is a valid uniform certificate.

## Cross-check relation to the linear-state enumerator

The separate linear-state relaxed-scalar probe enumerates every state when the combined linear rank is at most20. When both probes execute, they implement the same scalar-relaxed state set by two different algorithms, so their final half-span and second-lift totals should agree. This provides a useful independent cross-check.

No complete-leaf, representation, arithmetic-work, alpha, ranking/search, or full-round claim follows by itself.
