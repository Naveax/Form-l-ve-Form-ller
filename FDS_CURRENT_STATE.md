# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Its bounded-family result remains distinct from the full-exact Walsh line below.

The active work while historical measured-runtime provenance is blocked is mathematics-first exact Walsh tensor-network analysis. Code is a calculator/falsifier, not the research object.

## Exact q138 one-QR structural chain

For the q138 fixed-output exact one-quarter-round Walsh object, the complete certified dense-message upper-bound chain remains

`44 -> 42 -> 41 -> 40`.

- `44`: natural fused-site path;
- `42`: optimal fused-site carving tree;
- `41`: exact minimal-TT-core refinement;
- `40`: exact q138 rank-528 separator compression plus a complete 536-leaf / 535-internal-node contraction tree.

Width-40 authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`

`W<=40` is an exact message-dimension upper bound for this q138 fixed-output one-QR representation. It is not an optimality theorem, arithmetic-work bound, arbitrary-mask result, double-round result or practical-memory claim.

## Width-40 bottleneck

The unique `2^40` maximum cluster contains 171 leaves and splits `64|107` through six binary interface bits. Its 40 parent-external bits partition `16|24`.

### Left child

The 64-leaf map

`L_64 : 2^16 -> 2^6`

has exact rational rank 48 for all 64 combinations of its six relevant fixed T1/T2 input bits.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48_THEOREM.md`
- `scripts/verify_v26_qr_q138_width40_left_rank48.py`

A stronger row-space fact is now known: the exact 48-dimensional left row space has only two classes, selected solely by the shared bit `u2_8`. The other five left fixed bits do not change the row space.

## Five-site right-map transfer structure

The opposite 107-leaf map factors exactly over sites `3,4,5,6,7`, with site sizes

`18,21,21,21,26`.

Every interior site cut carries exactly five binary sigma/carry bits, so

- one-copy hidden state dimension = `32`;
- doubled Gram state dimension = `1024`.

The earlier generalized affine-control family allowed `tau=(u1,u2,p)` and gave an exact common reachable hull of dimension 197 with copy-swap split `138+59`. That theorem remains valid for that larger model.

However the physical q138 parity relation is exactly

`u4_i xor v3_{i+12} xor w2_i = 0`,

so `p_i=0` is not a physical fixed-mask control.

## Sharp physical quotient: `1024 -> 162`

Restricting to the four physical interior transfer types `(u1,u2,p=0)` gives exact cumulative reachable dimensions

`15 -> 70 -> 153 -> 162 -> 162`.

Therefore the sharp physical doubled reachable hull is

`dim U_phys = 162`.

Copy exchange splits it exactly as

`162 = 114 + 48`

with symmetric/antisymmetric sectors.

In `(u1,u2)=00,01,10,11` order, transfer ranks restricted to the physical hull are

`159,79,99,97`.

Symmetric-block ranks:

`112,56,71,66`.

Antisymmetric-block ranks:

`47,23,28,31`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`

Do not use the 197-state generalized hull as the sharp physical q138 state space. It remains useful only as an independent larger-family check.

## Exact physical fixed-mask rank envelope

The actual right-map fixed controls are

- `u1_3,...,u1_7`;
- `u2_3,...,u2_8,u2_31`.

There are exactly `2^12=4096` physical fixed-mask cases.

Exact rational transfer enumeration over this finite family gives

`11 <= rank(R_m) <= 38`.

The shared `u2_8` bit is right-rank inert.

The bit-31 boundary control creates a strong split:

- `u2_31=0`: right rank `22..38`;
- `u2_31=1`: right rank `11..19`.

Combining each right Gram space with the correct one of the two exact left row-space classes gives the 171-leaf parent envelope

`5 <= rank(M_m) <= 27`.

More sharply:

- `u2_31=0`: parent rank `16..27`;
- `u2_31=1`: parent rank `5..8`.

The previous fixed-mask checks are reproduced exactly:

- zero representative: `(right,parent)=(34,23)`;
- all-one representative: `(19,8)`;
- previous high representative: `(37,26)`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

Thus every physical fixed-input/fixed-output q138 coefficient instance has an exact Schmidt factorization of the formal 40-bit parent bottleneck through at most 27 channels across the certified `16|24` partition.

The rank basis may depend on the fixed mask. This is a uniform rank-dimension envelope, not a claim of one universal 27-dimensional basis for all masks simultaneously.

## Current sharp mathematical bottleneck

The active problem is now **global reinsertion of the uniform physical rank envelope**.

1. Use the exact `rank(M_m)<=27` factorization for the certified 171-leaf bottleneck.
2. Rebuild the global q138 fixed-IO one-QR network with the parent kept factorized through a bond of dimension at most 27.
3. Seek a complete contraction tree/work certificate strictly below the current `W<=40` dense-message baseline.
4. Require a complete machine-verifiable tree before changing the admitted global width.
5. If pure geometry stalls, analyze whether the rank-27 family itself has a common sector decomposition or mask-conditioned transfer basis that can be attached to the outside network without dense parent materialization.
6. Only after exact algebraic routes stall should certified epsilon-rank/tail approximation become active.

Exploratory reinsertion already shows very small top-level balanced separators, but one natural recursive geometry still encounters a subproblem that cannot split below 40. This is only a scoped geometry result, not a lower bound or mathematical NO-GO for `W<40`.

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
