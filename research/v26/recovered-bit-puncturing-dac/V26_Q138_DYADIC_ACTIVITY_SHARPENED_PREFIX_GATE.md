# V26 Q1.38 dyadic activity-sharpened prefix gate

## Scope

This theorem recounts the four-predecessor-leaf dyadic product after the uniform A/D second-residue activity sharpening

`A1<=219`, `D1<=207`.

B/C first residues remain

`B0<=1052`, `C0<=1160`.

Every still-unresolved single-leaf residue uses only the universal S1 row-rank cap2048.

The result supersedes the earlier five-layer prefix search gate based on A1=309,D1=310. It still does not bound the complete dyadic tail.

## Per-leaf rank series used

A: `[3,219,2048,2048,2048,2048,...]`.

B: `[1052,2048,2048,2048,2048,2048,...]`.

C: `[1160,2048,2048,2048,2048,2048,...]`.

D: `[3,207,2048,2048,2048,2048,...]`.

The four-leaf layer rank bounds are the convolution coefficients of these four series.

## Revised product layers

The exact envelope gives

| layer k | four-leaf rank bound |
|---|---:|
|0|10,982,880|
|1|1,600,340,544|
|2|76,184,143,968|
|3|1,351,960,461,312|
|4|10,725,441,372,160|
|5|42,810,709,344,256|

Thus k0..k4 sum to

`12,155,197,300,864`.

The generic four-leaf S1 budget is

`2^44=17,592,186,044,416`.

The remaining exact leaf-channel headroom is therefore

`5,436,988,743,552`.

Equivalently the first-five prefix exponent is

`log2(12,155,197,300,864)=43.46663854464549...`,

leaving

`log2(2^44/prefix)=0.533361455354506...`

bits of multiplicative headroom.

The generic k5 envelope is still too large:

`42,810,709,344,256 /5,436,988,743,552 =7.87397424631923...`.

So coefficient-specific higher residues are still required, but the old25.417x deficit is reduced by more than a factor3.

## Complete S1 prefix

Using the admitted central rank

`R_center=3829*2^29=2,055,678,722,048`,

the complete-S1 k0..k4 prefix has at most

`24,987,180,453,681,406,486,249,472`

channels, exponent

`84.36939048949566...`.

This is

`0.53336145535451...`

bits below the current complete-factor exponent84.90275194485017. The unresolved tail prevents promotion of that gap to a new full representation or factor-generation bound.

## Revised tail criterion

A complete dyadic improvement now requires

`sum_{k>=5} rank(layer_k) <5,436,988,743,552`.

This supersedes the older tail target `1,935,451,277,056` that used A1=309,D1=310.

The previous depth-gate warning is also superseded as a search statement. Under the impossible optimistic assumption that the first unresolved quartet

`A2,D2,B1,C1`

all has rank0, the revised k5 is

`1,351,960,461,312`,

which is now below the new tail budget. Therefore the improved A/D early ranks return the search to a regime where strong compression of the next residue families can in principle make layer5 fit.

This does not say the full tail fits; later layers remain.
