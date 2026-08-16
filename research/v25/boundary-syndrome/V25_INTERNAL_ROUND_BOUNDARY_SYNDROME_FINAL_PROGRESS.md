# V25 Internal Round-Boundary Candidate-Trajectory Syndrome

## Final verdict

`ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN`

`ALPHA_REDUCTION_NOT_DEMONSTRATED`

The family progressed through structural dependency cones, fresh survivor confirmation, candidate-ensemble cache optimization, and b=10..16 scaling.

### Stage0
All 80 `(split,word)` choices cost 18 QR versus 24 QR full-state. Frozen tie rule selected split1/word0. 10,240 partial/full equality checks passed.

### Stage1
Frozen b=10 targets and widths `[1,2,4,8,16,32]` were evaluated. Width16 was selected by minimum median TOTAL QR and left exactly one survivor on all 12 development targets. Conservative QR ratio: 0.858119.

### Stage2
Width16 on 12 untouched b=10 targets left one survivor on 12/12; true key survived 12/12 and direct word0 verification was unique 12/12. Conservative QR speedup: 1.16534x.

### Candidate-ensemble cache
For the current b<=32 layout only state word4 varies. Exact cached accounting is `15*2^b + 6 + 17*N_survivors` QR versus fair direct baseline `18*2^b + 3`. On untouched Stage2 targets median QR speedup was 1.1984x and median wall speedup 1.1313x; wall win 12/12.

### Stage3 scaling
| b | median survivors | median QR ratio | median QR speedup | median wall speedup |
|---:|---:|---:|---:|---:|
|10|1|0.834445|1.19840x|1.13412x|
|12|1|0.833611|1.19960x|1.12975x|
|14|1|0.833403|1.19990x|1.11990x|
|16|2.5|0.833372|1.19994x|1.15562x|

All 16/16 true keys survived and all 16 direct survivor verifications were unique. Exact QR log2 slope is 0.99967 and measured algorithm wall slope 1.00113. The leading term is `15*2^b`, therefore algorithmic alpha is exactly 1.

## Admitted
For the controlled 6-round reduced-key layout with active bits confined to key/state word4 and b=10..16, split1/word0 width16 boundary syndrome plus exact common-subexpression caching gives about 20% QR constant reduction and 12–16% measured Python wall reduction while preserving the true candidate on all frozen/fresh tests.

## Not admitted
alpha<1; subexponential key search; full-round relevance; arbitrary key-layout generality; arbitrary data compression.

## Next
Reduced-key layout transfer falsifier.
