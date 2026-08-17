# V26 Q1.38 predecessor-leaf B/C half-sector lift Pareto NO-GAIN

## Scope

The four weight122 unique-solution sectors share one affine support and have sign bits `q1..q4`. Their current first dyadic parity lift uses

`p=q1 xor q2 xor q3 xor q4`

and costs at most20 rational rank. The resulting second-bit correction is the Boolean function

`f=1` iff the number of negative signs is0,3,or4.

This note asks whether one can modify only this local four-sector first lift to obtain an intermediate tradeoff: slightly larger first-layer rank but much smaller second correction.

## Complete16-state lift family

Any integer first lift with the same parity can be written locally as

`K=p+2h`

for an arbitrary Boolean function h on the16 possible sign states. The residual second bit becomes

`g=f xor h`.

There are exactly `2^16=65536` choices of h.

For any Boolean function on `(q1..q4)`, use its exact4-bit Walsh support. On the common affine support:

- support intersection dimension is2, hence at most4 affine rectangles;
- for each Walsh character indexed by subset S, the exact S1/complement cross-bilinear rank `r_S` is known from the four sign phases;
- a sign character contributes rank at most `2^r_S` per rectangle.

Thus each h gives certified first/second rank-envelope pair `(R0(h),R1(h))`.

## Exact exhaustive Pareto result

Enumerating all65536 Boolean h gives the same Pareto frontier for B and C:

`(R0,R1)=(20,2048)`

and

`(R0,R1)=(2048,0)`.

There is no Pareto-minimal intermediate point under this exact local Walsh/cross-rank certificate.

The first point is the current cheap parity lift. The second absorbs the complete half-sector correction into the first layer at the generic2048 row cap.

## Consequence

Within this local four-sign lift family and this exact rectangle/Walsh rank certificate, there is no useful gradual tradeoff between first- and second-layer rank. Any improvement must exploit structure not represented by the independent Walsh-character rank envelope, such as assembled right-coefficient cancellation, predecessor-input restrictions, cancellation against other correction sectors, or a product-level regrouping.

This is a method-scope NO-GAIN, not a proof that the true half-sector correction rank is2048.
