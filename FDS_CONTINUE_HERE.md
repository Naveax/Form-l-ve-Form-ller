# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**One-double-round representation:** `W_repr(1)<=79+log2(87)=85.44294349584872...`.  
**d>=2 representation law:** `W_repr(d)<=520d-384+log2(24,663,038,400)`.  
**Constructive double-round ledger:** `W_2_construct<=95`.  
**Topology-only double-round:** `W_2_topo<=236`.  
**Measured-execution blocker:** missing exact recovered V25 runtime bytes.  
**Active work:** global/cross-cut signed rank, constructive realization, and slope reduction.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## One-QR facts to preserve

- corrected exact I9 support `117..218`;
- support-indicator rank64 across 64 left masks;
- old support216/rank12 selector line revoked;
- global one-QR peak `218*2^31`;
- left interface rank48;
- six-left-mask coefficient-family span64, TT profile `2,4,8,16,32,64`;
- physical right rank `11..38`;
- parent rank `5..27`;
- right doubled hull162;
- RL218 width-tree dense-work proxy about `4.0160678967x` worse than rank27 source topology;
- `ALPHA_PASS=0`.

## Gram-image warning

`G_m=R_mR_m^T` rank-space results remain useful for rank diagnostics:

- Gram family145;
- prefix140;
- closure16;
- `L G_m` span124;
- row directions47;
- 12-control Gram-image TT profile `2,4,8,16,32,64,128,119,196,136,143,124`.

They are **not** single-copy coefficient amplitudes. Do not propagate 124/U47 through another QR as if it retained the 24 right-external coefficient legs.

## Specialized d=1 signed theorem

Frozen critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact central ranks:

- `rank_center(S1)<=87*2^35` from disjoint ranks16 and2784 plus26 raw row bits;
- `rank_center(S2)<=31*2^35` from exact top D-sector ranks.

With four generic diagonal leaf exponents44:

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Clean run `32019335785`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`;
- `.github/workflows/double-round-signed85.yml`.

Representation existence only. Constructive ledger remains95.

## d>=2 joint-sector theorem

Frozen common-tree maximizer up to complement:

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

All44 S3 physical central row bits are covered by exact signed blocks.

### AB group, first24 row bits

- block A rank434 on `A/B/D27..29 + C11..13`;
- block B rank1792 on disjoint `A/B/D11..13 + C27..29`.

They share crossed `v3_7..9` and `v3_23..25` sectors. Exact projection rank pairs:

- `(16,120)` x36;
- `(16,75)` x12;
- `(11,120)` x12;
- `(11,75)` x4.

Joint sector sum:

`rank_AB<=102660`.

### CDE group, remaining20 row bits

- two symmetric occurrence-closed pair blocks rank192 each;
- site19/site3 cross-cut row block rank12;
- shared sectors: `v3_0..1`, `v3_16..17`, `sigma1_19`, `sigma2_19`.

Exact six-bit sector recount gives

`rank_CDE<=240240`.

Therefore

`rank_center(S3)<=102660*240240=24,663,038,400`,

with exponent

`34.52163149454245...`.

This improves the generic central exponent44 by `9.47836850545755...` bits.

Recounting every common-tree node gives for all `d>=2`

`W_repr(d)<=520d-384+log2(24,663,038,400)`.

Equivalent intercept form:

`W_repr(d)<=520d-349.47836850545755...`.

Verified values:

- d2 `690.5216314945425...`;
- d3 `1210.5216314945425...`;
- d4 `1730.5216314945425...`;
- d5 `2250.5216314945425...`;
- d6 `2770.5216314945425...`;
- d7 `3290.5216314945425...`;
- d8 `3810.5216314945425...`;
- d9 `4330.5216314945425...`.

Clean run `32020902579`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_JOINT_SECTOR_LAW.md`;
- `scripts/verify_v26_q138_depth_joint_sector_law.py`;
- `.github/workflows/depth-joint-sector-law.yml`.

The fully-open QR cap65 is unchanged, so slope520 remains.

## Falsifiers / cautions

- old graph cardinality boundaries k11..16 `51,52,55,54,55,56`;
- old d=1 refined terminal cuts `44,44,44`, exactly binary cut indices;
- pure GF(2) critical-boundary codim `0,0`;
- generic leaf terminal-cut exponent11.

Historical leaf full-rank witness run `32011941759` ended with exit143 during the heavy witness search. It is not clean authority. Do not claim source-specific/full-rank leaf lower bounds from it.

## First unfinished mathematical pass

Continue in this order.

1. d=1 S1: the easy occurrence-closed disjoint local blocks are largely exhausted. Search cross-cut/global sector coupling before attempting larger brute-force local blocks.
2. Test whether the S1 rank16 and rank2784 factors have nontrivial joint coupling through longer carry/gap transfer sectors. The direct common-`v3_12` projection was full product, so any further gain must use more global structure.
3. Constructive gap: turn d=1 signed rank factors into an explicit factor-generation/contraction scheme and seek `W_2_construct<95`. Do not identify representation existence with construction.
4. Joint central×leaf factorization: four generic leaf Hilbert ranks may overcount sectors shared with the central signed factors.
5. d>=2 slope: attack the coefficient-independent fully-open QR cap65. Intercept work alone cannot change slope520.
6. For S3, any further central improvement must exploit coupling **between** the AB and CDE joint groups through gap transfer/carry structure; their local physical row bits are already fully covered.
7. Coefficient-specific leaf work requires clean completed uniform/parametric computation or an explicitly frozen outer128 mask. Do not assume zero masks.
8. Every new rank/cap must be reinserted into all nodes of the relevant complete tree before changing authority.
9. Keep representation width, constructive peak, storage, arithmetic work and error separate.

## Approximation rule

All admitted reductions remain exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
