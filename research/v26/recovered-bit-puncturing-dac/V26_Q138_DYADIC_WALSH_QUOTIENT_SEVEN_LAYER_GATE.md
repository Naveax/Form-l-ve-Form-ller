# V26 Q138 Walsh-quotient seven-layer dyadic gate

Use the current predecessor-leaf dyadic envelopes

A: `[3,219,2048,2048,...]`,

B: `[36,812,2048,2048,...]`,

C: `[84,972,2048,2048,...]`,

D: `[3,207,2048,2048,...]`.

The B/C second entries use the exact Walsh-quotient second-lift theorem. Unresolved higher residues use only the universal 2048 row cap.

Exact four-leaf convolution gives

- `k0 = 27,216`;
- `k1 = 4,793,472`;
- `k2 = 315,450,720`;
- `k3 = 9,979,784,064`;
- `k4 = 171,359,156,304`;
- `k5 = 1,703,063,715,840`;
- `k6 = 10,186,815,307,776`;
- generic `k7 = 38,736,654,106,624`.

The first seven layers sum to

`12,071,538,235,392 < 2^44`.

Thus the unresolved `k>=7` leaf-channel budget is

`5,520,647,809,024`.

Attaching the exact center `3829*2^29` gives

`24,815,204,292,884,195,564,322,816`

channels for the seven-layer prefix, exponent

`84.3594267039546...`.

This is `0.54332524089557...` bits below the current complete-factor exponent `84.90275194485017...`.

The generic k7 fallback is still too large:

`38,736,654,106,624 / 5,520,647,809,024 = 7.0166863467...`.

Therefore no complete-factor bound changes yet. The next exact task is to control the full `k>=7` tail.

A useful revised depth observation is that if all four index-2 residues were zero while every deeper residue stayed at the generic cap, then

`k7 = 1,703,063,715,840 < 5,520,647,809,024`.

So unlike the superseded 1016/1220 envelope, the current 812/972 envelope makes progress on the *next* single-leaf residues sufficient in principle to fit k7. Actual nonzero index-2 ranks must still be bounded, and the complete later tail remains open.
