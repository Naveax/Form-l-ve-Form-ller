# FDS_CONTINUE_HERE

**State:** Issue #9 `PASS_COLLISION_TOLERANT_CONSTANT_FACTOR_ALPHA1`; Issue #8 remains NO-GO.  
**Next:** freeze and run `V25_BOUNDARY_SYNDROME_KEY_HALF_SEPARABILITY_AUDIT`.

1. Resolve fresh main + authority.
2. Treat Issue #5–#9 outcomes as immutable.
3. Stop widening the constant-factor screening family; alpha is still 1.
4. Freeze a b=16 logical 8+8 key split, fresh target(s), exact separability metrics, controls and kill gates before inspection.
5. Build the complete 256×256 16-bit syndrome table with the exact admitted evaluator.
6. Test exact XOR rectangle identities and GF(2) rank per syndrome bit; low-rank approximations are secondary only.
7. Translate any exact structure into explicit MITM TOTAL work including table construction, matching, collisions and verification.
8. Admit an exponent claim only if TOTAL asymptotics are genuinely below `2^b`; otherwise close the half-key family.
9. Commit plan/source/tests/results/decision/manifest and update continuity.

No full-round claim; no post-hoc split/target tuning.
