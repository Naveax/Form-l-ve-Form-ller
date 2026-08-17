# V26 q138 Double-Round Generic Leaf Storage Accounting

## Purpose

The exact double-round HT construction reduces separator/message width by hierarchically factorizing each fixed-input/single-output diagonal leaf as a 32-bit vector. This note asks a different question: does the same generic factorization also reduce factor storage?

## Exact generic counts

An arbitrary 32-bit leaf vector has

`2^32 = 4,294,967,296`

scalar coefficients.

For the explicit frozen HT tree used by the q138 double-round construction, assign every tree edge the generic exact rank

`2^min(|S|,32-|S|)`.

Summing the scalar entries of all leaf physical matrices and all transfer cores gives, for one leaf,

`4,308,611,904`

scalar slots, with

`log2 ~= 32.00457600827341`.

The largest individual HT core already contains

`2^32`

scalars, at the 21-bit cluster whose children have sizes 10 and 11.

For four generic leaves, the corresponding scalar upper bound is

`17,234,447,616`,

with

`log2 ~= 34.00457600827341`.

## Interpretation

The generic HT construction improves **separator geometry**, not generic storage.

Indeed, the vector space of arbitrary 32-bit leaf vectors has dimension `2^32`, so any uniform linear parametrization capable of representing every such vector needs at least `2^32` scalar degrees of freedom. The explicit HT tree is slightly above this information-dimension floor.

Therefore a storage improvement requires coefficient-specific structure of the ChaCha leaf family, such as actual Schmidt-rank deficiency for the relevant fixed input masks. Generic Hilbert-space rank bounds alone cannot provide it.

## Verification

Authority:

`scripts/verify_v26_q138_double_round_storage_accounting.py`.

Clean GitHub Actions run `32011044811`, job `95330454582`, passes with the exact counts above.

## Scope

This is factor-storage accounting only. It does not measure arithmetic operations needed to construct the factors and does not alter the message-width results `W_2_construct<=95` or `W_2_repr<=88`.
