# V26 Q1.38 k9 B748/C916 higher-residue sensitivity

## Status

Exact arithmetic sensitivity certificate for the separated-leaf k0..k9 convolution after the admitted index-1 envelopes

- `B1 <= 748`;
- `C1 <= 916`.

It updates the historical B748/C936 sensitivity table. It is not a lower bound on the true B/C higher-residue ranks, not a complete dyadic-tail theorem, and not a claim that separated-leaf residue summation is the only viable architecture.

`ALPHA_PASS=0`.

## Exact index-2 formula

Let

- `b = B2`;
- `c = C2`;

with B3+/C3+ kept at the generic cap 2048.

Direct expansion gives

`F(b,c) = 15,658,378,343,680`

`       + 5,177,652,568 b`

`       + 3,952,624,408 c`

`       + 1,096,366 b c`,

where `F(b,c)=sum(k0..k9)`.

The product gate is

`2^44 = 17,592,186,044,416`.

Hence the exact feasible region is `F(b,c) <= 2^44`.

Compared with the preceding B748/C936 formula, lowering C1 from 936 to 916 reduces both the constant term and the coefficient of B2. This changes the arithmetic target even though no new B2/C2 structural theorem has been proved.

## Exact index-2 thresholds

### C2 eliminated

With `c=0`, the largest admissible B2 is `B2 <= 373`.

At B2=373 the gate passes by `2,543,292,872`; B2=374 fails by `2,634,359,696`.

The previous B748/C936 threshold was 323, so the allowable B2 target increases by 50.

### B2 eliminated

With `b=0`, the largest admissible C2 is `C2 <= 489`.

At C2=489 the gate passes by `974,365,224`; C2=490 fails by `2,978,259,184`.

The previous threshold was 430, an increase of 59.

### Equal index-2 caps

For `b=c=t`, the largest passing integer is `t = 206`.

At `(206,206)`, cumulative k0..k9 is `17,585,740,788,312`, leaving margin `6,445,256,104`.

At `(207,207)`, cumulative k0..k9 is `17,595,323,864,446`, failing by `3,137,820,030`.

The previous common-cap target was 180.

### One side generic

If C2 remains 2048, the formal threshold is `B2<=-831`.

If B2 remains 2048, the formal threshold is `C2<=-1399`.

Both remain negative. Thus reducing only one side cannot make k9 pass while the other remains generic.

For example:

- `(B2,C2)=(0,2048)` fails by `6,161,167,086,848`;
- `(2048,0)` fails by `8,670,024,758,528`.

## Historical B direct-e2 envelope 1796

The historical B direct-e2 support-only envelope `<=1796` remains far from sufficient as a standalone k9 repair.

Even granting `C2=0`, B2=1796 still fails by `7,365,256,311,392`.

With C2 left generic 2048, the deficit is `19,492,893,291,104`.

So the structural priority remains a repeated higher-residue mechanism, a much stronger complete-leaf bound, or a nonlocal/product-level cancellation theorem.

## Repeated equal higher-residue caps

Set `B_i = C_i = t` for every `i=2..m`, with later B/C entries held at 2048.

The exact largest passing common caps are:

| Last improved index m | largest passing cap t |
| ---: | ---: |
| 2 | 206 |
| 3 | 588 |
| 4 | 643 |
| 5 | 649 |
| 6 | 650 |
| 7 | 650 |
| 8 | 650 |
| 9 | 650 |

The historical B748/C936 targets were `{2:180,3:568,4:623,5:630,6:631,7:631,8:631,9:631}`.

Thus C1=916 relaxes the repeated-cap target by 26 at index2, 20 at indices3-4, and 19 from index5 onward. A repeated structural lift around `<=650` through the B/C residues relevant to k9 would now suffice under this separated-leaf upper-bound architecture.

The number 650 is an arithmetic target, not a lower bound and not a necessity theorem.

## Authority and scope

Input arithmetic authority is PR #118 / main commit `6894f57860ff4295543fe5a1e8ad03c4738ecebb`, which certifies the exact B748/C916 k0..k9 convolution.

`scripts/verify_v26_q138_k9_bc748_916_sensitivity.py` recomputes the bilinear coefficients directly from the four-leaf convolution, verifies all boundary points, and exact-searches each repeated-cap threshold.

Promotion requires one clean-checkout successful CI run.

Not included:

- complete B2/C2 structural bounds;
- complete dyadic-tail theorem;
- W_repr reduction;
- arithmetic-work theorem;
- ranking/search or full-round claim.

`ALPHA_PASS=0`.
