# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=84.90275194485017...`.  
**d=1 coefficient-blind static method:** `W_static,blind=95`.  
**d>=2 law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0`.

All admitted reductions are exact, `epsilon=0`. Code is only calculator/falsifier; finite claims require clean-checkout execution.

## d=1 center authority

`S1={0,1,2,3,4,5,12,13,14,15,16}`. All44 physical S1 row bits are occurrence-closed.

`rank_center(S1)<=3829*2^29=2,055,678,722,048`, clean `32043410513`.

Generic predecessor-leaf exponent44 gives

`dim_factor<=3829*2^73`,

`W_repr(1)<=84.90275194485017...`.

Factor-generation message/storage constructivity matches this bound; clean `32043554316`. Arithmetic work is still not reduced.

Central work structure per high prefix remains

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

Materialization, separate full low/high bases and generic monotone complement interleaving are scoped work NO-GAIN routes; clean `32044123499`, `32055881609`, `32056604049`.

## Current predecessor-leaf dyadic authority

Leaf topology cut11 is exact; topology alone cannot beat `2^11=2048`.

Natural coefficient scales:

`L_A,L_D in 2^-92 Z`,

`L_B,L_C in 2^-121 Z`, clean `32058413111`.

### A/D

`M_A=2^92L_A`, `M_D=2^92L_D`.

First layer:

`rank_F2(M_A mod2)<=3`,

`rank_F2(M_D mod2)<=3`, clean `32058931522`.

Write `M=M0+2M1` with integer rank<=3 first lift.

The old sector-sum309/310 bounds are superseded. Uniform predecessor-input activity gives

`rank_F2(M1_A mod2)<=219`,

`rank_F2(M1_D mod2)<=207`.

Exact affine activity maxima are181 and171; signed budgets are38 and36. Clean theorem `32065522597`.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_AD_ACTIVITY_RANK219_207.md`;
- `scripts/verify_v26_q138_predecessor_leaf_ad_activity_rank219_207.py`.

Cheap A/D refinements closed:

- no duplicate canonical-support XOR gain (`32064086782` probe);
- homogeneous affine Fourier frequency unions saturate all2048 S1 frequencies (`32065783472` probe).

### B/C

`M_B=2^121L_B`, `M_C=2^121L_C`.

The original first-residue decomposition has103 odd affine supports plus one signed four-sector support; clean GF(2) sum bounds1052/1160 (`32063042288`). Input-mask mutual exclusion cannot sharpen those sums; all objects can be active simultaneously, clean `32065964357`.

The decisive improvement is Fourier alignment. Across all103 affine supports the union of homogeneous S1 Walsh frequencies has size

- B:16;
- C:64.

Thus the ordinary integer affine sums have Q-rank<=16 and<=64. The signed common-support Boolean term has Q-rank<=20 because support intersection dimension2 gives at most4 rectangles and cross-bilinear rank2 gives Boolean rank<=5 per rectangle.

Therefore explicit coefficient-aligned first lifts exist:

`M_B=K_B+2R_B`, `rank_Q(K_B)<=36`,

`M_C=K_C+2R_C`, `rank_Q(K_C)<=84`.

Clean `32066435545`.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_BC_FOURIER_LIFT_RANK36_84.md`;
- `scripts/verify_v26_q138_predecessor_leaf_bc_fourier_lift_rank36_84.py`.

Use36/84, not1052/1160, as the current B/C first-layer dyadic envelopes.

## Current exact dyadic prefix

Natural four-leaf scale is `2^426`.

Use per-leaf envelopes

A `[3,219,2048,2048,...]`,

B `[36,2048,2048,...]`,

C `[84,2048,2048,...]`,

D `[3,207,2048,2048,...]`.

Four-leaf product layer bounds:

- k0 `27,216`;
- k1 `6,076,512`;
- k2 `528,287,760`;
- k3 `22,588,489,728`;
- k4 `499,782,844,416`;
- k5 `5,718,621,093,888`;
- k6 `33,271,289,282,560`.

Prefix k0..k5:

`6,241,526,819,520`.

Generic four-leaf budget:

`2^44=17,592,186,044,416`.

Current unresolved tail budget:

`11,350,659,224,896`.

Attach center: k0..k5 complete-S1 prefix channels

`12,830,573,875,979,191,540,776,960`,

exponent `83.4077880718021...`.

This leaves1.494963873 bits below the current full-factor exponent84.90275194485017, but **no complete-factor bound is lowered** until the exact k>=6 tail is controlled.

Generic k6 is `33,271,289,282,560`, only2.9312208765x the entire tail budget. Clean six-layer gate `32066572887`.

Authority:

- `V26_Q138_DYADIC_FOURIER_SHARPENED_SIX_LAYER_GATE.md`;
- `scripts/verify_v26_q138_dyadic_fourier_sharpened_six_layer_gate.py`.

Older five-layer gates and old depth warnings are superseded search envelopes, not current blockers.

## Sharp next target

A full dyadic improvement requires

`sum_{k>=6} rank(layer_k) <11,350,659,224,896`.

The next unknown single-leaf ranks are

`a2=A third`, `d2=D third`, `b1=B second`, `c1=C second`.

Useful k6 thresholds:

- all four next ranks equal: k6 fits at about1386.8 or below;
- A/D next remain2048: B/C next about<=968 each makes k6 fit;
- B/C next remain2048: A/D next about<=785 each makes k6 fit.

These only make k6 fit; the later tail still needs a total bound.

## Active exact probes

1. **B/C second residue:** weight120 rank128 unique-solution sectors, determined cheaply in the4D top-nullspace quotient, are being tested for S1 Fourier saturation. Early-stop if union reaches2048.
2. **A/D third residue:** weight90 rank128 unique-solution sectors are exactly the8281 three-zero patterns containing `(j1,0)` or `(j3,0)`; their S1 Fourier union is being probed.

If either union stays substantially below2048, promote it into the next residue theorem. If it saturates quickly, change structure rather than enumerating millions of sectors for sport.

## Non-authoritative / provenance warnings

- old leaf coefficient full-rank run `32011941759`: exit143 before result;
- exploratory dense 2048x2048 minor `32054802994`: bad path /32-GiB failure before rank result;
- fixed-mask low-activity probes are not uniform theorems;
- no canonical frozen `outer128` predecessor mask is available, so source-specific leaf claims remain provenance-gated;
- old four-site ranks96/208 and W84/W83 claims remain revoked.

## d>=2 — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, d>=2.

## First unfinished mathematical pass

1. Resolve the active A/D third-residue and B/C second-residue Fourier probes; promote only exact non-saturation results.
2. Build explicit next-residue lifts with target ranks roughly in the785–1387 range and recount k6 immediately.
3. Continue until the entire `k>=6` dyadic tail is rigorously below `11,350,659,224,896`; only then reconsider `W_repr(1)` / `W_factor-gen`.
4. Only after total dyadic control, fuse the leaf decomposition into the D16 common/private center and count total arithmetic work.
5. Other nonlocal center regroupings, semi-open B<55 and fully-open S3<63.562 remain separate exact routes.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
