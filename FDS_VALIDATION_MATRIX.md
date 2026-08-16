# FDS_VALIDATION_MATRIX

| Family | Fresh/Exact result | Verdict |
|---|---|---|
| Boundary syndrome b10..16 | correctness+QR+wall gates PASS | constant-factor win admitted |
| Layout transfer L1 QR | 48/48 unique true; 5/5 non-control gates PASS | broad QR transfer admitted |
| Generic layout cache exactness | 147,456 equality/predicate checks PASS | exact engine admitted |
| Generic layout cache wall | 0/5 non-control median wall gates PASS | no broad generic wall transfer |
| Specialized codegen wall | fresh targets frozen; not measured | ACTIVE NEXT |
| alpha<1 | leading term remains C*2^b | NOT DEMONSTRATED; alpha=1 |
| full-round relevance | — | NO CLAIM |
