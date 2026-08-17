# V26 q138 predecessor-leaf dyadic descent

## Exact statement

For every fixed external input mask and every open output mask beta, the exact predecessor-leaf coefficient satisfies

- output position A or D: `L(beta) in 2^-92 Z`;
- output position B or C: `L(beta) in 2^-121 Z`.

No approximation is used.

## A/D

At j4 the output expression is identically zero for A/D. Since the bit31 current carry is zero, the local support rule forces the predecessor j4 carry to zero; induction forces all31 j4 current-carry bits to zero. Hence total carry weight is at most93.

At the unique weight93 pattern, j1..j3 carries are all1 and j4 carries are all0. The internal GF(2) coefficient matrix on `(u3,v3,u4,v4)` has rank127/128 for both A and D. Every nonempty top fiber therefore has two assignments, so its signed numerator is even. Thus the top contribution is in `2^-92 Z`; lower weights already are.

## B/C weight124 and123

Weight124 has internal rank124, nullity4 and sign polar rank2. Every affine-fiber Gauss sum is `0` or `+/-8`, so weight124 lies in `2^-121 Z`.

For the124 one-zero carry sectors at weight123, the exact `(internal rank, nullity, sign-polar rank)` distribution is

- `(124,4,2)`:95;
- `(125,3,2)`:14;
- `(125,3,0)`:7;
- `(126,2,0)`:8.

The corresponding signed Gauss numerators are always divisible by4, hence every weight123 sector lies in `2^-121 Z`.

## B/C weight122

There are `C(124,2)=7626` two-zero carry sectors. Their internal rank distribution is

- rank124:4465;
- rank125:2058;
- rank126:1025;
- rank127:74;
- rank128:4.

All rank<=127 fibers have even size, hence even signed numerator.

The four rank128 sectors are exactly

- `(j1 bit0,j2 bit0)`;
- `(j1 bit0,j4 bit0)`;
- `(j2 bit0,j3 bit0)`;
- `(j3 bit0,j4 bit0)`.

After eliminating all128 internal variables, these four sectors leave one identical rank8 affine consistency system on `(A0,B0,C0,D0,beta)` for B, and likewise one identical system for C. Thus for any external assignment the four unique-solution sectors are either all absent or all present. If present, four signs sum to an even integer. Therefore the total weight122 contribution is in `2^-121 Z`.

All lower weights are individually in `2^-121 Z`, proving the B/C statement.

## Next algebra

Use position-dependent integer scalings `2^92` for A/D and `2^121` for B/C when constructing the next modulo2 predecessor-leaf Schmidt-rank certificate. Dense rational 2048x2048 materialization is unnecessary.
