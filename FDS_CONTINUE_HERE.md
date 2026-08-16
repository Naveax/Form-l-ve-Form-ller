# FDS_CONTINUE_HERE

**State:** Issue #12 W4_W6 single-boundary disjoint-half MITM NO-GO.  
**Next:** freeze exhaustive all-two-key-word layout dependency search.

1. Target-free structural audit only.
2. Enumerate all 28 unordered active key/state-word pairs from words 4..11.
3. For each layout enumerate all 80 internal cones.
4. Use the identical exact support criterion from Issue #12.
5. PASS only if at least one layout/cone gives `{wordA}` vs `{wordB}` nonempty disjoint coverage.
6. Numerical target/TOTAL work opens only for such candidates.
7. If zero candidates among 2,240 layout-cones, close simple two-word single-boundary dependency-separated MITM globally for this reduced 6-round structure.
8. No approximate dependency or target tuning.
