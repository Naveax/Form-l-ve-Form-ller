# V26 Q1.38 k9 B/C index-2 and repeated-cap sensitivity

## Scope

This is an exact arithmetic sensitivity certificate for the separated-leaf k0..k9 convolution after the admitted uniform second-residue improvements

- B1 <= 748;
- C1 <= 936.

The first part keeps B3+/C3+ at the generic cap2048 and asks how small B2/C2 alone would have to become. The second part asks how the threshold changes if the same improved cap is obtained simultaneously across several consecutive B/C higher residues.

It is not a lower bound on the true B/C ranks, not a complete-tail theorem, and not a statement that dyadic residue work is the only viable architecture.

## Exact index-2 bilinear formula

Let

- `b = B2`;
- `c = C2`;

while B3+/C3+ remain2048. Direct expansion gives

`F(b,c) = 15,892,005,024,640`

`       + 5,260,847,048 b`

`       + 3,952,624,408 c`

`       + 1,096,366 b c`,

where `F(b,c)=sum(k0..k9)`.

The product gate is

`2^44 = 17,592,186,044,416`.

Therefore the feasible region is exactly

`F(b,c) <= 2^44`.

## Index-2-only thresholds

### If C2 were eliminated completely

With `c=0`, the largest admissible B2 is `323`.

`b=323` passes by `927,423,272`, while `b=324` fails by `4,333,423,776`.

### If B2 were eliminated completely

With `b=0`, the largest admissible C2 is `430`.

`c=430` passes by `552,524,336`, while `c=431` fails by `3,400,100,072`.

### Equal index-2 caps

If `b=c=t`, the largest integer value that passes is `t=180`.

At `(180,180)`, cumulative k0..k9 is

`17,585,952,145,120`,

leaving margin `6,233,899,296`.

At `(181,181)`, cumulative k0..k9 is

`17,595,561,404,702`,

which fails by `3,375,360,286`.

### One side left generic

If C2 remains2048, the formal threshold is `B2<=-852`.

If B2 remains2048, it is `C2<=-1465`.

Since ranks are nonnegative, even setting the other index-2 contribution to zero cannot make k9 pass while one side remains generic2048.

Indeed

- `(B2,C2)=(0,2048)` fails by `6,394,793,767,808`;
- `(2048,0)` fails by `9,074,033,735,528`.

## Consequence for the historical B direct-e2 support envelope1796

The clean historical structural theorem gives a B direct-e2 support-only left-frequency envelope <=1796. That result remains useful for understanding third-residue geometry, but it is nowhere near sufficient as a standalone k9 fix.

Even granting `C2=0`, setting `B2=1796` gives a deficit `7,748,300,278,432`.

With C2 left generic2048 the deficit is `19,875,937,258,144`.

Therefore a program that only turns the B support-only1796 envelope into a complete `B2<=1796` statement cannot solve the present k9 gate by itself.

## Repeated equal higher-residue caps

The picture changes substantially if one structured construction propagates through several consecutive B/C residues.

Set

`B_i = C_i = t`

for every `i=2..m`, while all later B/C entries remain2048. Exact binary search over the integer cap gives:

| Last improved index m | largest passing common cap t |
| ---: | ---: |
| 2 | 180 |
| 3 | 568 |
| 4 | 623 |
| 5 | 630 |
| 6 | 631 |
| 7 | 631 |
| 8 | 631 |
| 9 | 631 |

Each listed value passes and the next integer fails.

So the arithmetic target is not necessarily “force B2 and C2 near zero”. A repeated structured lift with roughly `<=631` caps through the B/C residues relevant to k9 would also suffice under the current separated-leaf architecture.

This makes two directions substantially more attractive than an isolated modest index-2 theorem:

1. a lift mechanism whose structural rank control repeats into later residues; or
2. a direct complete-leaf Schmidt bound around631 or below, which would bypass the residue-by-residue bookkeeping more cleanly.

The number631 is an arithmetic target for the present k9 upper-bound table, not a lower bound and not a claim that complete leaf rank631 is necessary.

## Research implication

The exact arithmetic prioritizes:

1. repeated B/C higher-residue structure rather than a one-off 1796-style index2 cap;
2. complete-leaf Schmidt compression if a direct invariant route can reach the ~631 scale;
3. nonlocal/product-level cancellation or factorization that bypasses separate leaf-residue summation.

This is a prioritization theorem about the current upper-bound architecture, not an impossibility theorem for the underlying object.
