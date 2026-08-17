# V26 Q138 coefficient-aware factor generation at `3829*2^73`

## Statement

The new exact representation bound

`rank_center(S1) <= R = 3829*2^29`

can be made constructive in the coefficient-aware **materialized-factor memory/message ledger** without exceeding the resulting factor-table size.

Therefore

`W_factor-gen <= 73+log2(3829) = 84.90275194485017...`.

This matches the new representation-existence bound.

No arithmetic-work reduction is claimed. The construction below may require absurd amounts of recomputation and exact elimination; only simultaneously stored/message state is bounded.

## 1. Materialized factor size

The four predecessor leaves contribute exponent44. Thus either materialized rank factor has at most

`R*2^44 = 3829*2^73`

scalar entries.

This has exponent

`73+log2(3829)=84.90275194485017...`.

## 2. Streaming exact physical-row basis selection

The central S1 matricization has

- `2^44` physical S1 rows;
- a 51-bit central S1/complement graph boundary, hence at most `2^51` explicit central columns before leaf attachment.

Do not materialize the full `2^44 x 2^51` matrix.

Use an exact central-entry oracle and scan physical rows/columns. Maintain a set of pivot physical rows and pivot columns. If the true central rank is `r`, the clean representation theorem guarantees

`r <= R`.

An exact Gaussian row-basis selection can be implemented while storing only the pivot minor/inverse plus the current streamed row/column data. The largest dense pivot object has

`r^2 <= R^2`

entries.

Its exponent is at most

`2 log2 R = 81.8055038897003...`,

strictly below the materialized-factor exponent84.90275.

A complete physical central row has only `2^51` entries, also far below the factor table. It may instead be streamed scalar-by-scalar; this only reduces storage.

The selected rank basis consists of **actual physical S1 rows**, which is important for the right-entry construction.

## 3. Physical-row to rank-coordinate transform

Once pivot physical rows/columns are fixed, coordinates of every physical S1 row in the rank basis are obtained from its values on the pivot columns using the stored inverse.

Storing the entire physical-to-rank transform would cost at most

`2^44 * R = 3829*2^73`

entries, exactly the target factor-table envelope. It may also be streamed instead.

Thus coordinate generation does not exceed the claimed width.

## 4. Right-factor entry generation

Because the rank basis rows are ordinary physical S1 assignments, each right-factor entry is a contraction with a fixed physical S1 central slice.

The previously certified 21-site complement tree remains valid. For a fixed leaf-left assignment its peak is

`80` bits of message exponent.

The fixed-physical S1 central boundary is51 and exact predecessor-leaf generation is at most44. Therefore

`max(80,51,44) = 80 < 84.9027519...`.

Each selected physical rank-basis row can be processed independently and streamed into the materialized right table.

## 5. Left factor

The left table combines the exact physical-to-rank coordinates with the predecessor-leaf values on the S1 side. It has the same `R*2^44` output envelope.

Any recomputation or summation over physical rows changes arithmetic work, not the maximum stored table/message dimension.

## 6. Conclusion

The largest required stored object is the materialized rank factor itself:

`3829*2^73` entries.

Hence

`W_factor-gen <= 73+log2(3829)=84.90275194485017...`.

Keep separate:

- exact representation existence: now `<=84.90275194485017...`;
- coefficient-aware materialized-factor generation: now `<=84.90275194485017...`;
- coefficient-blind static graph+leaf method: still95 in that representation;
- arithmetic work: not reduced or bounded by this theorem.

## Authority

- `V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_factor_generation_rank3829.py`;
- `.github/workflows/factor-generation-rank3829.yml`.
