# V26 Q1.38 B/C half-sector exact right21 probe

## Scope

This probe attacks the remaining half-sector relaxation at the explicit max-overlap predecessor witnesses.

The four weight122 unique-solution sectors share one affine support and have sign bits `q1..q4`. Their current first dyadic parity lift uses `p=q1 xor q2 xor q3 xor q4`. The resulting second-bit correction is exactly

`f = 1 xor q1 xor q2 xor q3 xor q4 xor (q1q2 xor q1q3 xor q1q4 xor q2q3 xor q2q4 xor q3q4)`,

which is equivalently `f=1` iff the number of negative signs is 0, 3, or 4.

The existing 252/280 uniform half-span theorem and the fixed-predecessor 212/280 specialization span this degree-two Boolean function by treating right-dependent phase pieces independently. The clean joint-image rank probe shows that the four cross-frequency families plus support syndrome are actually driven by the same 21 right-beta bits, with joint ranks 17 for B and 14 for C.

This probe goes further and tracks the **right-only scalar phase bits exactly**, rather than relaxing them independently.

For each position B/C it:

1. fixes the clean max-overlap predecessor witness;
2. keeps the common affine support exactly;
3. decomposes each of the four completed quadratic phases into left phase, left/right cross frequency, and a right-only quadratic scalar function;
4. validates that right-only quadratic model against direct `q_eval` samples;
5. traverses all `2^21` right-beta assignments in Gray-code order;
6. tracks the common support syndrome, four cross frequencies, and four right-only scalar phase bits exactly;
7. evaluates the exact second-bit Boolean correction `f` as a 2048-bit left vector and forms its GF(2) span;
8. asserts that the resulting exact half basis lies inside the previously validated fixed-predecessor half span.

The result is therefore an exact half-sector correction span only for the two explicit predecessor witnesses. It is not a uniform B/C second-lift theorem.

## Claim discipline

A smaller exact half rank is useful evidence for later combined e0+half witness certificates and for designing a uniform predecessor argument. It does not by itself replace the canonical uniform B/C bounds 812/972.

No complete-leaf Schmidt-rank, representation, arithmetic-work, alpha, search/ranking, or full-round claim follows.
