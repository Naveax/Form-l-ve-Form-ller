# FDS_CONTINUE_HERE

**State:** Issues #10 XOR and #11 modular 8+8 separability are NO-GO; Issue #9 constant-factor PASS; alpha=1.  
**Next:** freeze exact disjoint-half dependency-cone MITM audit.

1. New audit is structural/target-free first.
2. Use b16 logical halves placed in separate active state words via `W4_W6_SPLIT` (low half word4, high half word6).
3. Enumerate all 80 split1..5 / word0..15 cones.
4. For each cone derive active key-half support needed by forward initial-state cone and backward implied-final-state cone.
5. Primary structural PASS requires the two sides to be nonempty, disjoint, and together cover both halves, i.e. `{low}` vs `{high}` in either orientation.
6. Only such a cone may open exact numerical MITM equality and TOTAL tests.
7. If none exists, close simple single-boundary dependency-separated MITM immediately.
8. No target tuning or approximate dependency rescue.
