# V26 q138 signed S1 block1 explicit rank-16 factor theorem

Scope: the five-row-bit occurrence-closed S1 block used by the d=1 signed85 theorem. This upgrades the rank count to an explicit exact local factorization.

Rows are indexed by

`(A0,B0,C15,C16,D0)`

and retained columns by

`(s2_16,v2_15,s2_14,s1_0,u3_0,v3_12)`.

The exact 32x64 dyadic matrix has:

- 8 zero physical rows;
- 24 nonzero physical rows;
- exactly16 normalized row classes up to nonzero rational scaling.

Those16 normalized rows are linearly independent over Q. Hence the matrix has exact rank16 and admits an especially simple explicit factorization:

- V consists of the16 normalized retained-column rows;
- each nonzero physical row of U has exactly one nonzero coordinate, equal to the scalar relating that row to its normalized V row;
- each zero physical row has no active coordinate.

Dense storage envelopes are only512 entries for U and1024 entries for V.

Verifier:

`scripts/verify_v26_q138_signed_block1_explicit_factor.py`.

This removes block1 local factor generation as a constructive<95 blocker. It does not by itself prove a full complement/right contraction certificate.
