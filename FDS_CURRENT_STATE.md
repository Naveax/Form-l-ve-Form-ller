# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured QR-cap execution remains frozen behind missing V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is a calculator/falsifier and new finite claims require clean-checkout execution.

## Clean-revalidated one-QR authority

For all 4096 physical fixed-mask cases,

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

The corrected sharp one-QR bound is

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... <39`.

The old `support<=216`, 13 support classes and rank-12 support-selector claims are revoked. Correct I9 support is defined by the exact Gram diagonal `g_m(i)=sum_rest L_m(i,rest)^2`.

Across all 64 physical six-left-mask cases:

- support range `117..218`;
- 64 distinct exact support sets;
- union392;
- intersection42;
- exact rank of the `64 x 512` support indicator64;
- residual `epsilon=0`.

Thus `rank_{I9|rest}(L_m)<=218<256`.

The six-left-mask complete coefficient family has full span64 and natural TT profile `[2,4,8,16,32,64]`.

Physical right/parent facts retained from clean exact transfer algebra:

- right doubled reachable hull `1024 ->162 =114+48`;
- right rank over 4096 masks `11..38`;
- parent rank `5..27`;
- `u2_31=0`: parent `16..27`;
- `u2_31=1`: parent `5..8`;
- all 64 left fixed-mask maps share one exact 48-dimensional interface row space.

## Gram-image semantics

For the single-copy right coefficient map `R_m`, define `G_m=R_mR_m^T`.

Exact rank-space results:

- `dim Span{G_m}=145`;
- site3--6 prefix family rank140;
- site7 closure family rank16;
- `L G_m` family span124;
- its row directions span47;
- natural 12-control Gram-image selector TT profile `[2,4,8,16,32,64,128,119,196,136,143,124]`.

These are Gram/rank-space objects only. They do not retain the 24 right-external coefficient amplitudes. Do not propagate the 124/U47 family through another QR as if it were the single-copy coefficient tensor.

## Exact q138 inverse-double-round structure

The backward inverse-double-round dependency cone has one active final column QR plus four predecessor diagonal QRs.

Maintain three separate ledgers:

### Topology-only

`W_2_topo <=236`.

### Constructive exact representation

Keep the central fixed-output/open-four-input QR in exact reduced graph form. Contract each fixed-input/single-output diagonal leaf to its exact 32-bit vector and hierarchically factor the four vectors on the frozen bit tree.

Certified constructive peak:

`W_2_construct <=95`.

Leaf factor generation remains below exponent44 and dense leaf output has exponent32.

### Exact representation existence: signed local-rank bound

The former generic result `W_2_repr<=88` and the intermediate nonlinear-support result `<=86+log2(3)` are superseded by exact signed local Walsh rank factorizations.

Use the same frozen HT tree and its two unique critical 11|21 central bipartitions

`S1={0,1,2,3,4,5,12,13,14,15,16}`

and

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

The q138 final central QR has fixed j4 output mask `2^3`. Exact modular-addition MSB conservation gives

`msb(u4)=msb(v4)=3`,

then the j3 rotation relation gives

`msb(u3)=msb(v3)=27`.

For S1 two disjoint exact signed local factorizations are certified.

Block 1 uses the five physical row bits

`A0,B0,C15,C16,D0`.

All their central occurrences are included in j1 bit0 and j2 bits15,16. The exact dyadic flattening has rational rank

`16`

instead of the raw32 row states.

Block 2 uses the thirteen row bits

`A13..16, B13..16, D13..16, C0`.

All second occurrences of D13..16 are closed using j2 bits29..31 and j2 bit0. Exact sector-basis Kronecker products over the16 D sectors give union rank

`2784`

instead of8192 raw row states.

The blocks use disjoint physical row-variable sets. Passing the remaining26 S1 row bits trivially gives

`rank_center(S1) <= 16 * 2784 * 2^26 = 87 * 2^35`.

For S2, exact j1 bits31..27 ranks are computed sectorwise over the top five D bits. Two D sectors have rank32 and thirty have rank64, so the exact safe sector-channel count is

`2*32 + 30*64 = 1984 = 31*2^6`.

Passing the remaining29 S2 row bits gives

`rank_center(S2) <= 31 * 2^35`.

The four diagonal leaf vectors retain generic Hilbert exponent44 on the critical 11|21 splits. Therefore

- S1 message `<=87*2^79`;
- S2 message `<=31*2^79`.

Every noncritical node of the frozen HT tree remains at generic exponent at most80. Hence the exact representation-existence maximum is

`D_2,repr <= 87 * 2^79`,

so

`W_2_repr <= 79 + log2(87) = 85.44294349584872...`.

Clean GitHub Actions run `32019335785` completed `success`, running both the historical HT dependency and the signed verifier from clean checkout.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`;
- `.github/workflows/double-round-signed85.yml`.

