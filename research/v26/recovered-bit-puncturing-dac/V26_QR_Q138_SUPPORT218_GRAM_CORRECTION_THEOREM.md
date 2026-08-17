# V26 q138 Exact I9 Gram-Support Correction

## Status

This note supersedes the previously admitted `support<=216`, `13 support classes`, and rank-12 mask/support-selector claims.

Those older claims came from Booleanizing nonzero entries of a particular TT-core factorization and projecting path existence. Once the width-40 certificate JSON was repaired and the verifier chain was run from a clean repository checkout, that Booleanized-core verifier did not reproduce its own frozen expected distribution.

The correct exact support object is the Gram diagonal of the actual rational left-child map.

## Exact definition

For each physical six-bit left fixed-mask choice `m`, let

`L_m(i,r)`

be the exact 64-leaf left-child coefficient map, where `i` is the nine-bit `I9` coordinate and `r` denotes all remaining left-child boundary coordinates.

Define

`g_m(i) = sum_r L_m(i,r)^2`.

All coefficients are rational/dyadic, hence `g_m(i)>=0`, and

`g_m(i)>0` iff the `I9=i` row of the exact coefficient map is genuinely nonzero.

This test is immune to signed cancellation and does not replace TT-core coefficients by Boolean path indicators.

## Exact 64-mask result

Clean-checkout exact computation gives

- support minimum: 117;
- support maximum: 218;
- distinct support sets: 64;
- union of active I9 coordinates: 392;
- intersection: 42;
- exact rational rank of the `64 x 512` mask/support indicator matrix: 64.

Therefore every physical left mask obeys

`rank_{I9|rest}(L_m) <= 218 < 256`.

The exact support selector has full row rank 64, so there is no nontrivial linear selector compression across the 64 physical left-mask cases in this coordinate representation.

## Global consequence

The prior global tree topology remains valid after replacing the incorrect auxiliary support bond dimension 216 by the correct safe dimension 218.

The corrected maximum message is

`218 * 2^31 = 468,151,435,264`,

hence

`W_1 <= log2(218*2^31) = 38.768184324776925... < 39`.

Thus the clean sub-39 one-QR result survives, slightly weakened numerically.

Authority:

- `scripts/verify_v26_qr_q138_left_i9_gram_support.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json`;
- `scripts/verify_v26_qr_q138_general_rank27_support218_global_sub39.py`.

## Revoked consequences

Do not use the older claims

- support maximum 216;
- 13 exact support classes;
- union 384;
- intersection 96;
- mask/support selector rank 12;
- rank-12 support-sector composition bridge.

They are not authority for subsequent mathematics.

## Scope

This correction changes the support/composition branch, not the separately derived parent rank envelope `5..27`, the right-map transfer construction, or the historical width-40 tree. Those dependencies must be verified independently from clean checkout before further composition claims are admitted.
