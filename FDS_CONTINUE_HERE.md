# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first full-exact / controlled-error tensor analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh/trail tensor and its exact or certified approximate contraction.

## Mathematics authority

Read, in this order, under `research/v26/recovered-bit-puncturing-dac/`:

1. `V26_TENSOR_RANK_MATHEMATICAL_REFRAMING.md`
2. `V26_FULL_QR_PARSEVAL_LEMMA.md`
3. `V26_COHERENT_TRAIL_TAIL_BOUNDS.md`
4. `V26_MODADD_SIGMA_SHELL_THEOREM.md`
5. `V26_SIGMA_SEMANTICS_SEPARATION.md`
6. `V26_STAGE0_PARSEVAL_GAP_BOUNDS.md`
7. `V26_EPSILON_RANK_BRIDGE_THEOREM.md`
8. `V26_LOCAL_TO_GLOBAL_ERROR_TELESCOPING.md`
9. `V26_MODADD_RESIDUAL_GRAM_THEOREM.md`
10. `V26_ERROR_REPRESENTATION_EXPONENT.md`

Core mathematical chain:

`local/on-orbit Walsh residual`

`-> Gram-aware local error`

`-> QR/layer telescoping`

`-> certified global epsilon`

`-> capped 2|2 singular/rank structure`

`-> full-exact epsilon-rank`

`-> controlled contraction / downstream score error`

`-> error-vs-cost exponent theta`.

Established facts:

- full exact QR/double-round Walsh operators are orthogonal and every normalized subset marginal has squared norm 1;
- cap4 C0/C3 zero marginals therefore cannot be full-exact zeros;
- under compatible normalization, cap4 Stage0 residual floors for C0..C3 are `1`, `0.2793271761`, `0.2687631657`, `1`;
- exact capped rank is brittle under tails; epsilon-rank is the robust invariant;
- fixed small hard per-addition published-sigma caps are not uniformly accurate over masks;
- do not identify that published hard-cap model with project `max_sigma_weight` until the missing core proves the semantics;
- for the published hard-cap addition model, local source-conditioned residuals can be computed exactly as `eta^2=c^T G_res c` using a polynomial-time four-state bit DP rather than enumerating `(u,v)` or trails;
- if residual decays `q^K` and representation grows `r^K`, the natural controlled-representation exponent is `theta=log(r)/(-log(q))`.

## First unfinished mathematical pass

Turn the abstract error-cost theory into the strongest possible **source-conditioned factor-graph certificate** without guessing missing project cap semantics:

1. characterize which local mask families are actually reached symbolically by the q138 ChaCha wiring, independently of cap implementation details where possible;
2. derive mask-family residual bounds or Gram structures for local modular additions;
3. formulate the adaptive local error-budget problem over four-addition QR and alternating column/diagonal layers;
4. derive a global epsilon bound by telescoping;
5. combine epsilon with 2|2 singular tails to obtain a full-exact epsilon-rank bound;
6. state the first preregistrable theta protocol: residual-decay sequence, representation/work growth sequence, scaling family, and kill/pass conditions.

Prefer theorem -> lemma -> finite falsifier. Use terminal code only to validate finite identities or evaluate formulas.

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
