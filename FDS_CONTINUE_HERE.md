# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**One-double-round representation:** `W_repr(1)<=79+log2(87)=85.44294349584872...`.  
**d>=2 representation law:** `W_repr(d)<=log2(24,663,038,400)+379+log2(98415)+(8d-12)log2(189*2^56)`.  
**Numeric d>=2 law:** `W_repr(d)<=508.4979393937686...d-332.6386869947327...`.  
**Constructive double-round:** `W_2_construct<=95`.  
**Topology-only double-round:** `W_2_topo<=236`.  
**Measured-execution blocker:** missing exact recovered V25 runtime bytes.  
**Active work:** semi-open B/D and multi-site coupling, fully-open multi-site coupling, d=1 constructive/central×leaf structure.

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

`G_m=R_mR_m^T` rank-space data remain rank diagnostics only: Gram family145, prefix140, closure16, `L G_m` span124, row directions47, natural12-control Gram-image TT profile `2,4,8,16,32,64,128,119,196,136,143,124`.

They are **not** single-copy coefficient amplitudes and do not retain the24 right-external mask legs.

## d=1 signed theorem

Critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact central bounds:

- `rank_center(S1)<=87*2^35`;
- `rank_center(S2)<=31*2^35`.

With four generic predecessor-leaf Hilbert exponents44:

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Clean run `32019335785`: success.

Representation existence only; constructive ledger stays95.

## d>=2 central S3 joint rank

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Exact central bounds:

- `rank_AB<=102660`;
- `rank_CDE<=240240`;
- `rank_center(S3)<=24,663,038,400`;
- exponent `34.52163149454245...`.

Clean run `32020902579`: success.

## Fully-open signed slope result

Old fused fully-open S3 cap65.

Exact local ranks:

- site11 `256->168`;
- site19 `128->96`;
- site27 `256->192`.

Remaining42 channels stay binary, giving

`rank_fully_open(S3)<=189*2^56`,

`F_S3<=56+log2(189)=63.562242424221076...`.

Clean run `32023025384`: success.

## Semi-open exact signed A/C theorem

The four predecessor orientations are A/B/C/D, not interchangeable by assumption.

On the57-channel EC S3 boundary, use four disjoint local channel blocks totaling27 raw bits:

- site4: `t4,t3,t2,t1,K0,K1`;
- site11: `t4,t3,t2,t1,K0,K1,z0`;
- site19: `t4,t3,t2,t1,K0,K1,d1`;
- site27: `t4,t3,t2,t1,K0,K1,z1`.

Exact rational local ranks:

- A: `48,60,96,96`;
- C: `48,72,96,96`.

Proof method per block:

1. exact nonzero rows collapse into equality/sign classes; class count equals claimed rank, giving the Q upper bound;
2. rank modulo1000003 equals the same value, witnessing a nonzero integer minor and giving the Q lower bound.

Thus

`rank_A(S3)<=405*2^46`, exponent `54.661778097771986...`,

`rank_C(S3)<=243*2^47`, exponent `54.92481250360578...`.

B and D remain at generic `2^55`.

Combined four-semi product:

`<=98415*2^203`, exponent `219.58659060137776...`.

Gain versus generic220: `0.413409398622235...` bits.

Clean run `32024935318`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_SEMI_OPEN_S3_SIGNED_AC_THEOREM.md`;
- `scripts/verify_v26_q138_semi_open_s3_signed_ac.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_SEMI_OPEN_SIGNED_INTERCEPT_THEOREM.md`;
- `scripts/verify_v26_q138_depth_semi_open_signed_intercept.py`.

## Current d>=2 law

For every `d>=2`,

`W_repr(d)<=log2(24,663,038,400)+379+log2(98415)+(8d-12)log2(189*2^56)`.

Numeric form:

`W_repr(d)<=508.4979393937686...d-332.6386869947327...`.

Verified:

- d2 `684.3571917928045...`;
- d3 `1192.855131186573...`;
- d4 `1701.3530705803416...`;
- d5 `2209.85100997411...`;
- d6 `2718.348949367879...`;
- d7 `3226.8468887616473...`;
- d8 `3735.344828155416...`;
- d9 `4243.842767549185...`.

Slope remains `508.4979393937686...`; the semi-open theorem improves the intercept only.

## Clean falsifiers / cautions

- Semi-open occurrence-closed physical `i<->i+16` pair factors are full row rank for A/B/C/D, total55 each. Clean run `32023730565`: success. This closes only that pair-factor route.
- Direct fully-open minimal-TT refinement on S3 has exact terminal hypergraph cut86 after lexicographic witness correction. Clean run `32023648911`: success. It is worse than fused65 and not a lower bound on true Walsh Schmidt rank.
- Historical coefficient-specific leaf witness run `32011941759` terminated exit143 and is not authority.
- d=1 pure GF(2) critical-boundary codimension remains0,0.

## First unfinished mathematical pass

Continue in this order.

1. Semi-open B/D: generic55 still wins. Search exact fused-channel **multi-site** coupling. Single occurrence-closed physical pairs are full rank, so do not repeat that route.
2. Semi-open A/C: current local rank product may still overcount coupling between site11/19/27 through internal z/carry/K channels. A naive direct-sum sector split can be worse than the blind product; any theorem must contract shared sectors rather than simply sum conditioned ranks.
3. Fully-open S3: seek genuine multi-site contraction rank below `189*2^56`. The obvious z-sector conditioning did not improve the blind product.
4. d=1 S1: easy disjoint local blocks are exhausted. Seek longer cross-cut coupling or central×leaf joint rank.
5. Constructive gap: realize signed d=1 factorizations as an explicit generation/contraction scheme and seek `W_2_construct<95`.
6. Coefficient-specific leaf work requires a clean uniform/parametric theorem or an explicitly frozen outer128 mask. Do not assume zero masks.
7. Reinsert every improvement into every node of the complete relevant tree before changing authority.
8. Keep representation width, constructive peak, storage, arithmetic work and error separate.

## Approximation rule

All admitted reductions remain exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
