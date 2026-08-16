# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains the admitted collision-tolerant constant-factor reduced-model screen; leading enumeration remains `2^b`, alpha=1.

Exact exponent-reduction hypotheses closed NO-GO:
- Issue #10 exact XOR 8+8 half-output separability;
- Issue #11 exact modular-additive 8+8 half-output separability;
- Issue #12 W4_W6 single-boundary disjoint-half dependency;
- Issue #13 exhaustive all-two-key-word single-boundary dependency separation.

Issue #13 searched **28 active word pairs × 80 cones = 2,240 cases**. Candidate count: **0**. No two-key-word placement yields exact nonempty disjoint half supports on opposite sides of a single boundary.

No alpha<1 result exists.

## Next
Only a genuinely different cancellation mechanism is worth testing. Next candidate: exact XOR projections of two internal boundary words, which can in principle cancel half dependence even when raw dependency unions are mixed. This requires a separately frozen fresh numerical protocol.
