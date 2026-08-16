# V26 Modular-Addition Class-Parity Conservation

## Purpose

`V26_MODADD_TERNARY_CLASS_CORE_THEOREM.md` identifies the rank-3 transverse states of one modular-addition Walsh bit tensor with the classes

`00`, `11`, `unequal`.

This note derives the exact binary conservation law carried by those ternary states and its telescoping form along the sigma/carry chain.

The result gives a sector rule that can be used in separator-rank analysis without choosing an arbitrary TT/SVD gauge.

## 1. Unequal indicator

For a ternary equality class `c`, define

`e(c)=0` for `c in {00,11}`

and

`e(c)=1` for `c=unequal`.

Equivalently, if

`c = class(x,y)`,

then

`e(c)=x xor y`.

For one interior modular-addition bit, recall

`c = class(u,t)`

and

`d = class(v,w)`,

where `s=sigma_i` and `t=sigma_{i-1}` satisfy

`t = s xor u xor v xor w`.

Therefore

`e(c)=u xor t`

and

`e(d)=v xor w`.

## 2. Local class-parity law

Substituting the sigma recurrence gives

`e(c) xor e(d)`

`= u xor t xor v xor w`

`= s`.

Hence every nonzero local Walsh tensor entry obeys the exact rule

`e(c) xor e(d) = s`.

This is also visible directly in the semantic middle tensor `H(c,s,d)`:

- for `s=0`, both class states are equal-sector states (`00` or `11`);
- for `s=1`, exactly one side is `unequal`.

Thus current sigma is precisely the **sector-flip bit** between the two ternary class states.

## 3. Direct-sum structure of the ternary bond

The rank-3 class space decomposes canonically as

`E direct_sum U`,

where

- `E = span{00,11}` has dimension 2;
- `U = span{unequal}` has dimension 1.

For `s=0`, the middle tensor acts only inside `E` and preserves the equal value:

`00 -> 00`,

`11 -> 11`.

For `s=1`, the middle tensor is off-diagonal with respect to `E direct_sum U`:

- equal `c` maps to unequal `d`, with the signed amplitudes `-1/2,+1/2` for `00,11`;
- unequal `c` maps to either equal `d` state with amplitude `1`.

So the ternary bond is not an undifferentiated dimension-3 state. It is a `2+1` sector decomposition controlled by the binary sigma bit.

## 4. Adjacent-bit transfer law

At bit i write the class states as `c_i,d_i` and the current sigma as `s_i`.

At the next bit `i+1`, the downward carry-chain identity is

`t_{i+1}=s_i`.

Therefore

`e(c_{i+1})`

`= u_{i+1} xor t_{i+1}`

`= u_{i+1} xor s_i`

`= u_{i+1} xor e(c_i) xor e(d_i)`.

Equivalently,

`e(c_i) xor e(c_{i+1}) xor e(d_i) = u_{i+1}`.

This is an exact GF(2) transfer law between neighboring semantic class sectors.

## 5. Segment telescoping theorem

Take an interior bit segment with endpoints `a<b`, so all required class states are defined.

XOR the adjacent-bit transfer law for

`i=a,...,b-1`.

Every interior `e(c_i)` appears twice and cancels. The exact segment relation is

`e(c_a) xor e(c_b) xor XOR_{i=a}^{b-1} e(d_i)`

`= XOR_{i=a+1}^{b} u_i`.

Thus an arbitrarily long carry/sigma segment has a one-bit boundary-sector law independent of its length.

This is the semantic-class version of telescoping the sigma recurrence, but it exposes which part of each rank-3 bond participates: only the unequal/equal sector bit `e`, not the full ternary state.

## 6. Fixed-u chains

In the fixed-input/fixed-output ChaCha QR reduction, additions T1 and T2 have the first modular-addition mask leg `u_i` fixed by the external masks.

For such a chain, the right-hand side of the segment theorem is a known constant.

Therefore every interior segment gives a pure boundary selection rule

`e(c_a) xor e(c_b) xor XOR e(d_i) = const`.

If several disjoint segment laws survive projection onto a separator and are linearly independent, each law removes one binary sector degree of freedom from the formal boundary support.

This is a direct route from local rank-3 semantics to exact separator support/rank reduction.

## 7. Variable-u chains

For T3 and T4 the corresponding `u_i` masks are internal variables shared with other QR factors.

The segment law still holds exactly, but the right-hand side is not automatically fixed. It must be combined with the cross-addition XOR/rotation constraints before claiming any separator reduction.

This prevents a common mistake: a local conservation law is not automatically an independent global boundary law after internal variables are projected out.

## 8. Relation to previous linear-parity checks

Earlier fused-site calculations found only zero or one independent GF(2) parity on several large separators. There is no contradiction.

The present theorem is a **local/segment identity**. Whether it produces an independent external boundary constraint depends on:

- which class-sector indices cross the chosen refined separator;
- which `u` variables are fixed, internal, or cross the separator;
- whether several segment identities become dependent after all internal variables are eliminated.

The theorem supplies the correct semantic variables in which to perform that elimination.

## 9. Use in width-41 separator analysis

The certified minimal-core QR tree has a largest formal message boundary of 41 binary indices. Its rank-2 TT edge indices can be gauged to the corresponding first/last binary physical legs because those endpoint flattenings have exact rank 2.

This permits boundary analysis in physical/sigma variables rather than anonymous TT coordinates.

For any rank-3 bond introduced in a refined separator, use the canonical `E direct_sum U` basis above and first eliminate the sector bits with the segment theorem before attempting dense Schmidt calculations.

A successful separator reduction must count only **independent projected laws**. No reduction below the existing `W<=41` certificate is claimed in this note by itself.

## 10. Claims not admitted

This theorem does not prove a global width-40 tree, does not yet give the exact rank of the certified width-41 boundary message, and does not establish practical QR evaluation, a double-round/full-round result, ranking gain, or `alpha<1`.
