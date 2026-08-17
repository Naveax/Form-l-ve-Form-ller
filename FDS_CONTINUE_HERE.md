# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / coefficient-valued joint-mask composition.

Code is only a calculator/falsifier. Clean-checkout execution is now required before a new finite claim becomes authority.

## Corrected current one-QR result

For all 4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

Corrected maximum:

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... <39`.

Read/verify:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT218_GRAM_CORRECTION_THEOREM.md`;
- `scripts/verify_v26_qr_q138_left_i9_gram_support.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json`;
- `scripts/verify_v26_qr_q138_general_rank27_support218_global_sub39.py`.

Both corrected support and corrected global tree pass from a clean GitHub Actions checkout.

## Support facts that replace the old support216/rank12 line

Exact support is defined by the Gram diagonal

`g_m(i)=sum_rest L_m(i,rest)^2`.

Across the 64 physical left fixed masks:

- support range: `117..218`;
- distinct support sets: `64`;
- union: `392`;
- intersection: `42`;
- exact `64 x 512` support-indicator rank: `64`;
- residual: `epsilon=0`.

Therefore the old claims `support<=216`, `13 support classes`, and `selector rank 12` are revoked. Do not use the old rank-12 support composition bridge.

## Why the old support result failed

The old verifier replaced nonzero TT-core coefficients by Boolean ones and projected auxiliary path existence. After the width-40 certificate JSON was repaired and the verifier was finally run on a clean checkout, it did not reproduce its own expected distribution.

The exact Gram-diagonal test avoids this issue and is now authority.

## Clean dependency revalidation in progress

Before second-layer work, rerun from clean checkout:

1. `scripts/verify_v26_qr_q138_algebraic_width40.py`;
2. `scripts/verify_v26_qr_q138_width40_left_rank48.py`;
3. `scripts/verify_v26_qr_q138_physical_right_hull162.py`;
4. `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`.

Workflow:

`.github/workflows/core-exact-dependencies.yml`.

Do not promote common-span47 or a new mask coefficient theorem until this run closes.

## First unfinished mathematical pass

Two exact branches must be solved and then joined.

### Branch A — right/control coefficient family

Candidate exact family factorization:

`P_m = sum_lambda D(m,lambda) K_lambda`.

Current verifier candidate:

`scripts/verify_v26_qr_q138_mask_coeff124_tt.py`.

It must prove from a clean checkout:

1. exact family span dimension (currently hypothesized 124);
2. exact coverage of all 4096 physical right-control cases;
3. row span of the fixed family basis;
4. exact TT prefix profile of `D` in the twelve physical control bits.

Treat `124` as unadmitted until this verifier passes.

### Branch B — six-left-mask coefficient tensor

The support indicator has full rank 64, so support-only compression cannot solve joint-mask composition.

Construct the **actual coefficient-valued** left tensor with the six physical controls

`u1_8,u1_9,u1_10,u2_8,u2_9,u2_10`

kept explicit, together with

- `I9`;
- the remaining seven left external bits `O7`;
- the six parent interface bits or a verified fixed coefficient basis.

Determine exact matrix-family/TT/sector ranks of this tensor. Do not replace coefficient dependence by support classes.

### Join

Only after A and B are exact:

1. identify the shared `u2_8` control explicitly;
2. build a single exact joint factor graph without multiplying independent rank bounds by fiat;
3. restore the exact inter-QR mask permutation/wiring;
4. attach one more QR layer;
5. compute topology-only separators;
6. compute algebraic ranks of the actual bottlenecks;
7. require a complete contraction tree before admitting `W_2`.

## Approximation rule

Current corrected one-QR reduction is exact with `epsilon=0`.

Do not activate epsilon-rank while the coefficient-valued exact route remains open. Residual-Gram/tail machinery becomes active only after an explicit exact composition bottleneck is identified and exact rank/sector methods genuinely stall.

## Accounting

Corrected peak-message improvement relative to `2^40`:

`256/109 ~= 2.3486238532x`,

log-width gain:

`~1.2318156752 bits`.

The old `RL216` dense-work ratio is stale. Recompute work/storage for `RL218` after the current exact dependencies and coefficient representations are frozen.

`ALPHA_PASS=0` remains unchanged.

No certified `W_2`, round-depth law, arithmetic-work exponent reduction, full second-layer solution, ranking gain or full-round relevance is admitted.

## Historical measured execution

Still blocked by missing V25 runtime bytes:

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`;
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`.
