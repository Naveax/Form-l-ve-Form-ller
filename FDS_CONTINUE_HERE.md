# FDS_CONTINUE_HERE

**State:** Issue #14 single/pair XOR cancellation NO-GO.  
**Active:** `V25_FULL_LINEAR_BOUNDARY_WORD_XOR_NULLSPACE_AUDIT`.

1. Use frozen W4_W6_SPLIT b16 plan and fresh targets `[25053,23109,35877,44733]`.
2. Do not enumerate projection arity manually; cover all 65,535 nonzero GF(2) masks by exact 16-variable nullspace algebra.
3. For each split/orientation build forward half-variation equation span.
4. Add opposite-half backward equation spans for all four fresh outputs.
5. Rank16 means nullity0 and kills all nonzero masks at once.
6. Only stable nonzero masks may form 256+256 equality-match tables.
7. PASS requires true pair 4/4 and <=512 matches on every target.
8. No approximate nullspace, target-specific mask or second target set.
9. Only exact PASS opens fresh TOTAL exponent scaling.
