# FDS_CONTINUE_HERE

**State:** recovered bit-puncturing/D&C Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Next:** freeze `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.

1. Preserve all prior NO-GO/inapplicable results and Stage0 exact marginal evidence.
2. Do not interpret zero column marginals as absent joint correlation.
3. Apply one next-layer inverse QR linearly to each exact signed column marginal; this is an exact marginal transform but not a joint four-column contraction.
4. cap2 must match explicit global first-layer hull + exact next-column QR propagation for all four columns.
5. Measure cap3 transformed support/time/RSS for all columns under a separately frozen budget before attempting cap4.
6. If transformed marginal already explodes, kill this separator route before joint tensor work.
7. Only a PASS opens a pairwise/junction-tree cross-column contraction plan.
8. No AI prompt yet; real separator behavior is now measurable locally.
9. No alpha/full-round claim.
