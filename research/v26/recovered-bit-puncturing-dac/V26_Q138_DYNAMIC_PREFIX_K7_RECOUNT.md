# V26 Q1.38 dynamic prefix-through-k7 recount

## Scope

This corrects the interpretation of the older frozen-tail k7 search gate.

Use the current first two predecessor-leaf envelopes

A `[3,219,a2,2048,...]`,
B `[36,812,b2,2048,...]`,
C `[84,972,c2,2048,...]`,
D `[3,207,d2,2048,...]`.

When any index-2 rank `a2,b2,c2,d2` is improved, layers k2..k6 decrease together with k7. Therefore comparing the new k7 alone against the old frozen tail budget `5,520,647,809,024` is a conservative sufficient test, not a mathematical necessity statement.

The correct immediate dynamic partial-sum test is

`S_0..7(a2,b2,c2,d2) <= 2^44`.

This is still not a complete dyadic-tail theorem because k>=8 remains unresolved.

## Exact dynamic polynomial

Exact four-leaf convolution gives

`S_0..7 =`

`210 a2 b2 c2 +1056 a2 b2 d2 +399936 a2 b2`

`+848 a2 c2 d2 +257952 a2 c2 +1141248 a2 d2 +3127931904 a2`

`+222 b2 c2 d2 +58908 b2 c2 +412608 b2 d2 +1168937856 b2`

`+268128 c2 d2 +930192576 c2 +3188419584 d2`

`+2858783053824`.

All coefficients are nonnegative.

At the generic index-2 cap `(2048,2048,2048,2048)`,

`S_0..7 = 50,808,192,342,016 > 2^44`.

So third-residue improvement is still necessary somewhere.

## Correction to the frozen-tail interpretation

Set the A/D index-2 ranks to the ideal zero while leaving B/C generic:

`a2=d2=0`, `b2=c2=2048`.

Then

`S_0..6 = 1,809,267,529,728`,

`k7 = 5,595,612,708,864`,

and therefore

`S_0..7 = 7,404,880,238,592 < 2^44`

with remaining budget

`10,187,305,805,824`.

Thus B/C reduction is **not mathematically necessary merely to make the dynamically recounted prefix through k7 fit**. The older statement that B/C reduction was necessary applies only to the frozen old-tail sufficient gate.

Likewise, setting the direct A/D e2 pieces hypothetically to zero and retaining only the admitted inherited-correction envelopes

`a2=362`, `d2=171`, `b2=c2=2048`

gives

`S_0..7 = 10,598,653,759,488 < 2^44`.

Again this is only a hypothetical prefix-through-k7 diagnostic; actual A/D third residues still include unresolved direct-e2 parts.

## Conditional dynamic thresholds with B/C generic

With `b2=c2=2048` and `d2=0`, the largest A rank compatible with the dynamic prefix-through-k7 gate is

`a2=1902`;

`a2=1903` fails.

With `b2=c2=2048` and `a2=0`, the largest D rank is

`d2=1847`;

`d2=1848` fails.

If `a2=d2=x` while B/C remain generic2048, the largest equal A/D rank is

`x=706`.

These are conditional search thresholds, not full-tail necessity bounds.

## Equal four-leaf diagnostic

If all four index-2 ranks are equal to x, then the largest x with

`S_0..7 <=2^44`

is exactly

`x=1068`.

`x=1069` fails.

## Consequence

The immediate research gate must distinguish:

1. frozen-tail sufficient tests, useful for conservative search pruning;
2. dynamic prefix-through-k7 recounts, which correctly account for reductions in k2..k6;
3. the actual complete requirement, which still needs the full `sum_{k>=8}` tail.

No complete-factor, arithmetic-work, ranking/search, alpha, or full-round claim follows from this correction.
