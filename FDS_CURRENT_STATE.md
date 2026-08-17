# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

`ALPHA_PASS=0`.

Historical measured V25/V26 execution remains frozen behind missing exact recovered-runtime bytes. Active progress is mathematics-first exact Walsh/tensor algebra. Code is only a calculator/falsifier; every admitted finite claim requires clean-checkout execution.

## One-QR exact authority

For all4096 physical fixed-mask cases:

`44 -> 42 -> 41 -> 40 -> 38.768184324776925... <39`.

Current sharp peak is `218*2^31`. All admitted one-QR reductions are exact, `epsilon=0`.

## d=1 ledgers — NEW canonical bound

Keep distinct:

- topology-only `W_2_topo<=236`;
- coefficient-blind static reduced-central-graph + four-generic-leaf method `W_2_static,blind=95`, method-optimal inside that representation;
- exact representation existence
  `W_repr(1)<=73+log2(3829)=84.90275194485017...`;
- coefficient-aware materialized-factor generation
  `W_factor-gen<=73+log2(3829)=84.90275194485017...`;
- arithmetic work: **not reduced/admitted**.

The previous exact representation/factor-generation bound

`78+log2(171)=85.4178525148859...`

is superseded for the first two exact/message ledgers above. Exact exponent improvement:

`log2(5472/3829)=0.5151005700357...`.

### Full S1 physical set

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

There are44 physical S1 row bits. The new merged decomposition consumes all44; no raw S1 physical bit remains.

Low 23-bit set:

`A0..5,B0..5,D0..5,C12..16`.

High/gap 21-bit set:

`A12..16,B12..16,D12..16,C0..5`.

These are disjoint and cover the complete S1 physical row set.

## Exact low block and bridge structure

### Repeated-D low chain through D5

The complete occurrence-closed low repeated-D chain has

`rank(D0..5)=524288=16*2^15=2^19`.

The key structural identity is that the relevant old carry graph is invariant under pure carry-slice swap, so its graph operator satisfies `G^2=I`. The local repeated-D rank24/32 kernels remain unreachable through D5.

Clean D5 run `32041446052`: success.

Authority:

- `V26_Q138_BLOCK1_D5_INVOLUTION_FIBER_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_d5_involution_fiber_no_gain.py`.

### C12..C14 bridge

The three physical C carry sites form a universal rank16/16 operator on their complete domain. Therefore they multiply any incoming rank by exactly `2^3`.

Applying them to D0..5 gives the exact low merged rank

`n=2^22`.

Clean merged-C run `32040887484`: success.

Authority:

- `V26_Q138_BLOCK1_C12_D04_MERGED_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_c12_d04_merged_no_gain.py`.

### j2 bits22..31 high bridge

The physical/domain coordinates are `(sigma2_21,D12..15)`, dimension32. An explicit 32x32 dyadic minor has full rank modulo65521, proving exact Q rank32/32.

Thus the bridge is injective and the sixteen D12..15 high prefixes remain direct after attaching the low block.

Clean run `32041617140`: success.

Authority:

- `V26_Q138_J2_BRIDGE22_31_INJECTIVE.md`;
- `scripts/verify_v26_q138_j2_bridge22_31_injective.py`.

## Exact gap mechanism: the first useful merged overlap

### Local j2 bits1..11 gap rank66

Rows `(C1..C5,sigma2_0,sigma2_11)` have naive dimension128. The implicit retained-column space has `2^28` assignments.

A four-state paired-carry exact Gram DP sums the entire column space without materializing it and gives

`rank(M M^T)=rank(M)=66`.

So the local gap has a real62-dimensional kernel.

Clean run `32042410012`: success.

Authority:

- `V26_Q138_J2_GAP1_11_RANK66.md`;
- `scripts/verify_v26_q138_j2_gap1_11_rank66.py`.

The fixed-D16 minimal block1+C12..14+bit0 loop nevertheless misses this kernel: its boundary graph is an exact rank124 projector on a248-dimensional fixed-sigma2_11 projection, and both relevant gap pencils are rank32. Minimal-loop rank remains full8192.

Clean run `32042794811`: success.

Authority:

- `V26_Q138_MINIMAL_GAP_LOOP_NO_GAIN.md`;
- `scripts/verify_v26_q138_minimal_gap_loop_no_gain.py`.

### D16 sectors after closing C1..5

The useful mechanism appears only when the two D16 sectors are kept together.

For physical rows `(D16,C0..C5)`:

- fixed D16=0 rank64;
- fixed D16=1 rank64;
- union rank65;
- intersection dimension63.

Crucially, the exact same63-dimensional coefficient relation occurs in every fixed shared retained slice

`q=(v3_12,sigma2_11)`.

Therefore for any incoming row space W on q, `dim W=n`, the lifted local sector geometry is universally

`64n,64n,intersection63n`.

Clean local run `32043345651`: success.

Authority:

- `V26_Q138_BIT0_GAP1_11_SECTOR_RANK65.md`;
- `scripts/verify_v26_q138_bit0_gap1_11_sector_rank65.py`.

