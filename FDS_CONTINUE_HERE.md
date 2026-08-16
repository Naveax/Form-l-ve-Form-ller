# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first full-exact / controlled-error tensor analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh/trail tensor and its exact or certified approximate contraction.

## Mathematics authority added

Read, in this order, under `research/v26/recovered-bit-puncturing-dac/`:

1. `V26_TENSOR_RANK_MATHEMATICAL_REFRAMING.md`
2. `V26_FULL_QR_PARSEVAL_LEMMA.md`
3. `V26_COHERENT_TRAIL_TAIL_BOUNDS.md`
4. `V26_MODADD_SIGMA_SHELL_THEOREM.md`
5. `V26_SIGMA_SEMANTICS_SEPARATION.md`
6. `V26_STAGE0_PARSEVAL_GAP_BOUNDS.md`
7. `V26_EPSILON_RANK_BRIDGE_THEOREM.md`
8. `V26_LOCAL_TO_GLOBAL_ERROR_TELESCOPING.md`

Core mathematical chain:

`local/on-orbit Walsh approximation error`

`-> QR/layer telescoping`

`-> certified global residual epsilon`

`-> capped 2|2 singular/rank structure`

`-> full-exact epsilon-rank bound`

`-> controlled tensor contraction / downstream score error`.

Important facts already established:

- full exact QR/double-round Walsh operators are orthogonal and every normalized subset marginal has squared norm 1;
- cap4 C0/C3 zero marginals therefore cannot be full-exact zeros;
- under compatible normalization, cap4 Stage0 residual floors for C0..C3 are `1`, `0.2793271761`, `0.2687631657`, `1`;
- exact capped rank is brittle under omitted tails; epsilon-rank is the robust invariant;
- fixed small hard per-addition published-sigma caps are not uniformly accurate over masks;
- do **not** identify that published hard-cap model with project `max_sigma_weight` until the missing core proves the semantics;
- local source-conditioned/on-orbit error is the promising route, because uniform worst-case operator error can be useless.

## First unfinished mathematical pass

Derive the strongest source-independent/on-orbit error certificate possible without guessing project cap semantics. In particular, work toward a dynamic error-budget formulation over the ChaCha factor graph:

- local mask-conditioned residual bounds;
- Gram-aware combination when residual columns overlap;
- telescoping through four-addition QR and alternating column/diagonal layers;
- resulting `epsilon_K` supplied to the epsilon-rank bridge;
- downstream contraction/ranking stability stated with explicit error margins.

Prefer theorem/lemma/falsifier order. Use code only to check finite identities or explore candidate bounds.

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

Do not retune the frozen QR plan. Do not turn pure mathematical lemmas into numerical project claims without the missing semantic/provenance bridge.

Still no admitted full second-layer solution, ranking gain, alpha<1, or full-round relevance.
