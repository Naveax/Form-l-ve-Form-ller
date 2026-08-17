# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=84.90275194485017...`.  
**d=1 coefficient-blind static graph+leaf method:** `W_static,blind=95`, method-optimal inside that representation.  
**d>=2 exact representation law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**d2:** `683.1007639817401...`.  
**ALPHA_PASS=0`.  
**Active work:** the complete natural S1 j2 bridge is now exact and gives the first useful d=1 merged overlap. Representation and coefficient-aware factor-generation are both84.90275. Arithmetic work is now the main blocker. Secondary exact representation work should test nonlocal retained-coordinate regroupings below the new center `3829*2^29`.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## Ledger discipline

Keep separate:

1. exact representation existence;
2. coefficient-blind static stored-factor method;
3. coefficient-aware materialized factor generation;
4. arithmetic work.

Unrestricted scalar streaming/recomputation has no canonical width without a work budget.

## New d=1 exact center

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

All44 physical S1 row bits are now inside occurrence-closed factors. No raw S1 row bit remains.

Low23 physical bits:

`A0..5,B0..5,D0..5,C12..16`.

High/gap21 physical bits:

`A12..16,B12..16,D12..16,C0..5`.

### Low rank

The complete repeated-D chain through D5 has exact rank

`524288=16*2^15=2^19`.

The physical C12..14 carry operator is universally injective and multiplies rank by `2^3`, so the low merged rank is

`n=2^22`.

Clean D5 run `32041446052`. Clean C-bridge run `32040887484`.

### High bridge

The j2 bits22..31 bridge has exact rank32/32 on domain `(sigma2_21,D12..15)`. Therefore all16 D12..15 high prefixes remain direct after attaching the low block.

Clean run `32041617140`.

### The useful gap overlap

The j2 bits1..11 local gap has rows `(C1..5,sigma2_0,sigma2_11)`, naive dimension128, and exact rank

`66`.

Its kernel dimension is62. This is certified by an exact four-state paired-carry Gram DP that implicitly sums all `2^28` retained columns.

Clean run `32042410012`.

At fixed D16, the smallest physical loop misses this kernel; clean run `32042794811`.

The gain appears when the two D16 sectors are kept together after closing C1..5. For physical rows `(D16,C0..5)`:

- fixed D16=0 rank64;
- fixed D16=1 rank64;
- union rank65;
- intersection63.

The same63-dimensional sector relation holds in every fixed shared retained slice

`q=(v3_12,sigma2_11)`.

Therefore for any incoming row space W on q, `dim W=n`, the exact lifted local geometry is

`64n,64n,intersection63n`.

Clean run `32043345651`.

### Combine with the j1 D16 geometry

For every fixed D12..15 prefix, extended-block2 j1 has

`448,448,intersection424`.

Thus per prefix

`448*(64n)+448*(64n)-424*(63n)=30632*n`.

With `n=2^22` and16 direct prefixes:

`rank_center(S1)<=16*30632*2^22`

`=3829*2^29`

`=2,055,678,722,048`.

Old center: `171*2^34`.

Exact center gain:

`5472/3829`.

Clean complete rank/tree run `32043410513`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BIT0_GAP1_11_SECTOR_RANK65.md`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_bit0_gap1_11_sector_rank65.py`;
- `scripts/verify_v26_q138_full_s1_gap_rank3829.py`.

## Frozen HT-tree bound

The four predecessor leaves contribute exponent44 at S1, so

`dim_factor<=3829*2^73`.

Hence

`W_repr(1)<=73+log2(3829)=84.90275194485017...`.

S2 remains `31*2^79`, and every noncritical frozen-tree node remains at most `2^80`, so S1 still controls the complete tree.

The exact improvement over the previous85.4178525 bound is

`log2(5472/3829)=0.5151005700357...` bits.

## Factor-generation constructivity

Let the true central rank be `r<=R=3829*2^29`.

There are `2^44` physical S1 rows and a51-bit central boundary. Exact streaming Gaussian can select actual physical row basis elements with a pivot minor/inverse of at most `R^2` entries:

`log2(R^2)<=81.8055038897003...`.

The physical-row to rank-coordinate transform has at most

`2^44*R=3829*2^73`

entries, exactly the materialized-factor envelope. A complete physical central row is only `2^51` entries.

Using actual physical basis rows allows reuse of the clean21-site complement tree at peak80; leaf generation stays44.

Therefore

`W_factor-gen<=84.90275194485017...`.

Clean run `32043554316`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FACTOR_GENERATION_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_factor_generation_rank3829.py`.

A complete materialized factor still contains

`3829*2^73 = 36,163,882,525,815,743,046,483,968`

scalars. This is not an arithmetic-work win.

## Closed / revoked d=1 routes

- block2 D11 one-bit extension: no gain;
- contiguous C12..C14 alone: full naive rank;
- repeated-D D0..5: full naive rank despite local kernels;
- direct shared `v3_12` alone: product bound exact;
- 39-bit natural bridge before C1..5: reproduces old center exactly;
- local gap rank66 exists, but fixed-D16 minimal loop misses it;
- old four-site ranks96/208 and derived W84/W83 claims are **revoked** after int32 overflow correction; corrected ranks256/256.

Do not revive revoked ranks without a mathematically independent derivation.

## d>=2 authority — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

Current law for every d>=2:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

## First unfinished mathematical pass

1. **d=1 arithmetic work.** This is now the main blocker. Exploit the 63-channel D16 overlap without materializing `3829*2^73` scalars. Any work claim must count factor generation, contraction, recomputation, memory traffic and output handling.
2. **Secondary exact d=1 representation.** Beat central `3829*2^29` using a nonlocal regrouping absent from the completed natural j2 bridge. First cheap probe: the retained-only j1 carry gap between low sites0..5 and high sites12..16. Then inspect any additional shared retained-coordinate overlap.
3. **Coefficient-specific predecessor leaves.** Any gain needs a clean uniform/parametric theorem or explicitly frozen outer128 mask.
4. **Semi-open B<55.** Respect rotation7 output wiring plus offset16 D reuse.
5. **Fully-open S3<63.562.** Need genuine multi-site row-space overlap.
6. Recount every complete relevant tree and clean-checkout every finite claim before changing authority.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
