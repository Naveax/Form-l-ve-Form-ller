# V25 Internal Round-Boundary Candidate-Trajectory Syndrome — Stage0

## Verdict

`PASS_CONSTANT_FACTOR_ONLY`

A purely structural dependency-cone audit was run before any Stage1 target/oracle selection.

- 6 reduced ChaCha rounds = 24 full quarter-round evaluations.
- All 80 `(split, boundary_word)` combinations for splits 1..5 and words 0..15 were enumerated.
- Every combination has exact forward+backward dependency-cone cost **18 QR**.
- Frozen tie rule therefore selects `split=1, word=0`: 1 forward QR + 17 backward QR.
- Partial forward/inverse word evaluators were checked against full-state round boundaries on 64 deterministic random states.
- 80 cones × 64 states × two directional equality checks = **10,240 exact equality checks**, all PASS.

This is a real 25% QR-count reduction relative to naïve 24-QR full-permutation verification, but candidate enumeration remains `2^b`. It is only a constant-factor opportunity; `alpha < 1` is not demonstrated.

## Fair Stage1 baseline

Stage1 will not compare against an intentionally wasteful 24-QR full-state verifier. A single final output word has a direct dependency cone of **21 QR**, so the fair direct-word baseline is `21 * 2^b` QR evaluations. The Stage0 syndrome screen costs `18 * 2^b` before survivor verification.
