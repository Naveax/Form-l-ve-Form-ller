# REVOKED: V26 q138 d=1 signed83 two-factor candidate

This file records a revoked candidate, not an admitted theorem.

The candidate combined two relaxed four-site rank reductions:

- special `{2,3,18,19}` claimed rank96/256;
- generic `{4,5,20,21}` claimed rank208/256.

Both ranks were artifacts of int32 overflow in an optimized NumPy einsum/Gram path. The contraction result remained int32 despite the draft requesting an int64 dtype; Gram multiplication overflowed before accumulation.

After explicitly casting all tensor inputs to int64 before einsum, both relaxed Grams are full row rank modulo the odd prime1000003:

- special rank256/256;
- generic rank256/256.

Therefore the candidate S1 bound `3393*2^28`, factor dimension `3393*2^72`, and exponent83.7283457147 are invalid and revoked.

Canonical d=1 authority remains

`W_repr(1)<=W_factor-gen<=79+log2(87)=85.44294349584872...`.

The corrected regression lives in

`scripts/verify_v26_q138_double_round_signed84_multisite.py`.
