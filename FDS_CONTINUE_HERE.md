# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 representation:** `W_repr(1)<=79+log2(87)=85.44294349584872...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=85.44294349584872...`.  
**d=1 coefficient-blind static graph+leaf method:** `W_static,blind=95`, method-optimal in that representation.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**ALPHA_PASS=0`.  
**Active work:** lower d=1 S1 rank/work, semi-open B rotation7 multi-site rank, fully-open multi-site coupling.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## Ledger semantics

Do not collapse these quantities:

1. `W_repr`: representation existence.
2. `W_static,blind`: static coefficient-blind stored-factor contraction model.
3. `W_factor-gen`: coefficient-aware materialized factor generation, allowing repeated exact slice contractions but materializing the signed factor table.
4. arithmetic work: separate and currently unresolved.

Unrestricted scalar streaming/recomputation is not assigned a canonical memory width without a work budget; otherwise the metric becomes degenerate.

## d=1 current exact structure

Critical S1:

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

Central rank:

`R1<=16*2784*2^26=87*2^35`.

Four predecessor leaves give generic exponent44, hence

`W_repr(1)<=87*2^79`, exponent85.44294349584872.

S2 remains below it with central rank `31*2^35`.

## Static95 is method-optimal

Exact central graph minima for smaller-side cardinality11..16 are

`51,52,55,54,55,56`.

Adding four generic leaf Hilbert costs gives

`95,100,107,110,115,120`.

Balanced-edge lemma forces some11..16 edge in every32-leaf binary tree; existing static tree attains95. Clean run `32028136767`: success.

This closes tree reordering **inside the coefficient-blind graph+leaf model only**.

## Signed factors are explicit

Block1:

- exact rank16 on32x64 matrix;
-8 zero rows,16 normalized nonzero row classes;
- explicit trivial-sparse U/V factor.

Block2:

-3584 natural product channels;
- exact span2784 in `2^18` columns;
- exact rational coordinate map, max41 nonzeros, mean2.5398995535714284;
- denominator set `{1,2,3,4,6,8,9,12,16,24,32,48,64,96,128,256,512}`;
- max abs numerator37.

Physical-row bridge:

-8192 physical rows span all2784 compressed directions;
- each normalized basis direction is an exact combination of at most64 physical rows, mean3.654094827586207;
- physical-row coordinate max184, mean11.8597412109375.

Clean constructive94 dependency run `32030121710`: success.

## Factor-generation85 theorem

Use signed rank `R=87*2^35` and materialize a factor indexed by44 leaf-left bits and r:

`R*2^44=87*2^79` entries.

Generate the right factor entrywise using physical-row basis slices. For the21-site complement use

`[[[10,11],[17,[18,19]]],[[[[30,31],[28,29]],[[8,9],[6,7]]],[[[26,27],[24,25]],[[22,23],[20,21]]]]]`.

For complement cluster T:

`C(T)=gb(T)+4*min(|T|,21-|T|)`.

Peak is80, at exactly two clusters:

- `{20,21,22,23,24,25,26,27}`:48+32;
- `{6,7,8,9,20,21,22,23,24,25,26,27,28,29,30,31}`:60+20.

Since80 <85.443, the materialized signed factor table dominates. Therefore

`W_factor-gen<=79+log2(87)=85.44294349584872...`.

Clean run `32030620625`: success.

Authority:

- `V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_factor_generation85.py`;
- `.github/workflows/double-round-factor-generation85.yml`.

This does **not** reduce arithmetic work. One complete factor already contains

`87*2^79 = 52,588,273,153,236,369,099,718,656`

scalar entries.

## d>=2 authority

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Central:

`rank_center(S3)<=24,663,038,400`, exponent34.52163149454245.

Fully-open:

`rank<=189*2^56`, exponent63.562242424221076.

Semi-open:

- A `405*2^46`, exp54.661778097771986;
- B generic `2^55`;
- C `243*2^47`, exp54.92481250360578;
- D `3429*2^42`, exp53.74357218893564.

Current depth law:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, `d>=2`.

## Scoped falsifiers already done

- semi-open physical `i<->i+16` pair route full rank55 A/B/C/D;
- B `[4,5]` interval minor rank1763, insufficient for current sub55 route;
- B site11->13 carry segment adds no compression beyond isolated site11;
- naive internal-sector direct sums for B/fully-open are worse than blind products;
- direct fully-open minimal-TT S3 cut86, worse than fused65;
- d=1 block1 + physical `C13,C14` carry extension has exact rank64=`16*4`, no gain;
- historical leaf full-rank witness run `32011941759` ended exit143 and is not authority.

## First unfinished mathematical pass

1. **d=1 S1 rank below `87*2^35`.** Remaining raw row bits are all A/B/C/D on sites1..5 and12 plus C13,C14. The C13/C14 carry extension is full. Search only occurrence-valid cross-cut/global couplings, especially those linking remaining sites1..5/12 to block1 or block2 retained interfaces.
2. **d=1 arithmetic work.** Factor-generation memory is now constructive at85.443, but output-size alone is already exponent85.443. Derive rigorous work accounting for factor generation; do not claim compute gain from memory gain.
3. **semi-open B<55.** Respect rotation7 B-output sites `S3-7={4,5,6,12,13,14,20,21,22,29,30}` and offset16 D reuse. Pair/carry-only routes are closed.
4. **fully-open <63.562.** Need genuine multi-site row-space overlap, not direct-sum sector splitting.
5. **leaf-specific structure.** Any coefficient-specific leaf theorem must be clean uniform/parametric or use an explicitly frozen outer128 mask.
6. After every new rank/cap, recount every node of the relevant complete tree before changing authority.

All admitted reductions remain exact, `epsilon=0`. Approximation stays inactive while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
