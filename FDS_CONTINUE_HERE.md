# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 representation:** `W_repr(1)<=78+log2(171)=85.4178525148859...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=85.4178525148859...`.  
**d=1 coefficient-blind static graph+leaf method:** `W_static,blind=95`, method-optimal in that representation.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**ALPHA_PASS=0`.  
**Active work:** extend the new D-sector-overlap mechanism in d=1, then semi-open B and fully-open multi-site coupling; arithmetic work remains separate.

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
- block1 + A1,B1,D1 occurrence-closed one-step extension exact rank128=`16*8` locally; add a clean regression before treating this as frozen authority;
- corrected relaxed adjacent four-site S1 blocks are full rank256;
- historical leaf witness run `32011941759` ended exit143 and is not authority.

## First unfinished mathematical pass

1. **Generalize the new D-sector overlap.** The 58/57 gain came from `D16=0/1` j1 subspace intersection424 together with a1D bit0 intersection. Search the same mechanism one bit farther or in the block1 side, using exact subspace intersections rather than dense integer Grams.
2. **Try block2 + another occurrence-closed raw bit group.** Remaining S1 raw bits are all A/B/C/D on sites1..5 plus C12,C13,C14. Site12 A/B/D are now consumed; C12 remains.
3. **d=1 work accounting.** Message/storage is85.41785 but output-size alone is the same exponent. No work gain yet.
4. **semi-open B<55.** Respect rotation7 output and offset16 D reuse; pair/carry routes are closed.
5. **fully-open <63.562.** Need genuine multi-site row-space overlap, not direct-sum sector splitting.
6. Recount every complete relevant tree and clean-checkout every finite claim before changing authority.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes are open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
