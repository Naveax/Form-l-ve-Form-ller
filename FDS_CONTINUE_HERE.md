# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / controlled-error analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor, its exact low-state factorization, and exact or certified approximate contraction.

## Current exact q138 chain

The source-independent/local results establish bond-2 longitudinal modular-addition MPO structure, exact local TT rank `[2,3,3,2]`, semantic ternary equality classes `00/11/unequal`, class-parity conservation, Parseval/orthogonality, residual-Gram calculus and epsilon-rank machinery.

For the q138 fixed-output one-quarter-round exact Walsh network, the global structural chain is

`44 -> 42 -> 41 -> 40`.

Core authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_MAP_RANK528_THEOREM.md`
- `scripts/verify_v26_qr_width41_left_rank528.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_BOTTLENECK_RANK64_BOUND.md`

The width-40 proof chain is:

1. width-41 bottleneck child topology-only interface dimension `3072`;
2. q138 exact rational rank `528`;
3. exact replacement by `X --(528)-- Z`;
4. modified 536-leaf network;
5. complete 535-internal-node tree;
6. maximum message exactly `2^40` on a 171-leaf cluster crossing 40 binary indices.

The new 171-leaf maximum cluster itself has certificate split `64|107`:

- 16 of the 40 parent-external bits are on the 64-leaf side;
- 24 are on the 107-leaf side;
- the child interface is only six binary bits.

Therefore the 40-bit parent flattening has rank `<=64`. The 64-leaf child can itself be constructed with peak message `2^22`.

`W <= 40` remains the admitted complete-tree global message-width bound. The rank-64 child factorization has not yet produced a complete `W<40` global certificate.

## First unfinished mathematical pass

The next pass is **rank-64 reinsertion / actual child rank**.

Work in this order:

1. rerun the rank-528 and width-40 verifiers as baseline;
2. reconstruct the unique 171-leaf maximum cluster and its 64|107 child split;
3. compile the 64-leaf child map `L_64 : 2^16 -> 2^6` exactly, initially using a rank-64 factorization through the six interface bits;
4. reinsert that factorization into the already rank-528-compressed global q138 network;
5. search for a complete global tree below 40 and require machine verification of every cluster before claiming success;
6. if `W<=39` does not close, compute the exact rational rank of the `2^16 x 64` map. A rank `<64` is the next genuine algebraic compression mechanism;
7. if the map has full rank 64 and topology still stalls, analyze the opposite 107-leaf map and/or a different 40-bit separator partition before activating approximation;
8. only after exact algebraic routes stall should certified epsilon-rank/tail truncation become active.

Do not claim `W<=39` from partial separators. A preliminary search on one natural rank-64 continuation did not close 39; that is not a lower bound.

## Measured execution remains frozen behind provenance

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Preferred snapshot SHA-256:

`fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`

Core SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

When bytes become available:

1. run SHA-locked rematerialization;
2. prove exact project cap semantics/normalization/nestedness from the core;
3. restore dependencies and reproduce historical `19/19 PASS`;
4. run the already-frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing 2 GiB RSS / 1 GiB compact gates.

Still no admitted practical exact QR evaluation, exact arithmetic-work reduction, full second-layer solution, ranking gain, alpha<1, or full-round relevance.
