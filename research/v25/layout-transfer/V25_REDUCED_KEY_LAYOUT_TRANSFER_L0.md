# V25 Reduced-Key Layout Transfer — Stage L0 Structural Cost

Frozen before any layout survivor measurement.

The boundary algorithm remains split1 / word0 / syndrome width16. Six b=10 logical-key layouts are fixed: word4 control, word5/6/7 single-word moves, a word4+word8 same-column split, and a word4+word6 cross-column split.

Candidate-dependence is propagated structurally through the exact QR execution order. No target output, true key, survivor count, or oracle statistic is used.

| layout | screen candidate/fixed QR | direct candidate/fixed QR | N=1 conservative ratio |
|---|---:|---:|---:|
| W4_CONTROL | 15 / 3 | 18 / 3 | 0.83450 |
| W5_SINGLE | 14 / 4 | 18 / 3 | 0.77901 |
| W6_SINGLE | 14 / 4 | 18 / 3 | 0.77901 |
| W7_SINGLE | 14 / 4 | 18 / 3 | 0.77901 |
| W4_W8_SPLIT | 16 / 2 | 18 / 3 | 0.88999 |
| W4_W6_SPLIT | 16 / 2 | 19 / 2 | 0.84320 |

All six are structurally performance-eligible because the screen leading candidate QR coefficient is lower than the fair direct-word baseline coefficient. This is not a transfer result. L1 survivor/correctness gates remain unopened.
