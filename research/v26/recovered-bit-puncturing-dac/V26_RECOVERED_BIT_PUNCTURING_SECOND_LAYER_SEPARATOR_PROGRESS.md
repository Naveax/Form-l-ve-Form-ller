# V26 Recovered Bit-Puncturing D&C — Second-Layer Separator Stage0

Frozen Stage0 completed without retuning.

Recovered trail core regression: 19/19 PASS. New packed separator regression: 2/2 PASS; each test validates all four next-column signed marginals against explicit first-layer global materialization.

Exact supports:
- cap2: `[0, 1152, 48, 0]`;
- cap3: `[0, 125056, 1136, 0]`;
- cap4: `[0, 11846464, 26912, 0]`.

cap4 global 222,660,480 Cartesian trails were never materialized. Packed exact cap4 marginals use an estimated 284,961,024 bytes at 24 bytes/nonzero, measured peak RSS 859,368 KiB and about 20.6 s wall. Both frozen memory gates pass.

The zero marginals in columns0/3 are exact signed cancellations, not global-state absence. Column marginals alone do not preserve cross-column joint correlations.

Decision: `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Next gate is a separately frozen single-column QR transform falsifier before attempting joint cross-column contraction. No alpha/full-round claim.
