# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured execution remains frozen behind missing exact recovered V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is only a calculator/falsifier and every admitted finite claim requires clean-checkout verification.

## One-QR exact authority

For all4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925... <39`.

Current sharp peak:

`D_max=218*2^31=468,151,435,264`.

Old support216 / 13 support classes / rank12 selector is revoked. Exact I9 support over64 left masks is117..218, with64 distinct supports, union392, intersection42, support-indicator rank64 and `epsilon=0`. Six-left-mask coefficient-family span64 with TT profile `[2,4,8,16,32,64]`. Physical right rank11..38, parent rank5..27, right doubled hull162=114+48, and all64 left maps share one exact48-dimensional interface row space.

Gram-image objects such as `G_m=R_mR_m^T`, the span124 family and U47 row-direction diagnostics are rank-space objects, not single-copy coefficient amplitudes. Never propagate them through a later QR as amplitude data.

## Double-round ledgers: keep semantics separate

Current d=1 numbers refer to different models and must not be collapsed into one word "constructive":

- topology-only: `W_2_topo<=236`;
- coefficient-blind static reduced-central-graph + four-generic-leaf method: `W_2_static,blind=95`, method-optimal inside that representation;
- coefficient-aware materialized-factor generation: `W_2_factor-gen<=79+log2(87)=85.44294349584872...`;
- exact representation existence: `W_repr(1)<=79+log2(87)=85.44294349584872...`.

The equality of the last two upper bounds is a constructivity result for the signed factor representation, **not** an arithmetic-work result. Unrestricted scalar-by-scalar recomputation is not assigned a canonical width without a work budget because it would make a pure-memory metric degenerate.

### d=1 signed representation

Critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact central bounds:

- `rank_center(S1)<=87*2^35`;
- `rank_center(S2)<=31*2^35`.

Four generic predecessor-leaf Hilbert factors contribute exponent44, hence

`W_repr(1)<=87*2^79`, exponent `85.44294349584872...`.

Clean signed85 run `32019335785`: success.

### Static coefficient-blind method is stuck at95

Clean cardinality MILP gives exact reduced-central-graph minima for smaller-side cardinalities11..16:

`51,52,55,54,55,56`.

Adding four generic leaf Hilbert exponents gives costs

`95,100,107,110,115,120`.

The balanced-edge lemma forces every32-leaf binary contraction tree to contain an edge with smaller side11..16. The old constructive95 tree attains95. Therefore tree reordering alone cannot beat95 inside this coefficient-blind graph+leaf method.

Authority:

- `V26_Q138_CONSTRUCTIVE_GRAPH_LEAF95_METHOD_OPTIMAL_THEOREM.md`;
- `scripts/verify_v26_q138_constructive_graph_leaf95_optimal.py`;
- clean run `32028136767`: success.

This is not a lower bound on the true Walsh tensor rank or on coefficient-aware constructions.

### Explicit signed factors

S1 block1:

- matrix32x64, exact rank16;
- 8 zero physical rows,24 nonzero rows,16 normalized independent row classes;
- explicit U coordinate has0/1 active channel per physical row;
- explicit V has16 normalized rows.

S1 block2:

- 3584 natural product channels in a `2^18` retained-column space;
- exact rank2784;
- all3584 channels reconstruct exactly from an explicit rational2784 basis;
- coordinate nonzeros max41, mean2.5398995535714284;
- denominator set `{1,2,3,4,6,8,9,12,16,24,32,48,64,96,128,256,512}`;
- max absolute numerator37, max denominator512.

An earlier draft called the coefficients dyadic. Clean verification correctly rejected that adjective; the exact factor itself was unchanged.

Physical-row bridge:

- all8192 actual block2 physical rows span the full2784-dimensional compressed space;
- 2784 basis directions can therefore be generated from physical rows;
- a normalized basis direction uses at most64 physical rows, mean3.654094827586207;
- every physical row has at most184 nonzero coordinates in that basis, mean11.8597412109375.

The signed-left bridge has dense S1 factor size `87*2^79`, and S2 factor size `31*2^79`, both below the former95 peak. Clean left-bridge run `32028501148`: success.

The full coefficient-aware constructive94 dependency run `32030121710` is success and revalidated block1, corrected block2, the physical-row bridge and its94 complement contraction certificate.

### Sharper factor-generation tree

For the21-site complement of S1, use the explicit tree

`[[[10,11],[17,[18,19]]],[[[[30,31],[28,29]],[[8,9],[6,7]]],[[[26,27],[24,25]],[[22,23],[20,21]]]]]`.

For complement cluster T, one fixed physical S1 slice plus four restricted21-bit predecessor leaves has safe exponent

`gb(T)+4*min(|T|,21-|T|)`.

The complete tree has peak80. Its two peak clusters are

- `{20,21,22,23,24,25,26,27}`: central boundary48 + leaf contribution32;
- `{6,7,8,9,20,21,22,23,24,25,26,27,28,29,30,31}`: central boundary60 + leaf contribution20.

The signed factor table itself has

`R*2^44 =87*2^79`

entries and therefore dominates the80-bit entry-generation contraction. Materializing a left or right signed factor gives

`W_2_factor-gen<=79+log2(87)=85.44294349584872...`.

Clean run `32030620625`: success. It revalidated both explicit local factors, the physical-row bridge and the complete factor-generation85 ledger from clean checkout.

Authority:

- `V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_factor_generation85.py`;
- `.github/workflows/double-round-factor-generation85.yml`.

This construction can require astronomical repeated computation. Merely materializing one complete signed factor requires `87*2^79 = 52,588,273,153,236,369,099,718,656` scalar entries, so arithmetic work is emphatically not solved.

## d>=2 common-tree central signed rank

Frozen maximizer, up to complement:

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Exact joint-sector result:

- `rank_AB<=102660`;
- `rank_CDE<=240240`;
- `rank_center(S3)<=24,663,038,400`;
- central exponent `34.52163149454245...`.

Clean run `32020902579`: success.

## Fully-open signed slope theorem

Old fused fully-open S3 cap65 is reduced by exact local ranks

- site11 `256->168`;
- site19 `128->96`;
- site27 `256->192`.

Remaining42 channels stay binary, hence

`rank_fully_open(S3)<=189*2^56`,

`F_S3<=56+log2(189)=63.562242424221076...`.

Clean run `32023025384`: success. Current asymptotic common-tree slope is

`8*F_S3=508.4979393937686...`,

an exact improvement of11.5020606062314 bits per added inverse double round from the old520 slope.

## Semi-open exact A/C/D bounds

Orientations are genuinely A/B/C/D and may not be silently identified.

- A: `rank_A(S3)<=405*2^46`, exponent54.661778097771986;
- B: generic `2^55` remains;
- C: `rank_C(S3)<=243*2^47`, exponent54.92481250360578;
- D: `rank_D(S3)<=3429*2^42`, exponent53.74357218893564.

D uses the complete `[4,5]` interval: exact rational rank1016 on twelve fused crossing channels; Gram zero rows1520, signed representatives1760, odd-prime rank1016, and744 further modular dependencies all lift to exact integer relations. Sites11/19/27 each have exact rank96. Clean A/C run `32024935318`; clean A/C/D depth run `32026645042`: success.

Four-semi product:

`<=337,465,035*2^190`, exponent218.3301627903134.

## Current d>=2 exact representation law

For fixed outer input masks and every `d>=2`,

`W_repr(d) <= log2(24,663,038,400)+log2(337,465,035*2^190)+(8d-12)log2(189*2^56)+176`.

Numerically:

`W_repr(d)<=508.4979393937686... d -333.8951148057971...`.

Examples:

- d2 `683.1007639817401...`;
- d3 `1191.5987033755086...`;
- d4 `1700.0966427692774...`.

## Clean/scoped falsifiers

- semi-open physical `i<->i+16` pair factors are full row rank55 for A/B/C/D; clean run `32023730565`;
- direct fully-open minimal-TT S3 terminal cut is exact86, worse than fused65; clean run `32023648911`;
- B `[4,5]` interval alone cannot close sub55 in the current decomposition: an1800x1800 odd-prime minor already has rank1763, above the required `<1490` threshold;
- B site11->13 carry-only segment gives no gain beyond the isolated site11 factor;
- naive direct-sum conditioning on internal B or fully-open sectors can be worse than the blind product;
- d=1 block1 extended by physical `C13,C14` through the shared j2 carry has exact rank64=`16*4`; this local carry extension gives no further S1 compression;
- historical coefficient-specific leaf witness run `32011941759` ended exit143 and is not authority.

## Storage/work status

One-QR RL218 width optimization still has a dense-work proxy about4.016x worse than the rank27 source topology. The new d=1 factor-generation85 result improves a materialized-factor message/storage ledger, **not arithmetic work**. Output-size alone gives at least `87*2^79` scalar generations for one complete signed factor. No ranking/search reduction or alpha gain is admitted.

## Current sharp blockers

1. d=1 representation/factor-generation: lower S1 central rank below `87*2^35`. Easy disjoint local blocks and the `C13,C14` carry extension are exhausted; next gain must use longer/global cross-cut structure or central×leaf coupling.
2. d=1 work: turn the signed factor-generation representation into a genuinely lower-work algorithm. Memory/message constructivity is no longer the main blocker; arithmetic work is.
3. Semi-open B remains generic55. Any gain must respect rotation7 B-output wiring together with offset16 D reuse; pair, carry-only and naive sector routes are already falsified.
4. Fully-open S3 may still fall below63.562 through genuine multi-site row-space overlap.
5. Coefficient-specific predecessor-leaf compression requires a clean uniform/parametric theorem or an explicitly frozen outer128 mask.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.
