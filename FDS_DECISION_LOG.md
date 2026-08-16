# FDS_DECISION_LOG

## 2026-08-16 — Boundary/codegen results
Reduced 6-round constant-factor compute win admitted; broad b10 QR layout transfer and broad non-universal specialized wall realization admitted. Alpha remains 1.

## 2026-08-16 — Strict multi-layout b10→16 scaling
Frozen strict gate required raw syndrome uniqueness at every layout/b target. W5 fails b10 and b16; W4+W6 fails b12 and b16. **Decision:** `NO_GO_STRICT_MULTI_LAYOUT_SCALING_GATE`.

All collisions were eliminated by the exact direct verifier and all frozen cases retained positive TOTAL/wall savings. This is a new hypothesis only; it does not retroactively change the failed gate.

## Next
Fresh preregistered collision-tolerant verified-screen scaling, with the verified candidate set and full survivor-verification cost as the end-to-end criterion.
