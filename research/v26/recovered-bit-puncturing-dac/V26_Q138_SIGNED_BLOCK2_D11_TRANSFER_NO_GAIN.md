# V26 q138 signed block2 D11 one-bit transfer no-gain theorem

## Statement

Start from the exact extended S1 block2

`A12..16, B12..16, D12..16, C0`

with certified rational row rank

`21888`.

Extend the local subnetwork one bit farther through the next repeated external D variable `D11`:

- j1 bit11 contains the first occurrence of `D11`;
- j2 bit27 contains the second occurrence of the same `D11`;
- `D11` is outside S1, so it remains a right-side/column variable rather than becoming a new physical row bit.

Closing both occurrences of `D11` in this one-bit extension does **not** lower the exact row rank of the current block2 sector-overlap construction. The rank remains

`21888`.

Therefore this specific “one bit farther through D11” route gives no improvement over the current

`W_repr(1) <= 78 + log2(171) = 85.4178525148859...`

bound.

All statements are exact over `Q`; `epsilon=0`.

## 1. Dependency: the rank21888 block2 theorem

For each fixed prefix

`p = D12..15`,

the two `D16` j1 spaces satisfy

- `dim J0 = dim J1 = 448`;
- `dim(J0 ∩ J1) = 424`.

The j2 bit0 spaces satisfy

- `dim K0 = dim K1 = 2`;
- `dim(K0 ∩ K1) = 1`.

The sixteen `D12..15` j2-high sectors are a direct sum.

Hence the already-certified per-prefix union dimension is

`448*2 + 448*2 - 424*1 = 1368`,

and the full block rank is

`16*1368 = 21888`.

## 2. j1 bit11 transfer is injective for each D11 slice

Fix `D11=d`.

At j1 bit11, the old outgoing carry `sigma11` is mapped through the exact local Walsh tensor while the outside-S1 variables `A11,B11,u11,x11` remain columns.

The resulting two-row map

`sigma11 -> (A11,B11,u11,x11,sigma10)`

has exact rational rank2 for both

`d=0` and `d=1`.

Thus the bit11 transfer is injective on the two-dimensional carry interface in each fixed-D11 column slice.

Tensoring this transfer with the identity on the rest of the j1 retained columns preserves every j1 subspace dimension and every intersection dimension. In particular, for each prefix p it preserves

`448, 448, intersection 424`

for the two D16 sectors.

## 3. j2 bit27 transfer is also injective

Again fix `D11=d`.

At j2 bit27, the old high-sector carry `sigma27` is mapped to

`(C27,W27,sigma26)`

through the exact local Walsh tensor with `D11=d`.

This two-row transfer also has exact rational rank2 for both D11 values.

Therefore extending the old j2 bits28..31 high vector through bit27 does not lose the two-dimensional carry information merely because of the new local transfer.

## 4. The sixteen D12..15 sectors remain direct inside each D11 slice

For each fixed D11 value, extend all sixteen exact j2-high vectors indexed by `D12..15` through bit27.

Exact rational elimination gives

`rank = 16`

for `D11=0`, and independently

`rank = 16`

for `D11=1`.

So the sixteen high-prefix sectors remain linearly independent in either D11 column slice.

This prevents a new cross-prefix cancellation from appearing solely because the common D11 column has been exposed.

## 5. Shared-D11 coupling preserves the old per-prefix geometry

For a fixed prefix p, let `L_d` denote the injective j1 bit11 transfer in D11 slice d, and let `h_{p,d}` be the nonzero j2-high vector after the bit27 extension in the same slice.

The shared-D11 extension acts on a j1 vector x as the direct-sum map

`Phi_p(x) = (L_0 x) tensor h_{p,0}  direct-sum  (L_1 x) tensor h_{p,1}`.

Because each `L_d` is injective and each high vector is nonzero, `Phi_p` is injective.

The same `Phi_p` acts on the two D16 j1 subspaces, so

`Phi_p(J0) ∩ Phi_p(J1) = Phi_p(J0 ∩ J1)`.

Hence the dimensions remain

- `448`;
- `448`;
- intersection `424`.

The bit0 D16 spaces K are unchanged. Therefore the per-prefix union remains exactly

`1368`.

Across prefixes, the fixed-D11 high vectors have rank16, so the sixteen prefix contributions remain a direct sum. The total rank is consequently

`16*1368 = 21888`.

## 6. C12 one-site check

The remaining physical S1 bit `C12` occurs locally in j2 bit12.

If that single site is appended with both neighbouring carry interfaces left open, its exact two-row Walsh map has rank2.

So an isolated C12 append costs the naive factor2 and gives no local rank compression by itself.

This does **not** close the more interesting possibility in which C12 is coupled through a genuine multi-site j2 carry corridor to the existing high/bit0 block. That is now the next mathematical target.

## 7. Consequence

The first canonical “one bit farther” attempt after the rank21888 result is closed negatively:

`D11 occurrence-closed one-bit transfer: NO GAIN`.

Together with the clean block1 two-site falsifier, which also reached its naive rank, the next useful search should not repeat another isolated local append. It should test a multi-site carry-coupled construction, with C12 as the natural remaining S1 row bit and exact subspace intersections as the authority metric.

## Verification

Authority verifier:

`scripts/verify_v26_q138_signed_block2_d11_transfer_no_gain.py`

It checks with exact `Fraction` arithmetic:

- j1 bit11 fixed-D11 transfer rank `2,2`;
- j2 bit27 fixed-D11 transfer rank `2,2`;
- extended sixteen-prefix high-sector rank `16,16` by D11 slice;
- the inherited `1368` per-prefix and `21888` total rank arithmetic;
- isolated C12 row rank2.

## Scope

This is a scoped exact NO-GAIN result for the one-bit D11 extension of the current sector-overlap factorization. It is not a lower bound on the full S1 central matricization and does not rule out longer multi-site carry coupling, alternative contraction trees, arithmetic-work improvements, ranking gains, `alpha<1`, or full-round relevance.
