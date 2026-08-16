# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / controlled-error analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor, its exact local tensor-network representation, and exact or certified approximate contraction.

## Current mathematical chain

The source-independent work has established:

1. exact modular-addition Walsh coefficients admit a binary carry/sigma MPO of bond dimension 2;
2. q138 rotations turn short carry tails into high-bit masks, explaining explicit support explosion without implying large local representation state;
3. published hard-sigma local truncations have exact shell/residual Gram calculus, but are not identified with historical project `max_sigma_weight`;
4. full exact QR/double-round Walsh operators obey Parseval/orthogonality, so bounded-cap zeros are not full-exact zeros;
5. capped low rank can transfer to full-exact epsilon-rank only after a certified residual exists;
6. local residuals can telescope through QR/layers/rounds;
7. for one fixed-IO 32-bit QR coefficient, exact local elimination gives a site network with four nearest-neighbor sigma bonds plus offset-8 and offset-12 binary bonds;
8. exact weighted path cutwidth is 44;
9. exact weighted carving width is 42, so ordinary topology-only contraction ordering is exhausted;
10. conditioning the 20 cyclic long-range wrap variables yields an exact 24-state-bit open-chain DP, trading memory for boundary-enumeration work.

Relevant notes under `research/v26/recovered-bit-puncturing-dac/` include:

- `V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`
- `V26_EXACT_QR_PATHWIDTH_THEOREM.md`
- `V26_QR_WEIGHTED_CUTWIDTH_CERTIFICATE.md`
- `V26_QR_WEIGHTED_CARVING_WIDTH_CERTIFICATE.md`
- `V26_QR_EXACT_TIME_MEMORY_TRADEOFF.md`
- plus the earlier Parseval, tail, residual-Gram, epsilon-rank and error-exponent notes.

## First unfinished mathematical pass

**Do not search another site ordering.** The next distinct mechanism is algebraic compression of the certified width-42 separator.

Work in this order:

1. choose one width-42 cut from the certified carving decomposition;
2. write the crossing indices explicitly by type: sigma, offset-8 `v4`, offset-12 `v3`;
3. derive every exact linear/parity conservation law induced by the sigma recurrence and fixed boundary masks;
4. determine how many formal `2^42` boundary states are immediately impossible;
5. derive a factorized Gram or transfer representation of the contracted-side boundary message;
6. compute exact small-instance Schmidt/rank spectra only as a finite falsifier for the derived algebra;
7. if exact rank is still large, move to certified singular-value/epsilon-rank analysis rather than another graph permutation;
8. separately examine whether the 20 conditioned wrap variables admit meet-in-the-middle or low-rank boundary-transfer reuse that reduces **total work**, not only memory.

The success condition for this mathematical pass is a rigorous reduction in effective separator dimension/rank below the topology-only 42-bond space, or a scoped NO-GO showing that the chosen algebraic mechanism does not reduce it.

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
2. prove exact cap semantics/normalization/nestedness from the core;
3. restore dependencies and reproduce historical `19/19 PASS`;
4. run the already-frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing `2 GiB RSS / 1 GiB compact` gates.

Do not retune the frozen QR plan. Do not turn source-independent mathematical lemmas into project-specific numerical claims without the missing semantic/provenance bridge.

Still no admitted full second-layer solution, ranking gain, alpha<1, or full-round relevance.
