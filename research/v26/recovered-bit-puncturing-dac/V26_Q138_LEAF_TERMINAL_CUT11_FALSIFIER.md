# V26 q138 Leaf Terminal-Cut-11 Falsifier

## Statement

On each of the three critical 11|21 partitions attaining the double-round HT88 bound, the reduced fixed-input/single-output leaf QR topology has terminal min-cut exponent exactly

`11`.

Thus the reduced leaf topology cannot certify a Schmidt rank smaller than the generic physical output-side bound `2^11` on those partitions.

## Reduced leaf graph

For every local output position A/B/C/D, the exact fixed-input/single-output QR reduction has the same inter-bit skeleton after the allowed cyclic relabeling:

- four parallel sigma path bonds;
- one cyclic offset-8 family;
- one cyclic offset-12 family;
- one physical open output bit at each site.

For a critical site subset `S`, attach source terminals to output bits in `S` and sink terminals to output bits in the complement, each with unit capacity. Internal graph capacities are the exact binary bond multiplicities.

## Result

For all three HT88 maximizing partitions, max-flow/min-cut gives

`11`.

The smaller physical side has 11 output bits, so the trivial physical Hilbert-space rank exponent is also 11. The topology saturates that cap.

Hence the route

`HT88 -> refine/generic leaf topology -> rank exponent <11`

is closed on the critical partitions.

## What remains possible

This is not an actual coefficient-rank lower bound. A particular fixed leaf input Walsh mask can produce a leaf vector whose true 11|21 Schmidt rank is smaller than `2^11` because of coefficient-specific algebraic cancellation.

The q138 repository authority currently specifies the fixed/open boundary pattern for the double-round theorem but does not freeze one concrete 128-bit outer leaf-input mask value for all four leaves. Therefore no source-specific leaf rank is asserted here.

To lower 88 safely, one must either

1. freeze the exact outer input mask(s) and compute actual leaf Schmidt ranks;
2. prove a uniform coefficient-level leaf rank theorem for a class of input masks;
3. prove actual central coefficient rank below `2^44`;
4. or exploit joint central/leaf cancellation beyond independent envelope multiplication.

## Verification

Authority:

`scripts/verify_v26_q138_leaf_terminal_cut11_falsifier.py`.

Clean GitHub Actions run `32010227963`, job `95328022119`, passes with terminal cuts `11,11,11`.

## Scope

Topology/rank-envelope falsifier only. No practical work bound, tensor-rank lower bound, attack lower bound, `alpha` claim or full-round result.
