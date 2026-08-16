# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

V25 exponent track remains closed with `ALPHA_PASS=0`. Closed V26 exact families now include first/second counter derivatives, cross-word XOR projection, source-orbit 8-D counter cube, and the rotational applicability branch.

Rotational applicability result: `NOT_APPLICABLE_TO_FDS_SINGLE_KEY_SOURCE_MODEL`.
- nonzero rotations preserving all four fixed ChaCha constants: none;
- generic arbitrary same-key direct rotations: none;
- public/generic same-key RX key differences: none;
- direct applicable rotations: none;
- raw permutation oracle: unavailable.

Source counter pairs exist for some rotations, so data volume is not the fundamental blocker. Fixed constants, fixed unknown key relation and block-function observability are.

No rotational Stage1 opens. `alpha<1` remains NOT DEMONSTRATED; no full-round claim.

## Next
Open a mechanism-distinct exact key-interaction graph/separator audit using existing exact ANF infrastructure. Goal: determine whether the R6 key-variable interaction graph admits any nontrivial separator/factorization before building another solver.
