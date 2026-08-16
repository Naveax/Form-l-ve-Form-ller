# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains an admitted collision-tolerant **constant-factor** reduced-model screen; alpha=1. Issue #8 strict raw uniqueness remains NO-GO.

Structural exponent audits:
- Issue #10 exact XOR 8+8 separability: NO-GO, 0 exact bits on 4/4 targets, dense GF(2) ranks.
- Issue #11 exact modular-additive 8+8 separability: NO-GO. No target is exact even at modulus 2^4; common exact width=0; 65,536 matches remain.

No alpha<1 result exists.

## Next
Move from output-function factorization to structural dependency separation. Audit all 80 internal `(split,word)` cones for `W4_W6_SPLIT`: does the forward boundary depend on only one 8-bit key half while the backward boundary depends only on the other, with disjoint active-word support? This is a target-free exact prerequisite for a genuine bidirectional MITM.
