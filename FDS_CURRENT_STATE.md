# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Its bounded-family result remains distinct from the full-exact Walsh line below.

The active work while historical measured-runtime provenance is blocked is mathematics-first exact Walsh tensor-network analysis. Code is a calculator/falsifier, not the research object.

## Exact q138 one-QR structural chain

For the full physical fixed-mask family of the q138 fixed-output exact one-quarter-round Walsh object, the complete certified dense-message upper-bound chain remains

`44 -> 42 -> 41 -> 40`.

- `44`: natural fused-site path;
- `42`: optimal fused-site carving tree;
- `41`: exact minimal-TT-core refinement;
- `40`: exact q138 rank-528 separator compression plus a complete 536-leaf / 535-internal-node contraction tree.

Width-40 authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`

`W<=40` remains the unconditional physical-family exact message-dimension upper bound. It is not an optimality theorem, arithmetic-work bound, arbitrary-mask result, double-round result or practical-memory claim.

## Width-40 bottleneck algebra

The unique `2^40` maximum cluster contains 171 leaves and splits `64|107` through six binary interface bits. Its 40 parent-external bits partition `16|24`.

### Left child

The 64-leaf map `L_64 : 2^16 -> 2^6` has exact rational rank 48 for all 64 relevant fixed T1/T2 input-bit combinations. Its exact 48-dimensional row space has only two classes, selected solely by the shared bit `u2_8`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48_THEOREM.md`
- `scripts/verify_v26_qr_q138_width40_left_rank48.py`

### Physical right-map quotient

The 107-leaf right map is an exact five-site transfer chain. The formal doubled Gram state has dimension 1024, but the physical q138 parity law fixes the generalized affine parity control to `p=0`.

The sharp physical reachable hull is

`1024 -> 162`,

with cumulative growth

`15 -> 70 -> 153 -> 162 -> 162`

and exact copy-swap split

`162 = 114 + 48`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`

The earlier 197-state theorem remains valid only for the larger generalized affine-control falsifier family; it is not the sharp physical state space.

## Exact physical fixed-mask rank envelope

The physical right map has twelve fixed input-mask controls:

- `u1_3,...,u1_7`;
- `u2_3,...,u2_8,u2_31`.

All `2^12=4096` physical cases are solved by exact rational transfer algebra.

Right-map envelope:

`11 <= rank(R_m) <= 38`.

Parent 171-leaf bottleneck envelope:

`5 <= rank(M_m) <= 27`.

More sharply:

- `u2_31=0`: right rank `22..38`, parent rank `16..27`;
- `u2_31=1`: right rank `11..19`, parent rank `5..8`.

The shared `u2_8` bit is rank-inert after the correct left row-space class is used.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

Thus every physical fixed-input/fixed-output q138 coefficient instance has an exact Schmidt factorization of the formal 40-bit bottleneck through at most 27 channels across the certified `16|24` partition. The rank basis may depend on the fixed mask.

## New conditioned global result: `u2_31=1`

The strong physical subclass

`u2_31=1`

has parent bottleneck rank at most 8 for every compatible fixed-mask instance.

Replace the certified 171-leaf bottleneck by two exact factors connected by a dimension-8 Schmidt bond, padding ranks 5, 6 or 7 with zeros when needed. Retain the pre-existing exact rank-528 compression elsewhere.

The resulting exact structural network has

- 367 tensor leaves;
- 366 internal nodes in the certified binary contraction tree;
- 467 nontrivial indices;
- 371 binary indices;
- 94 ternary indices;
- one dimension-528 bond;
- one dimension-8 Schmidt bond.

The complete machine-verified tree has maximum message dimension

`D_max = 528 * 2^30 = 566,935,683,072`,

so

`log2(D_max) = 39.04439411935845... < 40`.

The maximizing cluster contains 230 leaves and crosses exactly

- 27 binary indices;
- the rank-528 bond;
- the rank-8 Schmidt bond.

Therefore the exact source-conditioned chain is now

`44 -> 42 -> 41 -> 40 -> 39.044394119...`

for the physical `u2_31=1` subclass.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_u2_31_one_rank8_global_sub40.py`
- algebraic dependency: `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

This is the first admitted complete global message-width result below 40 in the exact q138 line, but it is explicitly conditioned on `u2_31=1`.

It does **not** prove `W<=39`, global optimality, an arithmetic-work exponent reduction, a universal mask-independent rank-8 basis, or a sub-40 result for `u2_31=0`.

## Current sharp mathematical bottlenecks

Two exact directions remain active.

### A. General physical family

Use the exact uniform `rank(M_m)<=27` envelope to seek a complete sub-40 global tree for all physical fixed masks. The old outside-tree topology is insufficient by itself: exact dynamic programming over placements still reaches 40. That is a scoped topology result, not a lower bound or NO-GO.

If another global geometry does not close below 40, isolate the exact residual cluster and analyze its algebraic separator rather than returning to blind ordering search.

### B. Strong `u2_31=1` subclass

The new maximum is `528*2^30`, only about 0.0444 bits above the clean threshold 39. The next exact target is to remove at least one binary degree of freedom from that maximizing message, or algebraically compress the rank-528/binary separator, and then require another complete tree certificate before claiming `W<=39`.

Only after exact rank/geometry mechanisms stall should certified epsilon-rank/tail approximation become active.

## Measured-execution blocker

The frozen historical project-cap QR measurement remains blocked by the missing exact recovered V25 runtime bytes.

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Required identities:

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

This remains a provenance blocker, not a mathematical NO-GO.

After byte recovery: SHA-locked rematerialization -> prove exact historical cap semantics -> historical `19/19 PASS` -> frozen cap2 all-column QR regression -> only PASS opens cap3 under the existing resource gates.

Still not admitted: practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.
