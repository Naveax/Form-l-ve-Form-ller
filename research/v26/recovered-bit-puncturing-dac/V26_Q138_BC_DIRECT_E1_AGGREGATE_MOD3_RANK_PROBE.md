# V26 Q1.38 B/C complete direct-e1 aggregate mod-3 rank probe

## Mathematical target

The signed-sector Schmidt theorem shows that a single direct-e1 sector may already have exact rational row rank 2048. The whole-sector cancellation probe then shows that identical affine supports do not cancel as complete `+M/-M` sector functions. The remaining sharp question is whether **partial cancellation between different supports** can nevertheless make the complete signed direct-e1 aggregate subgeneric.

The first clean run of this probe at predecessor `x=0` was mathematically inconclusive for a structural reason: every reachable global direct-e1 B/C sector is externally inconsistent after fixing all predecessor bits to zero. Thus the complete direct-e1 aggregate is identically zero at that predecessor, and the observed modular rank zero says nothing about cancellation.

This corrected probe therefore chooses, separately for B and C, a deterministic **reachable predecessor witness** extracted from the affine support of a direct-e1 sector already certified to have exact signed Schmidt rank 2048:

- B witness sector: zero set `{(1,5)}`, internal class `(124,4,2)`;
- C witness sector: zero set `{(1,1)}`, internal class `(124,4,2)`.

For each position, solve that affine support exactly, take the predecessor128 projection of the canonical particular solution, and then evaluate the complete normalized direct-e1 signed aggregate at that fixed predecessor.

Let

`K_X = sum_nu 1_{A_nu} (-1)^{q_nu}`

be the normalized complete direct-e1 integer aggregate for leaf position `X in {B,C}` at the selected predecessor. Direct-e1 normalization makes every reachable sector coefficient exactly `+1` or `-1`.

## Exact predecessor specialization

The complete Gauss-corrected phase is retained as a quadratic Boolean function on all160 external variables. After fixing predecessor vector `p`, the beta-only phase is specialized exactly:

- the constant becomes `q(p,0)`;
- each beta linear coefficient gains the polar cross term `B(p,e_beta)`;
- beta-beta quadratic coefficients are unchanged.

Affine support equations are specialized by XORing the predecessor contribution into their RHS. The witness sector is asserted active after specialization.

## Exact modular certificate

Reduce `K_X` modulo the odd prime 3. Any selected-column submatrix satisfies

`rank_F3(K_X[selected columns] mod 3) <= rank_Q(K_X)`.

Therefore, if a deterministic selected-column submatrix reaches the full 2048 row rank over `F3`, then necessarily

`rank_Q(K_X)=2048`.

A full-rank witness for one fixed reachable predecessor input is enough to rule out any **uniform** subgeneric rational-rank upper bound for the complete direct-e1 aggregate.

## Computation without full materialization

The verifier never materializes the `2^11 x 2^21` aggregate.

For each direct-e1 sector active at the selected predecessor it uses the already-validated complete Gauss-corrected quadratic phase, specialized exactly as above. Each chosen21-bit right-beta column is evaluated as a2048-bit signed left vector.

All sector sums modulo3 are accumulated in two Python big-int ternary bitplanes. Gaussian elimination over `F3` is also implemented with exact bit-sliced ternary arithmetic. Right-beta columns are traversed by a deterministic Gray code whose coordinates are ordered by support/cross-phase activity; at most4096 columns are examined.

If rank2048 is not reached, the reported modular rank is only a certified lower bound. No upper bound follows from failure to saturate this particular selected-column family.

## Scope discipline

A full-rank result closes the direct-e1 complete-aggregate rank route for the tested fixed predecessor and therefore falsifies a uniform `<2048` direct-e1 aggregate bound. It does **not** prove the complete predecessor-leaf rank, product-level rank, lower `W_repr(1)`, arithmetic-work reduction, `alpha<1`, or full-round relevance.

The earlier `x=0` clean run is retained only as a diagnostic demonstrating that zero predecessor activates no direct-e1 sectors for B/C; it is not a cancellation result.

Authority requires one clean PR-checkout run of the corrected

`scripts/probe_v26_q138_bc_direct_e1_aggregate_mod3_rank.py`.
