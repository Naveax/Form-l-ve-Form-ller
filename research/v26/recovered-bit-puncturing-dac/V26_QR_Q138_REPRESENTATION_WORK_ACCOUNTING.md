# V26 q138 Representation / Work / Error Accounting

## Purpose

The full physical q138 one-QR family now has a complete exact structural message-width certificate below 39. This note keeps representation width, dense contraction work, approximation error and round depth separate.

That separation is mandatory: lowering the largest message does not automatically lower arithmetic work.

## 1. Exact representation result

Previous complete dense-message baseline:

`D_old = 2^40`.

New complete all-mask structural maximum:

`D_new = 216 * 2^31 = 463,856,467,968`.

Therefore the exact maximum-message reduction factor is

`D_old / D_new = 512/216 = 64/27 ~= 2.37037037037`.

Log-width gain:

`log2(64/27) ~= 1.24511249783653 bits`.

The new certified width is

`W_1 <= 38.75488750216347...`

for the q138 fixed-output one-quarter-round physical fixed-mask family.

## 2. Error

The support-216 reduction removes only nine-bit assignments that are impossible in the Boolean nonzero-support projection of the exact minimal-TT network.

Hence the residual introduced by this pruning is

`epsilon = 0`.

The parent rank-27 and common-span-47 results are also exact rational algebra.

No epsilon-rank approximation is used in the admitted one-QR reduction.

## 3. Formal dense tree-work diagnostic

As a scoped diagnostic, compare two trees **after** the mask-conditioned parent rank factorization is treated as already available:

A. the previous source topology with the parent Schmidt bond enlarged to the safe full-family dimension 27;
B. the new support-216 width-optimized tree.

For each binary tree contraction, define the naive dense local operation size as the product of dimensions of the union of the two child-message boundary indices. Sum this quantity over internal contractions.

This is only a formal dense contraction-work proxy. It excludes the cost of constructing the rank/support factors themselves and is not an end-to-end complexity theorem.

For topology A:

- formal summed dense operation count: `36,464,139,277,420,602`;
- `log2 ~= 55.0173278584`.

For topology B:

- formal summed dense operation count: `145,280,691,954,501,690`;
- `log2 ~= 57.0116205922`.

Thus the width-optimized tree has about

`3.9842073564 x`

larger naive dense tree-work in this comparison, a penalty of about

`1.9942927338` log2 work bits.

The largest single dense operation also increases in this specific comparison.

## 4. Interpretation

The current exact result is therefore a genuine **representation/message-width** gain but not an arithmetic-work gain.

This is not a contradiction. The support-216 factorization introduces an additional nonbinary bond and changes the association order. It lowers the maximum retained message while some contractions touch larger unions of auxiliary indices.

FDS accounting must keep these axes separate:

- representation / peak message: improved;
- approximation error: zero;
- naive dense tree work: worse in the current width-optimized tree;
- factor-generation work: not yet fully accounted;
- round depth: certified only for one QR object;
- end-to-end attack exponent: not admitted.

## 5. Current round-depth status

The certified quantity is a one-QR fixed-output structural bound, denote it `W_1`:

`W_1 <= 38.75488750216347...`.

There is not yet a certified `W_2` for two composed QR layers and therefore no admitted recurrence or asymptotic law `W(R)`.

The common parent span 47 and rank-12 support selector provide the exact coordinate bridge needed to begin that composition, but they do not determine separator growth by themselves.

## 6. Alpha / attack claims

`ALPHA_PASS=0` remains unchanged.

No claim is admitted for

- exact arithmetic-work exponent reduction;
- `alpha<1`;
- full second-layer contraction;
- four-inverse-round exact energy;
- ranking reduction;
- full-round relevance.

## 7. Next work-accounting target

Once the mask-to-common-span-47 coefficient transfer tensor is factorized and one more QR is composed, record separately:

1. representation size / peak message;
2. total compact factor storage;
3. dense/sparse arithmetic operations;
4. factor-generation work;
5. exact residual or certified error;
6. separator growth with round depth.

Only after those quantities are simultaneously controlled should an arithmetic-work or attack-exponent claim be considered.