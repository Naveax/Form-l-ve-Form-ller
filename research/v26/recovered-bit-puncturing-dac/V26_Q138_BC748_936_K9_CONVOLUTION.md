# V26 Q1.38 B748/C936 k9 convolution

## Status

Arithmetic certificate for the currently admitted predecessor-leaf dyadic envelopes after the clean uniform B/C second-residue improvement.

This file does **not** claim a complete dyadic-tail theorem, a lower `W_repr(1)`, arithmetic-work improvement, `ALPHA_PASS=1`, ranking/search improvement, or full-round relevance.

The admitted leaf envelopes used here are

- A `[1,41,564,1761,2048,...]`;
- B `[36,748,2048,2048,...]`;
- C `[84,936,2048,2048,...]`;
- D `[1,20,173,838,1958,2048,...]`.

The B/C index-1 improvements are the clean uniform relaxed-scalar result from PR104 / authority run `34134200886`.

## Exact convolution

For total valuation layer `k`, use the same subadditive four-leaf convolution

`sum_{i+j+q+r=k} A[i] B[j] C[q] D[r]`.

The exact coefficients through k9 are

- k0 `3,024`;
- k1 `280,992`;
- k2 `11,542,464`;
- k3 `275,107,184`;
- k4 `4,247,967,584`;
- k5 `45,333,814,960`;
- k6 `348,805,355,152`;
- k7 `1,987,672,008,800`;
- k8 `8,552,484,855,456`;
- k9 `28,420,855,930,176`.

Hence

`sum(k0..k8)=10,938,830,935,616`.

Against

`2^44=17,592,186,044,416`,

the exact remaining margin after k8 is

`6,653,355,108,800`.

So k8 still passes.

However

`sum(k0..k9)=39,359,686,865,792 > 2^44`,

and the exact k9 deficit is

`21,767,500,821,376`.

Thus the current separated-leaf residue envelope still fails at k9.

## Improvement over the preceding 812/972 arithmetic

The previous sharpened table with B1=812 and C1=972 had

- `sum(k0..k8)=11,651,939,386,272`;
- k8 margin `5,940,246,658,144`;
- k9 layer `29,952,328,904,800`;
- cumulative k0..k9 `41,604,268,291,072`;
- k9 deficit `24,012,082,246,656`.

The new uniform B/C lift improves

- k0..k8 cumulative by `713,108,450,656`;
- k9 layer by `1,531,472,974,624`;
- cumulative k0..k9 and the k9 deficit by `2,244,581,425,280`.

This is a real arithmetic improvement but not enough to cross the k9 gate.

## Authority semantics

`scripts/verify_v26_q138_bc748_936_k9_convolution.py` contains exact integer assertions for all k0..k9 coefficients, both cumulative totals, the k8 margin, the k9 deficit, and the comparison to the superseded 812/972 arithmetic table.

Promotion to canonical arithmetic authority requires one clean-checkout successful CI execution of that verifier. The interpretation remains arithmetic-only even after that clean run.

## Next target

The new 748/936 result lowers the pressure on k9 but does not change the structural diagnosis: further progress needs either a stronger B/C higher-residue construction, overlap-aware inherited-correction lift, complete-leaf Schmidt reduction, or a nonlocal/product-level cancellation theorem. Repeating dimension-only dyadic closure cannot solve this because the saturated-complement theorem already closes that route.
