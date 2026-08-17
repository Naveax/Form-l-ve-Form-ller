# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured QR-cap execution remains frozen behind missing V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is a calculator/falsifier and new finite claims require clean-checkout execution.

## One-QR exact authority

For all 4096 physical fixed-mask cases,

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

Corrected sharp bound:

`D_max=218*2^31=468,151,435,264`,

so

`W_1<=38.768184324776925...<39`.

The old support216 / 13-support-class / rank12-selector line is revoked. Correct exact I9 support over the 64 left masks is `117..218`, with64 distinct support sets, union392, intersection42, support-indicator rank64 and `epsilon=0`. The six-left-mask complete coefficient family has full span64 and natural TT profile `[2,4,8,16,32,64]`.

Physical right/parent exact facts retained:

- right doubled hull162=114+48;
- right rank11..38;
- parent rank5..27;
- `u2_31=0`: parent16..27;
- `u2_31=1`: parent5..8;
- all64 left fixed-mask maps share one exact 48-dimensional interface row space.

## Gram-image semantic warning

For single-copy right coefficient map `R_m`, `G_m=R_mR_m^T` has exact Gram/rank-space structure:

- Gram family span145;
- prefix140;
- closure16;
- `L G_m` span124;
- its row directions span47;
- natural12-control Gram-image TT profile `[2,4,8,16,32,64,128,119,196,136,143,124]`.

These are rank/Schmidt-space objects, not the full single-copy coefficient tensor. They do not retain the 24 right-external coefficient amplitudes. Do not propagate 124/U47 through another QR as if it were coefficient amplitude data.

## Inverse-double-round ledgers

The q138 backward inverse-double-round cone has one active final column QR plus four diagonal predecessor QRs.

Keep separate:

- topology-only `W_2_topo<=236`;
- explicit constructive `W_2_construct<=95`;
- exact representation existence `W_repr(1)<=79+log2(87)=85.44294349584872...`.

The constructive95 method keeps the central QR in exact reduced graph form, materializes the four fixed-input/single-output diagonal leaves as exact32-bit vectors and hierarchically factors them. The signed representation bound below does not replace this constructive ledger.

### Specialized d=1 signed theorem

Frozen critical sets:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

q138 final central j4 output mask `2^3` gives exact MSB conservation `msb(u4)=msb(v4)=3`, then `msb(u3)=msb(v3)=27`.

S1 exact signed blocks:

- row bits `A0,B0,C15,C16,D0`: rank16;
- occurrence-closed row bits `A13..16,B13..16,D13..16,C0`: rank2784;
- remaining26 row bits raw.

Thus `rank_center(S1)<=87*2^35`.

S2 exact top-sector calculation gives `rank_center(S2)<=31*2^35`.

Four generic diagonal leaf Hilbert factors contribute exponent44 at the critical 11|21 splits. Therefore the complete frozen HT tree has

`W_repr(1)<=79+log2(87)=85.44294349584872...`.

Clean Actions run `32019335785`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`;
- `.github/workflows/double-round-signed85.yml`.

## d>=2 common-tree central signed rank

Frozen common-tree maximizer up to complement:

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Exact occurrence-closed signed blocks plus shared-sector projection cover all44 physical central row bits:

- AB joint sector bound `rank_AB<=102660`;
- CDE joint sector bound `rank_CDE<=240240`.

Hence

`rank_center(S3)<=24,663,038,400`,

with exponent

`34.52163149454245...`.

Clean Actions run `32020902579`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_JOINT_SECTOR_LAW.md`;
- `scripts/verify_v26_q138_depth_joint_sector_law.py`.

## New fully-open signed slope theorem

The same common-tree S3 partition had a fused fully-open QR envelope of65 binary channels. Exact signed coefficient rank now reduces this value.

Use fused local channels

- `b_i=Bout_{i+7}`;
- `z_i=J4_v[i] xor Dout_i`;
- `K_i=J3_v[i] xor Bout_{i+7}`,

with the four longitudinal carry channels and exact local Walsh sums over `J4_u` and `J3_u`.

Three disjoint S3 crossing-channel groups have exact rational ranks:

