# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted. Exact signed first-layer marginals onto all four second-layer column interfaces matched explicit global materialization at cap2/cap3. At cap4, the global 222,660,480 Cartesian trails were avoided; packed exact separator supports were `[0,11846464,26912,0]`, total 24-byte compact estimate ~285 MB, measured peak RSS ~839 MiB.

Stage0 verdict: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.

Important limit: these are exact signed marginals inside the frozen bounded trail family, not a complete joint or full-exact second-layer distribution.

## Mathematics-first structural track

The research center is now the exact/controlled-error mathematics of the signed Walsh/trail tensor. Code is a calculator/falsifier, not the object of study.

Canonical mathematical notes under `research/v26/recovered-bit-puncturing-dac/` now establish:

- `V26_TENSOR_RANK_MATHEMATICAL_REFRAMING.md`: the boundary object is a signed mixture of tensor products; column subsets and 2|2 flattenings inherit Kronecker factorizations and rank bounds.
- `V26_FULL_QR_PARSEVAL_LEMMA.md`: full exact QR/double-round Walsh operators are orthogonal; every normalized subset marginal has squared l2 norm exactly 1; whole-column singular spectra are invariant under the next full exact QR layer.
- `V26_COHERENT_TRAIL_TAIL_BOUNDS.md`: omitted trail error must be bounded after coherent signed endpoint merging; individual trail-square sums alone are not safe hull-error bounds.
- `V26_MODADD_SIGMA_SHELL_THEOREM.md`: the published one-addition sigma definition has an exact two-state shell-energy recurrence and fixed hard per-addition caps are not uniformly accurate over masks.
- `V26_SIGMA_SEMANTICS_SEPARATION.md`: do not identify that published hard-cap model with recovered project `max_sigma_weight` until the missing core proves the semantics.
- `V26_STAGE0_PARSEVAL_GAP_BOUNDS.md`: under compatible Walsh normalization, cap4 Stage0 column marginals have unavoidable l2 distance from full exact marginals of at least `1`, `0.2793271761`, `0.2687631657`, `1` for C0..C3.
- `V26_EPSILON_RANK_BRIDGE_THEOREM.md`: a capped rank/singular-tail result plus certified residual epsilon yields a full-exact epsilon-rank guarantee; exact capped rank alone is not stable enough.
- `V26_LOCAL_TO_GLOBAL_ERROR_TELESCOPING.md`: certified local/on-orbit defects telescope through QR/layer/round composition, giving `local error -> global residual -> full-exact epsilon-rank -> controlled contraction` without global trail enumeration.
- `V26_MODADD_RESIDUAL_GRAM_THEOREM.md`: for the published hard-sigma addition model, a four-state bivariate bit-DP computes exact pairwise residual Gram entries; an arbitrary reached mask mixture has exact local defect `eta^2=c^T G_res c`. The recurrence was exhaustively matched to rational brute-force Walsh sums for n=2,3,4.
- `V26_ERROR_REPRESENTATION_EXPONENT.md`: if certified local residual decays as `A q^K` while cost grows as `B r^K`, the natural controlled-compression exponent is `theta=log(r)/(-log(q))`; for m contractive local steps, fixed global tolerance gives `C_total=O(m^(1+theta) epsilon^(-theta))`. Adaptive error allocation is a constrained optimization problem, not post-hoc threshold tuning.

This math track does not require the missing historical bytes for source-independent lemmas. The bytes are required only to attach project-specific cap semantics, numerical residuals and a project-specific theta to them.

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

1. Keep full exact Walsh theory and the abstract/project capped family distinct until cap semantics are proven.
2. Pursue source-conditioned/on-orbit local residual certificates, preferably Gram-aware rather than cancellation-blind per-column sums.
3. Telescope local defects to a global `epsilon_K`.
4. Determine capped 2|2 singular spectra/rank bounds and combine them with `epsilon_K` through the epsilon-rank bridge.
5. Measure/derive residual-decay versus factor-cost growth and freeze the first project-specific `theta` scaling protocol only after the residual is certified.
6. Optimize cap/rank jointly under a fixed downstream error budget; only then judge pairwise/junction-tree contraction as a useful controlled representation.

## Next measured execution after byte recovery

1. SHA-locked rematerialization.
2. Prove exact project cap semantics/normalization/nestedness.
3. Restore dependencies and reproduce historical `19/19 PASS`.
4. Execute the already-frozen cap2 all-column QR regression.
5. Only cap2 PASS opens packed cap3 under the existing 2 GiB RSS / 1 GiB compact gates.

Still not admitted: full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, alpha<1, or full-round relevance.
