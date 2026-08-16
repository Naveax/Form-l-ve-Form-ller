# FDS_CONTINUE_HERE

**State:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Active:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.

1. Use the frozen plan in `research/v26/recovered-bit-puncturing-dac/V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json`.
2. Preserve all prior NO-GO/inapplicable results and Stage0 separator evidence.
3. cap2: transform each exact signed column marginal through one exact bounded inverse QR and compare with explicit global first-layer hull + global next-column propagation + marginalization, all four columns.
4. Equality requires support, every signed coefficient, and energy within 1e-12.
5. cap3: no global joint materialization; construct all four transformed marginals with cached local QR hulls and packed signed merge.
6. PASS requires all cap2 exact checks plus complete cap3 transforms under 2 GiB peak RSS and 1 GiB total 24-byte compact representation.
7. Zero input marginals stay zero by linearity but are not evidence of absent joint correlations.
8. Only PASS opens a separately frozen pairwise/junction-tree cross-column contraction stage.
9. No AI prompt or alpha/full-round claim at this gate.
