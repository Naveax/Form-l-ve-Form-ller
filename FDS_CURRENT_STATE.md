# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured QR-cap execution remains frozen behind missing V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is a calculator/falsifier and new finite claims require clean-checkout execution.

## Clean-revalidated one-QR authority

For all 4096 physical fixed-mask cases,

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

Corrected sharp one-QR bound:

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... <39`.

The old `support<=216`, 13 support classes and rank-12 support-selector claims are revoked. Correct I9 support is defined by the exact Gram diagonal. Across the 64 physical six-left-mask cases:

- support range `117..218`;
- 64 distinct support sets;
- union392, intersection42;
- support-indicator rank64;
- residual `epsilon=0`.

The six-left-mask complete coefficient family has full span64 and natural TT profile `[2,4,8,16,32,64]`.

Physical right/parent facts retained from clean exact transfer algebra:

- right doubled hull `162=114+48`;
- right rank `11..38`;
- parent rank `5..27`;
- `u2_31=0`: parent `16..27`;
- `u2_31=1`: parent `5..8`;
- all 64 left fixed-mask maps share one exact 48-dimensional interface row space.

## Gram-image semantics

For single-copy coefficient map `R_m`, let `G_m=R_mR_m^T`.

Exact Gram/rank-space structure:

- Gram family span145;
- prefix140;
- closure16;
- `L G_m` family span124;
- its row directions span47;
- natural 12-control Gram-image TT profile `[2,4,8,16,32,64,128,119,196,136,143,124]`.

These objects do **not** retain the 24 right-external coefficient amplitudes. Do not propagate the 124/U47 Gram-image family through a later QR as if it were the single-copy coefficient tensor.

## Exact inverse-double-round ledgers

The q138 backward inverse-double-round cone has one active final column QR plus four diagonal predecessor QRs.

Keep three ledgers separate:

- topology-only: `W_2_topo<=236`;
- explicit constructive structural bound: `W_2_construct<=95`;
- exact representation existence: `W_2_repr<=79+log2(87)=85.44294349584872...`.

The constructive95 method keeps the central QR in exact reduced graph form, materializes each fixed-input/single-output leaf as an exact 32-bit vector, then uses hierarchical leaf factorization. Leaf generation peak is at most44 and dense leaf output exponent32.

### Specialized d=1 signed theorem

Frozen HT-tree critical partitions:

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

Exact q138 MSB conservation from final j4 mask `2^3` gives `msb(u4)=msb(v4)=3` and `msb(u3)=msb(v3)=27`.

For S1:

- block on `A0,B0,C15,C16,D0`: exact rank16;
- occurrence-closed block on `A13..16,B13..16,D13..16,C0`: exact rank2784;
- remaining26 S1 row bits pass trivially.

Hence

`rank_center(S1)<=16*2784*2^26=87*2^35`.

For S2, exact j1 bits31..27 sector ranks give

`rank_center(S2)<=31*2^35`.

Four generic diagonal leaf Hilbert factors contribute exponent44 at the critical 11|21 splits. Thus the complete frozen tree has maximum

`87*2^79`,

so

`W_2_repr<=79+log2(87)=85.44294349584872...`.

Clean Actions run `32019335785` is `success`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`;
- `.github/workflows/double-round-signed85.yml`.

This remains representation existence; `W_2_construct<=95` is not replaced.

## Multi-double-round joint-sector law

For fixed outer input masks and `d>=2`, use the frozen common tree whose generic maximizer has smaller side

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

The previous generic central cap was `2^44`. Exact signed occurrence-closed factorization and shared-sector projection now reduce this central matricization sharply.

### First 24 S3 row bits

Block A:

`A27..29,B27..29,D27..29,C11..13`, exact rank434.

Block B, disjoint physical row variables:

`A11..13,B11..13,D11..13,C27..29`, exact rank1792.

They share six crossed internal `v3` sector bits. Exact sector projection pairs are

- `(16,120)` in36 sectors;
- `(16,75)` in12;
- `(11,120)` in12;
- `(11,75)` in4.

