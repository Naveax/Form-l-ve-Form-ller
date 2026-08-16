# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

`ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN` remains valid. Layout transfer now shows the QR-count mechanism is not confined to word4.

### New layout-transfer result
- Fixed split1/word0/width16.
- Six frozen b=10 layouts, eight fresh paired targets.
- 48/48 cases: exactly one syndrome survivor and unique true direct verification.
- 5/5 non-control layouts pass all QR/correctness gates.
- Median TOTAL QR ratios: 0.7790–0.8900 across non-control layouts.
- Exact generic cache equivalence: 49,152 full syndrome + 49,152 screen + 49,152 direct checks PASS.
- Generic Python wall gate: 0/5 non-control layouts pass; interpreter/copy overhead eats the QR gain.

Admitted: broad constant-factor **QR transfer across the tested layouts**. Not admitted: broad generic Python wall transfer. Prior specialized word4 wall win remains in prior scope. Alpha remains 1.

## Exact next
`V25_LAYOUT_SPECIALIZED_CODEGEN_WALL_REALIZATION`, frozen fresh targets `[404,274,285,190,939,749,785,460]`.
