# V26 q138 Rank-12 Support-Selector Composition Bridge

## Purpose

The full physical q138 one-QR family has an exact per-mask left-I9 support bound of at most 216 states and a complete global message-width certificate below 39. To compose this mechanism into a later QR/layer, the fixed-mask dependence must be represented without 64 unrelated support tables.

This note gives the exact bridge for the **support selector** and records how it combines with the now-proved common parent-interface span 47.

## 1. Selector tensor

Let the six physical left fixed-mask bits be

`m in {0,1}^6`

and let

`i in {0,1}^9`

index the nine `I9` boundary bits.

Define

`C(m,i)=1`

when `i` is feasible in the Boolean nonzero-support projection of the exact minimal-TT left child for mask `m`, and zero otherwise.

`C` is a `64 x 512` exact binary matrix.

## 2. Exact rank

Exact rational elimination gives

`rank_Q(C)=12`.

The 13 distinct support rows also span a 12-dimensional space.

One valid set of 12 independent mask rows is

- `000000`;
- `000001`;
- `000010`;
- `000011`;
- `000100`;
- `000101`;
- `001000`;
- `001010`;
- `001100`;
- `010100`;
- `011100`;
- `011101`.

One valid set of 12 pivot nine-bit columns is

- `000000000`;
- `000000001`;
- `000000010`;
- `000000011`;
- `000000100`;
- `000000101`;
- `000000110`;
- `000001001`;
- `000001100`;
- `000100000`;
- `000100001`;
- `000100100`.

Using those basis rows/pivot columns, every one of the 64 selector rows is an exact linear combination of the 12 basis rows with coefficients only in

`{-1,0,1}`.

Therefore an exact factorization exists

`C(m,i)=sum_{r=1}^{12} A(m,r) B(r,i)`.

The verifier now checks this explicit factorization, not only the rank number.

## 3. Coordinate support facts

Across all masks:

- maximum active `I9` states per mask: 216;
- distinct support sets: 13;
- union of active coordinates: 384;
- intersection: 96.

Thus two exact support representations are available:

1. a common coordinate envelope of 384 `I9` states;
2. an exact rank-12 mask/support selector factorization.

The rank-12 form is the stronger generative description of mask dependence.

## 4. Parent-interface composition result

The physical rank-envelope theorem now proves that all 4096 mask-conditioned parent Schmidt/interface spaces lie in one fixed exact 47-dimensional rational subspace of the canonical 64-dimensional interface coordinate.

Therefore next-layer composition has two fixed exact ingredients:

- a rank-12 support-feasibility selector;
- a fixed 47-dimensional parent-interface ambient basis.

The stronger hypothesis that one universal rank-27 parent basis works for every mask is false: the exact union span is 47.

## 5. Remaining composition blocker

The common span itself is no longer the blocker.

The unresolved tensor is the **mask-to-coefficient transfer inside the fixed 47-dimensional parent-interface basis**.

The next task is to determine its exact TT/rank/sector structure and compose those sectors with the rank-12 support selector before applying another QR layer.

Do not multiply `12*47` and call it a universal coefficient rank without proving the coupling structure. The two auxiliary descriptions control different aspects of the tensor.

See also:

`V26_QR_Q138_JOINT_MASK_COMPOSITION_BRIDGE47.md`.

## 6. Relation to approximation

No epsilon-rank approximation is needed. The selector factorization, the 384-state coordinate envelope and the common parent span 47 are exact; support pruning has residual

`epsilon=0`.

The error-representation exponent is therefore not the active metric for this branch.

## 7. Verification

Support authority:

`scripts/verify_v26_qr_q138_left_i9_support216.py`.

It checks the support distribution, 13 classes, union/intersection, exact rank 12, the explicit 12 pivot rows/columns and reconstruction coefficient alphabet `{-1,0,1}`.

Common parent-span authority:

`scripts/verify_v26_qr_q138_physical_rank_envelope27.py`.

## 8. Scope

This is an exact composition bridge, not a complete second-layer theorem. It does not establish full second-layer contraction, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.