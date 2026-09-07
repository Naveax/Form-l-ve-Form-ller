# V26 Q138 sharpened k9 convolution

## Status

Arithmetic certificate for the currently admitted predecessor-leaf envelopes. This file does not claim a new B/C higher-residue bound, a complete dyadic-tail theorem, a lower `W_repr(1)`, arithmetic-work improvement, `ALPHA_PASS=1`, or full-round relevance.

The admitted leaf envelopes used here are

- A `[1,41,564,1761,2048,...]`;
- B `[36,812,2048,2048,...]`;
- C `[84,972,2048,2048,...]`;
- D `[1,20,173,838,1958,2048,...]`.

Their mathematical provenance remains in the separate A/D universal carry-offset, A direct-e3, and B/C authority files. The purpose of this certificate is narrower: record the exact four-sequence convolution after replacing the previously used A index3 cap2048 by the clean theorem cap1761.

## Exact convolution

For each total valuation layer `k`, the subadditive four-leaf bound is

`sum_{i+j+q+r=k} A[i] B[j] C[q] D[r]`.

The exact sharpened coefficients through k9 are

- k0 `3,024`;
- k1 `287,664`;
- k2 `12,038,592`;
- k3 `291,137,584`;
- k4 `4,539,375,120`;
- k5 `48,676,699,184`;
- k6 `374,710,427,136`;
- k7 `2,128,245,966,160`;
- k8 `9,095,463,451,808`;
- k9 `29,952,328,904,800`.

Hence

`sum(k0..k8)=11,651,939,386,272`.

Against the current product gate budget

`2^44=17,592,186,044,416`,

the exact remaining margin after k8 is

`5,940,246,658,144`.

Therefore k8 still passes, with a larger margin than the preceding non-sharp certificate.

However

`sum(k0..k9)=41,604,268,291,072 > 2^44`,

so k9 still fails. Equivalently the k9 layer alone exceeds the entire remaining k8 margin by

`24,012,082,246,656`.

## Comparison with the superseded non-sharp arithmetic table

The preceding clean dynamic arithmetic used A index3=2048 and had

`sum(k0..k8)=12,320,846,080,000`.

The A e3=1761 theorem reduces the certified k0..k8 total by exactly

`668,906,693,728`.

It also reduces the k9 layer by

`2,059,014,328,224`,

but that is nowhere near enough to make k9 pass while B/C index2 remain at2048.

## Authority semantics

`scripts/verify_v26_q138_sharpened_k9_convolution.py` contains exact integer assertions for every k0..k9 coefficient, both cumulative totals, the k8 margin, and the k9 deficit.

Promotion to canonical arithmetic authority requires a clean-checkout successful CI execution of that verifier. Until such a run exists, the numbers in this file are a proposed certificate, not frozen authority.

Even after a clean run, the interpretation remains limited: the sharpened arithmetic proves only that the current admitted envelopes pass through k8 and fail at k9. It does not prove that the true k9 rank is large, because sharper B/C higher-residue representations or nonlocal/product cancellation may still reduce it.

## Next mathematical target

The arithmetic isolates the blocker cleanly. Further A3 bookkeeping is no longer the useful direction. Progress must reduce the B/C-heavy k9 contribution, most plausibly through

1. a genuinely stronger B/C index2/index3 lift that survives the existing direct-e1 full-rank/cancellation obstructions; or
2. a nonlocal/product-level cancellation or factorization theorem that bypasses separate leaf-residue rank summation.
