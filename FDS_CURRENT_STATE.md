# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`.

Historical measured V25/V26 execution remains frozen behind missing exact recovered-runtime bytes. Active progress is mathematics-first exact Walsh/tensor algebra. Code is only a calculator/falsifier; every admitted finite claim requires clean-checkout execution.

## One-QR exact authority

For all4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925... <39`.

Current sharp peak `218*2^31`. Old support216 / 13 support classes / rank12 selector is revoked. Exact I9 support is117..218 over64 left masks; support-indicator rank64; all64 left maps share an exact48-dimensional interface row space. `epsilon=0`.

## d=1 canonical ledgers

Keep separate:

- topology-only `W_2_topo<=236`;
- coefficient-blind static graph+leaf method `W_2_static,blind=95`;
- exact representation existence
  `W_repr(1)<=73+log2(3829)=84.90275194485017...`;
- coefficient-aware materialized-factor generation
  `W_factor-gen<=84.90275194485017...`;
- arithmetic-work reduction: **not admitted**.

The old exact representation/factor-generation value

`78+log2(171)=85.4178525148859...`

is superseded. Exact exponent improvement:

`log2(5472/3829)=0.5151005700357...` bits.

## Full S1 exact decomposition

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

All44 physical S1 row bits are occurrence-closed. No raw S1 bit remains.

Low23 physical rows:

`A0..5,B0..5,D0..5,C12..16`.

High/gap21 physical rows:

`A12..16,B12..16,D12..16,C0..5`.

### Low block

The complete repeated-D chain D0..5 has exact rank

`2^19`.

The C12..14 carry operator is universally injective, rank16/16, so the low merged rank is

`n=2^22`.

Clean runs:

- D5 `32041446052`;
- C bridge `32040887484`.

### High bridge

The j2 bits22..31 bridge has exact rank32/32 on `(sigma2_21,D12..15)`. Therefore all16 D12..15 high prefixes remain direct after low-block attachment.

Clean run `32041617140`.

## Useful j2 gap overlap

The j2 bits1..11 gap has row domain

`(C1..5,sigma2_0,sigma2_11)`,

dimension128, exact rank66 and kernel dimension62. An exact four-state paired-carry Gram DP sums all `2^28` retained columns implicitly.

Clean run `32042410012`.

At fixed D16 the smallest physical loop misses this kernel; clean run `32042794811`.

Keeping D16=0/1 together after closing C1..5 gives local physical geometry

`64,64,intersection63`.

The same63-dimensional sector relation holds in every fixed shared retained slice

`q=(v3_12,sigma2_11)`.

Therefore for any incoming W on q, `dim W=n`, the exact lifted local geometry is

`64n,64n,intersection63n`.

Clean run `32043345651`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_J2_GAP1_11_RANK66.md`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_MINIMAL_GAP_LOOP_NO_GAIN.md`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BIT0_GAP1_11_SECTOR_RANK65.md`.

## New full S1 central rank

For each fixed D12..15 high prefix, the extended-block2 j1 D16 spaces have

`448,448,intersection424`.

Combine with the new local D16 geometry:

`448*(64n)+448*(64n)-424*(63n)=30632*n`.

Sixteen high prefixes are direct, so

`rank_center(S1)<=16*30632*2^22`

`=3829*2^29`

`=2,055,678,722,048`.

The previous center was `171*2^34`. Exact center gain:

`5472/3829`.

Clean complete rank/tree run `32043410513`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_full_s1_gap_rank3829.py`.

## Frozen HT-tree recount

At S1, predecessor-leaf exponent44 gives

`dim_factor<=3829*2^73`.

Thus

`W_repr(1)<=73+log2(3829)=84.90275194485017...`.

S2 remains `31*2^79`; every noncritical frozen-tree node remains at most `2^80`. S1 still controls the complete tree.

## Coefficient-aware factor-generation constructivity

Let `R<=3829*2^29` be the true central rank. There are `2^44` physical S1 rows and a51-bit central boundary.

Streaming exact Gaussian can select actual physical row-basis elements while storing a pivot minor/inverse of at most `R^2` entries:

`log2(R^2)<=81.8055038897003...`.

The physical-row -> rank-coordinate transform has at most

`2^44*R=3829*2^73`

entries. A complete physical central row has only `2^51` entries. Using physical basis rows allows reuse of the clean21-site complement-entry tree at peak80.

Therefore

`W_factor-gen<=84.90275194485017...`.

Clean run `32043554316`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FACTOR_GENERATION_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_factor_generation_rank3829.py`.

