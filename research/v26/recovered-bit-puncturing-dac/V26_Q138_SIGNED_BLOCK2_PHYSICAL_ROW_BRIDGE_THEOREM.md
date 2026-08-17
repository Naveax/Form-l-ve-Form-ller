# V26 q138 signed block2 physical-row bridge theorem

Scope: the exact S1 block2 rank-2784 factor used in the d=1 signed theorem. The goal is constructive generation of right/complement basis slices, not a new rank reduction.

Start from the clean explicit 3584-to-2784 retained-column factorization. There are 8192 actual physical block2 row assignments:

- 16 choices of `D13..16`;
- 256 choices of `A13..16,B13..16`;
- 2 choices of `C0`.

The verifier maps every physical row exactly into the 2784-dimensional retained-column coordinate space and performs exact rational elimination directly on those8192 coordinate vectors.

Result:

`rank(span of physical block2 rows) = 2784`.

Thus the full block2 row space can be based using actual physical rows; no abstract nonphysical row directions are required.

For constructive convenience the verifier keeps a normalized echelon basis generated from those physical rows. Each normalized basis vector is an exact rational combination of at most64 physical rows, with mean physical-row support

`3.654094827586207...`.

Conversely every one of the8192 physical rows has an exact coordinate vector in this basis with at most184 nonzeros, mean

`11.8597412109375`.

Therefore every block2 right-basis slice can be generated as an exact linear combination of at most64 ordinary physical central-QR slices. This is the key bridge from the signed rank theorem to a coefficient-aware constructive procedure: the right basis no longer needs an abstract V-oracle.

Verifier:

`scripts/verify_v26_q138_signed_block2_physical_row_bridge.py`.

This theorem is local. The complete double-round constructive peak requires a separate contraction/factor-generation certificate.
