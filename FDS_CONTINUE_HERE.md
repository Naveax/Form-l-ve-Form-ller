# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 representation:** `W_repr(1)<=78+log2(171)=85.4178525148859...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=85.4178525148859...`.  
**d=1 coefficient-blind static graph+leaf method:** `W_static,blind=95`, method-optimal in that representation.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**ALPHA_PASS=0`.  
**Active work:** simple one-bit/local d=1 extensions through block1 C12..C14, repeated-D D0..3, and block2 D11 are now closed negatively; move to genuine merged block1/block2 multi-site carry/repeated-D coupling or a new boundary-fiber mechanism. Arithmetic work remains separate.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## Ledger semantics

Keep separate:

1. representation existence;
2. coefficient-blind static stored-factor method;
3. coefficient-aware materialized factor generation;
4. arithmetic work.

Unrestricted scalar streaming/recomputation has no canonical width without a work budget.

## d=1 current exact rank structure

S1:

`{0,1,2,3,4,5,12,13,14,15,16}`.

Block1 remains exact rank16.

Extended block2 now uses physical row bits

`A12..16,B12..16,D12..16,C0`

and has exact rational rank21888.

Proof data:

- fixed `D12..16`: j1(12..16) rank448;
- fixed `D12..15`, union of `D16=0/1` j1 spaces rank472, intersection424;
- sixteen j2(28..31) high-sector vectors are exact independent;
- D16 bit0 spaces rank2+2, union3, intersection1;
- per high prefix rank1368;
- total `16*1368=21888`.

Old block2 rank2784 plus three raw bits would cost22272, so gain is exactly58/57.

Clean run `32033308335`: success.

Central S1 rank:

`16*21888*2^23 =171*2^34`.

With four leaf exponents44:

`W_repr(1)<=171*2^78`, exponent

`78+log2(171)=85.4178525148859...`.

## Factor-generation constructivity

The extended local matrix has `2^16` physical rows and `2^22` retained columns. Full local materialization is only `2^38` scalars; dense local U/V factor tables are below `2^37`. Exact Gaussian can therefore choose a physical row basis without controlling the global ledger.

Reuse the clean21-site complement tree with entry-generation peak80. The materialized global signed factor `171*2^78` dominates. Hence

`W_factor-gen<=85.4178525148859...`.

Clean factor-generation run `32033507588`: success.

Authority:

- `V26_Q138_SIGNED_BLOCK2_EXTEND12_RANK21888_THEOREM.md`;
- `scripts/verify_v26_q138_signed_block2_extend12_rank21888.py`;
- `V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION_EXTEND12_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_factor_generation_extend12.py`.

One complete factor contains

`171*2^78 = 51,681,578,788,525,397,218,689,024`

scalar entries. This is not a compute win.

## Exact no-gain closures after rank21888

### D11 one-bit repeated-variable extension

Take the next repeated external variable `D11`, appearing in j1 bit11 and j2 bit27. Since site11 is outside S1, `D11` remains a column variable.

Exact facts:

- j1 bit11 transfer has rank2 for fixed `D11=0` and rank2 for fixed `D11=1`;
- j2 bit27 transfer also has rank2 in each fixed-D11 slice;
- the sixteen `D12..15` high-sector vectors remain rank16 separately in each D11 slice.

Thus the new transfers are injective on the carry interfaces, preserve the old `448/448/intersection424` D16 geometry, preserve the sixteen-prefix direct sum, and leave block2 rank exactly

`21888`.

No d=1 exponent gain results from this one-bit D11 occurrence closure.

Clean run `32038491628`: success.

Authority:

- `V26_Q138_SIGNED_BLOCK2_D11_TRANSFER_NO_GAIN.md`;
- `scripts/verify_v26_q138_signed_block2_d11_transfer_no_gain.py`.

The same verifier finds isolated C12 physical-row rank2, so C12 cannot help as a one-site append with open neighbouring carries.

### Block1 contiguous C12..C14 carry extension

Extend the clean rank16 block1 through j2 bits14,13,12 using physical row bits `C14,C13,C12`.

Exact ranks:

- block1 + `C13,C14`: `64=16*4`;
- block1 + `C12,C13,C14`: `128=16*8`.

So even the natural contiguous C12 carry extension reaches the full naive rank and gives no compression.

Clean run `32038564342`: success.

Authority:

- `V26_Q138_BLOCK1_C12_C14_EXTENSION_NO_GAIN.md`;
- `scripts/verify_v26_q138_s1_local_extension_falsifiers.py`.

### Block1 repeated-D chain through D3

The clean occurrence-closed D0..2 block has exact rank

`1024=16*2^6`.

For the next site D3, the isolated coupled-carry local operator on `(A3,B3,D3,s2,s18)` has rank24/32 and an explicit 8D kernel. The eight kernel relations are exactly the pairs

`(A3=0,s2=1) == (A3=1,s2=0)`

for fixed `(B3,D3,s18)`.

However the old D0..2 row space has projection rank1024 onto both fixed-s2 column slices. Therefore it contains no nonzero vector supported wholly in either s2 slice, so the local 8D kernel has zero intersection with the actual domain `F^8 tensor V`.

Hence the D3 extension is injective on the actual old row space and the exact new rank is

`8192=16*2^9`.

No gain.

Clean run `32039125472`: success.

Authority:

- `V26_Q138_BLOCK1_D3_EXTENSION_KERNEL_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_d3_extension_kernel_falsifier.py`.

This kernel/fiber mechanism is more informative than another brute-force local rank. Future repeated-D work should inspect boundary-fiber geometry before adding D4/D5.

## Overflow correction, do not regress

Temporary four-site candidates96/208 and resulting bounds84.0279/83.7283 are revoked.

Bug: int32 inputs to optimized NumPy einsum produced int32 contraction output; Gram multiplication overflowed before accumulation. Correct implementation casts inputs to int64 before einsum and asserts dtype. Corrected special and generic four-site odd-prime ranks are both256/256.

Clean correction run `32032617791`: success.

The old theorem files remain only as explicit `REVOKED` records. Never revive those ranks without a new mathematically independent derivation.

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

## Scoped falsifiers already done

- semi-open physical pair route full rank55 A/B/C/D;
- B `[4,5]` interval insufficient;
- B carry-only site11->13 adds no gain;
- naive internal-sector direct sums can be worse than blind products;
- direct fully-open minimal-TT S3 cut86, worse than fused65;
- block1 + C13,C14 carry extension exact rank64=`16*4`;
- block1 + C12,C13,C14 contiguous carry extension exact rank128=`16*8`, clean run `32038564342`;
- block1 + D1/D2 occurrence-closed two-site extension exact union rank1024=`16*2^6`, clean run `32033943549`;
- block1 + D3 occurrence-closed extension exact rank8192=`16*2^9`, despite a local24/32 operator kernel; clean run `32039125472`;
- block2 one-bit D11 repeated-variable extension preserves rank21888, clean run `32038491628`;
- isolated C12 local row map rank2;
- corrected relaxed adjacent four-site S1 blocks are full rank256;
- historical leaf witness run `32011941759` ended exit143 and is not authority.

## First unfinished mathematical pass

1. **Do not blindly append D4. Characterize the new D3 boundary fibers first.** The D3 local operator has a real kernel, but D0..2 misses it. The next question is whether the D0..3 row space develops nonzero fibers on both new j1-carry slices; only then can the same local kernel reduce the D4 extension. Compute exact slice-projection ranks/intersections without materializing the full D0..3 matrix.
2. **In parallel, build the smallest merged block1/block2 multi-site factor.** The easy block1 side, C12 contiguous side, D3 side, and one-bit D11 side are all exact NO-GAIN. A new gain likely needs a coupling absent from those separate maps. Natural target: bridge the j2 carry structure between the block1 `C12..16` segment and the block2 high-sector side while closing every repeated S1 D variable whose second occurrence enters that bridge.
3. **Test joint block1 x block2 channel overlap directly.** The current product `16*21888` is only an upper bound; shared retained columns may make the joint row space smaller even when isolated append maps are injective.
4. **d=1 work accounting.** Message/storage is85.41785 but output-size alone is the same exponent. No work gain yet.
5. **semi-open B<55.** Respect rotation7 output and offset16 D reuse; pair/carry routes are closed.
6. **fully-open <63.562.** Need genuine multi-site row-space overlap, not direct-sum sector splitting.
7. Recount every complete relevant tree and clean-checkout every finite claim before changing authority.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes are open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
