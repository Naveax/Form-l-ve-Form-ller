# V26 q138 Fifteen-Step Exact Mathematics Pass Report

## Scope

This report closes the requested fifteen-step mathematics-first pass. Code was used only to reconstruct exact tensor objects, falsify hypotheses and verify finite exact claims.

The starting admitted one-QR full-physical-family bound was `W<=40`, with a conditioned `u2_31=1` subfamily certificate at `39.044394119...`.

The pass ends with a stronger all-physical-mask exact representation bound

`W <= 38.75488750216347... <39`,

plus a rank-12 support selector, a common parent-interface span of dimension 47, and explicit work/error accounting.

## 1. Analyze the 230-leaf conditioned maximum — PASS

The previous conditioned maximum `528*2^30` was reconstructed exactly.

Its 230-leaf cluster is a 229-leaf outside child plus the old left rank factor. The nine binary indices between them are

`v4_8, v4_9, v4_10, sig4_18, sig3_10, v3_21, v3_22, aux_j2_i10_k2, sig1_10`.

The temporary maximum is therefore strongly localized.

## 2. Topology-only Schmidt bound — PASS / NO FREE BIT

A topology-only terminal min-cut on the exact 64-leaf left child was computed for the relevant `I9 | (O7,J6)` split.

The cut capacity is about `12.5849625` bits, so topology alone does not provide the desired `<=8`-bit separator.

This route was falsified as a free topological reduction.

## 3. Exact algebraic/support deficiency — PASS

Coefficient calculations showed strong rank deficiency in representative cases, but the stronger uniform statement came from support algebra.

Boolean-semiring projection of the exact minimal-TT nonzero support onto `I9` gives at most 216 feasible assignments for every physical left mask.

Thus

`rank_{I9|rest} <=216<256`

uniformly.

## 4. Cross the clean `W<=39` threshold — PASS, stronger than requested

A single binary-degree reduction would have sufficed. The exact support result provides the stronger replacement `512 -> <=216` on the relevant nine-bit side.

## 5. Reinsert the deficiency globally — PASS

The left parent factor was split exactly as

`I9 -- RL216 -- (O7,RP)`.

This factorization was inserted back into the complete rank-528-compressed q138 network.

## 6. Complete global certificate — PASS

For the full physical family, using the safe uniform parent bond `RP27`, a complete deterministic contraction tree was verified with

- 368 leaves;
- 367 internal nodes;
- maximum message `216*2^31`;
- `W<=38.75488750216347...`.

This is a complete tree result, not an isolated separator.

## 7. Separate rank classes 5/6/7/8 — PASS / NO FURTHER GAIN IN THIS TREE

The conditioned `u2_31=1` parent ranks 5, 6, 7 and 8 were each substituted into the support-216 tree.

All four classes have the same maximum `216*2^31` because the parent Schmidt bond is internal to the maximizing `XB-Z` pair.

Thus rank-class splitting does not improve the current message maximum by itself.

## 8. Extend to the full physical `rank<=27` family — PASS

Replacing the conditioned rank-8 bond by the safe all-mask rank-27 bond leaves the same maximum `216*2^31`.

Therefore the sub-39 result applies to all 4096 physical fixed-mask cases, not only `u2_31=1`.

## 9. Isolate the new residual bottleneck — PASS

The new maximum is a two-factor `XB-Z27` node whose boundary is

- 31 binary indices;
- one dimension-216 support bond.

The internal parent Schmidt bond is already contracted and does not appear in the maximum.

A naive LCA/Steiner placement of the new factors was tested and gave a worse width, so that geometry was rejected. This is a scoped falsifier, not a lower bound on future trees.

## 10. Classify mask dependence / common basis — PASS

The 64 left masks produce 13 distinct `I9` support sets.

Support facts:

- maximum per mask: 216;
- union: 384;
- intersection: 96;
- all six left mask bits are required to determine exact support-set identity.

The exact `64 x 512` support-selector matrix has rational rank 12.

Additionally, exact 4096-case transfer closure proves that all parent Schmidt/interface spaces lie in one fixed 47-dimensional common span inside the canonical 64-dimensional interface coordinate.

## 11. Stronger common representation — PASS

Two exact common representations are now available:

1. support dependence: rank-12 selector with explicit basis and coefficients in `{-1,0,1}`;
2. coefficient/interface ambient space: one fixed 47-dimensional rational parent-interface space.

The stronger naive hypothesis “one universal rank-27 basis works for every mask” is falsified: the exact union span is 47, not `<=27`.

## 12. Activate epsilon-rank if exact rank stalls — CONDITION FALSE, CORRECTLY NOT ACTIVATED

The exact route did not stall. It produced support-216, selector-rank-12, common-span-47 and a complete full-family sub-39 tree.

Therefore activating approximation here would only weaken the result.

## 13. Certified residual-Gram error — NOT REQUIRED; EXACT RESIDUAL IS ZERO

Support pruning removes only impossible assignments. Its residual is

`epsilon=0`.

No residual-Gram budget is required for the admitted branch. Existing residual-Gram/tail machinery remains available if a future exact composition stalls.

## 14. Move toward the next QR / second layer — COMPOSITION BRIDGE PASS; FULL SECOND LAYER NOT SOLVED

The exact next-layer coordinate problem was advanced substantially:

- mask-dependent support is represented by an exact rank-12 selector;
- all mask-conditioned parent interface spaces share one fixed 47-dimensional ambient space.

This eliminates mask-specific ambient basis switching and gives a well-defined exact joint-mask starting representation.

The remaining next-layer object is the mask-to-coefficient transfer tensor **inside the fixed 47-dimensional basis**, and its compatibility with the rank-12 support sectors.

A complete two-QR / second-layer contraction and a certified `W_2` are not yet proved. This is the new sharp blocker.

## 15. Tie the result to FDS metrics — PASS WITH A NEGATIVE WORK RESULT

Representation / message width:

- old maximum: `2^40`;
- new maximum: `216*2^31`;
- reduction factor: `64/27 ~=2.37037037`;
- log-width gain: `log2(64/27) ~=1.2451124978` bits.

Error:

- exact, `epsilon=0`.

Formal dense tree-work diagnostic, treating rank factors as already available:

- previous rank-27 source topology summed dense proxy: `36,464,139,277,420,602`;
- new width-optimized support-216 tree: `145,280,691,954,501,690`;
- new tree is about `3.9842073564x` worse on this proxy.

Therefore the current result is a **representation/message-width improvement, not an arithmetic-work improvement**.

Round depth:

- one-QR bound `W_1<=38.754887502...` is certified;
- no certified `W_2` or recurrence `W(R)` yet.

`ALPHA_PASS=0` remains unchanged.

## Final status of the fifteen-step pass

Closed positively by exact theorem/certificate: steps 1, 3, 4, 5, 6, 7, 8, 9, 10, 11 and 15.

Closed by scoped falsification: step 2 and the naive LCA geometry inside step 9.

Correctly not activated because their trigger condition is false: steps 12 and 13.

Advanced to an exact composition bridge but not a complete second-layer theorem: step 14.

## New canonical research front

The first unfinished mathematical problem is now:

> Factor the physical mask-to-coefficient tensor in the fixed 47-dimensional common parent-interface basis, jointly with the rank-12 support sectors, and then compose one more exact QR layer without returning to 64 separate mask factorizations.

Only after that object is understood should a two-QR width `W_2`, a round-depth law, or an arithmetic-work exponent be claimed.