- site11: eight raw binary channels `256 ->168`;
- site19: seven raw channels `128 ->96`;
- site27: eight raw channels `256 ->192`.

The other42 fused crossing channels remain binary. Therefore

`rank_fully_open(S3)<=168*96*192*2^42=189*2^56`.

Fully-open S3 exponent:

`F=56+log2(189)=63.562242424221076...`.

This reduces the old65 by `1.437757575778924...` bits. Only S3 and its complement had old cap65; the next generic fully-open common-tree cap is62.

Each local rank is certified over Q by an odd-prime nonsingular minor plus a complete independent set of exact integer left-null relations. The null coefficients are only `{-1,0,1}`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FULLY_OPEN_S3_LOCAL_RANK_CERTIFICATE.json`;
- `scripts/verify_v26_q138_fully_open_s3_local_signed_rank.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_FULLY_OPEN_SIGNED_SLOPE_THEOREM.md`;
- `scripts/verify_v26_q138_depth_fully_open_signed_slope.py`;
- `.github/workflows/depth-fully-open-signed-slope.yml`.

Clean Actions run `32023025384`: success. It revalidated the central joint-sector dependency, all three local fully-open exact ranks, and the full depth recount from clean checkout.

## Current d>=2 exact representation law

For fixed outer input masks and every `d>=2`, the frozen common tree now gives

`W_repr(d) <= log2(24,663,038,400) + 396 + (8d-12)*log2(189*2^56)`.

Numerically,

`W_repr(d) <= 508.4979393937686...*d - 332.22527759611046...`.

Verified values:

- d2 `684.7706011914267...`;
- d3 `1193.2685405851953...`;
- d4 `1701.7664799789638...`;
- d5 `2210.2644193727324...`;
- d6 `2718.762358766501...`;
- d7 `3227.2602981602695...`;
- d8 `3735.7582375540383...`;
- d9 `4244.256176947807...`.

The asymptotic common-tree slope is therefore reduced from520 to

`508.4979393937686...`,

a gain of `11.5020606062314...` representation bits per additional inverse double round.

This is exact representation/message width only. No constructive or arithmetic-work reduction follows automatically.

## Current exact/scoped falsifiers

Retain:

- old central graph-cardinality boundaries k11..16 `51,52,55,54,55,56`;
- old d=1 refined terminal cuts `44,44,44` with binary cut indices;
- pure GF(2) d=1 critical-boundary codimension `0,0`;
- generic leaf terminal-cut exponent11.

The direct fully-open minimal-TT refinement route is being revalidated separately; do not cite its cut86 result as clean authority until its corrected clean workflow passes.

Historical coefficient-specific leaf full-rank witness run `32011941759` ended exit143 during the heavy witness step and is not clean authority.

## Storage/work status

One-QR RL218 compression is exact but its width-optimized dense-work proxy is about `4.0160678967x` worse than the rank27 source topology. No arithmetic-work improvement is admitted.

Generic hierarchical leaf factorization does not compress arbitrary leaf storage: one arbitrary32-bit leaf vector has information dimension `2^32`, while the frozen generic HT representation uses slightly more than `2^32` scalar slots per leaf.

The d=1 and d>=2 signed results are representation/message bounds, not constructive work bounds.

## Current sharp blockers

1. d=1: strengthen S1 central rank below `87*2^35` using global/cross-cut structure; easy disjoint local blocks are largely exhausted.
2. constructive gap: turn the signed central factorizations into explicit factor-generation/contraction and reduce `W_2_construct<95`.
3. joint central×leaf rank: independent central rank × four leaf Hilbert ranks may overcount shared sectors.
4. d>=2: lower the new fully-open S3 exponent `63.562242424...` with multi-site/channel coupling, or lower the four semi-open QR caps55. Single-site fully-open local compression is now exhausted at the obvious S3 sites; z19/z27 sector conditioning did not further reduce their product.
5. coefficient-specific leaf work requires a clean uniform/parametric result or an explicitly frozen outer128 mask.

All admitted reductions are exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.

Historical measured execution remains blocked by missing V25 runtime bytes; this is provenance, not a mathematical NO-GO.
