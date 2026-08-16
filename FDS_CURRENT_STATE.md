# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

`ADMIT_BROAD_NONUNIVERSAL_WALL_REALIZATION`.

Boundary syndrome QR transfer is broad across all five tested non-control b=10 layouts. Layout-specialized straight-line codegen realizes a real wall win on 4/5 non-control layouts: W5 1.113x, W6 1.128x, W7 1.122x, W4+W6 1.075x. W4+W8 fails at 1.008x, so the claim is broad but not universal.

Generated-vs-generic exactness: 49,152 full syndrome and 49,152 direct predicates PASS. Generator source 12,032 bytes; generation+compile ~14 ms.

Leading candidate enumeration remains `2^b`; alpha=1. No full-round claim.

## Exact next
`V25_MULTI_LAYOUT_CODEGEN_SCALING_B10_B16`: W5_SINGLE and W4_W6_SPLIT at b=10/12/14/16 on already frozen targets.
