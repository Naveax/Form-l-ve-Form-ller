# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`. Historical measured QR-cap execution remains frozen behind missing V25 runtime bytes. Active work is mathematics-first exact Walsh/tensor analysis; code is a calculator/falsifier and new finite claims require clean-checkout execution.

## Clean-revalidated one-QR authority

The exact q138 fixed-output one-QR chain for all 4096 physical fixed-mask cases is

`44 -> 42 -> 41 -> 40 -> 38.768184324776925...`.

Corrected sharp full-family bound:

`D_max = 218 * 2^31 = 468,151,435,264`,

so

`W_1 <= 38.768184324776925... <39`.

Clean dependency revalidation has passed the minimal-core width41 certificate, exact rank528 replacement, width40 tree, left rank48, physical right hull162 and physical rank-envelope/common-interface calculations. Historical JSON/script serialization defects were repaired without changing the mathematical networks.

Core retained facts:

- left fixed-mask interface rank: 48;
- all 64 physical left maps share one 48-dimensional interface row space;
- physical doubled right reachable hull: `1024 ->162 =114+48`;
- physical right rank over 4096 masks: `11..38`;
- parent rank: `5..27`;
- `u2_31=0`: parent `16..27`;
- `u2_31=1`: parent `5..8`.

## Exact support correction

The old `support<=216`, 13 support classes and rank-12 support-selector claims are revoked.

Correct support is defined by the exact Gram diagonal

`g_m(i)=sum_rest L_m(i,rest)^2`.

Across all 64 physical six-left-mask cases:

- support range: `117..218`;
- distinct exact support sets: 64;
- union: 392;
- intersection: 42;
- exact rank of the `64 x 512` support indicator: 64;
- residual: `epsilon=0`.

Hence the safe exact left boundary result is

`rank_{I9|rest}(L_m)<=218<256`.

Authority:

- `V26_QR_Q138_SUPPORT218_GRAM_CORRECTION_THEOREM.md`;
- `scripts/verify_v26_qr_q138_left_i9_gram_support.py`;
- `V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json`;
- `scripts/verify_v26_qr_q138_general_rank27_support218_global_sub39.py`.

## One-QR work accounting

Peak-message improvement relative to `2^40`:

`256/109 ~=2.3486238532x`,

or about `1.2318156752` log2 bits.

Current width-optimized `RL218` tree does **not** improve naive dense work. Exact bookkeeping gives a dense-work proxy ratio

`4.0160678967339065x`

worse than the rank27 source topology. No arithmetic-work reduction is admitted.

Authority:

`V26_QR_Q138_SUPPORT218_WORK_ACCOUNTING.md` and `scripts/verify_v26_qr_q138_support218_work_accounting.py`.

## Left mask coefficient family

The six physical left controls

`u1_8,u1_9,u1_10,u2_8,u2_9,u2_10`

have no linear family compression at the complete coefficient-map level:

`dim Span{L_m}=64`.

Natural TT profile:

`[2,4,8,16,32,64]`.

Conditioning on `u2_8` gives family ranks `32,32`.

Authority:

`V26_QR_Q138_LEFT_COEFFICIENT_FAMILY_FULL64_THEOREM.md` and `scripts/verify_v26_qr_q138_left_coeff_family_tt.py`.

## Right Gram / parent Gram-image mask structure

Do not confuse the following with full coefficient amplitudes needed by another QR.

For the exact right map `R_m`, define `G_m=R_m R_m^T`.

Clean exact family results:

- `dim Span{G_m}=145`;
- site3--6 prefix family rank 140;
- site7 closure family rank 16;
- with a fixed common left 48-dimensional interface basis `L`, the Gram-image family `H_m=L G_m` has span 124;
- the row directions of the 124 basis matrices span a 47-dimensional interface rank space.

Natural 12-control TT profile of the 124-sector Gram-image selector:

`[2,4,8,16,32,64,128,119,196,136,143,124]`.

These are exact rank/Schmidt-space objects only. `G_m` loses the orientation/amplitude information in the 24 right-external mask legs, so the 124-sector family cannot be propagated through a next QR as though it were the single-copy coefficient tensor.

Authority:

`V26_QR_Q138_RIGHT_PARENT_COEFFICIENT_FAMILY_THEOREM.md` (semantically corrected to Gram-image interpretation), `scripts/verify_v26_qr_q138_right_bilinear_family_span.py`, and `scripts/verify_v26_qr_q138_mask_coeff124_tt.py`.

## Exact q138 inverse-double-round structure

The q138 backward double-round dependency cone contains one active final column QR `(0,4,8,12)` plus four diagonal QRs, one for each intermediate word and local output position A/B/C/D.

