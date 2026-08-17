# V26 q138 signed constructive left-factor bridge

Scope: constructive generation/storage on the **row/left side** of the d=1 signed S1/S2 factorizations. This theorem deliberately does not claim a full constructive bound below95; the complement/right factor remains the active blocker.

## S1

The exact signed theorem supplies two occurrence-closed local ranks:

- block1: matrix shape `32 x 64`, rank16;
- block2: matrix shape `8192 x 2^18`, rank2784.

Dense exact rank factors can therefore be chosen with storage envelopes

- block1 U: `32*16=2^9`;
- block1 V: `16*64=2^10`;
- block2 U: `2^13*2784`, exponent `24.4429434958...`;
- block2 V: `2784*2^18`, exponent `29.4429434958...`.

Thus every local signed factor needed for the S1 decomposition is explicitly generable/storable below `2^30` scalars.

The S1 central rank envelope is

`R1=16*2784*2^26=87*2^35`.

A complete dense left factor indexed by the 44 S1 physical input-mask bits and the central rank channel therefore has

`2^44 * R1 = 87*2^79`

entries, exponent

`79+log2(87)=85.44294349584872... <94`.

## S2

The exact top-sector ranks sum to

`1984=31*2^6`,

and the remaining29 raw row bits give

`R2=31*2^35`.

The complete dense S2 left factor has

`31*2^79`

entries, exponent

`79+log2(31)=83.95419631038688... <94`.

## Consequence

The coefficient-aware signed factorizations do not fail constructive94 because of left-factor generation or storage. The only unresolved part is an explicit complement/right-side factor graph and contraction tree that preserves the signed rank bonds without materializing the old coefficient-blind 51-bit central boundary.

This is a one-sided constructive bridge, not a full evaluator or a claim that `W_2_construct<=94`.

Verifier:

`scripts/verify_v26_q138_signed_constructive_left_bridge.py`.
