# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`.

Historical measured execution remains frozen behind missing exact recovered V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is only a calculator/falsifier and every admitted finite claim requires clean-checkout verification.

## One-QR exact authority

For all4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925... <39`.

Current sharp peak `218*2^31`. Old support216 / 13 support classes / rank12 selector is revoked. Exact I9 support is117..218 over64 left masks; support-indicator rank64; `epsilon=0`. Physical right rank11..38, parent rank5..27, right doubled hull162, all64 left maps share an exact48-dimensional interface row space.

Gram-image objects (`G_m=R_mR_m^T`, span124/U47 diagnostics) are rank-space objects, not single-copy coefficient amplitudes.

## d=1 ledgers

Keep distinct:

- topology-only `W_2_topo<=236`;
- coefficient-blind static reduced-central-graph + four-generic-leaf method `W_2_static,blind=95`, method-optimal inside that representation;
- coefficient-aware materialized-factor generation `W_2_factor-gen<=78+log2(171)=85.4178525148859...`;
- exact representation existence `W_repr(1)<=78+log2(171)=85.4178525148859...`.

The last two are message/storage constructivity bounds, not arithmetic-work bounds. Unrestricted scalar streaming/recomputation has no canonical width without a work budget.

### Static coefficient-blind95

Clean MILP cardinality minima for central graph smaller-side sizes11..16 are `51,52,55,54,55,56`. Adding four generic leaf costs gives `95,100,107,110,115,120`. Balanced-edge lemma forces some11..16 edge in every32-leaf binary tree; existing tree attains95. Clean run `32028136767`.

### Block1 and extended block2

Block1 exact rank16 on physical rows `A0,B0,C15,C16,D0`.

Historical block2 rank2784 is exact.

Extended block2 adds physical `A12,B12,D12`, closing D12 at j1 bit12 and j2 bit28. Physical rows are

`A12..16,B12..16,D12..16,C0`.

Exact geometry:

- fixed D12..16 j1 rank448;
- fixed D12..15, D16 pair union472, intersection424;
- sixteen j2-high D12..15 vectors independent;
- D16 bit0 spaces rank2+2, union3, intersection1;
- per high prefix1368;
- total `rank(block2_ext)=16*1368=21888`.

Naive old block2 times three raw bits is22272, so the exact gain is58/57.

Clean run `32033308335`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_SIGNED_BLOCK2_EXTEND12_RANK21888_THEOREM.md`;
- `scripts/verify_v26_q138_signed_block2_extend12_rank21888.py`.

### d=1 representation and factor generation

Central S1 rank bound:

`16*21888*2^23 =171*2^34`.

Four predecessor leaves contribute exponent44, so

`W_repr(1)<=W_factor-gen<=78+log2(171)=85.4178525148859...`.

Clean factor-generation run `32033507588`.

A complete materialized factor still contains

`171*2^78 = 51,681,578,788,525,397,218,689,024`

scalars. No arithmetic-work reduction is admitted.

## Exact d=1 no-gain closures

### Block2 D11

The next repeated external D11 one-bit transfer is injective on the relevant j1/j2 carry interfaces and preserves block2 rank21888.

Clean run `32038491628`.

### Block1 C12..C14

- block1 + C13,C14 rank64=`16*4`;
- block1 + C12,C13,C14 rank128=`16*8`.

No compression. Clean run `32038564342`.

### Block1 repeated-D through D3

The occurrence-closed D0..2 block has rank1024=`16*2^6`.

The D3 local coupled-carry map has rank24/32 with an explicit8D kernel. However both old s2 projections have rank1024, so the local kernel misses the actual incoming space.

Thus

`rank(D0..3)=8192=16*2^9`.

No gain. Clean run `32039125472`.

### New: D3 boundary fibers and D4 closure

Let V be the exact D0..2 row space and define

`J(u0,u1)=(u1,-u0)`

on its two s2 coordinate slices.

The verifier constructs the exact rational basis of V and reduces `V+J(V)` modulo the prime

`p=2147483647`.

It obtains the maximum possible modular rank2048. Since valid reduction modulo p cannot increase rational rank, this full modular rank proves exactly over Q that

`V intersect J(V)={0}`.

The two fixed-D3 j2 transfer spaces each have exact rank2 and union rank4, so they form a direct sum.

Therefore the exact D0..3 space V3 satisfies

`rank(P_s3=0 V3)=8192`,

`rank(P_s3=1 V3)=8192`.

Both one-slice fiber dimensions are zero.

