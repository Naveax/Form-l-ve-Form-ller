# V25 Collision-Tolerant Verified-Screen Scaling

Frozen Issue #9 protocol completed without retuning.

- Full generated/generic exactness: **696,320/696,320 syndrome values + 696,320/696,320 direct predicates PASS** across 32 fresh layout/width/target cases.
- True key survived the 16-bit screen: **32/32**.
- Final exact verifier returned exactly `[true key]`: **32/32**.
- Raw syndrome collisions occurred in **7/32** cases and were all removed by the already-accounted verifier.
- Every fresh wall case showed positive speedup: **32/32**.
- All frozen gates passed for both `W5_SINGLE` and `W4_W6_SPLIT` at b=10,12,14,16.

Median wall speedups by b:
- W5: `1.1239x / 1.2529x / 1.2734x / 1.2840x`.
- W4+W6: `1.0707x / 1.1506x / 1.1822x / 1.2023x`.

Median TOTAL QR ratios by b:
- W5: `0.77901 / 0.77809 / 0.77785 / 0.77780`.
- W4+W6: `0.84320 / 0.84238 / 0.84217 / 0.84214`.

Decision: `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`.

Issue #8 remains NO-GO under its stricter raw-survivor uniqueness gate. This follow-on does not reinterpret it. Leading candidate enumeration remains `2^b`; algorithmic alpha remains **1.0**; no full-round or 256-bit key-recovery claim.
