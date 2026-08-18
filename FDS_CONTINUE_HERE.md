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

The first explicit Fourier-aligned lifts are

`M_B=K_B,0+2R_B`, `rank_Q(K_B,0)<=36`,

`M_C=K_C,0+2R_C`, `rank_Q(K_C,0)<=84`, clean `32066435545`.

The second residue is now closed. Support-only left Walsh spaces have dimensions668/788. Exact Gauss-completed sign-dependent GF(2) spans are348/432. After exact integer Walsh transform and projection modulo the support spaces, the ZZ/Q quotient ranks are144/184.

Therefore exact second integer lifts exist with

`R_B=K_B,1+2R_B,2`, `rank_Q(K_B,1)<=812`,

`R_C=K_C,1+2R_C,2`, `rank_Q(K_C,1)<=972`.

Equivalently,

`2^121L_B=K_B,0+2K_B,1+4R_B,2`,

`2^121L_C=K_C,0+2K_C,1+4R_C,2`.

Clean PR-checkout chain `32112658496` verifies sign spans348/432, quotient ranks144/184, final812/972 lifts and the seven-layer gate.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_RANK812_972.md`;
- `scripts/verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432.py`;
- `scripts/verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972.py`.

Use812/972, not1016/1220 or2048, as the current B/C second-layer envelopes.

## Current exact dyadic prefix

Natural four-leaf scale is `2^426`.

Use per-leaf envelopes

A `[3,219,2048,2048,...]`,

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`,

D `[3,207,2048,2048,...]`.

Four-leaf product layer bounds:

- k0 `27,216`;
- k1 `4,793,472`;
- k2 `315,450,720`;
- k3 `9,979,784,064`;
- k4 `171,359,156,304`;
- k5 `1,703,063,715,840`;
- k6 `10,186,815,307,776`;
- generic k7 `38,736,654,106,624`.

Prefix k0..k6:

`12,071,538,235,392 <2^44`.

Generic four-leaf budget:

`2^44=17,592,186,044,416`.

Current unresolved tail budget:

`5,520,647,809,024`.

Attach center: k0..k6 complete-S1 prefix channels

`24,815,204,292,884,195,564,322,816`,

exponent `84.3594267039546...`.

This leaves `0.54332524089557...` bits below the current full-factor exponent84.90275194485017, but **no complete-factor bound is lowered** until the exact k>=7 tail is controlled.

Generic k7 is7.0166863467x the entire tail budget. If all four index-2 residues were zero and every deeper residue remained generic, k7 would be `1,703,063,715,840`, already below the tail budget. Clean gate `32112658496`.

Authority:

- `V26_Q138_DYADIC_WALSH_QUOTIENT_SEVEN_LAYER_GATE.md`;
- `scripts/verify_v26_q138_dyadic_walsh_quotient_seven_layer_gate.py`.

Older six/five-layer gates and old depth warnings are superseded search envelopes, not current blockers.

## Sharp next target

A full dyadic improvement requires

`sum_{k>=7} rank(layer_k) <5,520,647,809,024`.

The next unknown single-leaf ranks are the index-2 residues

`a2=A third`, `b2=B third`, `c2=C third`, `d2=D third`.

The immediate gate is the exact k7 polynomial under these four ranks. The zero-index2 diagnostic proves that improving the next residue family is sufficient in principle to make k7 fit. This is only a k7 statement; later layers still need a complete sum bound.

## Active exact probes

1. **A/D third direct-e2 support component:** exact XOR-aggregated weighted predecessor-input activity. The first128-variable MILP clean run was cancelled after35 minutes without a certificate; current work reduces the objective to its global input-functional quotient before solving.
2. **A/D third correction component:** choose the e0 negative-sign second lift with coefficient `-1` at the same rank cost so those terms vanish exactly from the third residue. Current probe computes one uniform left span for the remaining e1 negative-sign corrections.
3. **B/C third residue:** now the next B/C unknown. Start from the explicit812/972 second lifts; do not reopen the closed B/C second residue.

Promote only theorem + clean verifier results. Fixed-mask/source-specific measurements remain non-authoritative without a frozen outer128 predecessor mask.

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

1. Finish A/D third residue as direct-e2 support plus e1 negative-sign correction under an explicit second lift.
2. Open B/C third residues from the canonical812/972 second lifts and recount k7 whenever any index-2 bound improves.
3. Continue until the entire `k>=7` dyadic tail is rigorously below `5,520,647,809,024`; only then reconsider `W_repr(1)` / `W_factor-gen`.
4. Only after total dyadic control, fuse the leaf decomposition into the D16 common/private center and count total arithmetic work.
5. Other nonlocal center regroupings, semi-open B<55 and fully-open S3<63.562 remain separate exact routes.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
