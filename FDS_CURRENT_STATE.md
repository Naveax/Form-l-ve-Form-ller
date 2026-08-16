# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #8 strict raw-survivor uniqueness scaling remains **NO-GO** and is not reinterpreted.

Issue #9 `V25_COLLISION_TOLERANT_VERIFIED_SCREEN_SCALING` completed on a separately frozen fresh protocol and **PASSed all family gates**.

- generated/generic exactness: 696,320 syndrome + 696,320 direct predicates PASS;
- fresh true-key screen survival: 32/32;
- final exact verified set `[true]`: 32/32;
- raw collision cases: 7/32, all eliminated by exact verification;
- positive wall-speedup cases: 32/32;
- W5 median wall speedup b10→16: 1.1239x, 1.2529x, 1.2734x, 1.2840x;
- W4+W6: 1.0707x, 1.1506x, 1.1822x, 1.2023x.

Verdict: `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`.

This closes the constant-factor verified-screen extension. Leading work remains `Theta(2^b)` and alpha=1.

## Next frontier
Return to structural exponent reduction. Do not extend this family by adding more layouts/widths merely to accumulate constant-factor evidence. Next candidate: exact/low-rank half-key separability of the boundary syndrome under a separately frozen reduced-model audit.
