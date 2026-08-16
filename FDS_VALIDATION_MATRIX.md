# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| Boundary syndrome b10..16 word4 | exact/QR/wall PASS | constant-factor win admitted |
| Layout QR transfer b10 | 5/5 non-control PASS | broad QR transfer |
| Generic layout wall | 0/5 PASS | NO-GO |
| Specialized codegen exactness | 98,304 fresh checks PASS | exact |
| Specialized codegen b10 wall | 4/5 non-control PASS | broad non-universal wall realization |
| Multi-layout codegen scaling b10..16 | frozen, not measured | ACTIVE NEXT |
| alpha<1 | leading `2^b` | NOT DEMONSTRATED; alpha=1 |
| full-round | — | NO CLAIM |
