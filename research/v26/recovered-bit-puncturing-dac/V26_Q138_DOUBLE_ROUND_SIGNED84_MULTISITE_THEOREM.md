# REVOKED: V26 q138 d=1 four-site signed84 candidate

This file records a **revoked candidate**, not an admitted theorem.

The earlier draft claimed exact ranks96 and208 for two relaxed four-site Gram constructions and derived candidate d=1 bounds84.0279 and83.7283. Clean-checkout CI rejected the first rank96 assertion.

Root cause: the draft used NumPy arrays with int32 inputs in an optimized `einsum` and requested `dtype=int64`. On the relevant builds the optimized einsum result remained int32; the subsequent Gram multiplication therefore overflowed. The overflow created artificial zero rows and false rank deficiency.

The corrected verifier casts the tensor inputs to int64 **before** einsum and asserts the resulting contraction dtype. With the corrected arithmetic:

- special block `{2,3,18,19}`: odd-prime rank256/256;
- generic block such as `{4,5,20,21}`: odd-prime rank256/256;
- neither corrected Gram has zero rows.

Thus these relaxed four-site blocks are full row rank and provide no compression.

Consequently the candidate bounds

- `W_repr(1)<=84.027905996...`,
- `W_repr(1)<=83.728345714...`,
- and associated factor-generation84/83 claims

are revoked.

Canonical d=1 authority remains the clean signed85 / factor-generation85 line until superseded by a new clean exact result:

`W_repr(1)<=W_factor-gen<=79+log2(87)=85.44294349584872...`.

Correction verifier:

`scripts/verify_v26_q138_double_round_signed84_multisite.py`.

This incident is also a standing rule: exact integer Gram claims must ensure the contraction itself is performed in a nonoverflowing dtype; casting only the accumulator after an int32 matrix product is insufficient.
