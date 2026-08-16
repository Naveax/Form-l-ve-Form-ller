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
5. fused-site QR path cutwidth 44 and fused-site carving width 42 are exact **only for the fused-site representation**;
6. exact local site refinement gives a 64-factor network with a balanced 41-bond cut, proving 42 is not a universal lower bound for the full factor network;
7. keeping the original addition-bit factors separate refines the network further; smaller balanced cuts exist, but the full refined contraction-tree optimum is not yet certified;
8. conditioning long-range wrap variables gives an independent exact 24-state-bit DP memory route with outer boundary enumeration.

Read especially:

- `V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`
- `V26_MODADD_LOCAL_TT_RANK_THEOREM.md`
- `V26_EXACT_QR_PATHWIDTH_THEOREM.md`
- `V26_QR_WEIGHTED_CUTWIDTH_CERTIFICATE.md`
- `V26_QR_WEIGHTED_CARVING_WIDTH_CERTIFICATE.md`
- `V26_QR_SITE_FUSION_REFINEMENT.md`
- `V26_QR_EXACT_TIME_MEMORY_TRADEOFF.md`
- plus the Parseval, residual-Gram, epsilon-rank and error-exponent notes.

## First unfinished mathematical pass

The next distinct mechanism is **global contraction of minimal-rank local cores**.

Work in this order:

1. decompose every interior modular-addition bit tensor into an exact TT with current sigma in the center and bond profile `[2,3,3,2]`;
2. rebuild one fixed-input/fixed-output QR network from those cores, preserving XOR/rotation constraints explicitly rather than collapsing them into oversized hyperfactors;
3. compute a rigorous global contraction-width upper bound and compare it to 44/42 fused-site baselines;
4. if the width drops, identify which bond-3 core placement causes the reduction and derive it algebraically;
5. if topology remains large, compute separator Schmidt/rank structure before any approximation;
6. only after the exact minimal-core route is exhausted should epsilon-rank/tail truncation become the active mechanism.

Do **not** cite fused-site carving width 42 as a lower bound for the full exact QR tensor network. It is a certified value for one exact but over-fused representation.

A successful pass must either:

- produce a rigorously smaller exact global width/representation using minimal-rank cores; or
- close that precise refinement as insufficient and state the remaining separator-rank bottleneck.

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

Still no admitted full second-layer solution, ranking gain, alpha<1, or full-round relevance.
