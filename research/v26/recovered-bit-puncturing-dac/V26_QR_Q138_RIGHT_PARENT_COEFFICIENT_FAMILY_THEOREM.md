# V26 q138 Right/Parent Coefficient-Family Theorem

## Statement

For the physical 12-control q138 width-40 right/parent geometry, order the controls as

`u1_3,u2_3,u1_4,u2_4,u1_5,u2_5,u1_6,u2_6,u1_7,u2_7,u2_8,u2_31`.

Clean exact rational computations prove:

1. the family of 4096 exact `64 x 64` right Gram matrices has linear span dimension

`145`;

2. after multiplication by the common exact 48-dimensional left interface row space, the family of 4096 parent coefficient matrices has linear span dimension

`124`;

3. the row directions of a fixed 124-matrix parent-family basis span the already admitted common parent interface space of dimension

`47`.

Thus one exact fixed-basis factorization is

`P_m = sum_{lambda=1}^{124} D(m,lambda) K_lambda`,

where `K_lambda` are fixed rational parent matrices and `D` is a `4096 x 124` exact mask-selector/coefficient tensor.

## Bilinear right-family structure

The right Gram construction factorizes across the five-site transfer chain into an 8-control site3--6 prefix object and a 4-control site7 closure object.

Exact family spans are

- prefix family rank: `140` out of 256 controls;
- closure family rank: `16` out of 16 controls.

The 2240 products of prefix/closure basis elements span only 145 independent right Gram matrices.

This independently explains the 145-dimensional right family without contracting 4096 unrelated networks.

Authority:

`scripts/verify_v26_qr_q138_right_bilinear_family_span.py`.

Clean Actions run `32008645947`, job `95323277617`.

## Parent-family span and TT profile

A separate exact verifier finds 124 independent physical parent matrices, reconstructs the witness basis over `Q`, and verifies exact coverage of all 4096 masks.

The family span first saturates at lexicographic mask index 2081.

For the natural 12-bit control order above, the exact prefix-flattening / tensor-train rank profile of the coefficient tensor `D(m,lambda)` is

`[2,4,8,16,32,64,128,119,196,136,143,124]`.

Hence the natural-order maximum TT bond is

`196`.

The exact fixed kernel from family sector to the `48 x U47` coordinates has shape

`124 x 48 x 47`

and, in the deterministic elimination basis used by the verifier, 31,491 nonzero rational entries.

The `4096 x 124` coefficient selector has 243,335 nonzero entries in that basis.

Authority:

`scripts/verify_v26_qr_q138_mask_coeff124_tt.py`.

Clean Actions run `32006391041`, job `95316690780`.

## Interpretation

The right/parent mask dependence is substantially compressed linearly:

- 4096 physical right controls -> right family dimension 145;
- after the common left interface action -> parent family dimension 124;
- parent interface directions -> common span 47.

However the natural bitwise TT is not uniformly low-bond: its maximum is 196. The family-rank 124 and TT maximum 196 measure different flattenings and are not contradictory.

This result also does not rescue the six-left-mask support/composition route: the separately verified complete left coefficient family has full rank 64.

## Next exact targets

1. optimize the 12 control-bit ordering or block/sector decomposition of `D`;
2. couple the 124-sector parent family to the actual inter-QR mask wiring rather than treating 124 as a generic second-layer bond;
3. exploit the exact double-round star representation bounds independently.

## Scope

No approximation is used. No arithmetic-work reduction, two-layer practical evaluator, optimal TT ordering, ranking gain, `alpha<1`, or full-round relevance is claimed.