Three separate structural ledgers are now frozen:

### Topology-only

Corrected common-prefix bound:

`W_2_topo <=236`.

The older 252 overcounted the offset-16 perfect matching by a factor two.

### Constructive exact representation

Contract each fixed-input/single-output diagonal leaf to a 32-bit vector and exactly factor the four vectors hierarchically while leaving the central QR in its graph form.

Complete structural construction:

`W_2_construct <=95`.

Leaf factor generation itself stays below exponent44; dense leaf output has exponent32.

### Exact representation existence

On the same explicit 32-bit partition tree, also replace the central contribution by its physical matricization rank envelope. This gives

`W_2_repr <=88`.

The 88 bound is an exact Schmidt-representation existence result; a central Schmidt-factor generation procedure with peak88 is not separately certified, hence the constructive ledger remains95.

Authority:

- `V26_Q138_EXACT_DOUBLE_ROUND_PATH236_CORRECTION.md`;
- `V26_Q138_DOUBLE_ROUND_CONSTRUCTIVE95_THEOREM.md`;
- `V26_Q138_EXACT_DOUBLE_ROUND_LEAF_HT88_THEOREM.md`;
- corresponding clean CI verifiers.

## Why 88 does not fall by more topology search

The generic-envelope method is exhausted.

Exact central cardinality MILPs for smaller-side sizes 11..16 give minimum graph boundaries

`51,52,55,54,55,56`.

The balanced-edge lemma forces one such split in every 32-leaf binary tree. Combining central physical caps with four generic leaf Hilbert ranks gives method lower bound88, attained by the explicit tree. Thus 88 is optimal **inside this generic envelope method**.

Further exact falsifiers:

- refined minimal-TT central terminal cuts on all three critical 11|21 partitions are `44,44,44`, saturating the four-input physical cap;
- reduced leaf terminal cuts on the same partitions are `11,11,11`, saturating the one-output physical cap.

Therefore an improvement below88 requires actual coefficient-specific Schmidt deficiency or a joint central/leaf factorization; further generic topology permutation is not enough.

Authority:

- `V26_Q138_DOUBLE_ROUND_HT88_METHOD_OPTIMALITY.md`;
- `V26_Q138_CENTRAL_REFINED_TERMINAL_CUT44_FALSIFIER.md`;
- `V26_Q138_LEAF_TERMINAL_CUT11_FALSIFIER.md`.

## Multi-double-round representation law

For fixed outer input masks:

- `W_repr(1)<=88`;
- for `d>=2`, one explicit common bit-partition tree gives

`W_repr(d)<=536d-364`.

Thus d=2 gives `<=708`, d=3 `<=1244`, d=4 `<=1780`.

This is representation/message width only, not arithmetic work. It explicitly accounts for one central QR, four semi-open QRs, fully-open interior layers and earliest fixed-input output-vector kernels.

Authority:

`V26_Q138_DEPTH_REPRESENTATION_LAW.md` and `scripts/verify_v26_q138_depth_representation_law.py`.

## Double-round factor storage

Generic hierarchical leaf factorization improves separator geometry but not generic factor storage. One arbitrary 32-bit leaf vector has information dimension `2^32`; the explicit generic HT tree uses 4,308,611,904 scalar slots for one leaf, slightly above dense `2^32` storage. Four leaves therefore require roughly `2^34` scalar storage in the generic worst case.

Coefficient-specific leaf structure is needed for actual storage compression.

## Current sharp mathematical blocker

The generic exact topology/rank envelope for one double round is exhausted at88.

To lower it, one must now obtain one of:

1. actual diagonal-leaf Schmidt ranks below `2^11` on the three critical partitions for the **specified fixed outer input masks**;
2. actual central coefficient Schmidt rank below `2^44`;
3. a joint central×leaf factorization that beats independent rank-envelope multiplication.

The repository freezes the fixed/open boundary pattern but does not currently freeze one concrete 128-bit outer leaf-input mask value for all four diagonal leaves. Do not assume those masks are zero. Without a specified source mask, only uniform/parametric leaf theorems are legitimate.

For true next-layer coefficient composition, the single-copy right map `R_m` with its 24 external mask legs, or an exactly equivalent factorization, must be retained. Gram-image 124/U47 data alone is insufficient.

## Approximation and attack status

All admitted reductions above are exact, `epsilon=0`. Do not activate epsilon-rank while exact coefficient-specific routes remain open.

Still not admitted:

- practical exact evaluation at the formal peaks;
- arithmetic-work reduction;
- ranking/search reduction;
- `alpha<1`;
- full-round cryptanalytic relevance.

Historical measured execution remains blocked by the missing V25 runtime bytes; this is provenance, not a mathematical NO-GO.
