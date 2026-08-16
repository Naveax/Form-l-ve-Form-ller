# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / source-conditioned rank compression.

Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank contraction structure.

## Current exact q138 chain

For the q138 fixed-output one-quarter-round exact Walsh object, the complete certified dense-message upper-bound chain remains

`44 -> 42 -> 41 -> 40`.

The width-40 maximum cluster has 171 leaves, 40 binary external indices, and certificate split `64|107` through six binary interface bits. Its external partition is `16|24`.

Left child:

`rank(L_64)=48`.

The exact left row space has only two classes, selected by the shared fixed bit `u2_8`.

## Sharp physical right-map quotient

The generalized affine `p`-control analysis and its 197-state hull remain valid for the larger falsifier family, but the physical q138 parity relation fixes `p=0`.

Physical doubled reachable hull:

`1024 -> 162`.

Exact cumulative growth:

`15 -> 70 -> 153 -> 162 -> 162`.

Copy-swap split:

`162 = 114 + 48`.

Read:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`

## Exact physical rank envelope

The physical right map has twelve fixed input-mask controls:

- `u1_3,...,u1_7`;
- `u2_3,...,u2_8,u2_31`.

All `4096` physical cases are now solved by exact rational transfer algebra.

Right map:

`11 <= rank(R_m) <= 38`.

Parent 171-leaf bottleneck:

`5 <= rank(M_m) <= 27`.

Boundary split by `u2_31`:

- `u2_31=0`: right `22..38`, parent `16..27`;
- `u2_31=1`: right `11..19`, parent `5..8`.

The shared `u2_8` bit is rank-inert after the correct left row-space class is used.

Read:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

The theorem reproduces the previous exact fixed-mask checks `(34,23)`, `(19,8)`, `(37,26)`.

Therefore every physical fixed-input/fixed-output q138 coefficient instance admits an exact bottleneck factorization across the certified `16|24` partition through at most 27 Schmidt channels.

The rank basis may depend on the fixed input mask. Do not promote this to one universal 27-dimensional basis without an additional theorem.

## First unfinished mathematical pass

The next pass is **global rank-27 reinsertion**.

Work in this order:

1. run the exact baselines:
   - `scripts/verify_v26_qr_q138_physical_right_hull162.py`;
   - `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`;
   - `scripts/verify_v26_qr_q138_algebraic_width40.py`;
2. replace the certified 171-leaf bottleneck by an exact mask-conditioned rank factorization
   - left external side: 16 binary indices;
   - right external side: 24 binary indices;
   - internal Schmidt bond dimension `rho_m <= 27`;
3. use 27 as the uniform structural bond bound while keeping in mind that individual masks may use smaller ranks;
4. rebuild the whole fixed-IO q138 one-QR hypergraph and search for a **complete** contraction tree with maximum message dimension strictly below the current `2^40` baseline;
5. do not claim `W<40` from a small root separator or isolated low-boundary cuts; every non-root cluster must be verified;
6. if no complete sub-40 tree closes, identify the exact residual cluster that forces 40 in that geometry and analyze its algebraic separator rather than returning to blind ordering search;
7. separately exploit the `u2_31=1` rank-8 branch as a strong source-conditioned subclass and test whether it admits a substantially smaller complete certificate;
8. only after exact rank/geometry mechanisms stall should certified epsilon-rank/tail approximation become active.

Exploratory rank-27 reinsertion already yields a very small balanced top-level separator, but one natural recursive continuation still hits a subproblem whose best split is 40. That is a scoped geometry falsifier only, not a lower bound or NO-GO for `W<40`.

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
4. run the frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing resource gates.

Still no admitted practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer solution, ranking gain, `alpha<1`, or full-round relevance.
