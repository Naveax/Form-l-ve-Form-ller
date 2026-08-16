# FDS_DECISION_LOG

## 2026-08-16 — Issue #10 XOR half separability
0 exact bits on every fresh target; dense GF(2) ranks. `NO_GO_SIMPLE_8P8_XOR_SEPARABILITY`.

## 2026-08-16 — Issue #11 modular-additive half separability
Fresh b16 W5 8+8 tables showed no exact modular-additive width even at m4. Zero residual fraction at m4 was only ~6.9%; no common exact width; match set remains 65,536. `NO_GO_SIMPLE_MODULAR_8P8_SEPARABILITY`.

## Next
Audit exact dependency separation across internal boundaries with the two logical halves placed in separate key/state words. This targets a real bidirectional MITM prerequisite rather than another output transform.
