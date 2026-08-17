# V26 q138 Constructive Double-Round Width-95 Theorem

## Statement

For the q138 fixed-output inverse-double-round five-QR star, there is an explicit exact factor-generation/contraction construction with peak structural message exponent

`W_2_construct <= 95`.

This is distinct from the tighter existence-only Schmidt representation bound `W_2_repr<=88`.

## Construction

Use the explicit 32-bit partition tree frozen in the HT construction. Keep the central fixed-output/open-four-input QR in its exact reduced graph representation. Contract each of the four diagonal fixed-input/single-output leaf QRs to its exact 32-bit output vector and factor that vector hierarchically on the same bit partition tree.

For every tree cluster `S`, the combined message exponent is

`b_center(S) + 4*min(|S|,32-|S|)`.

The complete explicit tree has maximum 95 on three clusters. Each maximum decomposes as

- central reduced graph boundary: 51;
- four exact leaf HT ranks: 44;
- total: 95.

## Factor generation

The four leaf vectors are not assumed free.

Each leaf can be generated from its original exact reduced QR network with path message exponent at most 44. The fully materialized output vector has only 32 binary coordinates, hence `2^32` entries. Exact hierarchical factorization can therefore be generated below the final `2^95` structural peak.

The central QR remains in its graph form, so no unproved central Schmidt-factor generation is required.

Thus 95 is a constructive structural upper bound, not merely an abstract factorization existence statement.

## Verification

Authority:

`scripts/verify_v26_q138_double_round_constructive95.py`.

Clean GitHub Actions run `32010784664`, job `95329682827`, passes.

## Relation to 88

A separate exact rank envelope replaces the central graph boundary by its physical matricization bound and yields `W_2_repr<=88`. That result proves existence of an exact representation but does not yet include a certified procedure for generating the central Schmidt factor within peak 88.

Therefore maintain two ledgers:

- constructive structural bound: `W_2_construct<=95`;
- exact representation existence bound: `W_2_repr<=88`.

## Scope

No arithmetic-work reduction, optimality, practical `2^95` evaluator, ranking gain, `alpha<1`, or full-round relevance is claimed.
