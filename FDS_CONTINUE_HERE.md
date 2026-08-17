# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**One-double-round representation:** `W_repr(1)<=79+log2(87)=85.44294349584872...`.  
**d>=2 representation law:** `W_repr(d)<=log2(24,663,038,400)+396+(8d-12)log2(189*2^56)`.  
**Numeric d>=2 law:** `W_repr(d)<=508.4979393937686...d-332.22527759611046...`.  
**Constructive double-round:** `W_2_construct<=95`.  
**Topology-only double-round:** `W_2_topo<=236`.  
**Measured-execution blocker:** missing exact recovered V25 runtime bytes.  
**Active work:** signed multi-site fully-open/semi-open rank, constructive realization, and central×leaf coupling.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## One-QR facts

- corrected exact I9 support `117..218`;
- support indicator rank64 across64 left masks;
- old support216/rank12 selector revoked;
- global one-QR peak `218*2^31`;
- left interface rank48;
- six-left-mask coefficient-family span64, TT profile `2,4,8,16,32,64`;
- physical right rank11..38;
- parent rank5..27;
- right doubled hull162;
- RL218 width-tree dense-work proxy about `4.0160678967x` worse than rank27 source topology;
- `ALPHA_PASS=0`.

## Gram-image warning

`G_m=R_mR_m^T` rank-space data remain rank diagnostics only:

- Gram family145;
- prefix140;
- closure16;
- `L G_m` span124;
- row directions47;
- 12-control Gram-image TT profile `2,4,8,16,32,64,128,119,196,136,143,124`.

They are **not** single-copy coefficient amplitudes and do not retain the 24 right-external mask legs.

## d=1 signed theorem

Critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact central bounds:

- `rank_center(S1)<=87*2^35` from ranks16 and2784 plus26 raw row bits;
- `rank_center(S2)<=31*2^35`.

With four generic leaf Hilbert exponents44:

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Clean run `32019335785`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`.

Representation existence only. Constructive ledger stays95.

## d>=2 central S3 joint rank

Common-tree maximizer:

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Exact central joint-sector bounds:

- `rank_AB<=102660`;
- `rank_CDE<=240240`;
- `rank_center(S3)<=24,663,038,400`;
- exponent `34.52163149454245...`.

Clean run `32020902579`: success.

## Fully-open signed slope result

Old fused fully-open S3 cap:65 binary channels.

Exact local fused-channel ranks on disjoint S3 crossing groups:

- site11: `256 ->168`;
- site19: `128 ->96`;
- site27: `256 ->192`.

The remaining42 crossing channels stay binary, so

`rank_fully_open(S3)<=168*96*192*2^42=189*2^56`.

Hence

`F_S3<=56+log2(189)=63.562242424221076...`.

Only S3/complement had old fully-open65; next generic common-tree fully-open cap62.

Each local rational rank is certified by

- a nonsingular odd-prime minor;
- a complete independent exact integer left-null system;
- null coefficients only `{-1,0,1}`.

Clean run `32023025384`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FULLY_OPEN_S3_LOCAL_RANK_CERTIFICATE.json`;
- `scripts/verify_v26_q138_fully_open_s3_local_signed_rank.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_FULLY_OPEN_SIGNED_SLOPE_THEOREM.md`;
- `scripts/verify_v26_q138_depth_fully_open_signed_slope.py`.

## Current d>=2 law

For every `d>=2`,

`W_repr(d)<=log2(24,663,038,400)+396+(8d-12)log2(189*2^56)`.

Equivalent numeric form:

`W_repr(d)<=508.4979393937686...d-332.22527759611046...`.

Verified:

- d2 `684.7706011914267...`;
- d3 `1193.2685405851953...`;
- d4 `1701.7664799789638...`;
- d5 `2210.2644193727324...`;
- d6 `2718.762358766501...`;
- d7 `3227.2602981602695...`;
- d8 `3735.7582375540383...`;
- d9 `4244.256176947807...`.

Slope improvement from520:

`11.5020606062314...` bits per added inverse double round.

This remains exact representation/message width, not construction/work.

## Semi-open orientation semantics

The four central input words `(0,4,8,12)` come from four diagonal predecessor QRs:

- `(0,5,10,15)` -> local output A;
- `(3,4,9,14)` -> local output B;
- `(2,7,8,13)` -> local output C;
- `(1,6,11,12)` -> local output D.

Therefore any semi-open signed theorem must cover all four one-output/open-four-input orientations. Do not analyze one convenient output word and generalize silently.

An occurrence-closed `i<->i+16` physical-pair full-rank falsifier is being clean-revalidated. Until that run succeeds, do not freeze it as authority.

## Scoped cautions

- direct fully-open minimal-TT refinement is also being revalidated after a witness-selection bug in its first clean workflow; do not cite cut86 as clean authority yet;
- d=1 pure GF(2) critical-boundary codimension remains0,0;
- historical coefficient-specific leaf witness run `32011941759` terminated exit143 and is not clean authority.

## First unfinished mathematical pass

Continue in this order.

1. Semi-open QR: finish clean validation of the four-orientation occurrence-closed pair test. If full rank55 holds, the easy local-pair route is closed and any semi-open improvement must be multi-pair/global.
2. Fully-open S3: local single-site ranks11/19/27 already reduce65 to63.562. The obvious z19/z27 sector conditioning did not reduce their blind product. Search larger multi-site coupling involving carries/K/z channels.
3. d=1 S1: easy disjoint occurrence-closed blocks are largely exhausted. Seek longer cross-cut sector coupling or central×leaf joint rank.
4. Constructive gap: realize the signed d=1 rank factors as an explicit generation/contraction tree and seek `W_2_construct<95`.
5. d>=2 central: AB/CDE blocks already cover all44 physical S3 row bits; further gain must exploit coupling between those joint groups or a different global factorization.
6. Leaf coefficient-specific work requires clean uniform/parametric computation or an explicitly frozen outer128 mask. Do not assume zero masks.
7. Reinsert every new rank/cap into every node of the complete relevant tree before changing authority.
8. Keep representation width, constructive peak, storage, arithmetic work and error separate.

## Approximation rule

All admitted reductions are exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
