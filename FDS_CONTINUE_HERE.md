# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**One-double-round representation:** `W_repr(1)<=79+log2(87)=85.44294349584872...`.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**Constructive double-round:** `W_2_construct<=95`.  
**Topology-only double-round:** `W_2_topo<=236`.  
**ALPHA_PASS=0`.  
**Active work:** semi-open B rotation-7 multi-site rank, fully-open multi-site coupling, then d=1 constructive/central×leaf coupling.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## Facts to preserve

One-QR:

- exact I9 support117..218;
- support-indicator rank64;
- global peak `218*2^31`;
- left interface rank48;
- right rank11..38;
- parent rank5..27;
- right doubled hull162;
- all64 left maps share a 48-dimensional row space;
- old support216/rank12-selector line revoked.

Gram-image objects (`G_m=R_mR_m^T`, span124/U47 diagnostics) are not single-copy coefficient amplitudes and must not be propagated through later QRs as amplitude data.

## d=1 representation

Critical central bounds:

- S1 `rank<=87*2^35`;
- S2 `rank<=31*2^35`.

With four generic leaf exponents44:

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Constructive ledger remains95.

## d>=2 common-tree data

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Central:

`rank_center(S3)<=24,663,038,400`, exponent `34.52163149454245...`.

Fully-open:

`rank_fully_open(S3)<=189*2^56`, exponent `63.562242424221076...`.

This gives the current slope

`8*log2(189*2^56)=508.4979393937686...`.

## Semi-open exact orientation bounds

- A: `405*2^46`, exponent `54.661778097771986...`;
- B: generic `2^55` remains;
- C: `243*2^47`, exponent `54.92481250360578...`;
- D: `3429*2^42`, exponent `53.74357218893564...`.

D proof: complete `[4,5]` interval has exact rational rank1016 on twelve fused crossing channels; exact Gram has1520 zero rows,1760 signed representatives, rank1016 modulo1000003, and744 additional modular dependencies all lift to exact integer relations. Sites11/19/27 each contribute exact rank96. Clean run `32026645042`: success.

Four-semi product:

`<=337,465,035*2^190`, exponent `218.3301627903134...`.

Current law:

`W_repr(d) <= log2(24,663,038,400)+log2(337,465,035*2^190)+(8d-12)log2(189*2^56)+176`.

Numeric:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

## Clean/scoped falsifiers

- semi-open occurrence-closed physical `i<->i+16` pair factors are full rank55 for A/B/C/D; clean run `32023730565`;
- direct fully-open minimal-TT S3 cut is exact86, worse than fused65; clean run `32023648911`;
- B complete `[4,5]` interval cannot by itself close sub55 through the current decomposition: a 1800x1800 odd-prime minor has rank1763, above the `<1490` threshold needed alongside the current site11 rank88 factor;
- B site11->13 carry-only segment gives rank1408 on 11 bits, exactly the same `log2(128/88)` gain as the isolated site11 factor, so carry propagation alone adds no compression;
- naive direct-sum conditioning on internal `z19,z27,Din11,Din27` sectors is worse than the blind product and is not a theorem route;
- historical coefficient-specific leaf witness run `32011941759` ended exit143 and is not authority.

## First unfinished mathematical pass

1. Semi-open B. Respect the fact that local site `i` carries physical `Bout[i+7]`; B-output row sites are `S3-7={4,5,6,12,13,14,20,21,22,29,30}`. Build an occurrence-closed multi-site physical/fused block that simultaneously respects rotation7 and offset16 D-copy reuse. Do not repeat the pair or carry-only routes already falsified.
2. Search B small multi-site blocks by exact Gram rank; a valid improvement must reduce the 55-bit physical cap, not merely the 57-channel graph envelope by less than2 bits.
3. After any B improvement, recount every complete common-tree node before changing the d>=2 authority.
4. Then attack fully-open S3 below `189*2^56` using genuine multi-site coupling.
5. In parallel, keep d=1 constructive gap separate: representation85.443 versus constructive95.
6. Keep representation width, constructive peak, storage, arithmetic work and error as separate ledgers.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact signed/sector/joint routes are open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round cryptanalytic relevance.
