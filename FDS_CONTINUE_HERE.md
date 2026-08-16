# FDS_CONTINUE_HERE

**State:** Issue #13 closes raw two-word/single-boundary dependency MITM for all 28 key-word placements.  
**Active:** `V25_BOUNDARY_WORD_XOR_PROJECTION_CANCELLATION_AUDIT`.

1. Use frozen W4_W6_SPLIT b16 plan under `research/v25/boundary-xor-cancellation/`.
2. Fresh targets are exactly `[61681,7339,53820,8140]`.
3. Splits 1..5; projections are 16 singles + 120 pairwise XORs at each split.
4. Test exact forward half-independence on the full 256x256 key grid.
5. Test the identical projection backward from each observed output; it must depend exactly on the opposite half on all four targets.
6. Only stable exact candidates may form 256+256 half match tables.
7. PASS requires true pair 4/4 and <=512 matches per target.
8. No approximate cancellation, 3+ word projection, alternate layout or second target set on FAIL.
9. Only exact PASS opens fresh TOTAL exponent scaling.
