# FDS_CONTINUE_HERE

**State:** Issue #14 single/pair boundary XOR cancellation NO-GO; Issues #10–#13 also structural NO-GO; alpha=1.  
**Next:** freeze full-linear boundary-word XOR nullspace audit.

1. Treat single/pair projection search as closed.
2. New audit must cover the entire nonzero GF(2) linear span of 16 boundary words at each split, not hand-picked higher arity masks.
3. Use exact bit-level linear constraints derived from half-variation differences.
4. Intersect forward one-half-independence nullspace with opposite backward-independence nullspaces over fresh outputs.
5. PASS only if a nonzero stable mask exists and produces bounded half-table matches.
6. No approximate nullspace, target-specific mask, or second target set on FAIL.
7. Only exact PASS opens TOTAL exponent scaling.
