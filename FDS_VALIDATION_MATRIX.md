# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| Issue #9 collision-tolerant verified screen | all fresh gates pass | PASS constant factor, alpha=1 |
| Issues #10/#11 half-output factorization | exact gates fail | NO-GO |
| Issues #12/#13 raw dependency MITM | 0 candidates | NO-GO |
| Issue #14 single/pair XOR cancellation | first fresh backward target kills all forward candidates | NO-GO |
| Issue #15 full linear XOR mask nullspace | all combined spaces rank16/nullity0 | NO-GO family-wide |
| Simple exact half-key MITM branch | multiple exact mechanisms exhausted | CLOSED |
| Conditional PNB/syncopation | historical positive neutrality, no work gain yet | NEXT RECOVERY |
| alpha<1 | — | NOT DEMONSTRATED |