The generic next-site local map is the same rank24/32 coupled-carry map with an8D pair kernel. Because V3 has no one-slice s3 fibers, that kernel again has zero intersection with the actual domain.

Hence

`rank(D0..4)=65536=16*2^12`.

No gain. Clean run `32040273839`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BLOCK1_D4_BOUNDARY_FIBER_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_d4_boundary_fiber_no_gain.py`;
- `.github/workflows/block1-d4-boundary-fiber-no-gain.yml`.

### New: direct block1 x block2 shared-v3_12 overlap

The rank16 block1 and block2 bit0 factor share the retained internal coordinate `v3_12`. The coordinate was merged exactly instead of duplicated.

For fixed D16 the merged spaces have exact ranks

`32,32`,

with union rank48 and intersection dimension16.

This is exactly the old standalone bit0 geometry `2,2,intersection1` scaled by block1 rank16.

Combining it with the certified D16 j1 geometry

`448,448,intersection424`

gives, for every independent D12..15 high prefix,

`448*32 + 448*32 - 424*16 =21888`.

Across the16 independent high prefixes the exact joint rank is

`16*21888=350208`,

which equals the existing product `rank(block1)*rank(block2_ext)`.

Thus the direct shared-v3_12 channel does not make the product bound loose.

Clean run `32040428488`: success. The same checkout first reverified the rank21888 prerequisite.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BLOCK1_BLOCK2_SHARED_V312_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_block2_shared_v312_no_gain.py`;
- `.github/workflows/block1-block2-shared-v312-no-gain.yml`.

## Overflow correction / revoked candidates

Temporary four-site candidate ranks96 and208 and derived W84/W83 claims are revoked. Cause: int32 overflow in an optimized NumPy path. Corrected odd-prime ranks for both relaxed adjacent four-site candidates are256/256. Clean correction run `32032617791`.

Do not revive the revoked ranks without a mathematically independent derivation.

## d>=2 authority

Frozen S3:

`{4,5,11,12,13,19,20,21,27,28,29}`.

Central rank exponent34.52163149454245.

Fully-open:

`rank<=189*2^56`, exponent63.562242424221076. Clean run `32023025384`.

Semi-open:

- A `405*2^46`, exp54.661778097771986;
- B generic `2^55`;
- C `243*2^47`, exp54.92481250360578;
- D `3429*2^42`, exp53.74357218893564.

Current depth law for every d>=2:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

Examples:

- d2 `683.1007639817401...`;
- d3 `1191.5987033755086...`.

## Scoped falsifiers already closed

- semi-open physical `i<->i+16` pair full rank55 A/B/C/D;
- B `[4,5]` interval insufficient;
- B site11->13 carry-only no gain;
- direct fully-open minimal-TT S3 cut86, worse than fused65;
- block1 C12..C14 no gain;
- block1 repeated-D D0..4 no gain through the new boundary-fiber theorem;
- block2 D11 no gain;
- direct block1 x block2 shared-v3_12 overlap equals the product exactly;
- relaxed adjacent four-site W84/W83 candidates revoked after overflow correction;
- historical leaf witness run `32011941759` ended exit143 and is not authority.

## Storage/work status

One-QR RL218 width optimization still has a dense-work proxy about4.016x worse than rank27 source topology. d=1 factor-generation message/storage is85.41785, but output-size alone has the same exponent. No arithmetic-work, ranking, search, or alpha gain is admitted.

## Current sharp blockers

1. **d=1 S1: build a genuine merged multi-site carry bridge.** Simple local appends are closed through C12..C14, repeated-D D0..4, block2 D11, and the only direct shared retained coordinate v3_12. Any new reduction below `171*2^34` must include additional central factors so that a carry/repeated-D coupling exists which is absent from the separate rank16 and rank21888 descriptions. Natural first target: enlarge around the block1 j2 C12..16 side and the extended-block2 high/wrap side while closing every S1 D reuse entering the bridge.
2. **Repeated-D secondary route:** before considering D5, characterize the new D0..4 boundary fibers. Do not materialize D5 blindly.
3. **d=1 work:** message/storage constructivity is exact; arithmetic work is not reduced.
4. **Semi-open B:** remains generic55; any gain must respect rotation7 output wiring plus offset16 D reuse.
5. **Fully-open S3:** may still fall below63.562 only through genuine multi-site row-space overlap.
6. **Coefficient-specific predecessor leaves:** require a clean uniform/parametric theorem or explicitly frozen outer128 mask.

All admitted reductions remain exact, `epsilon=0`. Approximation remains inactive while exact routes are open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.
