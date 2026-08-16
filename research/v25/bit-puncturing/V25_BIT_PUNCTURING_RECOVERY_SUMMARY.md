# Recovered V25 Bit-Puncturing Authority

Historical local canonical state recovered on 2026-08-16 and reattached to GitHub authority.

- PNB/CPNB exponent track is closed as `REDUCED_R6_CONSTANT_FACTOR_ONLY`.
- Final R8 later-round syncopation holdout: 64 keys, 58,560 samples, survival 0.141974, epsilon before 0.426844, after 0.430599, gain +0.003755 vs SE 0.010967. No robust gain.
- Exact Walsh puncturing equals affine-coset averaging in regression.
- Exact reduced q138 puncturing statistically outranks PNB-zero on small b10/b12 screens, but direct exact-map construction costs exhaustive work and is not an attack shortcut.
- Modular addition/subtraction Walsh coefficient formulas were brute-force validated.
- EUROCRYPT-2025-style Example-1 first extension reproduced exactly: **26 nonzero coefficients**, squared-correlation energy **0.666666746... ≈ 2^-0.585**.
- Recovered local tests: orbit PNB/CPNB **17/17 PASS**; bit puncturing **9/9 PASS**.

Canonical next unfinished pass is method validation: propagate the verified Walsh trail engine through a complete reduced ChaCha quarter-round, merge repeated input masks into linear-hull coefficients, prune under frozen beam/correlation budgets, and compare the partial spectrum to an exact reduced truth-table/FWT reference.

No alpha<1, full-round, or end-to-end key-recovery claim is admitted.
