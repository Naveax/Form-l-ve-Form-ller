# FDS_CONTINUE_HERE

**State:** recovered bit-puncturing/D&C separator Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Active:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Execution blocker:** the exact recovered `fds_v25_bit_puncturing.py` source is not present in current Git `main` or the current `/mnt/data` mount.

1. Use the frozen plan in `research/v26/recovered-bit-puncturing-dac/V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER_PLAN.json`.
2. Preserve all prior NO-GO/inapplicable results and Stage0 separator evidence.
3. First re-materialize the recovered bit-puncturing core and require SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`; do not substitute a rewritten core silently.
4. Restore the recovered runtime dependencies and re-run the historical `19/19 PASS` baseline before new measurement.
5. The cap2 falsifier implementation/reference/test are committed. Run all four columns only after the provenance gate passes.
6. cap2 equality requires exact support plus every signed coefficient and energy within `1e-12`.
7. cap3: no global joint materialization; construct all four transformed marginals with cached local QR hulls and packed signed merge.
8. PASS requires all cap2 exact checks plus complete cap3 transforms under 2 GiB peak RSS and 1 GiB total 24-byte compact representation.
9. Zero input marginals stay zero by linearity but are not evidence of absent joint correlations.
10. Only PASS opens a separately frozen pairwise/junction-tree cross-column contraction stage. No AI prompt or alpha/full-round claim at this gate.
