# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / controlled-error analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor, its exact low-state factorization, and exact or certified approximate contraction.

## Current exact q138 chain

The source-independent/local results establish bond-2 longitudinal modular-addition MPO structure, exact local TT rank `[2,3,3,2]`, semantic ternary equality classes `00/11/unequal`, class-parity conservation, Parseval/orthogonality, residual-Gram calculus and epsilon-rank machinery.

For the q138 fixed-output one-quarter-round exact Walsh network, the global structural chain is now

`44 -> 42 -> 41 -> 40`.

Read especially:

- `research/v26/recovered-bit-puncturing-dac/V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_MODADD_LOCAL_TT_RANK_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_MODADD_TERNARY_CLASS_CORE_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_MODADD_CLASS_PARITY_CONSERVATION.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_MINIMAL_CORE_WIDTH41_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_WIDTH41_SEPARATOR_TOPOLOGICAL_RANK_BOUND.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_MAP_RANK528_THEOREM.md`
- `scripts/verify_v26_qr_width41_left_rank528.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`

The width-40 proof chain is:

1. the certified width-41 34-leaf child has topology-only interface dimension `3072`;
2. for q138 fixed output its exact rational left-map rank is `528`;
3. replace that child by an exact rank factorization `X --(528)-- Z`;
4. reconstruct the modified 536-leaf hypergraph;
5. verify a complete 535-internal-node binary contraction tree;
6. maximum message dimension is exactly `2^40`, attained on a 171-leaf cluster crossing 40 binary indices.

This proves `W <= 40` for the stated q138 fixed-output one-QR representation. It does **not** prove optimality, arithmetic work `O(2^40)`, arbitrary-mask QR width 40, double-round width 40, or practical exact evaluation.

## First unfinished mathematical pass

The next distinct mechanism is **algebraic compression of the certified 40-bit bottleneck**.

Work in this order:

1. run both exact verifier dependencies first:
   - `scripts/verify_v26_qr_width41_left_rank528.py`;
   - `scripts/verify_v26_qr_q138_algebraic_width40.py`;
2. reconstruct the 171-leaf cluster that realizes the `2^40` maximum;
3. identify a useful child split or minimum terminal interface and preregister the corresponding topology-only Schmidt bound;
4. gauge binary endpoint TT bonds to physical/sigma legs where valid and use semantic `00/11/unequal` sectors for rank-3 states;
5. derive projected class-parity/nonlinear support laws rather than counting local constraints before projection;
6. compute exact rational rank of the smaller child map if its dimensions are tractable;
7. if strict rank deficiency exists, replace it by an exact rank factor and require a new **complete global tree certificate** before claiming any width below 40;
8. if exact algebraic rank is effectively full, only then activate certified epsilon-rank/tail approximation on this separator.

Do not return to fused-site ordering searches and do not claim `W<40` from isolated low-boundary cuts.

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
