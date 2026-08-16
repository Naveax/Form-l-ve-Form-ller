# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

V25 exponent track remains closed with ALPHA_PASS=0. V26 first exact family (feed-forward-cancelled first counter difference) is NO-GO.

V26 second exact family, counter second finite-difference ANF, is also **NO-GO** under frozen Issue #18.

R6 b16 second difference `[1,257,513]`:
- median per-bit degree reduction: 0;
- median per-bit support-exponent reduction: -3.4348e-05;
- stable sparse b14/b16 bits: 0.

All 3 primary gates fail. Counter-derivative order/stride tuning is retired; no polynomial stage, alpha<1 or full-round claim.

## Next
Move away from counter derivatives. Next target-free exact family: exhaustive cross-word XOR projections over all 120 word pairs, testing whether correlated dense outputs cancel high-degree ANF structure.
