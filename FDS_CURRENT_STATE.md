# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

Issue #9 remains the admitted reduced-model constant-factor screen; alpha=1.

Simple exact half-key/single-boundary MITM is closed by Issues #10–#15. Issue #15 exhausts all 65,535 nonzero linear XOR masks and finds stable nullspace size zero.

Historical PNB/CPNB authority has now been recovered: the exponent track was already closed as `REDUCED_R6_CONSTANT_FACTOR_ONLY`; final R8 syncopation gain was below one standard error.

Historical bit-puncturing authority is also recovered. The core Walsh puncturing/trail coefficient method is reproduced and exact puncturing shows reduced-map statistical benefit, but preprocessing/construction cost prevents an admitted attack shortcut.

## Active frontier
`V25_REDUCED_QUARTER_ROUND_WALSH_TRAIL_VALIDATION`.
Extend the verified addition/subtraction Walsh engine through one complete reduced ChaCha quarter-round and compare frozen partial-trail spectra to exact FWT truth-table spectra before attempting any key-recovery scaling.

No alpha<1 or full-round result exists.
