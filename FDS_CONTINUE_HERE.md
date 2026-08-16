# FDS_CONTINUE_HERE

**State:** exact XOR and modular half-output decompositions are NO-GO; Issue #9 constant-factor PASS; alpha=1.  
**Active:** `V25_DISJOINT_HALF_DEPENDENCY_BIDIRECTIONAL_MITM_CONE_AUDIT`.

1. Use frozen target-free plan under `research/v25/dependency-mitm/`.
2. W4_W6_SPLIT only: low half state4, high half state6.
3. Enumerate all 80 split1..5 / word0..15 cones.
4. Compute exact initial-side and final-side active half support sets.
5. PASS only for exact `{4}` vs `{6}` disjoint coverage in either orientation.
6. If none exists, close this simple single-word boundary MITM immediately.
7. Numerical half-table/target work opens only after structural PASS.
8. No approximate dependency or multi-boundary rescue in this milestone.
