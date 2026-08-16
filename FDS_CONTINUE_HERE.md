# FDS_CONTINUE_HERE

**State:** simple exact MITM branch closed; PNB exponent track historically closed; bit-puncturing method core recovered.  
**Next:** freeze `V25_REDUCED_QUARTER_ROUND_WALSH_TRAIL_VALIDATION`.

1. Do not reopen PNB exponent tuning or boundary MITM variants.
2. Use recovered exact modular-addition/subtraction Walsh coefficient semantics.
3. Freeze a small reduced word size, rotation rule, output masks, beam sizes/pruning, exact FWT reference and PASS gates before spectrum inspection.
4. Implement backward trail propagation through a complete ChaCha quarter-round, including exact XOR/rotation mask transport and four modular-addition expansions.
5. Merge duplicate input masks into linear-hull coefficients before pruning.
6. Compare partial-spectrum correlation/energy/error to exact truth-table Walsh spectrum.
7. Count trail expansion, merged coefficients, exact-reference cost and memory.
8. Only method-validation PASS may open source-orbit/key-ranking integration.
9. No alpha<1/full-round claim from quarter-round validation.
