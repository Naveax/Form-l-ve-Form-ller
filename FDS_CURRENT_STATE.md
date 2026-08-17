# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Its bounded-family result remains distinct from the full-exact Walsh line below.

The active work while historical measured-runtime provenance is blocked is mathematics-first exact Walsh tensor-network analysis. Code is a calculator/falsifier, not the research object.

## Exact q138 one-QR structural chain

For the full 4096-case physical fixed-mask family of the q138 fixed-output exact one-quarter-round Walsh object, the complete certified structural message-width chain is now

`44 -> 42 -> 41 -> 40 -> 38.75488750216347...`.

The sharp exact bound is

`D_max = 216 * 2^31 = 463,856,467,968`,

so

`W_1 <= 38.75488750216347... <39`.

The older conditioned `u2_31=1` certificate at `39.044394119...` remains valid historically but is superseded by the stronger all-mask result.

## Physical right/parent algebra

The certified 171-leaf parent bottleneck splits `64|107` through six binary interface bits and has external partition `16|24`.

The physical 107-leaf right map is an exact five-site transfer chain. Its formal doubled Gram state has dimension 1024, while the sharp physical reachable hull is

`1024 -> 162 = 114 + 48`.

Over all 4096 physical masks:

- right rank: `11..38`;
- parent rank: `5..27`;
- `u2_31=0`: parent rank `16..27`;
- `u2_31=1`: parent rank `5..8`.

The 64 physical left fixed-mask maps all have exact rank 48 and, after exact union-rank verification, **share one common 48-dimensional interface row space**. The older wording that there were two distinct classes selected by `u2_8` is superseded.

More strongly, the union of all 4096 mask-conditioned parent Schmidt/interface spaces has exact dimension

`47`

inside the canonical 64-dimensional interface coordinate.

Thus:

- each mask activates at most 27 parent directions;
- all masks together require 47 directions;
- one universal rank-27 basis is impossible;
- one universal 47-dimensional parent-interface ambient basis is exact.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

## Exact left-I9 support structure

The previous conditioned maximum exposed a nine-bit interface

`I9 = {v4_8,v4_9,v4_10,sig4_18,sig3_10,v3_21,v3_22,aux_j2_i10_k2,sig1_10}`.

For every physical left mask, Boolean-semiring projection of the exact minimal-TT nonzero support onto `I9` gives a feasible-support upper envelope of size at most 216.

Exact support-size distribution over 64 left masks:

- 117: 2;
- 120: 2;
- 144: 12;
- 174: 4;
- 177: 2;
- 180: 6;
- 216: 36.

Therefore

`rank_{I9|rest}(L_m) <=216`

for every physical left mask, and the same bound survives multiplication by any mask-conditioned interface basis used in the parent rank-27 factorization.

The 64 masks produce 13 distinct support sets, with

- union size 384;
- intersection size 96.

The exact `64 x 512` mask/support selector matrix has rational rank

`12`.

An explicit 12-row / 12-pivot factorization is machine-verified, with reconstruction coefficients only in `{-1,0,1}`.

Support pruning residual:

`epsilon=0`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`
- `scripts/verify_v26_qr_q138_left_i9_support216.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`

## Full-family exact global sub-39 certificate

Use a safe uniform parent Schmidt bond `RP27` and split the left parent factor exactly as

`I9 -- RL216 -- (O7,RP27)`.

After reinsertion into the rank-528-compressed global network, a complete deterministic tree rewrite gives

- 368 leaves;
- 367 internal tree nodes;
- 468 nontrivial indices.

Maximum message:

`216*2^31 = 463,856,467,968`,

with boundary

- 31 binary indices;
- one dimension-216 `RL216` bond.

The parent `RP27` bond is internal to the maximizing `XB-Z27` pair and does not appear in the maximum boundary.

Second-largest certified message:

`528*2^29 = 283,467,841,536`,

log-width `38.04439411935845...`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`

## Joint-mask / next-layer composition bridge

Two exact common structures are now available:

1. support feasibility: rank-12 mask/support selector;
2. parent coefficient/interface ambient space: fixed 47-dimensional rational common span.

This removes the need for 64 unrelated support tables and 64 unrelated ambient Schmidt coordinate systems.

The remaining exact composition object is the **mask-to-coefficient transfer tensor inside the fixed 47-dimensional basis**, including its sector/TT structure and compatibility with the rank-12 support selector.

Do not multiply 12 and 47 and call the result a universal coefficient rank without proving the coupling tensor.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_JOINT_MASK_COMPOSITION_BRIDGE47.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`

## Error / approximation status

The admitted reduction is exact:

`epsilon=0`.

Epsilon-rank/tail approximation is therefore not activated. Existing coherent-tail, residual-Gram, epsilon-rank and local-to-global error machinery remains available only if exact joint composition later stalls.

## Representation / work accounting

Relative to the previous `2^40` dense maximum:

- exact message reduction factor: `64/27 ~=2.37037037`;
- log-width gain: `log2(64/27) ~=1.2451124978` bits.

This is a genuine representation/message-width gain.

A scoped formal dense-tree work diagnostic, treating rank factors as already available, gives the opposite result for the current width-optimized tree:

- previous rank-27 source topology dense-work proxy: `36,464,139,277,420,602`;
- support-216 width-optimized tree: `145,280,691,954,501,690`;
- new tree is about `3.9842073564x` worse on that proxy.

Therefore no arithmetic-work reduction is admitted. Representation width and work must remain separate metrics.

Authority:

`research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_REPRESENTATION_WORK_ACCOUNTING.md`.

## Fifteen-step mathematics pass

The requested fifteen-step pass is recorded in

`research/v26/recovered-bit-puncturing-dac/V26_Q138_15_STEP_EXACT_PASS_REPORT.md`.

Key status:

- exact one-QR full-family sub-39 representation: PASS;
- rank-12 support selector: PASS;
- common parent span 47: PASS;
- epsilon-rank activation: correctly not triggered because exact route succeeded;
- full second-layer / `W_2`: not yet proved;
- arithmetic-work gain: not proved and current dense-work proxy is negative.

## Current sharp mathematical bottleneck

The first unfinished exact problem is now:

> Factor the physical mask-to-coefficient tensor in the fixed 47-dimensional common parent-interface basis, jointly with the rank-12 support sectors, and compose one more exact QR/layer without returning to separate per-mask bases.

Only after that should a two-QR width `W_2`, a round-depth law `W(R)`, or an arithmetic-work exponent be claimed.

A secondary one-QR optimization target remains lowering `38.754887502...`; the current two-factor maximum is not necessarily intrinsic, but a naive LCA/Steiner placement was worse and is only a scoped geometry falsifier.

`ALPHA_PASS=0` remains unchanged.

Still not admitted: practical exact QR evaluation at the formal maximum, exact end-to-end arithmetic-work reduction, complete second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.

## Measured-execution blocker

The frozen historical project-cap QR measurement remains blocked by the missing exact recovered V25 runtime bytes.

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Required identities:

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

This remains a provenance blocker, not a mathematical NO-GO.

After byte recovery: SHA-locked rematerialization -> prove exact historical cap semantics -> historical `19/19 PASS` -> frozen cap2 all-column QR regression -> only PASS opens cap3 under the existing resource gates.
