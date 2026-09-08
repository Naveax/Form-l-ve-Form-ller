# V26 Q1.38 B748/C916 k9 convolution

## Status

Exact arithmetic certificate consuming the admitted index-1 leaf envelopes after PR #117:

- A `[1,41,564,1761,2048,...]`;
- B `[36,748,2048,2048,...]`;
- C `[84,916,2048,2048,...]`;
- D `[1,20,173,838,1958,2048,...]`.

The B/C inputs come from the clean frozen verifier in PR #117: B uses the canonical grouped-e0 plus exact-linear-image relaxed-half construction, while C uses the reachable-joint grouped-e0 plus the same relaxed-half construction.

This note is arithmetic-only. It does not claim a complete dyadic-tail theorem, a lower `W_repr(1)`, arithmetic-work improvement, `ALPHA_PASS=1`, ranking/search improvement, or full-round relevance.

## Exact convolution

For total valuation layer `k`, use

`sum_{i+j+q+r=k} A[i] B[j] C[q] D[r]`.

The exact coefficients through k9 are:

- k0 `3,024`;
- k1 `280,272`;
- k2 `11,483,584`;
- k3 `273,032,624`;
- k4 `4,207,035,504`;
- k5 `44,830,527,280`;
- k6 `344,669,648,352`;
- k7 `1,964,027,333,680`;
- k8 `8,456,851,951,776`;
- k9 `28,140,806,593,696`.

Hence

`sum(k0..k8)=10,814,871,296,096`.

Against

`2^44=17,592,186,044,416`,

the exact remaining margin after k8 is

`6,777,314,748,320`.

So k8 still passes.

However

`sum(k0..k9)=38,955,677,889,792 > 2^44`,

and the exact k9 deficit is

`21,363,491,845,376`.

Therefore the separated-leaf residue envelope still fails at k9.

## Improvement over B748/C936

The immediately preceding admitted arithmetic table had

- `sum(k0..k8)=10,938,830,935,616`;
- k8 margin `6,653,355,108,800`;
- k9 layer `28,420,855,930,176`;
- cumulative k0..k9 `39,359,686,865,792`;
- k9 deficit `21,767,500,821,376`.

Replacing only C1 `936 -> 916` improves

- k0..k8 cumulative by `123,959,639,520`;
- k8 margin by `123,959,639,520`;
- k9 layer by `280,049,336,480`;
- cumulative k0..k9 and the k9 deficit by `404,008,976,000`.

This is a strict arithmetic improvement, but it does not cross the k9 gate.

## Authority

Structural input authority: PR #117, merged main commit `43575c5717407603b5c23098a8022613c4c2b559`; frozen verifier run `34214203191`, job `102021989964`.

`scripts/verify_v26_q138_bc748_916_k9_convolution.py` contains exact integer assertions for every k0..k9 coefficient, the k8 cumulative and margin, the k9 cumulative and deficit, and the differences from both the B748/C936 and B812/C972 arithmetic tables.

Promotion of this arithmetic table to repository authority requires one clean-checkout successful CI execution of that verifier.

## Next target

The new C1 improvement moves the arithmetic sensitivity thresholds but does not change the structural diagnosis. The next useful calculation is to recompute the exact B2/C2 and repeated-higher-residue thresholds under B1=748, C1=916. That determines how much third-and-later residue structure is now required to make k9 pass.

`ALPHA_PASS=0`.
