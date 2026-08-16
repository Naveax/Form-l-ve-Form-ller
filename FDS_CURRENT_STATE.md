# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 is admitted only as `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`; Issue #8 remains strict NO-GO. Leading enumeration is still `2^b`.

Issue #10 tested the first structural exponent hypothesis: exact XOR separability of the 16-bit boundary syndrome under a frozen b16 `W5_SINGLE` 8+8 logical key split.

Result: **NO-GO**.
- fresh targets: `[43051,21863,31754,45567]`;
- exact XOR-separable bits: `0/16` on every target;
- stable exact bits: `0`;
- half-signature matches: `65,536` on every target;
- raw GF(2) bit ranks: 254–256;
- rectangle-residual ranks: 253–255.

Verdict: `NO_GO_SIMPLE_8P8_XOR_SEPARABILITY`. No MITM scaling stage was opened and alpha<1 remains unproven.

## Next
A genuinely different exact ARX-compatible hypothesis may be tested on fresh targets: modular-additive half separability mod `2^16`. Do not retune XOR bits or use approximate rank to resurrect Issue #10.
