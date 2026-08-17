# V26 q138 Left Coefficient-Family Full-64 Theorem

## Statement

Keep the six physical left fixed-mask controls explicit in the order

`u1_8,u1_9,u1_10,u2_8,u2_9,u2_10`.

For each of the 64 masks, let `L_m` be the exact rational 64-leaf left-child coefficient map across its 16 external binary indices and six parent-interface bits.

Clean-checkout exact arithmetic proves

`dim_Q Span{L_m : m in {0,1}^6} = 64`.

Thus the 64 physical left-mask coefficient matrices are linearly independent. There is no nontrivial linear family compression of these six mask controls at the level of the complete left coefficient map.

## TT consequence

For the natural mask-bit order, the exact prefix-flattening/TT profile of the family-selector tensor is

`[2,4,8,16,32,64]`.

The maximum is therefore 64. Every successive bit doubles the exact family dimension; no mask bit is redundant in this representation.

Conditioning on the shared control `u2_8` gives two exact family spans

- `u2_8=0`: rank 32;
- `u2_8=1`: rank 32.

This is the expected halving from fixing one binary control, not an additional algebraic collapse.

## Relation to interface rank

Each individual `L_m` still has exact interface row rank 48. The theorem concerns the span across different masks, not the rank of one fixed-mask map.

Hence these statements coexist:

- fixed mask: `rank(L_m)=48`;
- mask family: `rank_family({L_m})=64`.

## Consequence for composition

The revoked rank-12 support-selector route cannot be replaced by a hidden low-rank coefficient selector on the complete left map. An exact next-layer construction must either

1. keep the six left mask bits as explicit binary legs;
2. exploit structure only after coupling them to the right/next-layer operator;
3. or find a nonlinear/block/sector representation not equivalent to a low linear family rank.

In particular, multiplying a hypothetical compressed support sector by a common coefficient basis is not valid.

## Verification

Authority:

`scripts/verify_v26_qr_q138_left_coeff_family_tt.py`.

Clean GitHub Actions run `32007243536`, job `95319150194`, passes with

- exact family rank 64;
- selector shape `64 x 64`, 93 nonzero coefficients in the chosen elimination basis;
- TT profile `2,4,8,16,32,64`;
- `u2_8` conditioned family ranks `32,32`;
- fixed-map interface row rank 48 for every mask.

No floating tolerance or approximation is used.
