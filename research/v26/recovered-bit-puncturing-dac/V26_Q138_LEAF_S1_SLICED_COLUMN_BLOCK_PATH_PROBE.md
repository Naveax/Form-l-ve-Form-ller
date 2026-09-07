# V26 Q1.38 leaf S1 sliced column-block path probe

## Motivation

The exact complete-leaf S1-minor target is a `2048 x 2048` matrix. The clean memory-bounded path diagnostic shows that forcing the whole22-output tensor through a small intermediate ceiling is possible only by very high-arity contractions with astronomically large estimated work. Memory alone is therefore the wrong optimization target.

## Boundary-transfer slicing

Split the22 open minor bits into:

- 11 S1 row bits, always open;
- 11 complementary column bits.

For `b=0..11`, leave only `b` column bits open and fix the remaining `11-b` column bits. One contraction then produces a `2048 x 2^b` block. Repeating over the `2^(11-b)` assignments of the fixed column bits reconstructs the exact full minor.

The fixed values affect local tensor entries but not tensor shapes, so the same contraction path can be reused for every block at a chosen `b`.

This probe performs path planning only. For A/B/C/D and every `b` it measures binary greedy and random-greedy paths, recording:

- largest intermediate;
- per-block optimizer cost;
- number of blocks;
- estimated total path cost = per-block cost times block count.

It then reports the lowest-total-cost plan available under several intermediate-size ceilings.

The next numerical step should choose a Pareto point with both manageable intermediate memory and manageable total block cost, execute those exact blocks over an odd prime, assemble the `2048 x 2048` minor, and rank it. If no practical Pareto point exists, a more structural transfer/variable-elimination theorem is required.

No leaf-rank, representation-width, arithmetic-work, alpha, or full-round claim is made here.
