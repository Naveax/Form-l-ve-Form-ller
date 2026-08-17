# V26 q138 Rank-12 Support-Selector Composition Bridge

## Purpose

The full physical q138 one-QR family now has an exact per-mask left-I9 support bound of at most 216 states and a complete global message-width certificate below 39. To compose this mechanism into a later QR/layer, the fixed-mask dependence itself must be represented without enumerating 64 unrelated support tables.

This note gives that exact bridge for the **support selector**.

## 1. Selector tensor

Let the six physical left fixed-mask bits be

`m in {0,1}^6`

in the same order used by the left-rank/support verifiers, and let

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

`C(m,i)=sum_{r=1}^{12} A(m,r) B(r,i)`

with rational, in fact integer, reconstruction coefficients for this chosen basis.

## 3. Coordinate support facts

Across all masks:

- maximum active `I9` states per mask: 216;
- distinct support sets: 13;
- union of active coordinates: 384;
- intersection: 96.

Thus there are two exact ways to carry the support condition into a later joint contraction:

1. a common coordinate envelope of 384 `I9` states;
2. an exact rank-12 mask/support selector factorization.

The rank-12 form is the stronger generative description of mask dependence.

## 4. Why this helps composition

When the six mask controls are fixed, the one-QR global certificate may use the mask-conditioned bond bound 216.

When those controls become summed or jointly represented in a later layer, blindly choosing one 216-state support set is invalid because the support class changes with the mask. The rank-12 selector provides an exact mechanism for carrying that dependence without enumerating 64 unrelated tables.

The selector has zero approximation error: assignments excluded by `C` are rigorously impossible in the local nonzero-support network.

## 5. Remaining composition blocker

This theorem controls only the **zero/nonzero support selector**. The exact parent Schmidt basis used by the rank-27 theorem may still depend on the fixed mask.

Therefore the next-layer joint contraction is not yet solved. The next sharp algebraic object is the common span/transfer representation of the mask-conditioned parent Schmidt spaces, or an equivalent joint coefficient tensor factorization.

Until that is solved, do not replace 64 mask-conditioned rank-27 factorizations by one universal rank-27 bond.

## 6. Relation to approximation

No epsilon-rank approximation is needed for this selector reduction. The selector factorization and the 384-state common coordinate envelope are exact, with residual `epsilon=0`.

The error-representation exponent `theta=log(r)/(-log(q))` is therefore not the appropriate metric for this exact branch because no nonzero residual decay parameter `q` is being used.

## 7. Verification

The rank, support-class, union/intersection and exact-rational selector checks are covered by

`scripts/verify_v26_qr_q138_left_i9_support216.py`.

The explicit basis above was independently reconstructed by exact rational row reduction; its reconstruction coefficients are all `-1`, `0` or `1`.

## 8. Scope

This is a composition bridge, not a complete second-layer theorem. It does not establish full second-layer contraction, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.