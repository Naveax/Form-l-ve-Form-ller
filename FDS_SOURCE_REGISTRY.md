# FDS_SOURCE_REGISTRY

| ID | Class | Scope | Status |
|---|---|---|---|
| SRC-V25-TRAIL-DAC-RECOVERED | HASHED HISTORICAL SNAPSHOT AUTHORITY + CERTIFIED_LOCAL | bit-puncturing/trail D&C first layer and recovered lineage | PASS_WITH_LIMITS; snapshot SHA known, exact bytes currently missing; recovery tracked in Issue #22 and `V26_MISSING_CANONICAL_BYTES.md` |
| SRC-V25-BIT-PUNCTURING-CORE | HASH-LOCKED HISTORICAL SOURCE | canonical `fds_v25_bit_puncturing.py` | MISSING BYTES; required SHA `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`; current mount SHA scan found 0 matches |
| SRC-V26-DAC-SEPARATOR | FROZEN_PROTOCOL + MEASURED_EXACT_WITHIN_CAP | recovered second-layer single-column separator Stage0 | `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0` |
| SRC-V26-DAC-QR-TRANSFORM | FROZEN_PROTOCOL + IMPLEMENTED_UNMEASURED | single-column inverse-QR transform falsifier | ACTIVE / BLOCKED ON EXACT RECOVERED CORE REMATERIALIZATION |
| SRC-V26-ANF-GRAPH | FROZEN_PROTOCOL + EXACT_LOCAL | all-output ANF graph | NO-GO |
| SRC-V26-ROT-APP | PRIMARY_LITERATURE + EXACT_SOURCE_AUDIT | rotational applicability | NOT APPLICABLE |
| SRC-V26-CUBE8 | FROZEN_PROTOCOL + EXACT_LOCAL | source-orbit cube | NO-GO |
| SRC-V25-EXPONENT | FROZEN_PROTOCOLS + MEASURED | other V25 exponent track | CLOSED ALPHA_PASS=0 |

## Canonical recovery hashes

- snapshot: `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- bit-puncturing core: `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

No rewritten implementation may replace these provenance identities silently.
