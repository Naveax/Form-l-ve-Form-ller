# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains a scoped constant-factor reduced-model PASS; leading enumeration remains `2^b`, alpha=1.

Exact exponent hypotheses closed NO-GO now include:
- #10 XOR 8+8 output separability;
- #11 modular-additive 8+8 output separability;
- #12/#13 raw single-boundary half-dependency separation across all two-key-word layouts;
- #14 single/pair boundary-word XOR cancellation.

Issue #14 searched 680 split/projections. Forward produced 156 exact half-oriented candidates; the first frozen fresh output target left **0** exact opposite-half backward candidates. Stable candidate count is therefore 0.

No alpha<1 result exists.

## Next
If XOR cancellation is pursued once more, do it exhaustively: solve for the entire GF(2) nullspace of all 65,535 nonzero linear masks over the 16 boundary words and intersect forward/opposite-backward half-independence spaces. Do not enumerate triples/quadruples piecemeal.
