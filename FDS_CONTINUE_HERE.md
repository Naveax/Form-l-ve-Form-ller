# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / joint-mask coefficient composition.

Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank generative structure.

## Current exact q138 chain

For the **entire 4096-case physical fixed-mask family** of the q138 fixed-output exact one-quarter-round Walsh object, the complete certified structural message-width chain is

`44 -> 42 -> 41 -> 40 -> 38.75488750216347...`.

Sharp bound:

`D_max = 216 * 2^31 = 463,856,467,968`,

so

`W_1 <= 38.75488750216347... <39`.

## Sharp proof chain

Rerun/read in this order:

1. physical right/parent rank and common-span theorem:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
   - `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`
2. left support theorem / rank-12 selector:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`
   - `scripts/verify_v26_qr_q138_left_i9_support216.py`
3. full-family global sub-39 theorem/certificate:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_THEOREM.md`
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json`
   - `scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`
4. joint-mask composition bridges:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_JOINT_MASK_COMPOSITION_BRIDGE47.md`
5. metric accounting:
   - `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_REPRESENTATION_WORK_ACCOUNTING.md`
6. fifteen-step closure report:
   - `research/v26/recovered-bit-puncturing-dac/V26_Q138_15_STEP_EXACT_PASS_REPORT.md`

## Exact facts to preserve

Physical interface algebra:

- right doubled reachable hull: `1024 ->162 =114+48`;
- right rank over 4096 masks: `11..38`;
- parent rank: `5..27`;
- all 64 physical left maps share one exact 48-dimensional row space;
- all 4096 mask-conditioned parent Schmidt/interface spaces have exact common span dimension `47` in the canonical 64-dimensional interface coordinate;
- therefore a universal rank-27 basis is impossible, but a fixed universal 47-dimensional ambient basis is exact.

Left support algebra:

- relevant boundary `I9` has nine binary indices;
- per-mask feasible-support upper envelope: `117..216`;
- exact distribution: `117:2, 120:2, 144:12, 174:4, 177:2, 180:6, 216:36`;
- 13 distinct support sets;
- union 384, intersection 96;
- exact `64 x 512` support-selector rank: 12;
- explicit selector basis coefficient alphabet: `{-1,0,1}`;
- support residual: `epsilon=0`.

Global sub-39 construction:

- safe parent Schmidt bond: `RP27`;
- safe support bond: `RL216`;
- exact left parent split: `I9 -- RL216 -- (O7,RP27)`;
- target tree: 368 leaves, 367 internal nodes;
- maximum boundary: `31 binary + RL216`;
- maximum dimension: `216*2^31`;
- second-largest: `528*2^29`.

## First unfinished mathematical pass

The common-span question is solved. The next pass is **mask-to-coefficient transfer inside the fixed 47-dimensional parent-interface basis**.

Work in this order:

1. choose/freeze one exact rational basis of the verified common space `U47`;
2. express every physical parent interface space and its exact coefficient action in that fixed basis;
3. retain the six physical mask controls as explicit binary variables initially;
4. compute exact TT/rank/sector structure of the mask-to-`U47` coefficient tensor;
5. combine that structure with the already exact rank-12 `I9` support selector;
6. test whether the five-site transfer algebra block-diagonalizes the joint coefficient/support tensor;
7. only after a finite exact joint representation is frozen, attach one more QR/layer and measure the new separator/bond growth;
8. certify a finite-depth `W_2` before discussing any round-depth recurrence `W(R)`;
9. keep representation width, factor storage, arithmetic work and error as separate ledgers;
10. do not promote a low message-width result into an attack/work-exponent claim without full accounting.

## Approximation rule

Do **not** activate epsilon-rank now.

The current branch is exact and has `epsilon=0`. Epsilon-rank, coherent-tail and residual-Gram machinery becomes active only if the exact coefficient-transfer/sector route genuinely stalls.

If that happens, freeze a residual budget before measurement and propagate it with the existing exact error calculus.

## Current FDS accounting

Representation/message gain relative to `2^40`:

`64/27 ~=2.37037037x`,

or

`~1.2451124978` log2 bits.

Error:

`epsilon=0`.

Arithmetic work:

not improved. In the current scoped dense-tree proxy, the width-optimized support-216 tree is about `3.9842073564x` more expensive than the compared rank-27 source topology after rank factors are treated as given.

Therefore `ALPHA_PASS=0` remains unchanged.

No `W_2`, round-depth law, arithmetic-work exponent reduction, full second-layer solution, ranking gain or full-round relevance is admitted.

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

Still not admitted: practical exact QR evaluation at the formal maximum, exact end-to-end arithmetic-work reduction, complete second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.