This supersedes the old pre-gap universal bit0 geometry `2n,2n,intersection n` for the new merged factor.

## New full S1 central rank

For every fixed D12..15 high prefix, the certified extended-block2 j1 D16 spaces remain

`448,448,intersection424`.

Combine them with the new local D16 geometry for low rank `n=2^22`:

`448*(64n)+448*(64n)-424*(63n)`

`=30632*n`.

The sixteen D12..15 prefixes are direct, so

`rank_center(S1) <= 16*30632*2^22`

`=3829*2^29`

`=2,055,678,722,048`.

The old center was `171*2^34`. Exact center gain:

`(171*2^34)/(3829*2^29)=5472/3829`.

Clean full theorem/tree run `32043410513`: success.

Authority:

- `V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_full_s1_gap_rank3829.py`;
- `.github/workflows/full-s1-gap-rank3829.yml`.

## Complete frozen HT-tree recount

The S1 critical message dimension is

`(3829*2^29)*2^44 =3829*2^73`.

Hence

`W_repr(1)<=73+log2(3829)=84.90275194485017...`.

S2 remains `31*2^79`, exponent below the new S1 value. Every noncritical frozen-tree node remains at most `2^80`. Therefore S1 still controls the complete tree.

## Coefficient-aware factor-generation constructivity

The new representation rank is also constructive in the materialized-factor memory/message ledger.

Let `R<=3829*2^29` be the true central row rank. There are `2^44` physical S1 rows and a51-bit central boundary.

An exact streaming Gaussian can select actual physical row basis elements while storing only a pivot minor/inverse of at most `R^2` entries:

`log2(R^2)<=81.8055038897003...`.

This is below the final factor table.

The physical-row -> rank-coordinate transform costs at most

`2^44*R <=3829*2^73`,

which equals the factor-table envelope. A single complete physical central row has only `2^51` entries.

Because selected rank rows are actual physical S1 assignments, the clean21-site complement-entry tree is reused unchanged at peak80. Leaf generation remains44.

Therefore

`W_factor-gen<=73+log2(3829)=84.90275194485017...`.

Clean run `32043554316`: success.

Authority:

- `V26_Q138_FACTOR_GENERATION_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_factor_generation_rank3829.py`;
- `.github/workflows/factor-generation-rank3829.yml`.

This is a memory/message constructivity theorem only. Streaming Gaussian/recomputation may have enormous arithmetic work.

A complete materialized factor still contains

`3829*2^73 = 36,163,882,525,815,743,046,483,968`

scalar entries.

## Important no-gain / revoked routes

- block2 one-bit D11 extension preserves rank21888;
- block1 contiguous C12..C14 alone is full naive rank;
- repeated-D route D0..5 is full naive rank despite local kernels;
- direct block1×block2 shared `v3_12` alone equals the product bound;
- the 39-bit natural bridge without C1..5 reproduces the old `171*2^34` center exactly;
- fixed-D16 minimal gap loop misses the rank66 kernel;
- old adjacent four-site ranks96/208 and derived W84/W83 claims are **revoked** due int32 overflow. Corrected ranks are256/256.

Do not revive revoked results without a mathematically independent derivation.

## d>=2 authority — unchanged

Frozen `S3={4,5,11,12,13,19,20,21,27,28,29}`.

Central exponent34.52163149454245.

Fully-open:

`rank<=189*2^56`, exponent63.562242424221076.

Semi-open:

- A `405*2^46`, exp54.661778097771986;
- B generic `2^55`;
- C `243*2^47`, exp54.92481250360578;
- D `3429*2^42`, exp53.74357218893564.

Current depth law for every `d>=2` remains

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

Examples:

- d2 `683.1007639817401...`;
- d3 `1191.5987033755086...`.

## Storage/work status

One-QR dense-work proxy remains worse than the source topology. For d=1, representation and coefficient-aware factor generation are now84.90275, but the materialized output itself has more than `3.616e25` scalar entries.

No arithmetic-work reduction, practical evaluator, ranking/search reduction, `alpha<1`, or full-round cryptanalytic relevance is admitted.

## Current sharp blockers / next mathematics

1. **d=1 arithmetic work is now the main blocker.** Find a contraction/evaluation method that exploits the 63-channel D16 overlap without materializing `3829*2^73` entries. Any claimed work gain must include generation, contraction, recomputation and storage traffic.
2. **d=1 secondary representation pass.** Test nonlocal regroupings not covered by the complete natural j2 bridge, especially the retained-only j1 carry gap between the low sites0..5 and high sites12..16, and any additional shared retained-coordinate overlap. The new canonical center to beat is `3829*2^29`.
3. **Coefficient-specific predecessor leaves.** Any further leaf compression needs a clean uniform/parametric theorem or an explicitly frozen outer128 mask.
4. **Semi-open B<55.** Must respect rotation7 output wiring plus offset16 D reuse.
5. **Fully-open S3<63.562.** Needs genuine multi-site row-space overlap.
6. Recount every complete relevant tree and clean-checkout every finite claim before changing authority.

All admitted reductions remain exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.
