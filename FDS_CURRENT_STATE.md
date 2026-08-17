# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured execution remains frozen behind missing exact recovered V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is only a calculator/falsifier and every admitted finite claim requires clean-checkout verification.

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

The last two are message/storage constructivity bounds, not arithmetic-work bounds. Unrestricted scalar streaming/recomputation is not assigned a canonical width without a work budget.

### Static coefficient-blind95 is method-optimal

Clean MILP cardinality minima for central graph smaller-side sizes11..16 are `51,52,55,54,55,56`. Adding four generic leaf costs gives `95,100,107,110,115,120`. Balanced-edge lemma forces some11..16 edge in every32-leaf binary tree; existing tree attains95. Clean run `32028136767`: success.

### Clean signed blocks before the new extension

Block1 rank16 is explicit on a32x64 matrix.

Historical block2 rank2784 is explicit:3584 natural product channels span2784 exact rational directions. The coordinate transform has max41 nonzeros/column, mean2.5398995535714284, denominator set `{1,2,3,4,6,8,9,12,16,24,32,48,64,96,128,256,512}`. All8192 physical block2 rows span all2784 directions; a normalized basis direction uses at most64 physical rows.

Clean factor-generation85 run `32030620625`: success.

### New exact block2 site12 extension

Extend block2 by the three previously raw physical S1 bits `A12,B12,D12`. This closes both occurrences of `D12`: j1 bit12 and j2 bit28. The exact physical block is

`A12..16, B12..16, D12..16, C0`.

Exact Fraction subspace structure:

- for every fixed `D12..16`, j1(12..16) rank448;
- for every fixed `D12..15`, the `D16=0/1` j1 union rank472, hence intersection424;
- the sixteen j2(28..31) high vectors indexed by `D12..15` are exact linearly independent;
- the two `D16` bit0 spaces each have rank2, union rank3, intersection1.

Thus for each high prefix the two `D16` tensor-product spaces have union dimension

`448*2 + 448*2 - 424*1 =1368`,

and across the16 independent prefixes

`rank(extended block2)=16*1368=21888`.

Naively keeping old block2 rank2784 plus the three raw bits costs22272. Exact gain:

`22272/21888 =58/57`.

Clean run `32033308335`: success.

Authority:

- `V26_Q138_SIGNED_BLOCK2_EXTEND12_RANK21888_THEOREM.md`;
- `scripts/verify_v26_q138_signed_block2_extend12_rank21888.py`;
- `.github/workflows/signed-block2-extend12-rank21888.yml`.

### New d=1 representation and factor-generation bound

Keep disjoint rank16 block1. Extended block2 consumes16 S1 physical row bits, leaving23 raw. Therefore

`rank_center(S1) <=16*21888*2^23 =171*2^34`.

Four predecessor leaves contribute44 S1 mask bits, so

`dim_factor <=171*2^78`,

and

`W_repr(1)<=W_2_factor-gen<=78+log2(171)=85.4178525148859...`.

For factor generation, the extended local matrix has only `2^16` physical rows and `2^22` retained columns. Even brute-force exact local materialization is `2^38` scalars; dense local U/V factors are below `2^37`. A physical row basis can therefore be selected exactly without controlling the global ledger. The clean21-site complement entry-generation tree remains peak80, below85.418. Clean factor-generation extension run `32033507588`: success.

Authority:

- `V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION_EXTEND12_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_factor_generation_extend12.py`;
- `.github/workflows/double-round-factor-generation-extend12.yml`.

Materializing one complete signed factor still requires `171*2^78 = 51,681,578,788,525,397,218,689,024` scalar entries. Arithmetic work remains unsolved.

### Overflow correction / revoked candidates

The temporary four-site candidate ranks96 and208, and the derived `W=84.0279` / `W=83.7283` claims, are **revoked**.

Cause: optimized NumPy `einsum` with int32 inputs returned int32 despite a requested int64 dtype on the draft path; the subsequent Gram multiplication overflowed. Correct code casts inputs to int64 before einsum and asserts the contraction dtype. Corrected odd-prime ranks are

- special `{2,3,18,19}`:256/256;
- generic `{4,5,20,21}`:256/256.

Clean correction workflow `32032617791`: success. The corresponding theorem files remain in the repo only as explicit `REVOKED` correction records. Canonical authority never moved to84/83.

## d>=2 authority

Frozen S3:

`{4,5,11,12,13,19,20,21,27,28,29}`.

Central joint-sector rank:

`rank_center(S3)<=24,663,038,400`, exponent34.52163149454245. Clean run `32020902579`.

Fully-open:

`rank<=189*2^56`, exponent63.562242424221076, from exact local ranks168,96,192 and42 raw binary channels. Clean run `32023025384`. Current slope `508.4979393937686...`.

Semi-open:

- A `405*2^46`, exp54.661778097771986;
- B generic `2^55`;
- C `243*2^47`, exp54.92481250360578;
- D `3429*2^42`, exp53.74357218893564.

D uses exact `[4,5]` interval rank1016. Clean A/C run `32024935318`; A/C/D depth run `32026645042`.

Current depth law for every `d>=2`:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

Examples: d2 `683.1007639817401...`, d3 `1191.5987033755086...`.

## Clean/scoped falsifiers

- semi-open physical `i<->i+16` pair factors full row rank55 for A/B/C/D;
- direct fully-open minimal-TT S3 cut86, worse than fused65;
- B `[4,5]` interval minor rank1763, insufficient for current sub55 route;
- B site11->13 carry-only segment gives no gain beyond isolated site11;
- naive internal-sector direct sums for B/fully-open can be worse than blind products;
- block1 + `C13,C14` carry extension rank64=`16*4`, no compression;
- block1 + occurrence-closed `A1,B1,D1` extension rank128=`16*8`, no compression (current exact local result; clean regression should be added before using it as a hard project checkpoint);
- corrected relaxed adjacent four-site S1 blocks are full rank256; the old96/208 numbers were overflow artifacts;
- historical coefficient-specific leaf witness run `32011941759` ended exit143 and is not authority.

## Storage/work status

One-QR RL218 width optimization still has a dense-work proxy about4.016x worse than rank27 source topology. d=1 factor-generation message/storage is now85.41785, but output-size alone already requires more than5.16e25 scalar entries for one materialized factor. No arithmetic-work gain, ranking gain or alpha gain is admitted.

## Current sharp blockers

1. d=1 S1: lower `171*2^34` further. The new gain came from **cross-sector overlap across D16** inside an occurrence-closed extension. Search analogous overlap mechanisms, not overflow-prone dense Grams.
2. d=1 work: factor-generation memory is constructive, arithmetic work is not.
3. Semi-open B remains generic55; any gain must respect rotation7 output wiring plus offset16 D reuse.
4. Fully-open S3 may still fall below63.562 through genuine multi-site row-space overlap.
5. Coefficient-specific predecessor-leaf compression requires a clean uniform/parametric theorem or explicitly frozen outer128 mask.

All admitted reductions remain exact, `epsilon=0`. Approximation stays inactive while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.
