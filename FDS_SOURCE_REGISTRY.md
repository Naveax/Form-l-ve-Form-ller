# FDS_SOURCE_REGISTRY

| ID | Class | Scope | Status |
|---|---|---|---|
| SRC-V25-SYNREL | HISTORICAL_RECOVERED + MEASURED_LOCAL | 24-target synthetic descriptor audit | NO-GO |
| SRC-V25-MDELTA | HISTORICAL_RECOVERED + MEASURED_LOCAL | public xor delta audit | NO-GO |
| SRC-V25-ADDDIST | MEASURED_LOCAL | public additive distance audit | NO-GO |
| SRC-V25-CARRY | MEASURED_LOCAL | 32-pair public carry-transition audit, preregistered on GitHub | `NO_GO_PUBLIC_CARRY_SIGNATURE` |
| SRC-V25-BORROW-PLAN | FROZEN_PROTOCOL | output-conditioned word4 subtraction borrow audit | ACTIVE NEXT |
| SRC-RAW-20260816 | HISTORICAL_RECOVERED | raw 94-file bootstrap provenance | Issue #2 |

Carry authority includes plan, builder, evaluator, compact results, decision, manifest and tests. Reproducible C1 shard scratch remains excluded from Git.
