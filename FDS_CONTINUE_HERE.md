# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / controlled-error analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor, its exact minimal-rank local factorization, and exact or certified approximate contraction.

## Current mathematical chain

Established source-independent results now include:

1. modular-addition Walsh tensor: exact longitudinal MPO bond dimension 2 from the sigma/carry recurrence;
2. one interior addition-bit tensor: exact optimal transverse TT profile `[2,3,3,2]`, so minimal maximum local TT bond dimension 3;
3. q138 rotation/carry amplification explains huge explicit support without implying huge local generative state;
4. full exact Parseval/orthogonality and controlled-error/residual-Gram/epsilon-rank calculus remain available for approximation work;
5. fused-site QR path cutwidth 44 and fused-site carving width 42 are exact only for the fused-site representation;
6. minimal-rank TT-core refinement now gives a complete machine-verified exact one-QR contraction tree with maximum message dimension `2^41`;
7. the width-41 certificate contains all 568 leaves / 567 internal nodes and is checked by an independent verifier that recomputes local rational TT ranks and every boundary dimension;
8. exploratory width-40 cuts exist but no complete width-40 tree is admitted;
9. conditioning long-range wrap variables remains an independent exact 24-state-bit DP memory route with outer boundary enumeration.

Read especially:

- `research/v26/recovered-bit-puncturing-dac/V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_MODADD_LOCAL_TT_RANK_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_EXACT_QR_PATHWIDTH_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_WEIGHTED_CUTWIDTH_CERTIFICATE.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_WEIGHTED_CARVING_WIDTH_CERTIFICATE.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_SITE_FUSION_REFINEMENT.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_MINIMAL_CORE_WIDTH41_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE.json`
- `scripts/verify_v26_qr_minimal_core_width41.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_EXACT_TIME_MEMORY_TRADEOFF.md`

## First unfinished mathematical pass

The minimal-core global-width pass has succeeded at `W <= 41`. The next pass is now **width-40-or-separator-rank**.

Work in this order:

1. run/inspect the width-41 verifier first; treat it as the exact baseline;
2. freeze `W <= 40` as the next exact topology target and require a complete 568-leaf tree, not isolated low-boundary cuts;
3. reuse the current minimal-core orders unless a different exact local order is explicitly preregistered;
4. if width-40 search stalls, stop spending effort on graph ordering and analyze the certified 340-leaf width-41 bottleneck cluster algebraically;
5. derive exact GF(2) parity sectors, nonlinear sigma-support constraints, and Schmidt/matrix rank bounds for its boundary message;
6. only if exact separator rank remains too large, move to certified singular-value/epsilon-rank with an explicit residual budget;
7. separately examine the 20 conditioned wrap variables for exact meet-in-the-middle / reusable boundary-transfer structure that reduces total work, not only memory.

The success condition for the next exact pass is either:

- a machine-verifiable complete tree with `W <= 40`; or
- a rigorous algebraic message-rank reduction below the formal `2^41` width-41 boundary space.

Do not report partial width-40 cuts as a global result.

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
5. only PASS opens packed cap3 under the existing `2 GiB RSS / 1 GiB compact` gates.

Still no admitted practical exact QR evaluation, full second-layer solution, ranking gain, alpha<1, or full-round relevance.
