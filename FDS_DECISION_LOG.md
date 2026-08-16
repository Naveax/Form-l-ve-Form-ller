# FDS_DECISION_LOG

## 2026-08-16 — V26 rotational applicability
Primary ChaCha rotational construction requires word-wise rotationally related permutation inputs. Under the fixed single-key source model, no nonzero rotation preserves all fixed constants, no arbitrary unknown key is generically equal to its rotation, and the corresponding same-key RX key difference is secret-dependent. The source exposes block outputs rather than a raw permutation oracle. Some rotated counter pairs exist, but they cannot repair the full-state incompatibility.

Decision: `NOT_APPLICABLE_TO_FDS_SINGLE_KEY_SOURCE_MODEL`. No rotational benchmark or Stage1.

## Next
Audit exact key-variable interaction/separator structure before attempting any new factorized solver.
