# V26 Q138 Fourier/Gauss-sharpened seven-layer dyadic gate

Use the current predecessor-leaf dyadic envelopes

A: `[3,219,2048,2048,...]`,

B: `[36,1016,2048,2048,...]`,

C: `[84,1220,2048,2048,...]`,

D: `[3,207,2048,2048,...]`.

The B/C second entries are the exact integer-lift envelopes from `V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_RANK1016_1220`. Unresolved higher residues use only the universal 11|21 row cap 2048.

Exact four-leaf convolution gives

- `k0 = 27,216`;
- `k1 = 5,028,048`;
- `k2 = 352,812,816`;
- `k3 = 12,065,376,240`;
- `k4 = 221,554,487,136`;
- `k5 = 2,288,332,406,784`;
- `k6 = 13,588,911,456,256`.

Therefore

`sum_{k=0}^6 r_k = 16,111,221,594,496`.

The generic four-leaf S1 Hilbert budget is

`2^44 = 17,592,186,044,416`.

Thus the first seven exact dyadic layers fit with residual leaf-channel budget

`1,480,964,449,920`.

The leaf-prefix exponent is

`log2(16,111,221,594,496) = 43.87313112059728...`.

Attaching the exact center `3829*2^29` gives a complete-S1 seven-layer prefix exponent

`84.77588306544745...`,

which is `0.12686887940272...` bits below the current complete-factor exponent

`84.90275194485017...`.

This does **not** lower `W_repr(1)` or `W_factor-gen`, because the unresolved `k>=7` tail must still fit inside `1,480,964,449,920` leaf channels.

With every unresolved single-leaf higher residue replaced by the generic cap 2048, the next product layer is

`k7 = 48,838,228,148,224`,

which is about `32.9773` times the entire remaining tail budget. The search therefore moves one dyadic layer deeper: the next task is to sharpen A/D third residues, B/C third residues, or exploit cross-leaf/product-level cancellation sufficiently to control the full `k>=7` tail.
