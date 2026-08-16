# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| Issue #9 verified screen | constant-factor gates pass | PASS alpha=1 |
| Issues #10/#11 half-output separability | exact gates fail | NO-GO |
| Issues #12/#13 raw dependency MITM | 0 candidates | NO-GO |
| Issue #14 single/pair boundary XOR cancellation | 156 forward -> 0 first-target opposite candidates | NO-GO |
| Full linear XOR nullspace audit | not frozen | NEXT |
| alpha<1 | — | NOT DEMONSTRATED |
