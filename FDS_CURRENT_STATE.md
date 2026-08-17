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

The old `support<=216`, 13 support classes and rank-12 support-selector claims are revoked. Correct I9 support is defined by the exact Gram diagonal `g_m(i)=sum_rest L_m(i,rest)^2`.

Across all 64 physical six-left-mask cases:

- support range `117..218`;
- distinct exact support sets64;
- union392;
- intersection42;
- exact rank of the `64 x512` support indicator64;
- residual `epsilon=0`.

Thus `rank_{I9|rest}(L_m)<=218<256`.

The six-left-mask complete coefficient family itself has full span64 and natural TT profile `[2,4,8,16,32,64]`.

Physical right/parent rank facts retained from clean exact transfer algebra:

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
- with fixed common left interface basis `L`, the Gram-image family `L G_m` has span124;
- its row directions span47;
- natural 12-control Gram-image selector TT profile `[2,4,8,16,32,64,128,119,196,136,143,124]`.

These are rank/Schmidt-space objects only. They do not retain the 24 right-external coefficient amplitudes. Do not propagate the 124/U47 Gram-image family through a later QR as if it were the single-copy coefficient tensor.

## Exact q138 inverse-double-round structure

The backward inverse-double-round dependency cone has one active final column QR plus four predecessor diagonal QRs.

Three structural ledgers remain separate:

### Topology-only

`W_2_topo <=236`.

### Constructive exact representation

Keep the central fixed-output/open-four-input QR in its exact reduced graph form. Contract each fixed-input/single-output diagonal leaf to its exact 32-bit vector and hierarchically factor the four vectors on the frozen bit tree.

Certified constructive structural peak:

`W_2_construct <=95`.

Leaf factor generation itself remains below exponent44 and dense leaf output has exponent32.

### Exact representation existence: new nonlinear-support result

The old generic physical-Hilbert result `W_2_repr<=88` is superseded.

The HT88 tree has two unique critical 11|21 bipartitions.

For

`S1={0,1,2,3,4,5,12,13,14,15,16}`

q138 modular-addition MSB conservation gives `msb(u4)=msb(v4)=3`, then `msb(u3)=msb(v3)=27`. Hence the central j2 masks obey

- `z2w_15=1`;
- `z2w_16..19=0`;
- `z2v_16=D_0`.

The exact nonlinear support recurrence at bits16 and15 implies

`C_15=0 => C_16=D_0`.

Only six of eight `(C15,C16,D0)` triples survive, so

`rank_center(S1) <= 3*2^42`.

For

`S2={6,7,8,9,10,11,27,28,29,30,31}`

j1 output top bits are determined by `u3` and `D`, and MSB conservation permits only342 of1024 top-pattern pairs `(A27..31,D27..31)`. Therefore

`rank_center(S2) <=342*2^34`.

Reinserting both exact support-row bounds into every node of the frozen HT tree gives maximum message dimension

`3*2^86`,

hence

`W_2_repr <= 86+log2(3) = 87.58496250072116... <88`.

The S1 bound is the new maximum; the S2 critical message is smaller, about exponent86.41785. Every noncritical node of the same tree remains at exponent at most80.

Clean GitHub Actions run `32017394330` passes the historical HT88 dependency and the new nonlinear-support verifier.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SUPPORT87_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_support87.py`;
- `.github/workflows/double-round-support87.yml`.

This is exact representation existence, not constructive factor generation. The constructive ledger stays95 until a procedure generating the compressed central factors below the new representation peak is certified.

## What the new result falsifies and what it does not

The old 88 generic-envelope method was optimal only inside its generic rank caps. Exact topology and linear-parity tests had saturated those caps:

- central cardinality MILP boundaries for smaller side11..16: `51,52,55,54,55,56`;
- refined central minimal-TT terminal cuts on old critical partitions: `44,44,44`, with exactly44 binary cut indices and no ternary cut bond;
- pure GF(2) projected boundary codimension: `0,0`;
- generic leaf terminal cuts: `11,11,11`;
- fixed-input leaf full-rank witnesses exist for every output position and critical partition for some outer masks.

The new improvement comes specifically from the nonlinear conditional Walsh-support rule `sigma=0 => u=v=w`, not from a better graph cut or a linear parity relation.

## Multi-double-round representation law

For fixed outer input masks:

- special one-double-round exact representation bound: `W_repr(1)<=86+log2(3)`;
- for `d>=2`, the current separate common-tree theorem gives

`W_repr(d)<=520d-340`.

Verified values: d2=700, d3=1220, d4=1740, d5=2260, d6=2780, d7=3300, d8=3820, d9=4340.

The d>=2 common tree has fully-open QR maximum65 and different maximizing 11-site clusters. The new S1/S2 support rule does not automatically change the `520d-340` law.

This remains representation/message width only, not arithmetic work.

## Storage/work status

One-QR RL218 message compression remains exact but its current width-optimized dense-work proxy is about `4.0160678967x` worse than the rank27 source topology. No arithmetic-work improvement is admitted.

Generic hierarchical leaf factorization also does not compress arbitrary leaf storage: one arbitrary 32-bit leaf vector has information dimension `2^32`, while the frozen generic HT representation uses slightly more than `2^32` scalar slots per leaf. Four generic leaves therefore remain roughly `2^34` storage.

## Current sharp mathematical blocker

The true double-round tensor now beats the exhausted generic88 envelope, but the new maximum is still the S1 critical partition with central support-row bound `3*2^42` times four generic leaf ranks `2^44`.

Next exact mechanisms, in priority order:

1. signed central coefficient Schmidt deficiency below the support-row bound `3*2^42` on S1;
2. a second independent nonlinear support restriction on S1;
3. joint central×leaf factorization across S1 that beats independent rank multiplication;
4. source-specific leaf rank only if a concrete canonical outer 128-bit mask is explicitly frozen. Do not assume zero masks;
5. analogous nonlinear-support analysis on the different maximizing cluster of the `520d-340` common tree.

All admitted reductions remain exact, `epsilon=0`. Do not activate epsilon-rank while these exact coefficient/support routes remain open.

Still not admitted:

- practical evaluator at formal peaks;
- arithmetic-work reduction;
- ranking/search reduction;
- `alpha<1`;
- full-round cryptanalytic relevance.

Historical measured execution remains blocked by missing V25 runtime bytes; this is provenance, not a mathematical NO-GO.
