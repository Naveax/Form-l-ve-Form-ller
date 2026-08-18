# V26 Q1.38 k7 A/D-only reduction no-go gate

## Scope

This is an exact dyadic-product search gate using the current predecessor-leaf envelopes

A `[3,219,a2,2048,...]`,
B `[36,812,b2,2048,...]`,
C `[84,972,c2,2048,...]`,
D `[3,207,d2,2048,...]`,

and the current unresolved tail budget

`T=5,520,647,809,024`.

It is not a complete-factor or arithmetic-work improvement.

## A/D-only reduction cannot make k7 fit

Set the unknown A/D index-2 ranks to the impossible ideal

`a2=d2=0`

while leaving B/C at the generic row cap

`b2=c2=2048`.

Exact four-leaf convolution at total index7 gives

`k7=5,595,612,708,864`.

Thus

`k7-T=74,964,899,840 >0`.

Therefore reducing only A/D third residues can never make the current k7 gate fit while B/C remain generic2048. Some B/C index-2 reduction is mathematically necessary.

## Equal B/C threshold under ideal A/D zero

With `a2=d2=0` and `b2=c2=x`, exact convolution gives

- `x=2009`: `k7=5,520,524,242,944 <T` by `123,566,080`;
- `x=2010`: `k7=5,522,449,121,280 >T` by `1,801,312,256`.

Hence the largest equal B/C index-2 rank compatible with k7 under ideal zero A/D third residues is exactly

`x=2009`.

## Threshold using only the admitted inherited A/D e1-correction envelopes

The clean inherited-correction theorem gives component bounds362 for A and171 for D. If, hypothetically, the direct e=2 components vanished completely, then set

`a2=362`, `d2=171`, `b2=c2=x`.

Exact convolution gives

- `x=1055`: `k7=5,519,255,787,951 <T` by `1,392,021,073`;
- `x=1056`: `k7=5,521,642,434,048 >T` by `994,625,024`.

So under that hypothetical direct-zero A/D scenario the exact equal B/C threshold is1055.

These threshold calculations are search criteria only. Actual A/D third residues still include unresolved direct e=2 terms, and the complete k>=7 tail remains open.