This is message/storage constructivity only.

## Secondary exact representation closure: j1 sites6..11

The S1-retained j1 carry gap at sites6..11 has only endpoint row variables

`(sigma1_5,sigma1_11)`,

dimension4.

All local `A,B,D,k,q` variables are retained on the S1 split. Exact six-site paired-carry Gram rank is

`4/4`.

Thus the direct retained-only j1 carry gap is injective and gives no reduction below center `3829*2^29`.

Clean run `32043801142`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_J1_GAP6_11_INJECTIVE.md`;
- `scripts/verify_v26_q138_j1_gap6_11_injective.py`.

## Arithmetic-work materialization gate

The exact per-high-prefix D16 channel space decomposes dimensionally as

`26712n + 1960n + 1960n =30632n`.

The `26712n` block is common to both D16 sectors, about87.2% of the union channels. This is the structure a scalar evaluator should preserve.

However any algorithm that explicitly materializes the complete coefficient-aware factor must emit

`3829*2^73`

`=36,163,882,525,815,743,046,483,968`

scalars.

Hence explicit factor materialization has an unavoidable scalar-output work exponent at least84.90275. It is scoped NO-GO as the route to an arithmetic-work reduction.

Clean run `32044123499`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_D1_ARITHMETIC_MATERIALIZATION_GATE.md`;
- `scripts/verify_v26_q138_d1_arithmetic_materialization_gate.py`.

This does not lower-bound scalar-on-the-fly contraction; that remains open.

## Closed / revoked d=1 routes

- block2 D11 one-bit extension: no gain;
- contiguous C12..C14 alone: full naive rank;
- repeated-D D0..5 alone: full naive rank despite local kernels;
- direct shared `v3_12` alone: product bound exact;
- 39-bit natural bridge before C1..5: reproduces old center exactly;
- fixed-D16 minimal gap loop: misses rank66 kernel;
- j1 retained-only gap6..11: rank4/4 injective;
- explicit full-factor materialization: scoped arithmetic NO-GO;
- old four-site ranks96/208 and W84/W83 claims are **revoked** due int32 overflow; corrected ranks256/256.

Do not revive revoked results without an independent derivation.

## d>=2 authority — unchanged

Frozen `S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076.

Semi-open:

- A54.661778097771986;
- B generic55;
- C54.92481250360578;
- D53.74357218893564.

Current law for every d>=2:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

## Current sharp blockers / next mathematics

1. **d=1 scalar arithmetic evaluator.** Preserve the exact per-prefix decomposition `common26712n + private0 1960n + private1 1960n`; do not materialize `3829*2^73`. Push predecessor-leaf contraction inside these blocks and count multiply/add, factor generation, recomputation, memory traffic and output.
2. **Predecessor-leaf Schmidt structure.** Current generic S1 accounting pays rank `2^11` per leaf, hence `2^44` across four leaves. Compute exact 11|21 Schmidt ranks for the relevant predecessor-leaf family. A uniform reduction is the clearest current path to scalar-work improvement. Coefficient-specific claims require a frozen outer128 mask or a uniform theorem.
3. **Other nonlocal retained-coordinate regroupings.** The direct j1 gap is closed; additional simultaneous retained-coordinate couplings may still beat `3829*2^29`.
4. **Semi-open B<55** and **fully-open S3<63.562** remain separate d>=2 rank problems.
5. Recount every complete relevant tree and clean-checkout every finite claim before authority changes.

All admitted reductions remain exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance.
