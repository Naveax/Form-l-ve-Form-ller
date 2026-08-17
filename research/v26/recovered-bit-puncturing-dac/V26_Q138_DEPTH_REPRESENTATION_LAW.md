# V26 q138 Multi-Double-Round Representation Law

## Scope

This note gives a finite-depth exact **representation/message** upper bound for a fixed outer input-mask coefficient family. It is not an arithmetic-work law.

## One double round

For `d=1`, use the sharper five-QR result

`W_repr(1) <= 88`.

A fully constructive graph-plus-leaf-factor version has `W_construct(1)<=95`.

## Common 32-bit partition tree for deeper layers

Use the explicit tree obtained by relabeling the HT tree with

`[17,1,0,15,18,8,3,6,30,31,22,5,2,25,9,10,16,19,12,27,26,11,21,28,20,14,13,29,24,4,23,7]`.

On this one fixed tree, the fully-open QR graph/rank envelope has maximum exponent 67.

For `d>=2`, the q138 backward dependency cone can be layered as

- one final fixed-output/open-four-input central QR;
- four input-open/single-output QRs in the next half-round;
- `8d-12` fully-open interior QRs;
- four earliest fixed-input/all-four-output kernels, each an exact 128-bit vector.

For a cluster `S` with `m=min(|S|,32-|S|)`, define

- central cap: `min(b_central(S),4m)`;
- semi-open cap: `min(b_central(S),5m)`;
- fully-open cap: `min(b_open(S),8m)`;
- earliest fixed-input output-vector cap: `4m` per QR.

Because all layers use the same bit partition tree, inter-layer equality wires are local to tree clusters and do not add independent separator dimensions.

Thus for `d>=2`

`w_d(S) <= c4(S) + 4*c5(S) + (8d-12)*c8(S) + 16m`.

The explicit tree satisfies

- `max_S c8(S)=67`;
- `max_S w_2(S)=708`.

Every additional double round contributes at most eight additional fully-open QRs, hence at most `8*67=536` exponent units on the same tree.

Therefore

`W_repr(d) <= 536d - 364`, for `d>=2`.

The verifier checks the explicit formula directly for `d=2,...,8`; the linear extension follows from the uniform fully-open bound 67.

## Result

The admitted exact representation bounds are therefore

- `W_repr(1)<=88`;
- `W_repr(d)<=536d-364` for `d>=2`.

In particular

- d=2: `<=708`;
- d=3: `<=1244`;
- d=4: `<=1780`.

These are substantially sharper than the old coarse topology laws based on a 90-bit fully-open QR path bound.

## Verification

Authority:

`scripts/verify_v26_q138_depth_representation_law.py`.

Clean GitHub Actions run `32010718604`, job `95329479157`, passes.

## Limitations

This is a structural representation/message bound for fixed outer input masks. It does not imply efficient arithmetic work. The bound is not claimed optimal, and it does not constitute an attack exponent or a ranking algorithm.

The one-double-round `88` mechanism does not simply repeat with depth because after the first backward half-round the four branches merge through full-state QR layers. The piecewise law above explicitly accounts for that layer-type change.
