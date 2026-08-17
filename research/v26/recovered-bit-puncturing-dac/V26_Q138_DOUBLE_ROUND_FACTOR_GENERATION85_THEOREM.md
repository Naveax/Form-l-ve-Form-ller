# V26 q138 coefficient-aware materialized-factor generation theorem

## Statement

For the q138 fixed-output inverse-double-round five-QR star, the exact signed S1 rank factor can be **explicitly generated and materialized** with maximum single-message/factor dimension

`87 * 2^79`,

so the coefficient-aware factor-generation message exponent satisfies

`W_2_factor-gen <= 79 + log2(87) = 85.44294349584872...`.

This equals the current d=1 representation-existence exponent. It does **not** mean the arithmetic work is practical or even remotely competitive.

## Why this is a different ledger from static constructive95

The coefficient-blind reduced-central-graph + four-generic-leaf static contraction method is method-optimal at95. That theorem forbids improving95 by tree reordering **inside that representation**.

Here the representation itself is changed. The exact signed S1 central factorization has

`R = 16 * 2784 * 2^26 = 87 * 2^35`

rank channels. Block1 is explicitly factored at rank16. Block2 has an explicit exact rational rank2784 factorization, and the physical-row bridge proves every normalized retained-column basis slice is an exact combination of at most64 ordinary physical block2 rows.

Hence both signed factors are genuinely generable; no abstract Schmidt oracle is assumed.

## Left factor size

The four predecessor leaves contribute44 S1 mask bits. Materialize

`U(alpha,r)`

with `alpha in {0,1}^44` and `r in [R]`. Its dimension is

`2^44 * R = 87 * 2^79`.

## Right factor generation

For each `(r,alpha)` generate the right scalar factor entry as follows.

1. Expand the block2 retained-column basis slice into at most64 actual physical S1 block2 rows using the clean physical-row bridge.
2. For one resulting physical S1 central row, fix all44 S1 central input-mask bits. The exact reduced central graph leaves a51-bit boundary to the21-site complement; internal left generation is smaller.
3. Fix the four predecessor-leaf S1 mask assignments to `alpha`. Each exact leaf vector becomes an arbitrary21-bit complement vector.
4. Contract the complement with the explicit binary tree

`[[[10,11],[17,[18,19]]],[[[[30,31],[28,29]],[[8,9],[6,7]]],[[[26,27],[24,25]],[[22,23],[20,21]]]]]`.

For a complement cluster T the safe exact structural exponent is

`gb(T) + 4*min(|T|,21-|T|)`.

The complete tree has peak80. The only peak80 clusters are

- `{20,21,22,23,24,25,26,27}` with central boundary48 and leaf contribution32;
- `{6,7,8,9,20,21,22,23,24,25,26,27,28,29,30,31}` with central boundary60 and leaf contribution20.

Therefore one right-factor entry can be generated with message peak at most80, plus the already smaller fixed-row central boundary51 and leaf-generation peak44.

Materialize the complete right table `N(r,alpha)`. It has the same dimension as U,

`87*2^79`,

which dominates the entry-generation peak80. Finally contract U and N over `(r,alpha)`.

Thus the maximum single materialized factor/message dimension is exactly bounded by

`87*2^79`, exponent `85.44294349584872...`.

## Ledger semantics

Keep the following distinct:

- `W_2_static,blind = 95`: coefficient-blind stored-factor contraction method, method-optimal in its class;
- `W_2_factor-gen <= 85.44294349584872...`: coefficient-aware materialized-factor generation using repeated exact slice contractions;
- `W_repr(1) <= 85.44294349584872...`: representation existence.

The equality of the last two upper bounds is a constructivity result for the signed representation, not an arithmetic-work result. The factor-generation procedure can require astronomical repeated computation.

Unrestricted scalar-by-scalar recomputation can make a pure memory metric even smaller and is therefore **not** assigned a canonical width without an accompanying work budget. The theorem deliberately materializes the signed factor tables so the ledger remains nondegenerate and auditable.

All operations are exact; `epsilon=0`.

Verifier:

`scripts/verify_v26_q138_double_round_factor_generation85.py`.
