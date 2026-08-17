# V26 q138 Outer Input-Mask Parameter Status

## Statement

The q138 project object fixes the output-side coordinate `word 4, bit 10` (global bit index 138) for the backward exact one-/double-round Walsh analysis. It does **not** by itself fix a unique 128-bit outer input Walsh mask for the earliest four diagonal leaf QRs in the inverse double-round dependency cone.

Therefore source-specific leaf Schmidt ranks cannot be assigned one canonical numerical value unless an additional outer input mask `alpha` is frozen.

Do not infer `alpha=0` from the q138 output coordinate.

## Relation to the primary ChaCha puncturing paper

Flórez-Gutiérrez and Todo, “Improved Cryptanalysis of ChaCha: Beating PNBs with Bit Puncturing,” EUROCRYPT 2025 / ePrint 2025/437, use a differential-linear distinguisher with an output linear mask `Gamma` and define key-recovery maps through expressions of the form

`<Gamma, E_2^{-1}(...)>`.

Their attack sections freeze particular internal/output masks `Gamma` at specified round positions, for example the 3.5-round distinguisher. This does not identify the q138 project coordinate with one unique outer input Walsh mask of the separate exact two-round correlation tensor studied here.

The paper also does not use the project identifier `q138`.

Hence the paper does not supply the missing 128-bit leaf input-mask value for this project object.

## Consequence

The currently valid double-round bounds are parameter-free structural statements for any fixed outer input masks:

- topology path: `W_2_topo<=236`;
- constructive graph/leaf-HT representation: `W_2_construct<=95`;
- exact generic rank-envelope representation existence: `W_2_repr<=88`.

To improve 88 by actual leaf coefficient rank, the research must proceed in one of two ways:

1. freeze a concrete outer input mask `alpha` and compute source-specific leaf ranks;
2. prove a parametric/uniform rank theorem over a class of `alpha` values.

Until then, no source-specific leaf rank below the generic exponent 11 is admitted.

## Scope

This note is a parameter/scope clarification. It does not alter the q138 output mask, the one-QR results, or the double-round structural upper bounds.
