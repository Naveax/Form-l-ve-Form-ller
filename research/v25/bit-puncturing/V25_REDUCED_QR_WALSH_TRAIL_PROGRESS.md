# V25 Reduced Quarter-Round Walsh Trail Validation

Frozen Issue #16 completed without beam/mask retuning.

Implementation gate: n=2 no-prune complete trail enumeration reproduces the exact quarter-round FWT spectrum coefficient-wise within 1e-12. Combined puncturing/trail tests: **11/11 PASS**.

n=5 beam4096:
- A0: cosine² 1.000000, exact-support 1.000000, 700 coeffs;
- B1: cosine² 0.789061, support 0.789862, 4096 coeffs;
- C2: cosine² 0.881276, support 0.881939, 4096 coeffs;
- D3: cosine² 1.000000, support 1.000000, 1060 coeffs.

Compactness gates pass, but the frozen >=0.90 quality gate fails for B1 and C2. Therefore q138/source-orbit integration is not opened at this beam budget.

Decision: `NO_GO_QR_TRAIL_BEAM4096_QUALITY`. Plan forbids extending beam after inspection. The trail engine remains semantically validated; this result is a budget/quality NO-GO, not an implementation failure.
