# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. The measured historical QR-cap line is still frozen behind the missing V25 runtime bytes. While blocked, active work is mathematics-first exact Walsh tensor-network analysis; code is only a calculator/falsifier.

## Corrected exact q138 one-QR chain

For the full 4096-case physical fixed-mask family, the complete exact structural message-width chain is now

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

The corrected sharp full-family bound is

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... < 39`.

The older `38.754887502...` value based on `RL216` is superseded.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT218_GRAM_CORRECTION_THEOREM.md`;
- `scripts/verify_v26_qr_q138_left_i9_gram_support.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json`;
- `scripts/verify_v26_qr_q138_general_rank27_support218_global_sub39.py`.

A clean GitHub Actions checkout independently passes both the exact Gram-support verifier and the complete `RL218` global tree verifier.

## Important support correction

The previous support claims

- maximum support 216;
- 13 exact support classes;
- union 384;
- intersection 96;
- exact mask/support selector rank 12;
- rank-12 support-sector composition bridge

are revoked.

The old verifier Booleanized nonzero entries of TT cores and counted auxiliary path existence. After the historical width-40 JSON certificate was repaired and the verifier chain was run from a clean checkout, that script did not reproduce its own frozen expected distribution.

The correct exact support test is

`g_m(i) = sum_rest L_m(i,rest)^2`.

Because this is an exact rational Gram diagonal,

`g_m(i)>0`

iff the corresponding `I9` row of the actual coefficient map is nonzero.

Across all 64 physical left fixed-mask cases:

- exact support range: `117..218`;
- distinct support sets: `64`;
- union: `392`;
- intersection: `42`;
- exact rational rank of the `64 x 512` support-selector matrix: `64`.

Thus the useful exact statement is

`rank_{I9|rest}(L_m) <= 218 < 256`

for every physical left mask. There is no nontrivial linear compression of the 64 support indicator rows in this coordinate representation.

Support pruning remains exact: `epsilon=0`.

## Width-40 certificate serialization repair

The historical width-40 certificate file in the repository contained one extra closing brace before its `scope` field and was not parseable by `json.loads`. A clean CI diagnosis located the defect exactly. One character was removed, after which the original width-40 structural verifier passed without changing the tree, rank-528 data, or mathematical content.

Repair commit: `ea8532e9bce90bdcca1f492c2a6d7e2cf5b9f2b7`.

This repair is serialization-only, but it exposed that later claimed verifiers had not all been exercised from a clean repository checkout. The active exact dependencies are therefore being revalidated through CI before further composition claims are admitted.

## Physical right/parent algebra

Previously admitted exact results are:

- right doubled reachable hull: `1024 -> 162 = 114 + 48`;
- physical right rank over 4096 masks: `11..38`;
- parent rank: `5..27`;
- `u2_31=0`: parent `16..27`;
- `u2_31=1`: parent `5..8`;
- the 64 physical left maps have rank 48 and were reported to share a common 48-dimensional interface row space;
- the union of all parent interface spaces was reported as dimension 47.

These claims are now being re-run from a clean checkout by `.github/workflows/core-exact-dependencies.yml`. Do not build new second-layer authority on the common-span-47 claim until that clean run passes.

## Current mask-coefficient investigation

A separate exact verifier is testing a stronger fixed-basis coefficient representation for the physical right-control family.

Proposed object:

`P_m = sum_{lambda=1}^{124} D(m,lambda) K_lambda`,

where `m` contains the twelve physical right-map controls and `K_lambda` are fixed parent matrices. The verifier independently seeks a 124-dimensional prime-field witness, reconstructs the witness over `Q`, checks exact coverage of all 4096 cases, derives the row span of the fixed family basis, and computes TT prefix ranks of `D`.

Authority candidate:

`scripts/verify_v26_qr_q138_mask_coeff124_tt.py`.

Until its clean CI run passes, `124` is a hypothesis under verification, not an admitted theorem.

## Corrected global sub-39 construction

Use the safe parent Schmidt bond `RP27` and the exact Gram-support bound `RL218`:

`I9 -- RL218 -- (O7,RP27)`.

The corrected complete tree has

- 368 leaves;
- 367 internal nodes;
- 468 nontrivial indices;
- maximum boundary `31 binary + RL218`;
- maximum dimension `218*2^31`;
- second-largest dimension `528*2^29`.

The parent `RP27` bond is internal to the maximizing two-factor node.

This remains an exact zero-error representation/message-width result. It is not an arithmetic-work theorem.

## Composition status

The previous rank-12 support-selector bridge is invalid and must not be used for a second QR.

The next-layer problem must keep the six physical left support-control bits explicitly, or find a different exact coefficient-level sector decomposition. A support-indicator linear compression cannot reduce them because the exact support selector has row rank 64.

The coefficient-side low-state/fixed-basis route remains promising but is being revalidated independently. Only after a clean fixed coefficient representation is proved should it be joined to the explicit left-mask variables and connected to another QR.

No certified `W_2` exists yet.

## Error / approximation

The corrected support reduction is exact: `epsilon=0`.

Do not activate epsilon-rank yet. The coherent-tail, residual-Gram, epsilon-rank and local-to-global error machinery remains reserved for a future point where exact coefficient/sector composition genuinely stalls.

## Representation / work accounting

Relative to `2^40`, the corrected peak-message reduction factor is

`2^40 / (218*2^31) = 256/109 ~= 2.3486238532`.

The corrected log-width gain is

`40 - 38.768184324776925 ~= 1.2318156752 bits`.

The previous dense-work diagnostic was computed for `RL216` and is stale after the support correction. It must be recomputed for `RL218` before quoting a current work ratio.

No arithmetic-work reduction is admitted. `ALPHA_PASS=0` remains unchanged.

## Revoked/superseded notes

The following remain in history but are not current authority for support/composition:

- `V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`;
- `verify_v26_qr_q138_left_i9_support216.py`;
- `V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`;
- `V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_*`;
- support-216/rank-12 portions of `V26_Q138_15_STEP_EXACT_PASS_REPORT.md` and the prior representation/work note.

## Current sharp mathematical front

1. finish clean-checkout revalidation of rank48, physical hull162, parent rank envelope27 and common-span47;
2. finish the exact physical mask-to-fixed-coefficient-family span/TT verifier;
3. construct the exact **coefficient-valued** six-left-mask tensor, not merely its support indicator;
4. combine left coefficient-mask dependence with the verified right-control coefficient representation without a fictitious rank-12 support sector;
5. only then attach one more QR and seek a complete `W_2` certificate;
6. keep peak message, factor storage, arithmetic work and error as separate ledgers.

Still not admitted: practical exact QR evaluation at the formal maximum, exact end-to-end arithmetic-work reduction, complete second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.

## Measured-execution blocker

Historical project-cap measurement remains blocked by missing exact recovered V25 runtime bytes.

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`;
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`.

This is a provenance blocker, not a mathematical NO-GO.
