# V26 Q138 j1 retained-only gap6..11 injectivity theorem

## Scope

This is the first cheap secondary representation probe after the new canonical center

`rank_center(S1)<=3829*2^29`.

It isolates j1 sites6..11, which lie outside S1. Therefore the physical `A_i,B_i,D_i` variables at these sites are retained-column variables for the S1 matricization, as are the local `k_i,q_i` variables. The only row/interface variables are the endpoint carries

`(sigma1_5,sigma1_11)`.

## Exact endpoint operator

For one site use

`T(s_new,s_old,A,k xor B,q xor D)`.

In the Gram product, the retained assignment `(A,B,D,k,q)` is shared by the two copies. This gives a four-state paired-carry transfer on `(s_old,s'_old)` to `(s_new,s'_new)`.

Raise this exact transfer through the six sites6..11. The resulting endpoint Gram has four rows indexed by

`(sigma1_5,sigma1_11)`.

After removing an irrelevant common positive scale from the duplicated retained B/D parameterization, it is equivalent to

```
[32    0    0  1/2]
[ 0   32  1/2    0]
[ 0  1/2   32    0]
[1/2   0    0   32]
```

and has exact rational rank4.

Thus the six-site retained-only carry gap is injective on the complete four-dimensional endpoint-carry domain.

## Consequence

No compression below the new center `3829*2^29` can come from treating j1 bits6..11 as an isolated retained-only carry bridge between the low sites0..5 and high sites12..16.

This closes the direct j1 carry-gap probe. It does not rule out a larger nonlocal regrouping that contracts additional retained coordinates simultaneously.

## Authority

- `scripts/verify_v26_q138_j1_gap6_11_injective.py`;
- `.github/workflows/j1-gap6-11-injective.yml`.