This is exact representation existence, not constructive factor generation. The constructive ledger remains95 until generation/contraction of the signed compressed central factors is certified under the same peak.

## Scoped falsifiers / corrections around the double-round bound

Retain these exact facts:

- old central cardinality MILP graph boundaries for smaller side11..16: `51,52,55,54,55,56`;
- refined central minimal-TT terminal cuts on the old critical partitions: `44,44,44`, each with exactly44 binary cut indices and no ternary cut bond;
- pure GF(2) projected boundary codimension on the two unique 44-bit critical boundaries: `0,0`;
- generic leaf terminal-cut exponent11.

The historical heavy coefficient-specific leaf full-rank witness workflow is **not clean authority**: run `32011941759` was terminated by the runner with exit143 during the expensive witness search. Its HT88 dependency passed, but the witness step did not complete. Therefore do not use a universal or source-specific leaf full-rank witness claim until revalidated.

The new gain is actual signed Walsh coefficient rank, not a better graph cut or a linear parity relation.

## Multi-double-round representation law

For fixed outer input masks:

- special one-double-round exact representation bound: `W_repr(1)<=79+log2(87)`;
- for `d>=2`, the separate common-tree theorem remains

`W_repr(d)<=520d-340`.

Verified current common-tree values: d2=700, d3=1220, d4=1740, d5=2260, d6=2780, d7=3300, d8=3820, d9=4340.

The d>=2 common tree has fully-open QR maximum65 and different maximizing clusters. The S1/S2 signed theorem does not automatically improve that law. A support-aware search restricted to the old HT tree shape did not beat the existing d2=700 tree; this is a scoped negative search result, not optimality.

## Storage/work status

One-QR RL218 compression is exact but its current width-optimized dense-work proxy is about `4.0160678967x` worse than the rank27 source topology. No arithmetic-work improvement is admitted.

Generic hierarchical leaf factorization also does not compress arbitrary leaf storage: one arbitrary 32-bit leaf vector has information dimension `2^32`, while the frozen generic HT representation uses slightly more than `2^32` scalar slots per leaf. Four generic leaves remain roughly `2^34` storage.

## Current sharp mathematical blocker

The exact double-round representation now has

`W_2_repr <=85.44294349584872...`,

while the explicit constructive ledger remains95.

Next exact mechanisms, in priority order:

1. strengthen S1 signed central rank below `87*2^35`, either by enlarging occurrence-closed local blocks or finding another disjoint exact factor;
2. build a constructive factor-generation/contraction realization of the signed S1/S2 rank factors and try to reduce `W_2_construct` below95;
3. seek a joint central×leaf factorization that beats independent central-rank × four-leaf Hilbert-rank multiplication;
4. revalidate coefficient-specific leaf ranks only with a clean completed computation; do not infer them from the terminated historical witness run and do not assume a concrete outer128 mask that the repo has not frozen;
5. derive analogous exact signed/support restrictions for the different maximizing cluster of the `520d-340` common tree.

All admitted reductions remain exact, `epsilon=0`. Do not activate epsilon-rank while these exact signed/support/joint routes remain open.

Still not admitted:

- practical evaluator at formal peaks;
- arithmetic-work reduction;
- ranking/search reduction;
- `alpha<1`;
- full-round cryptanalytic relevance.

Historical measured execution remains blocked by missing V25 runtime bytes; this is provenance, not a mathematical NO-GO.
