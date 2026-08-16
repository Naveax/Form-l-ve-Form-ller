# V25 Boundary Syndrome Key-Half Separability Audit

Frozen Issue #10 plan completed without retuning.

For each of four fresh b16 `W5_SINGLE` targets, the complete 256×256 low16 syndrome table was evaluated.

Primary exact XOR rectangle test:
- exact XOR-separable syndrome bits target43051: `[]`;
- target21863: `[]`;
- target31754: `[]`;
- target45567: `[]`;
- stable exact positions across all targets: **0**.

With no stable exact bits, the derived half-signature condition retains all **65,536** half pairs on every target. The primary >=8-bit / <=512-match gate therefore fails immediately.

Dense diagnostics reinforce the exact result: raw syndrome-bit GF(2) ranks lie in **254–256** and rectangle-residual ranks in **253–255**.

Decision: `NO_GO_SIMPLE_8P8_XOR_SEPARABILITY`. Approximate/SVD diagnostics cannot rescue the failed exact gate by preregistration. No MITM scaling stage is opened.
