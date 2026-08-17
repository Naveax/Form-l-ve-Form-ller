# V26 q138 predecessor-leaf top-carry cancellation

## Statement

For a fixed-input predecessor q138 quarter-round leaf with one open 32-bit output word at position A, B, C or D, write an exact leaf coefficient as a sum over the four modular-addition carry-mask chains and the 128 internal masks `(u3,v3,u4,v4)`.

Every nonzero local Walsh transition contributes a dyadic factor `2^{-s}` where the current carry-mask bit `s` is binary. Since each of the four additions has current-carry variables only at bit positions0..30, the formal maximum total carry weight is124.

The formal weight124 sector has the following exact structure.

1. For output positions A and D it is impossible.
2. For output positions B and C, whenever the weight124 affine constraints are consistent for the fixed external masks/output beta, the internal 128-variable coefficient matrix has exact GF(2) rank124. Thus every nonempty weight124 fiber contains exactly16 internal assignments.
3. On the resulting four-dimensional internal nullspace, the Walsh sign phase has polar bilinear rank2. Consequently its signed quadratic Gauss sum over any affine fiber is one of

   `0, +8, -8`.

Therefore every weight124 contribution is either zero or `±8/2^124 = ±1/2^121`, while every lower-weight contribution already lies in `2^-123 Z`.

Hence every exact predecessor-leaf coefficient satisfies

`L(beta) in 2^-123 Z`.

Equivalently the formal denominator exponent124 is never needed. The top carry layer cancels by at least one dyadic bit globally, and by three bits whenever it occurs by itself.

This is an exact coefficient-arithmetic theorem. It does not by itself reduce the 11|21 Schmidt rank.

## 1. Local transition at maximum carry

For an interior bit the exact local transition is

`T(s,t,u,v,w) = 1[t=s xor u xor v xor w] * 1[s=1 or u=v=w] * (-1)^((u xor w)(v xor w)) * 2^-s`.

At bit0 the absent predecessor-carry leg is summed. At bit31 the current carry is fixed to zero.

Formal total carry weight124 means every current carry at bits0..30 of all four additions equals1.

Therefore:

- at bits1..30, predecessor and current carries are both1, so
  `u xor v xor w =0`;
- at bit31, current carry is0 while predecessor carry is1, and the `s=0` support rule forces
  `u=v=w=1`;
- bit0 imposes no parity equation beyond the already-fixed current carry1.

These are affine GF(2) constraints in the 128 internal masks and external fixed masks/output beta.

## 2. A and D are impossible at weight124

At j4 bit31, maximum carry requires the local output mask `w4_31=1`.

For a one-open-word predecessor leaf at output position A or D, the j4 output expression is identically zero at every bit because j4 exposes only the B/C output occurrences.

Thus `w4_31=0`, contradicting the required `w4_31=1`.

So weight124 has no A- or D-position assignments for any fixed external masks.

## 3. B/C internal fiber dimension

For B or C, form the linear coefficient matrix of all maximum-carry equations with respect to the internal variables

`u3_0..31, v3_0..31, u4_0..31, v4_0..31`.

The exact GF(2) rank is124 for both output positions.

External fixed masks and beta affect only the affine right-hand side. Therefore every consistent external choice has an affine internal solution space of dimension

`128-124=4`,

hence exactly16 internal assignments.

The verifier also checks explicit consistent B and C witnesses, so the sector is genuinely reachable.

## 4. Sign Gauss sum

For current carry1, the local sign exponent is

`q_i=(u xor w)(v xor w)`.

Summing over all four additions and bits0..30 gives one quadratic phase `q(x)` over GF(2) on the internal masks. Restrict q to the four-dimensional nullspace N of the maximum-carry coefficient matrix.

For B and C the polar form

`B(a,b)=q(a+b)+q(a)+q(b)+q(0)`

has exact rank2 on N. The polar matrix is the same for B and C.

Changing the external affine right-hand side or choosing another particular solution changes the restricted phase only by an affine-linear function on N; its polar form remains the same.

The verifier enumerates every affine-linear perturbation of the four-dimensional restricted quadratic form and obtains exactly the possible Gauss sums

`{0,-8,+8}`.

Thus every consistent weight124 fiber contributes a signed numerator divisible by8.

## 5. Dyadic denominator consequence

All terms of carry weight at most123 already lie in `2^-123 Z`.

The weight124 sector contributes

`0` or `±8*2^-124 = ±2^-121`,

which is also contained in `2^-123 Z`.

Therefore the complete exact predecessor-leaf coefficient lies in

`2^-123 Z`.

This conclusion is uniform over the fixed external input masks and over beta.

## Next object

After scaling a predecessor leaf by `2^123`, the parity tensor modulo2 receives no contribution from the weight124 sector: `±2^-121 * 2^123 = ±4` is even.

Hence the first parity layer relevant to a small exact 11|21 rank certificate is the carry-weight123 sector. Analyze that sector directly rather than materializing a 2048x2048 dense leaf matrix.

## Scope

Exact, `epsilon=0`.

No Schmidt-rank reduction, arithmetic-work reduction, practical evaluator, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance is claimed.
