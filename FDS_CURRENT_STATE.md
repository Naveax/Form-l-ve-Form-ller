# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured execution remains frozen behind missing exact recovered V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is only a calculator/falsifier and new finite claims require clean-checkout execution.

## One-QR authority

For all 4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925... <39`.

Current sharp one-QR peak:

`D_max=218*2^31=468,151,435,264`.

Old support216 / 13 support classes / rank12 selector is revoked. Exact I9 support over64 left masks is117..218, with64 distinct support sets, union392, intersection42, support-indicator rank64 and `epsilon=0`. Six-left-mask complete coefficient family span64, TT profile `[2,4,8,16,32,64]`. Physical right rank11..38, parent rank5..27, right doubled hull162=114+48, and all64 left fixed-mask maps share one exact 48-dimensional interface row space.

Gram-image warning remains: `G_m=R_mR_m^T` rank-space data (Gram family145, `L G_m` span124, row directions47, etc.) are not single-copy coefficient amplitudes and must not be propagated through another QR as such.

## Inverse-double-round ledgers

Keep separate:

- topology-only `W_2_topo<=236`;
- explicit constructive `W_2_construct<=95`;
- exact d=1 representation existence `W_repr(1)<=79+log2(87)=85.44294349584872...`.

The constructive95 method is not superseded by the smaller representation theorem.

### d=1 signed theorem

Critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact central bounds:

- `rank_center(S1)<=87*2^35`;
- `rank_center(S2)<=31*2^35`.

With four generic predecessor-leaf Hilbert exponents44:

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Clean run `32019335785`: success.

## d>=2 central S3 rank

Frozen common-tree maximizer, up to complement:

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Exact joint-sector result:

- `rank_AB<=102660`;
- `rank_CDE<=240240`;
- `rank_center(S3)<=24,663,038,400`;
- central exponent `34.52163149454245...`.

Clean run `32020902579`: success.

## Fully-open signed slope theorem

Old fused fully-open S3 cap65 is reduced by exact rational local ranks

- site11 `256->168`;
- site19 `128->96`;
- site27 `256->192`.

The remaining42 channels stay binary, hence

`rank_fully_open(S3)<=189*2^56`,

`F_S3<=56+log2(189)=63.562242424221076...`.

Clean run `32023025384`: success. This changes the asymptotic common-tree slope from520 to

`8*log2(189*2^56)=508.4979393937686...`.

## Semi-open exact A/C/D theorems

The four predecessor orientations are A/B/C/D; they are not interchangeable by assumption.

### A and C

Four disjoint fused-channel blocks on sites4,11,19,27 give exact rational ranks

- A: `48,60,96,96`;
- C: `48,72,96,96`.

Therefore

`rank_A(S3)<=405*2^46`, exponent `54.661778097771986...`,

`rank_C(S3)<=243*2^47`, exponent `54.92481250360578...`.

Clean run `32024935318`: success.

### D interval theorem

For D, contract the complete S3 interval `[4,5]`: twelve fused crossing channels, with four internal carry channels contracted exactly. The resulting 4096-row map has exact rational rank

`rank_D[4,5]=1016`.

Certificate facts:

- exact Gram zero rows1520;
- signed-row representatives1760;
- odd-prime rank1016;
- 744 additional independent modular dependencies all lift to exact centered integer relations.

The remaining D entry blocks on sites11,19,27 each have exact rank96. Thus

`rank_D(S3)<=1016*96^3*2^24 =3429*2^42`,

`F_D<=53.74357218893564...`.

Clean Actions run `32026645042`: success. It revalidated central, fully-open, A/C, D interval, and the complete depth recount from clean checkout.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_SEMI_OPEN_S3_SIGNED_D_INTERVAL_THEOREM.md`;
- `scripts/verify_v26_q138_semi_open_s3_signed_d_interval.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_SEMI_OPEN_SIGNED_ACD_THEOREM.md`;
- `scripts/verify_v26_q138_depth_semi_open_signed_acd.py`;
- `.github/workflows/depth-semi-open-signed-acd.yml`.

B remains at the generic `2^55` cap.

The four semi-open contribution product is now

`rank_A rank_B rank_C rank_D <=337,465,035 * 2^190`,

with total exponent

`218.3301627903134...`.

## Current d>=2 exact representation law

For fixed outer input masks and every `d>=2`,

`W_repr(d) <= log2(24,663,038,400) + log2(337,465,035*2^190) + (8d-12)log2(189*2^56) +176`.

Numeric affine form:

`W_repr(d) <= 508.4979393937686... d -333.8951148057971...`.

Verified examples:

- d2 `683.1007639817401...`;
- d3 `1191.5987033755086...`;
- d4 `1700.0966427692774...`.

This remains exact representation/message width. No constructive or arithmetic-work reduction follows automatically.

## Clean scoped falsifiers

- Semi-open physical `i<->i+16` occurrence-closed pair factors are full row rank for A/B/C/D, total55 each; clean run `32023730565` success. This closes only that pair route.
- Direct fully-open minimal-TT refinement on S3 has exact terminal hypergraph cut86 after lexicographic witness correction; clean run `32023648911` success. It is worse than fused65 and is not a lower bound on true Walsh Schmidt rank.
- B interval `[4,5]` cannot by itself deliver the needed sub55 theorem: an 1800x1800 odd-prime minor has rank1763, already above the `<1490` threshold required when combined with the current site11 rank88 route. This is a scoped falsifier, not a global B lower bound.
- d=1 pure GF(2) critical-boundary codimension remains0,0.
- historical coefficient-specific leaf witness run `32011941759` ended exit143 and is not authority.

## Storage/work status

One-QR RL218 compression is exact but its width-optimized dense-work proxy is about `4.0160678967x` worse than the rank27 source topology. No arithmetic-work gain is admitted. Current d=1 and d>=2 signed results are representation/message bounds, not constructive-work bounds.

## Current sharp blockers

1. Semi-open B remains at generic55. Because B is the rotated output, local site `i` contains `Bout[i+7]`; physical B-output row sites are `S3-7={4,5,6,12,13,14,20,21,22,29,30}`. The next B theorem must respect this rotation-7 wiring together with offset16 D-copy structure. Simple carry-only segment coupling and simple internal-sector direct sums do not improve the existing site11 gain.
2. D may admit further interval/global coupling, but the current exact cap53.7436 already removes it as the largest semi-open blocker.
3. Fully-open S3 may still fall below63.562 through genuine multi-site channel coupling.
4. d=1 S1: seek longer cross-cut coupling or central×leaf joint rank.
5. Constructive gap: realize signed d=1 factorizations explicitly and reduce `W_2_construct<95`.
6. Coefficient-specific leaf work requires a clean uniform/parametric theorem or explicitly frozen outer128 mask.

All admitted reductions remain exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.
