# FDS_CONTINUE_HERE

**State:** `ADMIT_BROAD_QR_LAYOUT_TRANSFER_NO_GENERIC_WALL_TRANSFER`  
**Next:** `V25_LAYOUT_SPECIALIZED_CODEGEN_WALL_REALIZATION`.

1. Fresh main + authority read.
2. Keep split1/word0/width16 and all six layouts fixed.
3. Generate straight-line layout-specialized screen and equally specialized direct baseline from frozen structural classifications.
4. Fresh targets are `[404,274,285,190,939,749,785,460]`; do not reuse L1 wall targets for admission.
5. Full 48×1024 generated-vs-generic exactness must pass before wall admission.
6. Benchmark warmup3/repeat11 with alternating order; include target cache setup and survivor verification.
7. Wall gate per layout: median >=1.05, positive >=7/8, exact unique true 8/8.
8. Broad wall realization requires >=4/5 non-control layouts. No alpha/full-round claim regardless.
