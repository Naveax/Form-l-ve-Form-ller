# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

The first robust reduced-model compute win is admitted for the internal boundary-syndrome family, under a narrow layout scope.

### Boundary syndrome result
- Stage0: all 80 split/word cones cost 18 QR vs 24 full-state; 10,240 exact equality checks PASS.
- Frozen selection: split1 / word0.
- Stage1 selected width16 without retuning.
- Stage2 untouched b=10: one survivor on 12/12, true key retained 12/12.
- Candidate-ensemble cache: fair formula `15*2^b + 6 + 17*N` vs direct `18*2^b + 3`.
- Cached Stage2 median QR speedup 1.1984x; median wall speedup 1.1313x; wall positive 12/12.
- Stage3 b=10,12,14,16: all gates PASS; 16/16 true keys retained.
- Median wall speedup range 1.1199x–1.1556x; QR speedup ~1.20x.
- Exact algorithm QR slope 0.99967; measured wall slope 1.00113.

### Claim boundary
`ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN` only for the controlled 6-round layout where active reduced-key bits are confined to key/state word4. Leading work remains `15*2^b`; algorithmic alpha is exactly 1.

Not admitted: alpha reduction, subexponential search, full-round relevance, arbitrary key-layout generality, arbitrary data compression.

## Exact next
`REDUCED_KEY_LAYOUT_TRANSFER_FALSIFIER`: move/distribute the same b=10 active bits across multiple ChaCha key words and test whether the exact cache/syndrome advantage transfers.
