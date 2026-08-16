# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / source-conditioned rank analysis.

Do not reduce the project to code recovery. Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank contraction structure.

## Current exact q138 chain

For the q138 fixed-output one-quarter-round exact Walsh object, the certified global dense-message upper-bound chain is

`44 -> 42 -> 41 -> 40`.

Core authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_MAP_RANK528_THEOREM.md`
- `scripts/verify_v26_qr_width41_left_rank528.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_BOTTLENECK_RANK64_BOUND.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48_THEOREM.md`
- `scripts/verify_v26_qr_q138_width40_left_rank48.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_RANK_CONDITIONING_FALSIFIER.md`
- `scripts/verify_v26_qr_q138_right_map_rank_conditioning.py`

Width-40 proof chain:

1. width-41 bottleneck child topology interface `3072`;
2. q138 exact rank `528`;
3. exact rank-factor replacement;
4. modified 536-leaf network;
5. complete 535-node contraction tree;
6. maximum exact formal message `2^40` on one 171-leaf cluster.

## New 171-leaf bottleneck facts

The 171-leaf maximum cluster splits `64|107`.

- 40 parent-external bits split `16|24`;
- child interface is six binary bits;
- topology therefore gives parent Schmidt rank `<=64`.

The 64-leaf left map is now solved exactly:

`rank(L_64)=48`.

This rank is exact for all 64 combinations of the six relevant fixed T1/T2 input-mask bits, up to affine internal index relabelings. The six-bit raw interface therefore has a uniform exact `64 -> 48` algebraic compression.

The opposite 107-leaf map is qualitatively different: its rank changes with fixed input masks. Exact examples include

- right rank `34`, parent rank `23`;
- right rank `19`, parent rank `8`;
- right rank `37`, parent rank `26`.

Therefore **do not** promote any one of those right/parent ranks to a q138-wide invariant.

`W<=40` remains the admitted complete-tree global bound. A natural rank-48 reinsertion did not close a complete `W<=39` tree, but that is only a scoped geometry result, not a lower bound.

## First unfinished mathematical pass

The next pass is **source/input-conditioned right-map rank classification**.

Work in this order:

1. rerun the exact baselines:
   - `scripts/verify_v26_qr_width41_left_rank528.py`;
   - `scripts/verify_v26_qr_q138_algebraic_width40.py`;
   - `scripts/verify_v26_qr_q138_width40_left_rank48.py`;
   - `scripts/verify_v26_qr_q138_right_map_rank_conditioning.py`;
2. identify which fixed input-mask bits in the 107-leaf map genuinely change rank and which are only internal state relabelings/gauge;
3. derive a compact sector invariant or small control-bit set for
   - `rho_R(m)=rank R_m`, or preferably
   - `rho_parent(m)=rank(L_m R_m)`;
4. characterize the fixed-mask family actually reachable/relevant to the q138 source-conditioned path rather than optimizing over arbitrary impossible masks;
5. prove a uniform rank envelope on that relevant family or partition it into finitely many exact rank classes;
6. only after that, replace the 171-leaf bottleneck by conditioned rank factors and seek a complete globally verified representation/tree below the current width-40 baseline;
7. if exact conditioned ranks remain too large, activate certified epsilon-rank only with an explicit residual budget.

Prefer theorem -> sector law -> finite falsifier. Do not substitute a brute-force scan of arbitrary masks for the mathematical classification.

## Measured execution remains frozen behind provenance

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Preferred snapshot SHA-256:

`fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`

Core SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

When bytes become available:

1. SHA-locked rematerialization;
2. prove exact historical project-cap semantics/normalization/nestedness;
3. reproduce historical `19/19 PASS`;
4. run the already-frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing 2 GiB RSS / 1 GiB compact gates.

Still no admitted practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer solution, ranking gain, `alpha<1`, or full-round relevance.
