# V26 Q1.38 leaf S1 memory-bounded contraction-path probe

## Scope

The invariant research target after the saturated-complement NO-GO is the complete predecessor-leaf Schmidt rank. An older exact S1-minor probe already targeted this directly: fix one predecessor input, leave 11 S1 output bits plus an 11-bit complementary terminal set open, and form a `2048 x 2048` minor over `F_251`. A full-rank minor would certify complete-leaf rational rank `2048` for that fixed input.

The historical run did not produce a rank result. Its greedy contraction path created an intermediate whose NumPy execution attempted a 32 GiB allocation. That is a contraction-order failure, not a mathematical NO-GO. The final minor itself has only `2^22` entries.

This probe therefore performs **path planning only**. It constructs the same exact single-leaf factor graph but never executes a numerical contraction. For A/B/C/D it compares baseline greedy and `random-greedy-128` paths, then repeats them under explicit intermediate element ceilings `2^24,2^25,2^26,2^27`.

The reported quantities are:

- largest planned intermediate element count;
- optimizer FLOP-cost estimate;
- path length and maximum contraction-step arity;
- ratio of the best intermediate to the unavoidable `2^22` final output size.

If a practical bounded path is found, the next step is to execute exactly that path modulo an odd prime and rank the resulting `2048 x 2048` minor. If no bounded path is found, the next route is explicit slicing/variable elimination rather than repeating the old unbounded greedy contraction.

No leaf-rank, representation-width, arithmetic-work, alpha, or full-round claim is made by this path-only diagnostic.
