# V26 Source-Orbit Counter Cube Superpoly ANF Audit

Frozen Issue #19 Stage0 completed without retuning.

Two exact 8-dimensional public-counter cubes were restricted entirely to the canonical sequential source orbit: counters `512..767` and `1024..1279`.

Each cube XOR-sums all 256 assignments of the low 8 counter bits. Exact key ANFs were computed for b=8/10/12/14/16, R4 control and R6 primary, all 512 output bits, against same-base single-counter controls.

R6 b16: base512 degree reduction `0`, support-exponent reduction `+5.09065e-05`; base1024 degree reduction `0`, support-exponent reduction `+2.61937e-05`; sparse-useful bits `0` at both bases; stable sparse bits across both bases and b14/b16 `0`.

All **5/5 primary gates fail**. Decision: `NO_GO_SOURCE_ORBIT_COUNTER_CUBE_ANF`. No cube dimension/base/output/threshold retuning, no second development set, and no superpoly-solving stage.
