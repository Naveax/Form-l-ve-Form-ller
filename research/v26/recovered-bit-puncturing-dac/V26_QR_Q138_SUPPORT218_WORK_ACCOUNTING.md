# V26 q138 Corrected Support-218 Work Accounting

## Exact representation result

For the full 4096-case physical one-QR family, the corrected exact peak-message bound is

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... < 39`.

Relative to `2^40`, the exact peak-message reduction factor is

`2^40 / (218*2^31) = 256/109 ~= 2.3486238532`.

The reduction is exact: `epsilon=0`.

## Scoped dense-work diagnostic

Treat the mask-conditioned rank factorization as already available. For each binary tree contraction, use the product of dimensions in the union of the two child boundary index sets as a naive dense operation-size proxy, then sum over internal contractions.

Clean exact bookkeeping gives:

Previous rank-27 source topology:

- summed dense proxy: `36,464,139,277,420,602`;
- largest dense operation: `6,777,421,455,360`.

Corrected support-218 width-optimized tree:

- summed dense proxy: `146,442,453,764,374,842`;
- largest dense operation: `118,413,610,991,616`.

Ratio:

`4.0160678967339065`.

Log2 work penalty:

`2.005783962701019` bits.

## Interpretation

Peak representation/message width improves, while this particular dense-work proxy worsens by about fourfold. Therefore no arithmetic-work reduction follows from the current width certificate.

This is not paradoxical. The extra support bond lowers retained message size but changes contraction associations and creates larger dense unions at some operations.

The diagnostic also excludes factor-generation cost and ignores potential sparse arithmetic. It is not an end-to-end operation-count theorem.

## Authority

`scripts/verify_v26_qr_q138_support218_work_accounting.py`

Clean GitHub Actions run `32007505575`, job `95319924803`.

## Status

- representation/peak-message: improved;
- exact error: zero;
- current naive dense work: worse;
- sparse work: unresolved;
- factor-generation work: unresolved;
- `ALPHA_PASS=0` remains unchanged.
