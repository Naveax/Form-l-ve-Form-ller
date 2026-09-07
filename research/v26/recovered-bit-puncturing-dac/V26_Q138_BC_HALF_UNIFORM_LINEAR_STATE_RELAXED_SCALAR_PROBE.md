# V26 Q1.38 B/C uniform half linear-state relaxed-scalar probe

## Goal

The clean fixed-predecessor exact-right21 half probe gives exact half correction ranks 128 for B and 136 for C. Clean predecessor sampling later reproduces exactly the same ranks on four deterministic half-active predecessors per position, but sampling is not a uniform theorem.

This probe constructs a genuinely uniform upper span without enumerating the 123-dimensional half-active predecessor affine space.

## Exact state reduction

For the four common-support half sectors, changing the predecessor changes only:

- the common affine-support right-hand-side syndrome;
- the four left phase frequencies;
- the four scalar phase bits.

The left quadratic phase cores, the 21 right-beta cross-frequency maps, and the right quadratic polar data are predecessor independent.

Restrict the predecessor to the exact projected half-support affine space. Combine its free null directions with the 21 right-beta coordinates. The support syndrome and four left phase frequencies are linear functions of these combined variables. The script builds this exact linear image and computes its GF(2) rank.

For each exact linear image state, the true four scalar phase bits are some subset of the 16 possible patterns, determined by four quadratic Boolean functions. Instead of solving those quadratic feasibility conditions, the probe deliberately allows **all 16 scalar patterns**. This is a safe relaxation: every true predecessor/right-beta state is retained, possibly with additional impossible scalar states.

Each relaxed state determines an exact 2048-bit left correction vector through the already-validated degree-two half correction

`f = 1 xor q1 xor q2 xor q3 xor q4 xor sum_{i<j} qi qj`.

The GF(2) span of all such vectors is therefore a uniform upper span for the exact half correction over every predecessor. Predecessors outside the projected half-support affine space contribute no half sector and are covered by zero.

## Consequence if enumeration is feasible

The relaxed uniform half span is verified to lie inside the previously admitted uniform half span. It is then combined with the unchanged admitted uniform grouped-e0 span and the unchanged support-only Walsh space. The projected Walsh quotient is computed exactly over `ZZ`.

Thus any printed total

`support_only + exact_ZZ_quotient`

is a valid improved **uniform** B/C second-lift upper bound.

The scalar relaxation means the result need not be optimal. Failure to improve does not prove the existing 812/972 bounds minimal.

## Enumeration cap

The script enumerates the exact combined linear image only when its rank is at most 20. If the rank exceeds that cap it prints `SKIP`; this is only a computational planning result, not a mathematical obstruction. A later version may exploit the quadratic scalar structure or quotient the image further.

## Claim discipline

A successful lower total is a uniform binary-lift certificate for the second residue only. It does not by itself change the complete leaf rank, `W_repr(1)`, arithmetic work, ranking/search cost, alpha, or full-round relevance.
