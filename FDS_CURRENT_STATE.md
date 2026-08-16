# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted. Exact signed first-layer marginals onto all four second-layer column interfaces matched explicit global materialization at cap2/cap3. At cap4, the global 222,660,480 Cartesian trails were avoided; packed exact separator supports were `[0,11846464,26912,0]`, total 24-byte compact estimate ~285 MB, measured peak RSS ~839 MiB.

Stage0 verdict: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

Important limit: these are exact signed marginals inside the frozen bounded trail family, not a complete joint or full-exact second-layer distribution.

## Mathematics-first structural track

The research center is now the exact/controlled-error mathematics of the signed Walsh/trail tensor. Code is a calculator/falsifier, not the object of study.

### Controlled-error results

Canonical notes establish:

- exact tensor/Kronecker factorization for capped column subsets and 2|2 flattenings;
- full-exact QR/double-round Parseval and orthogonality: every normalized subset marginal has squared l2 norm 1 and whole-column singular spectra are invariant under exact local QR basis changes;
- coherent signed-tail bounds: individual trail-square sums are not safe hull-error bounds before signed endpoint merge;
- published one-addition sigma shell/energy recurrences and exact residual Gram DPs, including side-mask extension for reversible ChaCha addition gates;
- explicit separation between published hard-per-addition sigma and unresolved recovered `max_sigma_weight` semantics;
- cap4 Stage0 Parseval residual floors `1`, `0.2793271761`, `0.2687631657`, `1` for C0..C3 under compatible normalization;
- epsilon-rank bridge `delta_r(M) <= epsilon + delta_r(M_K)`;
- local-to-global error telescoping through QR/layer/round composition;
- error-representation exponent `theta=log(r)/(-log(q))` when certified residual decays as `q^K` and cost grows as `r^K`.

### Exact Walsh tensor-network results

A stronger exact direction is now active:

- `V26_EXACT_MODADD_WALSH_MPO_THEOREM.md`: the complete n-bit modular-addition Walsh tensor has an exact tensor-train/MPO representation with binary carry/sigma bond dimension at most 2 and O(n) local factors. Exponential explicit support is not an exponential representation lower bound.
- `V26_Q138_ROTATION_CARRY_AMPLIFICATION.md`: q138 wiring explains explicit support explosion algebraically; after the first 22-term `w=2^3` addition family, ROR8 moves masks to MSB 27, where the next full addition columns contain roughly 0.40–0.81 billion nonzero coefficients even though low-sigma shells can carry most local l2 energy.
- `V26_Q138_HARD_CAP_QR_ERROR_EXAMPLE.md`: the mathematical hard-per-addition K=2/K=3 model collapses to zero over one inverse QR despite strong local concentration; exact residual-Gram values demonstrate coherent kept/omitted interference. This is a semantic diagnostic, not a project-cap result.
- `V26_EXACT_QR_PATHWIDTH_THEOREM.md`: after fixing input/output masks and locally eliminating `u3_i,u4_i`, one exact QR coefficient reduces to n bit-site tensors linked by four nearest-neighbor sigma bonds plus binary offset-8 and offset-12 bonds. A contiguous bit sweep exposes at most 44 binary bonds, independent of word size n for fixed offsets.
- `V26_QR_WEIGHTED_CUTWIDTH_CERTIFICATE.md`: for n=32 the weighted path cutwidth is exactly 44; arbitrary linear bit reordering cannot improve it.
- `V26_QR_WEIGHTED_CARVING_WIDTH_CERTIFICATE.md`: the weighted carving width is exactly 42. Thus an arbitrary ordinary binary contraction tree can improve topology only from 44 to 42 binary frontier bonds. Topology-only contraction ordering is now exhausted for this reduced fixed-IO QR network.
- `V26_QR_EXACT_TIME_MEMORY_TRADEOFF.md`: conditioning the 20 cyclic offset-8/offset-12 wrap variables opens the network into a chain with only 24 dynamic state bits (8 delayed `v4` + 12 delayed `v3` + 4 sigma). This lowers exact memory to a `2^24` state table while moving work into `2^20` boundary enumeration; it is an exact memory/time tradeoff, not a work reduction.

## Current sharp mathematical bottleneck

For the reduced fixed-input/fixed-output exact QR network:

- exact local representation is compact (bond-2 addition MPOs);
- optimal linear topology frontier = 44 binary bonds;
- optimal general binary topology frontier = 42 binary bonds;
- conditioning can reduce dynamic memory to 24 state bits but not automatically total work.

Therefore the first genuinely new mechanism capable of beating the exact topology barrier is **algebraic compression of the width-42 separator tensor/message**:

- exact Schmidt/matrix rank;
- parity/conservation sectors;
- singular-value decay / epsilon-rank;
- low-rank boundary transfer factorization;
- reusable transfer subproblems / meet-in-the-middle over conditioned wrap variables.

Another bit ordering or ordinary contraction tree is no longer a new research direction.

## Active measured QR-transform falsifier

`V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json` remains frozen. Its cap2 factorized/reference implementation and all-four-column `1e-12` regression are committed. No new canonical transform measurement is admitted while provenance is missing.

## Current blocker — exact historical runtime bytes

The exact recovered `fds_v25_bit_puncturing.py` source required to identify historical cap semantics and rerun frozen measurements is absent.

Canonical recovery authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Required identities:

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

Latest recovery audit remains negative. This is a provenance blocker, **not a mathematical NO-GO**.

## Next mathematics

1. Analyze one certified width-42 QR separator algebraically instead of materializing `2^42` states.
2. Derive linear/parity constraints among its crossing sigma, `v3`, and `v4` indices.
3. Compute exact small-instance separator Schmidt spectra and search for a stable rank law.
4. If exact rank remains large, combine a certified residual with singular-value decay through the epsilon-rank bridge.
5. In parallel, analyze the 20-wrap-variable transfer operator for exact low-rank/MITM reuse that reduces total work, not merely memory.
6. Only after a controlled separator representation exists should the same construction be lifted to double-round cross-column contraction.

## Next measured execution after byte recovery

1. SHA-locked rematerialization.
2. Prove exact project cap semantics/normalization/nestedness.
3. Restore dependencies and reproduce historical `19/19 PASS`.
4. Execute the already-frozen cap2 all-column QR regression.
5. Only cap2 PASS opens packed cap3 under the existing 2 GiB RSS / 1 GiB compact gates.

Still not admitted: full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, alpha<1, or full-round relevance.
