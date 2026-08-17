# V26 q138 Depth Law with Semi-Open Signed A/C Compression

## Scope

This theorem updates the exact common-tree representation/message upper bound for fixed outer input masks and inverse-double-round depth `d>=2`.

It combines three previously separate exact ingredients on the common-tree maximizer

`S3={4,5,11,12,13,19,20,21,27,28,29}`:

1. central QR joint-sector rank `<=24,663,038,400`;
2. fully-open QR signed fused-channel rank `<=189*2^56`;
3. the new four-semi-open product rank `<=98415*2^203`.

The four earliest fixed-input/output-vector kernels still contribute exponent `4*44=176` on the S3 11|21 split.

## Exact bound

For every `d>=2`, the S3/common-complement message dimension is bounded by

`24,663,038,400 * (98415*2^203) * 2^176 * (189*2^56)^(8d-12)`.

Hence

`W_repr(d) <= log2(24,663,038,400) + 379 + log2(98415) + (8d-12)log2(189*2^56)`.

Recounting every node of the frozen common tree shows S3/complement still attain the maximum for `d=2,...,9`; the same affine extension applies for all larger `d` because each added inverse double round contributes eight fully-open QRs and the S3 fully-open exponent remains the common-tree maximum.

Numeric affine form:

`W_repr(d) <= 508.4979393937686... d - 332.6386869947327...`.

Verified values:

- `d=2`: `684.3571917928045...`;
- `d=3`: `1192.855131186573...`;
- `d=4`: `1701.3530705803416...`;
- `d=5`: `2209.85100997411...`;
- `d=6`: `2718.348949367879...`;
- `d=7`: `3226.8468887616473...`;
- `d=8`: `3735.344828155416...`;
- `d=9`: `4243.842767549185...`.

The slope is unchanged from the preceding fully-open signed theorem:

`508.4979393937686...` bits per inverse double round.

The intercept improves by

`0.413409398622235...` bits,

coming entirely from exact A/C semi-open signed rank compression.

## Authority

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_SEMI_OPEN_S3_SIGNED_AC_THEOREM.md`;
- `scripts/verify_v26_q138_semi_open_s3_signed_ac.py`;
- `scripts/verify_v26_q138_depth_semi_open_signed_intercept.py`.

## Limitations

This remains an exact representation/message upper bound. It does not provide a constructive evaluator at that peak, an arithmetic-work exponent, a ranking reduction, `alpha<1`, or a full-round cryptanalytic claim.

Orientations B and D still use the generic exponent55. Further semi-open improvement therefore requires B/D signed structure or multi-site/global coupling not captured by the occurrence-closed pair factorization.
