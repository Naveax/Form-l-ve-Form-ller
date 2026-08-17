# V26 Q1.38 dyadic Fourier-sharpened six-layer gate

## Scope

This theorem recounts the exact four-predecessor-leaf dyadic product after two uniform coefficient improvements:

- A/D second-residue envelopes `A1<=219`, `D1<=207`;
- B/C explicit Fourier-aligned first-layer integer lifts `B0<=36`, `C0<=84`.

All still-unresolved single-leaf residues use only the universal S1 row-rank cap2048.

The result supersedes the earlier activity-sharpened prefix gate based on B0=1052,C0=1160. The complete dyadic tail remains unresolved, so no full d=1 representation or work bound is lowered here.

## Per-leaf rank series

Use

A: `[3,219,2048,2048,2048,...]`,

B: `[36,2048,2048,2048,2048,...]`,

C: `[84,2048,2048,2048,2048,...]`,

D: `[3,207,2048,2048,2048,...]`.

The rank envelope for product layer k is the coefficient of `x^k` in the product of these four series.

## Revised product layers

Exact convolution gives

| k | four-leaf layer rank bound |
|---|---:|
|0|27,216|
|1|6,076,512|
|2|528,287,760|
|3|22,588,489,728|
|4|499,782,844,416|
|5|5,718,621,093,888|
|6|33,271,289,282,560|

The exact prefix k0..k5 sums to

`6,241,526,819,520`.

The generic four-leaf S1 Hilbert budget remains

`2^44=17,592,186,044,416`.

Therefore the unresolved leaf-tail budget is now

`17,592,186,044,416 -6,241,526,819,520`

`=11,350,659,224,896`.

The six-layer prefix exponent is

`log2(6,241,526,819,520)=42.50503612695195...`,

leaving

`log2(2^44/prefix)=1.49496387304805...`

bits of multiplicative headroom.

The generic k6 envelope is still too large but only by

`33,271,289,282,560 /11,350,659,224,896`

`=2.931220876544714...`.

This replaces the previous7.87x k5 deficit and the much older25.4x deficit.

## Complete S1 six-layer prefix

Attach the admitted exact center

`R_center=3829*2^29=2,055,678,722,048`.

The complete-S1 k0..k5 prefix has at most

`12,830,573,875,979,191,540,776,960`

channels, exponent

`83.4077880718021...`.

This is

`84.90275194485017... -83.4077880718021...`

`=1.49496387304807...`

bits below the current complete-factor exponent. The unresolved k>=6 tail prevents promotion of this headroom to a full representation/factor-generation bound.

## New sharp tail criterion

A complete dyadic improvement over the current generic four-leaf factor requires

`sum_{k>=6} rank(layer_k) <11,350,659,224,896`.

The generic2048 fallback fails already at k6 by a factor2.9312, so coefficient-specific higher residues are still necessary.

The high-value next objects are now the first unresolved residuals

- `A2,D2`: third A/D dyadic residues;
- `B1,C1`: second B/C dyadic residues built from the explicit Fourier-aligned lifts.

Because the deficit is only2.93x, moderate simultaneous compression of these next residues can materially change the gate; the search no longer needs the extreme reductions implied by the old prefix accounting.
