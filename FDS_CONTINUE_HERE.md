# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / joint-mask composition.

Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank generative structure.

## Current exact q138 chain

For the **entire 4096-case physical fixed-mask family** of the q138 fixed-output exact one-quarter-round Walsh object, the complete certified structural message-width chain is now

`44 -> 42 -> 41 -> 40 -> 38.75488750216347...`.

The sharp bound is

`D_max = 216 * 2^31 = 463,856,467,968`,

so

`W <= 38.75488750216347... < 39`.

This supersedes the earlier conditioned `u2_31=1` bound `39.044394119...` as the sharp complete global result, although that older certificate remains valid historically.

## Proof chain

Read/verify in this order:

1. physical right-map quotient:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
   - `scripts/verify_v26_qr_q138_physical_right_hull162.py`
2. physical parent rank envelope:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
   - `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`
3. left-I9 support bound:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`
   - `scripts/verify_v26_qr_q138_left_i9_support216.py`
4. complete global sub-39 theorem/certificate:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_THEOREM.md`
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json`
   - `scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`
5. next-layer support composition bridge:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`

## Exact facts to preserve

Physical right/parent algebra:

- doubled right reachable hull: `1024 -> 162 = 114 + 48`;
- right rank over 4096 masks: `11..38`;
- parent rank: `5..27`;
- `u2_31=0`: parent `16..27`;
- `u2_31=1`: parent `5..8`.

Left support algebra:

- relevant `I9` boundary has nine binary indices;
- physical per-mask feasible-support upper envelope size: `117..216`;
- exact support-size distribution: `117:2, 120:2, 144:12, 174:4, 177:2, 180:6, 216:36`;
- 13 distinct support sets;
- union size 384;
- intersection size 96;
- mask/support selector matrix size `64 x 512`, exact rational rank 12;
- explicit rank-12 basis verified with coefficient alphabet `{-1,0,1}`;
- support pruning residual: `epsilon=0`.

Global sub-39 construction:

- safe parent Schmidt bond: `RP27`;
- safe left support bond: `RL216`;
- exact left parent factorization: `I9 -- RL216 -- (O7,RP27)`;
- complete target network: 368 leaves, 367 internal tree nodes, 468 nontrivial indices;
- maximum boundary: `31 binary + RL216`;
- maximum dimension: `216*2^31`;
- second-largest dimension: `528*2^29`, log-width `38.044394119...`.

## First unfinished mathematical pass

The one-QR fixed-mask representation target is no longer the blocker. The next pass is **joint-mask / next-layer composition**.

Work in this order:

1. rerun the three sharp exact verifiers:
   - `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`;
   - `scripts/verify_v26_qr_q138_left_i9_support216.py`;
   - `scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`;
2. use the exact rank-12 support selector, not 64 unrelated support tables, when the six left mask controls become explicit variables;
3. construct the joint tensor whose legs are
   - the six mask controls,
   - the rank-12 support-sector variable,
   - the active `I9` coordinate,
   - and the mask-conditioned parent Schmidt/interface variable;
4. determine the common span of the mask-conditioned parent Schmidt spaces, or derive an equivalent finite transfer/sector representation;
5. falsify the hypothesis that one universal rank-27 basis suffices unless exact algebra proves it;
6. if the common coefficient-space span is small, freeze its exact basis and compose one more QR/layer through that basis;
7. if the common span is large, search for a block/sector decomposition conditioned by the rank-12 support selector rather than falling back to 64 separate factorizations;
8. only after an exact joint representation is obtained, build the next-layer tensor network and measure its separator/bond growth;
9. derive a round-depth cost law `W(R)` or a rigorous finite-depth bound from the composed network;
10. keep representation size and arithmetic work separate in all accounting.

## Approximation rule

Do **not** activate epsilon-rank merely because it exists.

The current reduction is exact and has `epsilon=0`. The previously derived coherent-tail, residual-Gram, epsilon-rank and local-to-global telescoping machinery becomes active only if the exact common-span/sector route genuinely stalls.

If approximation becomes necessary, freeze an explicit residual budget before measurement and propagate it with the existing exact error machinery.

## Current FDS accounting

Relative to the previous `2^40` dense maximum, the new exact representation/message maximum is smaller by

`2^40 / (216*2^31) = 64/27 ~= 2.37037037`.

Log-width gain:

`log2(64/27) ~= 1.2451124978 bits`.

This is a zero-error exact representation/message-width result only.

`ALPHA_PASS=0` remains unchanged. No arithmetic-work exponent reduction, full second-layer solution, ranking gain, or full-round relevance is admitted.

## Measured execution remains frozen behind provenance

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Preferred snapshot SHA-256:

`fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`

Core SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

When bytes become available:

1. SHA-locked rematerialization;
2. prove exact historical project-cap semantics/normalization/nestedness;
3. reproduce historical `19/19 PASS`;
4. run the frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing resource gates.

Still not admitted: practical exact QR evaluation at the formal maximum, exact end-to-end arithmetic-work reduction, full second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.
