# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / source-conditioned rank compression.

Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank contraction structure.

## Current exact q138 chain

For the full physical fixed-mask family, the complete certified dense-message upper-bound chain remains

`44 -> 42 -> 41 -> 40`.

The width-40 maximum cluster has 171 leaves, 40 binary external indices, and certificate split `64|107` through six binary interface bits. Its external partition is `16|24`.

Exact physical rank facts:

- left 64-leaf child rank = `48`;
- physical right doubled reachable hull = `162 = 114 + 48`;
- over all 4096 physical fixed masks, right rank = `11..38`;
- parent 171-leaf bottleneck rank = `5..27`;
- `u2_31=0`: parent rank `16..27`;
- `u2_31=1`: parent rank `5..8`.

Core authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

## New complete conditioned global result

For the physical subclass

`u2_31 = 1`,

the 171-leaf bottleneck can be replaced exactly by a Schmidt bond of dimension at most 8.

After reinserting a uniform dimension-8 bond into the rank-528-compressed global network, a complete machine-verified contraction tree now exists with

`367` leaves and `366` internal nodes.

Its maximum exact message dimension is

`528 * 2^30 = 566,935,683,072`,

so

`W <= 39.04439411935845... < 40`.

The maximizing 230-leaf cluster crosses

- 27 binary indices;
- one dimension-528 bond;
- one dimension-8 bond.

Read:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_u2_31_one_rank8_global_sub40.py`

Proof dependency:

- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

For this subclass the admitted exact structural chain is therefore

`44 -> 42 -> 41 -> 40 -> 39.044394119...`.

Do **not** generalize this conditioned sub-40 result to `u2_31=0`, the whole physical fixed-mask family, arbitrary masks, double round or full round.

## First unfinished mathematical pass

Two routes are now distinct. Continue in this priority order.

### Route 1 — conditioned `u2_31=1`: target `W<=39`

1. rerun:
   - `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`;
   - `scripts/verify_v26_qr_q138_u2_31_one_rank8_global_sub40.py`;
2. reconstruct the unique 230-leaf cluster realizing `528*2^30`;
3. treat its boundary as `27 binary + rank528 + rank8` and identify a useful child/interface partition;
4. derive topology-only Schmidt bounds first;
5. then compute exact algebraic rank of the smaller child map where tractable;
6. one eliminated binary degree of freedom is already enough to cross the clean `W<=39` threshold;
7. if rank deficiency is found, reinsert it and require another **complete** global tree certificate before changing the bound.

A fixed-topology dynamic program shows `39.044394...` is optimal only inside the preserved old outside-tree topology. A targeted split search on the current 231-leaf parent found no balanced `<=39` split; only extreme singleton peeling survives. These are scoped topology observations, not a global lower bound or NO-GO for `W<=39`.

### Route 2 — full physical family: rank-27 global reinsertion

1. replace the certified 171-leaf bottleneck by a mask-conditioned Schmidt factorization with bond dimension `rho_m<=27`;
2. use 27 as a safe uniform structural bond dimension, zero-padding smaller ranks;
3. rebuild the complete global network;
4. seek a complete sub-40 contraction tree;
5. the preserved old outside-tree topology still reaches 40, so do not waste effort pretending that topology is a lower bound;
6. if a different global geometry still stalls, isolate the exact residual cluster and attack its algebraic separator rather than returning to blind ordering search.

Only after exact algebraic/geometry mechanisms stall should certified epsilon-rank/tail approximation become active.

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

Still not admitted: practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer solution, ranking gain, `alpha<1`, or full-round relevance.
