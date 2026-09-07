# V26 Q1.38 k9 B/C index-2 sensitivity

## Scope

This is an exact arithmetic sensitivity certificate for the separated-leaf k0..k9 convolution after the admitted uniform second-residue improvements

- B1 <= 748;
- C1 <= 936.

Keep the current A/D envelopes fixed and keep all B/C residues from index3 onward at the generic cap2048. Let

- `b = B2`;
- `c = C2`.

This file asks how small `b,c` would have to become for the current separated-leaf k0..k9 cumulative gate to fit under `2^44`.

It is not a lower bound on the true B2/C2 ranks, not a complete-tail theorem, and not a statement that only index2 can ever matter.

## Exact bilinear formula

Direct expansion of the four-leaf convolution gives

`F(b,c) = 15,892,005,024,640`

`       + 5,260,847,048 b`

`       + 3,952,624,408 c`

`       + 1,096,366 b c`,

where `F(b,c)=sum(k0..k9)` with B3+/C3+ fixed at2048.

The product gate is

`2^44 = 17,592,186,044,416`.

Therefore the feasible region is exactly

`F(b,c) <= 2^44`.

## Thresholds

The exact integer thresholds are severe.

### If C2 were eliminated completely

With `c=0`, the largest admissible B2 is

`b=323`.

`b=323` still passes by `927,423,272`, while `b=324` fails by `4,333,423,776`.

### If B2 were eliminated completely

With `b=0`, the largest admissible C2 is

`c=430`.

`c=430` passes by `552,524,336`, while `c=431` fails by `3,400,100,072`.

### Equal index-2 caps

If `b=c=t`, the largest integer value that passes is

`t=180`.

At `(180,180)`, cumulative k0..k9 is

`17,585,952,145,120`,

leaving margin

`6,233,899,296`.

At `(181,181)`, cumulative k0..k9 is

`17,595,561,404,702`,

which fails by

`3,375,360,286`.

### One side left generic

If C2 remains2048, solving the exact inequality gives formal threshold

`B2 <= -852`.

If B2 remains2048, it gives

`C2 <= -1465`.

Since ranks are nonnegative, these mean that **even setting the other index-2 contribution to zero cannot make k9 pass while one side remains generic2048**.

Indeed

- `(B2,C2)=(0,2048)` fails by `6,394,793,767,808`;
- `(2048,0)` fails by `9,074,033,735,528`.

## Consequence for the historical B direct-e2 support envelope1796

The clean historical structural theorem gives a B direct-e2 support-only left-frequency envelope <=1796. That result remains useful for understanding third-residue geometry, but it is nowhere near sufficient as a standalone k9 fix.

Even granting the unrealistically favorable `C2=0`, setting `B2=1796` gives a deficit

`7,748,300,278,432`.

With C2 left generic2048 the deficit is

`19,875,937,258,144`.

Therefore a research program that only tries to turn the B support-only1796 envelope into a complete B2<=1796 statement cannot solve the current k9 gate by itself.

## Research implication

The arithmetic strongly prioritizes one of the following over isolated modest index-2 improvements:

1. simultaneous and very large B2/C2 reductions;
2. reductions in B3/C3 and higher layers together with index2;
3. complete-leaf Schmidt compression that bypasses the separated residue table;
4. nonlocal/product-level cancellation or factorization.

This is a prioritization theorem about the present upper-bound architecture, not an impossibility theorem for the underlying object.
