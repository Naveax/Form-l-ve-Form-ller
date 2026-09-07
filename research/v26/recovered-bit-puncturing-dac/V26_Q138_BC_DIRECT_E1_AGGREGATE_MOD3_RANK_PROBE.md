# V26 Q1.38 B/C complete direct-e1 aggregate mod-3 rank probe

## Mathematical target

The signed-sector Schmidt theorem shows that a single direct-e1 sector may already have exact rational row rank 2048. The whole-sector cancellation probe then shows that identical affine supports do not cancel as complete `+M/-M` sector functions. The remaining sharp question is whether **partial cancellation between different supports** can nevertheless make the complete signed direct-e1 aggregate subgeneric.

This probe attacks that question directly for the fixed predecessor input `x=0`.

Let

`K_X = sum_nu 1_{A_nu} (-1)^{q_nu}`

be the normalized complete direct-e1 integer aggregate for leaf position `X in {B,C}`, after fixing all 128 predecessor bits to zero. Direct-e1 normalization makes every reachable sector coefficient exactly `+1` or `-1`.

## Exact modular certificate

Reduce `K_X` modulo the odd prime 3. Any selected-column submatrix satisfies

`rank_F3(K_X[selected columns] mod 3) <= rank_Q(K_X)`.

Therefore, if a deterministic selected-column submatrix reaches the full 2048 row rank over `F3`, then necessarily

`rank_Q(K_X)=2048`.

A full-rank witness for one fixed predecessor input is enough to rule out any **uniform** subgeneric rational-rank upper bound for the complete direct-e1 aggregate.

## Computation without full materialization

The verifier never materializes the `2^11 x 2^21` aggregate.

For each reachable e1 sector it uses the already-validated complete Gauss-corrected quadratic phase on all 160 external variables. After fixing predecessor `x=0`, each chosen 21-bit right-beta column is evaluated as a 2048-bit signed left vector.

All sector sums modulo 3 are accumulated in two Python big-int ternary bitplanes. Gaussian elimination over `F3` is also implemented with exact bit-sliced ternary arithmetic. Right-beta columns are traversed by a deterministic Gray code whose coordinates are ordered by support/cross-phase activity; at most 4096 columns are examined.

If rank 2048 is not reached, the reported modular rank is only a certified lower bound. No upper bound follows from failure to saturate this particular selected-column family.

## Scope discipline

A full-rank result closes the direct-e1 complete-aggregate rank route for the tested fixed predecessor and therefore falsifies a uniform `<2048` direct-e1 aggregate bound. It does **not** prove the complete predecessor-leaf rank, product-level rank, lower `W_repr(1)`, arithmetic-work reduction, `alpha<1`, or full-round relevance.

Authority requires one clean PR-checkout run of

`scripts/probe_v26_q138_bc_direct_e1_aggregate_mod3_rank.py`.
