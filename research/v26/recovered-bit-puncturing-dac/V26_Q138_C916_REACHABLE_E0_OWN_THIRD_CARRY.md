# V26 q=138 C916 reachable grouped-e0 own third carry

## Status

Exact realized-family certificate for the **own basis-lift carry** of each individually reachable grouped-e0 correction in the current `C1 <= 916` gauge.

This is not a complete `C2` theorem.

## Authority-compatible setup

For C the probe reconstructs the same reachable-joint grouped-e0 target used by the current second-lift authority:

- raw e0 sectors: `577`;
- support groups: `250`;
- correlated joint-image groups: `111`;
- full-product groups: `139`;
- reachable grouped-e0 GF(2) basis dimension: `388`;
- support-only Walsh dimension: `788`;
- exact ZZ Walsh-complement quotient: `128`;
- admitted second-lift total: `788 + 128 = 916`.

## Exact fiber argument

For one grouped-e0 support group, the shared 149-bit state determines an exact affine image of

`(support syndrome, aggregate left frequency)`.

Condition on a fixed support syndrome. The left support mask is then fixed, while the aggregate left frequency is affine-linear in the remaining fiber coordinates. Therefore the local left truth vector

`support_mask & (qbits xor Walsh[frequency])`

is affine-linear over GF(2) in those fiber coordinates. Its coordinates in the fixed 388-vector reachable basis are also affine-linear.

For basis coordinates `a_i`, the explicit XOR-to-integer-lift carry is

`Q(a) = xor_{i<j} a_i a_j (v_i & v_j)`,

so it is quadratic. Hence the carry restricted to a fixed support-syndrome fiber has algebraic degree at most two. Zero, first differences, and mixed second differences therefore span every realized carry value on that fiber. Deterministic higher-weight probes independently check the degree-two reconstruction.

## Exact result

The clean exploratory run produced:

- maximum joint image rank per group: `15`;
- support-syndrome fibers processed: `2304`;
- scalar-gauge fibers processed: `4608`;
- maximum frequency-fiber dimension: `11`;
- degree-two ANF coefficients inserted: `161336`;
- carry evaluations: `174952`;
- unique local truth vectors / coordinate masks: `61841`;
- exact GF(2) span of all individually realized grouped-e0 own carries: **`1164`**.

There is no saturation at `2048`.

Thus

`C916 reachable grouped-e0 own third-carry span <= 1164 < 2048`.

The current repeated k9 higher-residue target is `650`, so this component by itself does **not** meet the target:

`1164 > 650`.

Verdict:

`SUBGENERIC_BUT_TARGET_NOT_MET`.

## Interpretation

The result is stronger than the coarse ambient pairwise hull `1848`: enforcing the actual per-group reachable support/frequency fibers reduces the own-carry span by `684` dimensions.

However, `1164` must not be added mechanically to the half-only `636` result or to support-only ambient bounds. The carry of a sum of grouped corrections contains bilinear cross terms between their global basis-coordinate functions. Those cross terms are correlated through the same 149-bit shared state.

The next valid route is therefore to compute the **aggregate grouped-e0 carry including cross-group quadratic polar terms**, preserving the shared-state correlations. The previously certified same-support aggregate separator for C has recursive width `58` (best displayed multiplicity-then-rank tree) with root-child separator dimensions `33` and `33`, so that decomposition is the natural contraction skeleton rather than enumerating all `2^149` shared states.

## Scope

Not included:

- carry from summing distinct grouped-e0 corrections;
- support-only/e1 carry;
- support-times-e0 cross carry;
- half/e0 or half/support cross carry;
- complete `C2`;
- complete leaf / `W_repr`;
- arithmetic-work factor;
- alpha/ranking/search/full-round claim.

Exploratory clean run: `34221803951`, job `102046432263`.

`ALPHA_PASS=0`.
