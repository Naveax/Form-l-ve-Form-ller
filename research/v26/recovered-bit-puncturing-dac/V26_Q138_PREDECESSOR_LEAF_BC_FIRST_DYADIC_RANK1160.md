# V26 Q1.38 predecessor-leaf B/C first dyadic residue

## Scope

This is an exact coefficient-arithmetic theorem for the predecessor one-QR leaf at output positions B and C across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

The previous dyadic-descent theorem proved

`L_B(beta),L_C(beta) in 2^-121 Z`.

Define the integer-scaled leaf

`M_B=2^121 L_B`, `M_C=2^121 L_C`.

This note bounds the GF(2) communication rank of the first parity residue `M mod2`. It does not bound the rational Schmidt rank of the complete leaf.

## Which carry weights can survive modulo2

For a fixed carry sector of weight `w`, let `S` be its signed internal Gauss sum. Its contribution to `M` is

`2^(121-w) S`.

Only weights124,123,122,121 can affect parity.

### Weight124

The all-one carry sector has internal rank124, nullity4 and sign polar rank2. Its Gauss sum is `0,+8,-8`, so after division by8 its parity is exactly the nonzero-Gauss affine indicator. The radical has dimension2.

### Weight123

The one-zero sectors have classes

- `(rank124,nullity4,polar2)`:95, parity vanishes after division by4;
- `(rank125,nullity3,polar2)`:14, nonzero-Gauss indicator survives;
- `(rank125,nullity3,polar0)`:7, parity vanishes;
- `(rank126,nullity2,polar0)`:8, nonzero-Gauss indicator survives.

Thus22 weight123 affine indicators survive.

### Weight122

The exact class distribution is

- `(124,4,2)`:4465;
- `(125,3,2)`:1372;
- `(125,3,0)`:686;
- `(126,2,0)`:1025;
- `(127,1,0)`:74;
- `(128,0,0)`:4.

After division by2, only the74 nullity-one equal-sign indicators and the four unique-solution sectors can affect parity.

The four rank128 sectors are

`((j1,bit0),(j2,bit0))`,
`((j1,bit0),(j4,bit0))`,
`((j2,bit0),(j3,bit0))`,
`((j3,bit0),(j4,bit0))`.

They have one identical external affine support. If their unique-solution sign phases are `q1..q4`, their combined half-integral contribution is

`(1/2) sum_k (-1)^qk`.

Modulo2 this equals `q1 xor q2 xor q3 xor q4` on the common support.

### Weight121

The all-one homogeneous system has rank124 and a4-dimensional internal nullspace. Setting one carry bit to zero adds exactly two homogeneous restrictions on that nullspace. Therefore rank of every three-zero sector can be decided inside a4D quotient matroid rather than by a fresh128D rank computation.

Exactly484 three-zero patterns span all four quotient dimensions and hence have internal rank128.

Full affine consistency leaves

- B: all484 reachable;
- C:480 reachable; four are globally inconsistent.

Each reachable sector contributes its affine support indicator modulo2.

## Exact affine cancellations

For a linear support indicator across the S1|complement split, let

`d = dim(im H_S1 intersect im H_comp)`.

For every fixed predecessor input word, its communication rank is at most `2^d`.

Collect all affine indicator contributions from weights121, the74 weight122 nullity-one sectors, the22 weight123 sectors and the weight124 top sector. Canonical row reduction exposes exact mod2 cancellations between identical support systems.

### Position B

Raw affine terms:581.

After cancelling even multiplicities,103 distinct support indicators remain, with intersection distribution

- `d=2`:9;
- `d=3`:63;
- `d=4`:31.

Hence their total communication-rank upper bound is

`9*4 +63*8 +31*16 =1036`.

### Position C

Raw affine terms:577.

Again103 odd-multiplicity support indicators remain:

- `d=2`:2;
- `d=3`:60;
- `d=4`:41.

Hence

`2*4 +60*8 +41*16 =1144`.

## Four-sector signed term

The common support of the four weight122 unique-solution sectors has intersection dimension2, hence support communication rank at most4.

After exact symbolic internal elimination, the quadratic phase

`q1 xor q2 xor q3 xor q4`

has S1/complement cross-bilinear rank2 for both B and C.

A quadratic Boolean matrix with cross-bilinear rank `r` has rank at most `r+2` on one rectangle. Decomposing the common support into at most4 rectangles therefore gives

`rank <=4*(2+2)=16`.

## Result

Therefore

`rank_F2((2^121 L_B) mod2 across S1) <=1036+16 =1052`,

`rank_F2((2^121 L_C) mod2 across S1) <=1144+16 =1160`.

Both are strictly below the generic single-leaf dimension `2^11=2048`.

This is a genuine coefficient-level non-saturation theorem for the first B/C dyadic layer, but it is not a rational leaf Schmidt-rank reduction: higher 2-adic residues may introduce additional channels.

## Next object

Choose a low-rank integer lift `M0` of this parity layer and analyze

`M1=(2^121 L-M0)/2`.

The arithmetic-work route becomes interesting only if enough successive dyadic layers remain compact and can be fused into the central D16 common/private decomposition before a complete low/high Cartesian basis is formed.
