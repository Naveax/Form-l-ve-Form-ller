# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 representation:** `W_repr(1)<=78+log2(171)=85.4178525148859...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=85.4178525148859...`.  
**d=1 coefficient-blind static graph+leaf method:** `W_static,blind=95`, method-optimal in that representation.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**ALPHA_PASS=0`.  
**Active work:** the obvious d=1 local/fiber/shared-single-channel extensions are now closed through block1 repeated-D D4 and direct block1×block2 shared `v3_12`; move to a genuine merged multi-site carry bridge. Arithmetic work remains separate.

Code is only a calculator/falsifier. New finite claims require clean-checkout verification.

## Ledger semantics

Keep separate:

1. representation existence;
2. coefficient-blind static stored-factor method;
3. coefficient-aware materialized factor generation;
4. arithmetic work.

Unrestricted scalar streaming/recomputation has no canonical width without a work budget.

## d=1 current exact rank structure

S1=`{0,1,2,3,4,5,12,13,14,15,16}`.

Block1 exact rank16.

Extended block2 physical row bits:

`A12..16,B12..16,D12..16,C0`.

Exact block2 rank:

`21888`.

Certified geometry:

- fixed `D12..16`: j1(12..16) rank448;
- fixed `D12..15`, D16 pair union472, intersection424;
- sixteen j2(28..31) high vectors independent;
- D16 bit0 spaces rank2+2, union3, intersection1;
- per high prefix1368;
- total `16*1368=21888`.

Old block2 rank2784 plus three raw bits would cost22272, giving exact gain58/57.

Clean block2 run `32033308335`: success.

Central S1 rank bound:

`16*21888*2^23 =171*2^34`.

With predecessor-leaf exponent44:

`W_repr(1)<=78+log2(171)=85.4178525148859...`.

Factor-generation constructivity matches this message/storage bound; clean run `32033507588`. One complete materialized factor still contains `171*2^78 = 51,681,578,788,525,397,218,689,024` scalars, so this is not a compute win.

## Exact no-gain closures after rank21888

### Block2 D11

The next repeated external D11 transfer is injective on both j1 and j2 carry interfaces and preserves the old D16 sector geometry. Block2 remains rank21888.

Clean run `32038491628`: success.

Authority:

- `V26_Q138_SIGNED_BLOCK2_D11_TRANSFER_NO_GAIN.md`;
- `scripts/verify_v26_q138_signed_block2_d11_transfer_no_gain.py`.

### Block1 C12..C14

Contiguous j2 carry extension gives

- block1 + C13,C14 rank64=`16*4`;
- block1 + C12,C13,C14 rank128=`16*8`.

No compression. Clean run `32038564342`.

### Block1 repeated-D through D3

The occurrence-closed D0..2 block has rank1024=`16*2^6`.

The D3 local coupled-carry operator has rank24/32 and an explicit8D kernel, but both old s2 projections have full rank1024. Hence the kernel misses the actual incoming row space and

`rank(D0..3)=8192=16*2^9`.

Clean run `32039125472`.

### New: D3 boundary fibers and D4

Let V be the exact D0..2 row space and define the quarter-turn on its s2 slices by

`J(u0,u1)=(u1,-u0)`.

The clean verifier reduces the exact rational basis modulo `p=2147483647` and obtains the maximum possible modular union rank

`rank_p(V+J(V))=2048`.

Because valid reduction modulo an odd prime cannot increase rational rank, this full modular rank proves exactly over Q that

`V intersect J(V)={0}`.

The fixed-D3 j2 transfer spaces each have exact rank2 and union rank4, so the two D3 sectors are a direct sum.

Consequently the exact D0..3 row space V3 has

`rank(P_s3=0 V3)=8192`,

`rank(P_s3=1 V3)=8192`.

Both one-slice fiber dimensions are zero.

Therefore the generic 8D next-site local kernel also misses `F^8 tensor V3`, and the occurrence-closed D4 extension has exact rank

`65536=16*2^12`.

No gain. Clean run `32040273839`: success.

Authority:

- `V26_Q138_BLOCK1_D4_BOUNDARY_FIBER_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_d4_boundary_fiber_no_gain.py`;
- `.github/workflows/block1-d4-boundary-fiber-no-gain.yml`.

### New: direct block1×block2 shared-v3_12 overlap

Block1 and the block2 bit0 factor share the retained coordinate `v3_12`. Identifying that coordinate exactly rather than duplicating it gives fixed-D16 merged spaces

`rank(K'_0)=32`,

`rank(K'_1)=32`,

`rank(K'_0+K'_1)=48`,

so their intersection dimension is16.

This is exactly the old bit0 geometry `2,2,intersection1` scaled by block1 rank16. Combining with the certified j1 D16 geometry `448,448,intersection424` gives per high prefix

`448*32 + 448*32 - 424*16 =21888`.

Across the16 independent D12..15 high sectors, the joint rank is

`16*21888=350208`,

exactly equal to the existing product `rank(block1)*rank(block2)`.

Thus the direct shared-v3_12 overlap gives no compression. Clean run `32040428488`: success; the same checkout first reverified the rank21888 prerequisite.

Authority:

- `V26_Q138_BLOCK1_BLOCK2_SHARED_V312_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_block2_shared_v312_no_gain.py`;
- `.github/workflows/block1-block2-shared-v312-no-gain.yml`.

## Overflow correction, do not regress

Temporary four-site candidates96/208 and resulting bounds84.0279/83.7283 are revoked. Corrected odd-prime ranks for the relaxed adjacent four-site candidates are256/256. Clean correction run `32032617791`.

Never revive the revoked ranks without a mathematically independent derivation.

## d>=2 authority

S3=`{4,5,11,12,13,19,20,21,27,28,29}`.

Central exponent34.52163149454245.

Fully-open `rank<=189*2^56`, exponent63.562242424221076, slope508.4979393937686.

Semi-open:

- A exp54.661778097771986;
- B generic55;
- C exp54.92481250360578;
- D exp53.74357218893564.

Current law:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, d>=2.

## First unfinished mathematical pass

1. **Build a genuine merged block1/block2 multi-site carry bridge.** Single local appends, D0..4 boundary-fiber reuse, D11, C12..C14, and the only direct shared retained coordinate `v3_12` are all exact NO-GAIN. A new d=1 improvement must include additional central factors so that a carry/repeated-D coupling exists which is absent from the separate rank16 and rank21888 descriptions. Natural first target: enlarge around the block1 j2 C12..16 side and the extended-block2 high/wrap side while explicitly closing every S1 D reuse that enters the bridge.
2. **Only as a secondary repeated-D route, characterize the new D0..4 boundary fibers before considering D5.** Do not materialize D5 blindly.
3. **d=1 arithmetic work.** Message/storage is85.41785, but output size alone has the same exponent. No work reduction is admitted.
4. **semi-open B<55.** Respect rotation7 output wiring plus offset16 D reuse; pair/carry-only routes are closed.
5. **fully-open <63.562.** Need genuine multi-site row-space overlap, not direct-sum sector splitting.
6. Recount every complete relevant tree and clean-checkout every finite claim before changing authority.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes are open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