Therefore the joint rank is safely bounded by the exact direct-sum sector sum

`rank_AB<=102660`,

far below the blind product `434*1792`.

### Remaining 20 S3 row bits

Two symmetric occurrence-closed site-pair blocks each have exact rank192 instead of256. They share four crossed `v3` sector bits.

The final site19 row block `A19,B19,C19,D19`, including both D19 and complement-side D3 occurrences plus shared `v3_15`, has exact rank12. It also shares carry sectors `sigma1_19,sigma2_19` with the pair blocks.

Conditioning jointly on the four `v3` bits and two carry bits gives

`rank_CDE<=240240`,

below both the blind `192*192*12` product and the earlier partial sector bound.

The AB and CDE row-variable groups are disjoint and cover all44 physical S3 row bits. Therefore

`rank_center(S3) <= 102660 * 240240 = 24,663,038,400`.

Central exponent:

`log2(rank_center(S3)) <=34.52163149454245...`.

This is a reduction of `9.47836850545755...` bits from the generic central exponent44.

Recounting every common-tree cluster gives, for all `d>=2`,

`W_repr(d) <= 520*d - 384 + log2(24,663,038,400)`.

Equivalently

`W_repr(d) <= 520*d - 349.47836850545755...`.

Current verified values:

- d2 `690.5216314945425...`;
- d3 `1210.5216314945425...`;
- d4 `1730.5216314945425...`;
- d5 `2250.5216314945425...`;
- d6 `2770.5216314945425...`;
- d7 `3290.5216314945425...`;
- d8 `3810.5216314945425...`;
- d9 `4330.5216314945425...`.

The coefficient-independent fully-open QR cap remains65, so the slope stays520; the improvement is in the intercept.

Clean Actions run `32020902579` is `success`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DEPTH_JOINT_SECTOR_LAW.md`;
- `scripts/verify_v26_q138_depth_joint_sector_law.py`;
- `.github/workflows/depth-joint-sector-law.yml`.

## Scoped falsifiers / cautions

Retain:

- old central cardinality MILP graph boundaries for smaller side11..16: `51,52,55,54,55,56`;
- refined central minimal-TT terminal cuts on old d=1 critical partitions: `44,44,44`, exactly44 binary cut indices and no ternary cut bond;
- pure GF(2) projected critical-boundary codimension `0,0`;
- generic leaf terminal-cut exponent11.

Historical coefficient-specific leaf full-rank witness workflow run `32011941759` terminated with exit143 during the heavy witness step. It is not clean authority. Do not use a source-specific leaf full-rank claim until revalidated, and do not assume an outer128 mask the repo has not frozen.

## Storage/work status

One-QR RL218 compression remains exact but its current width-optimized dense-work proxy is about `4.0160678967x` worse than the rank27 source topology. No arithmetic-work improvement is admitted.

Generic hierarchical leaf factorization does not compress arbitrary leaf storage: one arbitrary 32-bit leaf vector has information dimension `2^32`, while the frozen generic HT representation uses slightly more than `2^32` scalar slots per leaf.

The new d=1 and d>=2 signed bounds are representation/message upper bounds, not constructive or arithmetic-work bounds.

## Current sharp mathematical blockers

1. d=1: strengthen S1 central rank below `87*2^35` through genuinely global/cross-cut coefficient structure; the easy disjoint occurrence-closed local blocks are largely exhausted.
2. constructive gap: turn signed central factorizations into an explicit factor-generation/contraction procedure and reduce `W_2_construct` below95.
3. joint central×leaf rank: independent central-rank × four-leaf Hilbert-rank multiplication may still overcount shared sectors.
4. d>=2: reduce the fully-open coefficient-independent cap65 or find further global coupling beyond the S3 sector product; otherwise the slope520 remains.
5. leaf coefficient-specific compression requires a clean completed uniform/parametric theorem or an explicitly frozen outer mask.

All admitted reductions are exact, `epsilon=0`. Do not activate epsilon-rank while these exact signed/sector/joint routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.

Historical measured execution remains blocked by missing V25 runtime bytes; this is provenance, not a mathematical NO-GO.
