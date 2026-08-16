# V26 q138 Physical Right-Map Hull-162 Theorem

## Purpose

The generalized right-map transfer analysis allowed an affine parity control `p` at each local `P_i` factor and obtained a 197-dimensional doubled reachable hull. The physical q138 fixed-output Walsh network is stricter: its parity factor is exactly

`u4_i xor v3_{i+12} xor w2_i = 0`.

Therefore `p_i=0` is not a free source-mask bit. Restricting to the four physical interior transfer types `(u1,u2,p=0)` gives a strictly smaller exact invariant quotient.

## 1. Physical transfer alphabet

For each ordinary interior site the only physical fixed controls are

`(u1,u2) in {0,1}^2`.

The four doubled transfer operators are the generalized `tau` operators

`000, 010, 100, 110`.

Their ambient exact rational ranks in the formal 1024-state doubled Gram space are

`1016, 384, 454, 431`.

Thus the compression below is not caused by each ambient operator being low rank.

## 2. Boundary-conditioned reachable hull

Use every physical site-3 control `(u1_3,u2_3)` and all four values of the doubled first interface-bit sector.

The initial exact span has dimension

`15`.

Close monotonically under all four physical interior operators. The cumulative dimensions are

`15 -> 70 -> 153 -> 162 -> 162`.

Hence the exact common invariant physical reachable hull is

`U_phys`, `dim U_phys = 162`.

No approximation, sigma cap, floating tolerance or trail truncation is used.

The 197-dimensional generalized hull remains correct for its larger affine-control family; it is simply not the sharp physical q138 quotient.

## 3. Copy-exchange sectors

Exchange of the two Gram copies commutes with the four physical transfer operators. The 162-dimensional hull decomposes exactly as

`U_phys = U_+ direct_sum U_-`

with

- symmetric sector dimension `114`;
- antisymmetric sector dimension `48`.

The physical sector growth is

`(11,4) -> (50,20) -> (106,47) -> (114,48) -> (114,48)`.

## 4. Restricted transfer ranks

In control order

`(u1,u2) = 00,01,10,11`,

the exact ranks restricted to `U_phys` are

`159, 79, 99, 97`.

The symmetric-block ranks are

`112, 56, 71, 66`,

and the antisymmetric-block ranks are

`47, 23, 28, 31`.

The two block ranks add to the full restricted rank in every case.

## 5. Significance

The full doubled transfer state has formal dimension 1024. The generalized affine family reduces this to 197, but the actual physical q138 parity law reduces it further to

`1024 -> 162 = 114 + 48`.

This is source/model conditioning in the precise FDS sense: states that are algebraically possible in a generalized local tensor family need not be reachable in the actual cryptographic wiring.

Future right-map rank calculations should therefore use `U_phys`, not the 197-state generalized hull, except when independently validating the larger model.

## 6. Machine verifier

Authority verifier:

`scripts/verify_v26_qr_q138_physical_right_hull162.py`

It reconstructs the certified five-site right-map geometry, restricts all parity factors to the physical `p=0` relation, recomputes the exact rational cumulative hull and copy-swap sectors, and checks all ranks stated above.

## 7. Scope

This theorem concerns the q138 fixed-output 107-leaf right-map transfer object inside the certified width-40 one-QR representation. It does not by itself lower the complete global width below 40 and does not imply a double-round/full-round or ranking result.