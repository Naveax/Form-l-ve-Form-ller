# V26 q138 Exact Double-Round Nonlinear-Support Bound

## Statement

For the q138 fixed-output inverse-double-round five-QR star, the previously certified HT88 tree admits a strictly smaller exact representation-existence bound once the nonlinear modular-addition support law is used on its critical central partitions:

`W_2_repr <= 86 + log2(3) = 87.58496250072116... < 88`.

Equivalently the maximum message dimension in this representation is at most

`3 * 2^86`.

This improves the generic-envelope representation bound 88. It does **not** improve the currently explicit constructive factor-generation ledger `W_2_construct<=95`.

## 1. Exact addition support fact

For one modular-addition Walsh bit tensor with current sigma bit `s`, previous sigma bit `t` and mask bits `(u,v,w)`, nonzero support obeys

`t = s xor u xor v xor w`

and, if `s=0`,

`u=v=w`.

A standard immediate consequence is MSB conservation: for nonzero output mask `w`, the highest set bit of every nonzero input mask `u` and `v` equals the highest set bit of `w`.

Proof: start from terminal `sigma_{n-1}=0` and descend. Above the highest set bit of `w`, `sigma=0` forces `u=v=w=0`; at the highest set bit itself, `sigma=0` forces `u=v=w=1`.

## 2. Central q138 carry geometry

The final central QR has fixed j4 output mask `2^3`. Hence every nonzero j4 term has

`msb(u4)=msb(v4)=3`.

The j3 output relation is

`w3_i = v4_{i+8 mod 32}`.

Therefore

`msb(w3)=msb(u3)=msb(v3)=27`.

These two facts determine several central j2/j1 mask bits exactly and create nonlinear support restrictions on the two unique HT88 critical 11|21 partitions.

## 3. First critical partition

Use

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

For j2,

`z2w_i = u4_i xor v3_{i+12}`

and

`z2v_i = v4_{i+8} xor D_{i+16}`.

From the MSB facts above,

- `z2w_15=1`;
- `z2w_16=z2w_17=z2w_18=z2w_19=0`;
- `z2v_16=D_0`.

Now inspect bits 16 and 15 of the exact j2 support recurrence.

If `C_16 != D_0`, then at bit16 the triple `(C_16,z2v_16,z2w_16)` is not equal, so nonzero support forces `sigma_16=1`. The recurrence then gives `sigma_15=0`. At bit15, `sigma_15=0` forces all three local masks equal, but `z2w_15=1`. Therefore

`C_15=1`.

Hence the exact necessary boundary rule is

`C_15=0 => C_16=D_0`.

Of the eight assignments to `(C_15,C_16,D_0)`, only six can occur in a nonzero central coefficient. Therefore the number of potentially nonzero rows on the 44 physical central boundary bits of `S1` is at most

`6 * 2^41 = 3 * 2^42`.

Thus the central Schmidt rank on this partition obeys

`rank_center(S1) <= 3 * 2^42`.

The complementary 21-site cluster has the same matrix rank bound.

## 4. Second critical partition

Use

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

For j1,

`z1w = u3 xor D`.

Since `msb(u3)=27`, its top five bits obey

- `z1w_31..z1w_28 = D_31..D_28`;
- `z1w_27 = 1 xor D_27`.

Nonzero j1 support requires the input mask `A` to have the same highest active bit as `z1w`. If no bit27..31 of `z1w` is active, then no bit27..31 of `A` may be active either.

Counting the allowed pairs of five-bit top patterns `(A_27..31,D_27..31)` gives

- highest31: `16*16=256`;
- highest30: `8*8=64`;
- highest29: `4*4=16`;
- highest28: `2*2=4`;
- highest27: `1*1=1`;
- no active top bit: `1*1=1`.

Total:

`342`

out of 1024 possible top-pattern pairs.

The remaining 34 physical boundary bits may be counted freely for a safe upper bound, so

`rank_center(S2) <= 342 * 2^34`.

This is smaller than the S1 central bound after the leaf contribution is included.

## 5. Re-evaluating the HT88 tree

The four diagonal leaf vectors retain the exact generic Hilbert-rank exponent

`4*min(|S|,32-|S|)`.

At an 11|21 critical split this is 44.

For S1 and its complement, the complete central-times-leaf message dimension is therefore at most

`(3*2^42) * 2^44 = 3*2^86`,

with exponent

`86 + log2(3) = 87.58496250072116...`.

For S2 the corresponding dimension is

`(342*2^34) * 2^44 = 342*2^78`,

with exponent about 86.41785.

Every noncritical cluster in the same frozen HT tree already had generic-envelope exponent at most 80. Hence the new complete maximum is

`3*2^86`.

Therefore

`W_2_repr <= 86 + log2(3) < 88`.

## 6. Why this is different from the previous falsifiers

The refined terminal-cut theorem found a 44-binary-edge cut and the GF(2) projection theorem found zero pure linear boundary codimension. Neither includes the nonlinear conditional support rule

`sigma=0 => u=v=w`.

The present theorem exploits exactly that nonlinear rule together with MSB conservation. Thus there is no contradiction: topology and linear parity saturate 44, while nonlinear Walsh support removes physical boundary rows.

## 7. Constructive ledger

This theorem is an exact representation-existence bound. It bounds Schmidt rank by the number of nonzero physical rows on the critical partitions.

It does not yet give a separately certified procedure for constructing the new central support/Schmidt factors while staying below exponent `86+log2(3)`. Therefore retain

- representation existence: `W_2_repr <= 86+log2(3)`;
- explicit constructive graph-plus-leaf construction: `W_2_construct <=95`.

## 8. Verification

Authority verifier:

`scripts/verify_v26_q138_double_round_support87.py`.

The verifier independently enumerates the exact two-bit j2 support recurrence behind the S1 rule, counts the S2 top-pattern MSB restriction, and recomputes every cluster of the frozen HT tree using the improved central bounds.

## 9. Scope

No approximation is used. No arithmetic-work reduction, optimality of the true double-round tensor, practical evaluator, ranking gain, `alpha<1`, or full-round relevance is claimed.
