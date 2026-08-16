# FDS_SOURCE_REGISTRY

| ID | Class | Scope | Status |
|---|---|---|---|
| SRC-V25-SYNDROME | MEASURED_LOCAL + VERIFIED_REFERENCE | Stage0→Stage3 internal boundary syndrome | `ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN` |
| SRC-V25-SYNDROME-STAGE0 | VERIFIED_REFERENCE | 80 cones / 10,240 exact checks | PASS |
| SRC-V25-SYNDROME-STAGE2 | MEASURED_LOCAL | 12 untouched b10 targets | PASS |
| SRC-V25-SYNDROME-STAGE3 | MEASURED_LOCAL | b10/12/14/16 scaling | PASS CONSTANT FACTOR; alpha=1 |
| SRC-V25-LAYOUT-XFER | FROZEN_PROTOCOL_PENDING | reduced-key layout transfer | ACTIVE NEXT |
| SRC-V25-BORROW | MEASURED_LOCAL | output-conditioned borrow descriptors | NO-GO |
| SRC-V25-CARRY | MEASURED_LOCAL | public carry signature | NO-GO |
| SRC-V25-ADDDIST | MEASURED_LOCAL | public additive distance | NO-GO |
| SRC-V25-MDELTA | HISTORICAL_RECOVERED + MEASURED_LOCAL | public xor delta | NO-GO |
| SRC-V25-SYNREL | HISTORICAL_RECOVERED + MEASURED_LOCAL | synthetic descriptor audit | NO-GO |
| SRC-RAW-20260816 | HISTORICAL_RECOVERED | raw bootstrap provenance | Issue #2 |
