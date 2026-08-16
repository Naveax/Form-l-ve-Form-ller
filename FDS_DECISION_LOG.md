# FDS_DECISION_LOG

## 2026-08-16 — Boundary syndrome
Reduced-model constant-factor compute win admitted; alpha=1.

## 2026-08-16 — Layout QR transfer
5/5 non-control layouts pass exact QR/correctness gates. Broad QR transfer admitted. Generic Python cache wall transfer failed 0/5.

## 2026-08-16 — Layout-specialized codegen
Fresh straight-line codegen restores actual wall realization on 4/5 non-control layouts. W5/W6/W7/W4+W6 pass; W4+W8 fails. **Decision:** admit broad but non-universal b=10 layout wall realization. No universal layout claim.

## Next
Freeze already-recorded W5_SINGLE and W4_W6_SPLIT scaling at b10/12/14/16. Leading enumeration remains 2^b and alpha=1 regardless of fitted slopes.
