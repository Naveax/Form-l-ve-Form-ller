# FDS_DECISION_LOG

## 2026-08-16 — Issue #9 collision-tolerant verified screening
Fresh end-to-end protocol passed every constant-factor gate. Issue #8 remains NO-GO. Algorithmic alpha remains 1.

## 2026-08-16 — Issue #10 exact XOR half-key separability
Frozen b16 W5_SINGLE 8+8 audit built complete 256×256 syndrome tables for four fresh targets. No target had even one exact XOR-separable syndrome bit; stable exact bits = 0. Raw GF(2) ranks were 254–256 and rectangle residual ranks 253–255. The half-signature constraint therefore retained all 65,536 pairs.

Decision: `NO_GO_SIMPLE_8P8_XOR_SEPARABILITY`. No MITM scaling stage and no alpha claim.

## Next
Only genuinely different exact algebraic decompositions may open. First candidate: modular-additive separability mod 2^16 on a separately frozen fresh protocol.
