# REVOKED: V26 q138 factor-generation84 candidate

This file is retained only as a correction record. The claimed factor-generation84 bound depended entirely on a four-site rank96 result that was produced by int32 Gram overflow.

The corrected nonoverflowing verifier gives full row rank256 for the special `{2,3,18,19}` relaxed four-site block. Therefore the rank96 factor does not exist in this construction and no factor-generation84 reduction follows.

Canonical coefficient-aware materialized-factor generation remains

`W_2_factor-gen <= 79+log2(87)=85.44294349584872...`,

with clean run `32030620625`.

See:

- `V26_Q138_DOUBLE_ROUND_SIGNED84_MULTISITE_THEOREM.md` for the revocation and arithmetic cause;
- `scripts/verify_v26_q138_double_round_signed84_multisite.py` for the corrected int64 regression;
- `V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION85_THEOREM.md` for current authority.
