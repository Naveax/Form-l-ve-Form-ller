# V26 Q1.38 dyadic five-layer prefix gate

## Scope

This theorem pushes the exact predecessor-leaf dyadic lifting hierarchy far enough to identify the first sharp tail budget for beating the existing S1 factor bound.

It does not bound the full residual tail. It proves that the first five product layers already fit below the old generic four-leaf `2^44` channel budget, while the next layer with only generic fallback does not.

## Per-leaf recursive rank envelopes

For every predecessor leaf, recursively write an integer-scaled coefficient matrix as

`M = K0 +2 K1 +4 K2 +... +2^t Rt`.

At every residual step, the S1 side has only `2^11=2048` rows, so its modulo2 residue has GF(2) rank at most2048 and can be lifted to an integer rational-rank-at-most2048 matrix.

Use the certified sharper initial layers:

A:

`r_A(0)=3`, `r_A(1)=309`, `r_A(k)<=2048` for `k>=2`.

D:

`r_D(0)=3`, `r_D(1)=310`, `r_D(k)<=2048` for `k>=2`.

B:

`r_B(0)=1052`, `r_B(k)<=2048` for `k>=1`.

C:

`r_C(0)=1160`, `r_C(k)<=2048` for `k>=1`.

No coefficient-specific B/C second-residue claim is used here.

## Four-leaf product convolution

For

`P=M_A tensor M_B tensor M_C tensor M_D`,

the rank bound for the dyadic product layer multiplying `2^k` is the coefficient of `x^k` in the product of the four per-leaf rank generating series.

Using the envelopes above gives:

| k | four-leaf layer rank bound | exponent |
|---|---:|---:|
|0|10,982,880|23.38875308074955...|
|1|2,306,905,824|31.10331196332947...|
|2|140,380,802,112|37.030554695987725...|
|3|2,067,939,590,144|40.91133118006878...|
|4|13,446,096,486,400|43.61225264073539...|
|5|49,193,897,820,160|45.483544603356634...|

The first five layers `k=0..4` sum to

`15,656,734,767,360`.

The generic four-leaf S1 Hilbert budget is

`2^44=17,592,186,044,416`.

Therefore the exact prefix `k=0..4` still fits below the generic budget, with remaining leaf-channel headroom

`2^44 -15,656,734,767,360`

`=1,935,451,277,056`.

Equivalently the multiplicative headroom is

`1.1236178108535686...`

or

`0.168151398415024...` bits.

The generic bound for layer5 alone is

`49,193,897,820,160 >2^44`,

so generic2048 fallback is no longer sufficient at that layer.

## Complete S1 prefix

The admitted central rank is

`R_center=3829*2^29=2,055,678,722,048`.

Multiplying the first-five-layer leaf prefix by the same exact center gives

`32,185,216,518,011,095,382,753,280`

channels, exponent

`84.73460054643513...`.

The current complete materialized-factor exponent is

`84.90275194485017...`.

Thus the first five exact dyadic layers sit

`0.16815139841503...`

bits below the current full-factor bound. This does not lower the full bound because the unresolved tail `k>=5` remains.

## Sharp next criterion

A complete dyadic improvement over the current generic four-leaf factor requires the entire remaining tail to satisfy

`sum_{k>=5} rank(layer_k) <1,935,451,277,056`.

The generic layer5 bound misses that tail budget by a factor about25.42 even before later layers are counted. Therefore the next mathematics must find coefficient-specific compression in higher leaf residues; merely continuing the universal2048 row cap cannot succeed.

This tail budget is now the sharp quantitative target for the dyadic route.
