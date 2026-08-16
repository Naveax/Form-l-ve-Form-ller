# FDS_DECISION_LOG

## 2026-08-16 — Internal boundary syndrome
Admit reduced-model constant-factor compute win. Stable b10..16 QR speedup ~1.20x; specialized word4 Python wall speedup ~1.12–1.16x. Leading work remains C*2^b, alpha=1.

## 2026-08-16 — Reduced-key layout transfer
Frozen split1/word0/width16 transferred exactly across five non-control layouts. All 48 cases produced the unique true survivor. **Decision:** admit broad QR constant-factor transfer across tested layouts.

The generic cached Python executor did not realize a broad wall-time win: 0/5 non-control layouts met the preregistered median >=1.05 gate. This does not revoke the QR result; it blocks broad wall-time promotion for the generic interpreter.

## Next
Test a frozen layout-specialized straight-line code generator on fresh targets, with an equally specialized direct baseline. Do not retune the mathematical algorithm.
