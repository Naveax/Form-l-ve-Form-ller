# FDS_CHECKLIST

## Boundary syndrome — closed/admitted
- [x] Stage0 80 dependency cones enumerated.
- [x] 10,240 exact partial/full checks PASS.
- [x] Stage1 widths/targets frozen; width16 selected by frozen rule.
- [x] Stage2 untouched 12-target confirmation PASS.
- [x] Candidate-ensemble cache exact vs generic reference.
- [x] Cached Stage2 QR + wall win on 12/12.
- [x] Stage3 b10/12/14/16 scaling PASS.
- [x] Boundary regression 6/6 PASS; py_compile PASS.
- [x] Admit reduced-model constant-factor compute win.
- [x] Record alpha=1 / no exponent reduction.

## Active — layout transfer falsifier
- [ ] Freeze tested b=10 active-bit layouts.
- [ ] Freeze fresh targets before measurement.
- [ ] Derive exact candidate-dependent QR/cache cost per layout.
- [ ] Exact generic-vs-specialized equivalence tests.
- [ ] Survivor correctness and TOTAL QR per layout.
- [ ] Fair wall benchmark only after exactness passes.
- [ ] Scope or extend admitted claim based on frozen gates.
- [ ] Commit source/tests/results/manifest + continuity.
